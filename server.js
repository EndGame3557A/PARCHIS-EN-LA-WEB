import { createServer } from "node:http";
import { randomBytes, randomInt, randomUUID } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, extname, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";
import { WebSocket, WebSocketServer } from "ws";
import {
  PLAYERS,
  createGame,
  currentPlayer,
  rollDice,
  applyMove,
  skipMove,
  RULESETS,
} from "./public/game.js";

const projectRoot = dirname(fileURLToPath(import.meta.url));
const publicRoot = resolve(projectRoot, "public");
const rooms = new Map();
const roomAlphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
const contentTypes = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".svg": "image/svg+xml",
};
const server = createServer(serveFile);
const sockets = new WebSocketServer({
  server,
  maxPayload: 16 * 1024,
  verifyClient: ({ origin, req }, done) => {
    try {
      const allowed = Boolean(origin) && new URL(origin).host === req.headers.host;
      done(allowed, 403, allowed ? undefined : "Origen no permitido");
    } catch {
      done(false, 403, "Origen no válido");
    }
  },
});

function send(socket, value) {
  if (socket.readyState === WebSocket.OPEN) socket.send(JSON.stringify(value));
}

function sendError(socket, message) {
  send(socket, { type: "error", message });
}

function cleanName(value) {
  if (typeof value !== "string") return "Jugador";
  const name = value.replace(/[<>]/g, "").trim().slice(0, 18);
  return name || "Jugador";
}

function makeRoomCode() {
  let code;
  do {
    code = Array.from({ length: 6 }, () => roomAlphabet[randomInt(roomAlphabet.length)]).join("");
  } while (rooms.has(code));
  return code;
}

function publicRoom(room, self) {
  return {
    code: room.code,
    hostId: room.hostId,
    selfId: self.id,
    ruleset: room.ruleset,
    started: Boolean(room.state),
    players: room.players.map((player) => ({
      id: player.id,
      name: player.name,
      color: player.color,
      connected: Boolean(player.socket && player.socket.readyState === WebSocket.OPEN),
    })),
    state: room.state,
  };
}

function broadcastRoom(room) {
  for (const player of room.players) {
    if (!player.socket || player.socket.readyState !== WebSocket.OPEN) continue;
    send(player.socket, {
      type: "room",
      room: publicRoom(room, player),
      self: { id: player.id, color: player.color, token: player.token },
    });
  }
}

function broadcastState(room) {
  for (const player of room.players) {
    if (!player.socket || player.socket.readyState !== WebSocket.OPEN) continue;
    send(player.socket, {
      type: "state",
      state: room.state,
      room: publicRoom(room, player),
    });
  }
}

function attachPlayer(socket, room, player) {
  if (player.socket && player.socket !== socket && player.socket.readyState === WebSocket.OPEN) {
    player.socket.close(4001, "Session resumed");
  }
  player.socket = socket;
  socket.room = room;
  socket.player = player;
  broadcastRoom(room);
  if (room.state) broadcastState(room);
}

function createRoom(socket, message) {
  if (!Object.values(RULESETS).includes(message.ruleset)) {
    return sendError(socket, "Selecciona un formato de partida válido.");
  }
  const code = makeRoomCode();
  const player = {
    id: randomUUID(),
    token: randomBytes(24).toString("base64url"),
    name: cleanName(message.name),
    color: PLAYERS[0].id,
    socket: null,
  };
  const room = { code, hostId: player.id, ruleset: message.ruleset, players: [player], state: null };
  rooms.set(code, room);
  attachPlayer(socket, room, player);
}

function joinRoom(socket, message) {
  const code = typeof message.roomCode === "string" ? message.roomCode.toUpperCase() : "";
  const room = rooms.get(code);
  if (!room) return sendError(socket, "No encontramos esa sala. Revisa el código.");
  if (room.state) return sendError(socket, "La partida ya empezó y no acepta más jugadores.");
  if (room.players.length >= PLAYERS.length) return sendError(socket, "La sala ya está completa.");
  const player = {
    id: randomUUID(),
    token: randomBytes(24).toString("base64url"),
    name: cleanName(message.name),
    color: PLAYERS[room.players.length].id,
    socket: null,
  };
  room.players.push(player);
  attachPlayer(socket, room, player);
}

function resumeRoom(socket, message) {
  const code = typeof message.roomCode === "string" ? message.roomCode.toUpperCase() : "";
  const room = rooms.get(code);
  const player = room?.players.find((entry) => entry.id === message.playerId);
  if (!player || typeof message.token !== "string" || player.token !== message.token) {
    return sendError(socket, "No se pudo recuperar esa sesión. Vuelve a unirte con el código.");
  }
  attachPlayer(socket, room, player);
}

function activePlayer(socket) {
  const room = socket.room;
  const player = socket.player;
  if (!room || !player || !room.players.includes(player)) {
    sendError(socket, "Primero debes entrar a una sala.");
    return null;
  }
  if (!room.state) {
    sendError(socket, "La partida todavía no ha empezado.");
    return null;
  }
  if (currentPlayer(room.state) !== player.color) {
    sendError(socket, "Espera tu turno para hacer esa jugada.");
    return null;
  }
  return { room, player };
}

function handleMessage(socket, message) {
  if (!message || typeof message !== "object" || Array.isArray(message)) {
    return sendError(socket, "Solicitud no válida.");
  }
  if (message.type === "create") return createRoom(socket, message);
  if (message.type === "join") return joinRoom(socket, message);
  if (message.type === "resume") return resumeRoom(socket, message);

  const room = socket.room;
  const player = socket.player;
  if (message.type === "start") {
    if (!room || !player || room.hostId !== player.id) return sendError(socket, "Solo quien creó la sala puede empezar.");
    if (room.players.length < 2) return sendError(socket, "Invita al menos a una persona más para empezar.");
    if (room.players.some((entry) => !entry.socket || entry.socket.readyState !== WebSocket.OPEN)) {
      return sendError(socket, "Espera a que todos los jugadores vuelvan a conectarse.");
    }
    if (room.state) return sendError(socket, "La partida ya empezó.");
    room.state = createGame(room.players.map((entry) => entry.color), room.ruleset);
    broadcastRoom(room);
    broadcastState(room);
    return;
  }

  const session = activePlayer(socket);
  if (!session) return;
  try {
    if (message.type === "roll") {
      session.room.state = rollDice(session.room.state, [randomInt(1, 7), randomInt(1, 7)]);
    } else if (message.type === "move") {
      session.room.state = applyMove(session.room.state, message.index);
    } else if (message.type === "pass") {
      session.room.state = skipMove(session.room.state);
    } else {
      return sendError(socket, "Acción desconocida.");
    }
    broadcastState(session.room);
  } catch (error) {
    sendError(socket, error instanceof Error ? error.message : "La jugada no se pudo completar.");
  }
}

function handleDisconnect(socket) {
  const room = socket.room;
  const player = socket.player;
  if (!room || !player || player.socket !== socket) return;
  player.socket = null;
  broadcastRoom(room);
  if (room.players.every((entry) => !entry.socket) && !room.state) rooms.delete(room.code);
}

async function serveFile(request, response) {
  let pathname;
  try {
    pathname = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
  } catch {
    response.writeHead(400).end("Solicitud no válida");
    return;
  }
  if (pathname === "/") pathname = "/index.html";
  const file = resolve(publicRoot, `.${pathname}`);
  if (file !== publicRoot && !file.startsWith(`${publicRoot}${sep}`)) {
    response.writeHead(403).end("Prohibido");
    return;
  }
  try {
    const body = await readFile(file);
    response.writeHead(200, {
      "Content-Type": contentTypes[extname(file)] || "application/octet-stream",
      "X-Content-Type-Options": "nosniff",
      "X-Frame-Options": "DENY",
      "Referrer-Policy": "strict-origin-when-cross-origin",
      "Content-Security-Policy": "default-src 'self'; connect-src 'self' ws: wss:; style-src 'self' 'unsafe-inline'; script-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'self'; frame-ancestors 'none'",
      "Cache-Control": "no-cache",
    });
    response.end(body);
  } catch {
    response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" }).end("No encontrado");
  }
}

sockets.on("connection", (socket) => {
  socket.on("message", (raw) => {
    try {
      handleMessage(socket, JSON.parse(raw.toString()));
    } catch (error) {
      sendError(socket, error instanceof Error ? error.message : "No se pudo procesar la solicitud.");
    }
  });
  socket.on("close", () => handleDisconnect(socket));
  socket.on("error", () => handleDisconnect(socket));
});

const port = Number.parseInt(process.env.PORT || "3000", 10);
server.listen(port, process.env.HOST || "0.0.0.0", () => {
  console.log(`Parchís está listo en http://localhost:${port}`);
});

server.on("error", (error) => {
  console.error("No se pudo iniciar el servidor:", error);
  process.exitCode = 1;
});
