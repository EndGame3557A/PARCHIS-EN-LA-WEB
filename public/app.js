import {
  PLAYERS,
  SAFE_CELLS,
  TRACK_LENGTH,
  FINISH,
  RULESETS,
  createGame,
  currentPlayer,
  rollDice,
  applyMove,
  skipMove,
  describeMove,
} from "./game.js";

const $ = (selector) => document.querySelector(selector);
const screens = ["#home-screen", "#online-screen", "#lobby-screen", "#game-screen"];
const colors = Object.fromEntries(PLAYERS.map((player) => [player.id, player.color]));
const names = Object.fromEntries(PLAYERS.map((player) => [player.id, player.name]));
const SAFE_URL = new URL(location.href);
const board = $("#board");
const storedRuleset = localStorage.getItem("parchisRuleset");

let state = null;
let mode = "local";
let onlineSocket = null;
let onlineRoom = null;
let onlineColor = null;
let onlineIdentity = null;
let expectedOnlineAction = null;
let closeIntentionally = false;
let botRevision = -1;
let revision = 0;
let selectedRuleset = Object.values(RULESETS).includes(storedRuleset) ? storedRuleset : RULESETS.classic;
let localNames = { green: "Tú", red: "Coral", cream: "Marfil", blue: "Índigo" };

function updateFormatPicker() {
  const isPrevia = selectedRuleset === RULESETS.previa;
  for (const button of document.querySelectorAll("[data-ruleset]")) {
    const selected = button.dataset.ruleset === selectedRuleset;
    button.classList.toggle("selected", selected);
    button.setAttribute("aria-pressed", String(selected));
  }
  $("#format-description").textContent = isPrevia
    ? "Una ficha por equipo, todos salen a la pista y cada dado mueve el doble."
    : "Cuatro fichas por equipo, salida con dobles y recorrido completo.";
}

function renderRules() {
  const rules = selectedRuleset === RULESETS.previa
    ? [
      "Una ficha por equipo; todos empiezan en la pista.",
      "Cada dado mueve el doble de casillas; los dobles dan otro turno.",
      "Si te capturan, vuelves a casa; necesitas dobles y tienes tres intentos para regresar.",
      "La llegada requiere el número exacto: el primero en llegar gana.",
    ]
    : [
      "Cuatro fichas por equipo; se sale de casa con dobles.",
      "Si todas tus fichas están en casa, tienes tres intentos para sacar dobles.",
      "Puedes sumar los dados o repartirlos entre dos fichas.",
      "Las casillas seguras protegen; captura una ficha rival en las demás.",
      "La meta requiere el número exacto; el tercer doble lleva a casa la ficha más avanzada.",
    ];
  $("#rules-list").replaceChildren(...rules.map((text) => {
    const item = document.createElement("li");
    item.textContent = text;
    return item;
  }));
}

function showScreen(selector) {
  for (const screen of screens) $(screen).classList.toggle("hidden", screen !== selector);
  $(".status-pill").classList.toggle("hidden", selector === "#lobby-screen" || selector === "#game-screen");
}

function playerName(color) {
  if (mode === "online") {
    return onlineRoom?.players.find((player) => player.color === color)?.name || names[color];
  }
  return mode === "computer" && color !== "green" ? `${names[color]} · CPU` : localNames[color] || names[color];
}

function announce(message, isError = false) {
  const target = $("#online-error");
  target.textContent = message;
  target.classList.toggle("error-visible", isError);
}

function pointAt(index, radius = 194) {
  const angle = -Math.PI / 2 + (index / TRACK_LENGTH) * Math.PI * 2;
  return { x: 320 + Math.cos(angle) * radius, y: 320 + Math.sin(angle) * radius, angle };
}

function pointOnHome(color, step) {
  const player = PLAYERS.find((entry) => entry.id === color);
  const angle = -Math.PI / 2 + (player.start / TRACK_LENGTH) * Math.PI * 2;
  const radius = 176 - step * 19;
  return { x: 320 + Math.cos(angle) * radius, y: 320 + Math.sin(angle) * radius };
}

function yardPoint(color, pawn) {
  const player = PLAYERS.find((entry) => entry.id === color);
  const angle = -Math.PI / 2 + (player.start / TRACK_LENGTH) * Math.PI * 2;
  const centerX = 320 + Math.cos(angle) * 265;
  const centerY = 320 + Math.sin(angle) * 265;
  const tangentX = -Math.sin(angle);
  const tangentY = Math.cos(angle);
  const radialOffset = pawn < 2 ? -13 : 13;
  const tangentOffset = pawn % 2 === 0 ? -13 : 13;
  return {
    x: centerX + Math.cos(angle) * radialOffset + tangentX * tangentOffset,
    y: centerY + Math.sin(angle) * radialOffset + tangentY * tangentOffset,
  };
}

function svgCircle(point, radius, fill, className = "", extra = "") {
  return `<circle cx="${point.x.toFixed(1)}" cy="${point.y.toFixed(1)}" r="${radius}" fill="${fill}" class="${className}" ${extra}/>`;
}

function drawBoard() {
  const markup = [
    `<defs>
      <filter id="soft-shadow" x="-60%" y="-60%" width="220%" height="220%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000" flood-opacity=".28"/></filter>
      <radialGradient id="board-glow"><stop stop-color="#293b3d"/><stop offset="1" stop-color="#111d23"/></radialGradient>
    </defs>`,
    `<rect x="7" y="7" width="626" height="626" rx="38" class="board-bg"/>`,
    `<circle cx="320" cy="320" r="217" class="board-track"/>`,
  ];

  for (const player of PLAYERS) {
    const start = pointAt(player.start);
    const laneEnd = pointOnHome(player.id, 7);
    markup.push(`<line x1="${start.x}" y1="${start.y}" x2="${laneEnd.x}" y2="${laneEnd.y}" stroke="${player.color}" class="home-lane"/>`);
    for (let step = 0; step < 8; step += 1) {
      const point = pointOnHome(player.id, step);
      markup.push(svgCircle(point, 8.8, player.color, "home-step"));
    }

    const yard = yardPoint(player.id, 0);
    const center = { x: (yard.x + yardPoint(player.id, 3).x) / 2, y: (yard.y + yardPoint(player.id, 3).y) / 2 };
    markup.push(svgCircle(center, 46, `${player.color}18`, "base", `stroke="${player.color}"`));
  }

  for (let index = 0; index < TRACK_LENGTH; index += 1) {
    const point = pointAt(index);
    const startPlayer = PLAYERS.find((player) => player.start === index);
    const safe = SAFE_CELLS.has(index);
    const className = [
      "track-cell",
      safe ? "safe-cell" : "",
      startPlayer ? `start-${startPlayer.id}` : "",
    ].filter(Boolean).join(" ");
    const fill = startPlayer ? startPlayer.color : safe ? "#35483e" : "#26363d";
    markup.push(svgCircle(point, safe ? 9.5 : 8.5, fill, className));
    if (safe && !startPlayer) {
      markup.push(`<path d="M${point.x - 3} ${point.y + 2}l3 -6 3 6z" fill="#d2dfb6" opacity=".8"/>`);
    }
  }

  markup.push(`<circle cx="320" cy="320" r="29" fill="url(#board-glow)" stroke="rgba(226,240,229,.5)" stroke-width="1.5"/>`);
  markup.push(`<text x="320" y="324" fill="#dcebe0" font-size="12" font-weight="800" text-anchor="middle" letter-spacing="2">META</text>`);
  markup.push(`<circle cx="320" cy="320" r="5" class="home-goal"/>`);

  const occupiedPoints = new Map();
  for (const color of state?.players || PLAYERS.map((player) => player.id)) {
    const pawns = (state?.pawns[color] || [null, null, null, null]).slice(0, state?.tokensPerPlayer || 4);
    for (let pawn = 0; pawn < pawns.length; pawn += 1) {
      const progress = pawns[pawn];
      let point;
      if (progress === null) point = yardPoint(color, pawn);
      else if (progress >= FINISH) {
        const angle = -Math.PI / 2 + (PLAYERS.find((player) => player.id === color).start / TRACK_LENGTH) * Math.PI * 2;
        const offset = (pawn - 1.5) * 7;
        point = { x: 320 + Math.cos(angle + Math.PI / 2) * offset, y: 320 + Math.sin(angle + Math.PI / 2) * offset };
      } else if (progress >= TRACK_LENGTH) point = pointOnHome(color, progress - TRACK_LENGTH);
      else point = pointAt((PLAYERS.find((player) => player.id === color).start + progress) % TRACK_LENGTH);

      const key = `${Math.round(point.x)}:${Math.round(point.y)}`;
      const count = occupiedPoints.get(key) || 0;
      occupiedPoints.set(key, count + 1);
      if (count) {
        const angle = count * Math.PI * .72;
        point = { x: point.x + Math.cos(angle) * 8, y: point.y + Math.sin(angle) * 8 };
      }
      markup.push(svgCircle(point, 9.2, colors[color], "token", `filter="url(#soft-shadow)"`));
      markup.push(`<text x="${point.x}" y="${point.y + .5}" class="token-number">${pawn + 1}</text>`);
    }
  }
  board.innerHTML = markup.join("");
}

function renderPlayers() {
  const list = $("#players-list");
  list.innerHTML = "";
  const players = state?.players || PLAYERS.map((player) => player.id);
  $("#player-count").textContent = `${players.length} ${players.length === 1 ? "equipo" : "equipos"}`;
  for (const color of players) {
    const row = document.createElement("div");
    row.className = `player-row${color === currentPlayer(state) ? " active" : ""}`;
    const count = state.pawns[color].slice(0, state.tokensPerPlayer).filter((position) => position === FINISH).length;
    row.innerHTML = `<span class="player-color" style="background:${colors[color]}"></span><span></span><span class="player-pawns">${count}/${state.tokensPerPlayer} en casa</span>`;
    row.children[1].textContent = playerName(color);
    list.append(row);
  }
}

function renderMoves(canControl) {
  const list = $("#move-list");
  list.innerHTML = "";
  const pass = $("#pass-button");
  pass.classList.toggle("hidden", !(state.phase === "move" && state.options.length === 0 && canControl));
  for (const [index, option] of state.options.entries()) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "move-option";
    button.textContent = describeMove(option);
    button.disabled = !canControl;
    button.addEventListener("click", () => selectMove(index));
    list.append(button);
  }
}

function isMyTurn() {
  return mode !== "online" || onlineColor === currentPlayer(state);
}

function render() {
  if (!state) return;
  revision += 1;
  drawBoard();
  const color = currentPlayer(state);
  const isControl = isMyTurn();
  const player = PLAYERS.find((entry) => entry.id === color);
  const turnPlayer = $("#turn-player");
  turnPlayer.innerHTML = `<span class="turn-swatch" style="background:${player.color};color:${player.color}"></span><span></span>`;
  turnPlayer.children[1].textContent = playerName(color);
  $("#game-message").textContent = state.message;
  $("#dice-display").innerHTML = (state.dice || [null, null]).map((value) => `<span class="die">${value ?? "–"}</span>`).join("");
  const rollButton = $("#roll-button");
  rollButton.disabled = state.phase !== "roll" || !isControl;
  rollButton.classList.toggle("hidden", state.phase !== "roll" || (mode === "computer" && color !== "green"));
  $("#pass-button").disabled = !isControl;
  renderMoves(isControl);
  renderPlayers();
  $("#game-mode-label").textContent = mode === "online" ? "SALA EN LÍNEA" : mode === "computer" ? "CONTRA LA COMPUTADORA" : "PARTIDA LOCAL";
  selectedRuleset = state.ruleset || selectedRuleset;
  $("#board-caption").textContent = state.ruleset === RULESETS.previa ? "LA PREVIA · PARTIDA RÁPIDA" : "PARTIDA CLÁSICA";
  renderRules();
  $("#room-badge").classList.toggle("hidden", !onlineRoom);
  if (onlineRoom) $("#room-badge").textContent = `SALA ${onlineRoom.code}`;
  if (state.phase === "over" && state.winner) {
    const winnerTitle = mode === "local" && state.winner === "green"
      ? "¡Ganaste!"
      : `¡${playerName(state.winner)} gana!`;
    const captureCount = state.captures?.[state.winner] ?? 0;
    const captureLabel = captureCount === 1 ? "captura" : "capturas";
    $("#winner-title").textContent = winnerTitle;
    $("#winner-message").textContent = `Terminó ${state.ruleset === RULESETS.previa ? "La Previa" : "el Parchís clásico"} con ${captureCount} ${captureLabel}. ¿Quién se apunta a la revancha?`;
    $("#winner-overlay").classList.remove("hidden");
  } else {
    $("#winner-overlay").classList.add("hidden");
  }
  scheduleComputer();
}

function beginGame(nextMode, players = PLAYERS.map((player) => player.id)) {
  mode = nextMode;
  onlineRoom = null;
  onlineColor = null;
  state = createGame(players, selectedRuleset);
  closeOnlineConnection(true);
  showScreen("#game-screen");
  $("#board-caption").textContent = "PARTIDA EN CURSO";
  render();
}

function randomDice() {
  return [1 + Math.floor(Math.random() * 6), 1 + Math.floor(Math.random() * 6)];
}

function roll() {
  if (!state || state.phase !== "roll" || !isMyTurn()) return;
  if (mode === "online") {
    sendOnline({ type: "roll" });
    return;
  }
  state = rollDice(state, randomDice());
  render();
}

function selectMove(index) {
  if (!state || !isMyTurn()) return;
  if (mode === "online") {
    sendOnline({ type: "move", index });
    return;
  }
  state = applyMove(state, index);
  render();
}

function passTurn() {
  if (!state || !isMyTurn()) return;
  if (mode === "online") {
    sendOnline({ type: "pass" });
    return;
  }
  state = skipMove(state);
  render();
}

function scheduleComputer() {
  if (mode !== "computer" || !state || state.phase === "over" || currentPlayer(state) === "green" || botRevision === revision) return;
  botRevision = revision;
  const scheduledRevision = revision;
  window.setTimeout(() => {
    if (revision !== scheduledRevision || mode !== "computer" || !state) return;
    if (state.phase === "roll") {
      state = rollDice(state, randomDice());
      render();
      return;
    }
    if (state.phase === "move") {
      if (state.options.length === 0) state = skipMove(state);
      else {
        const color = currentPlayer(state);
        const moves = state.options.map((option, index) => {
          const progress = option.reduce((total, action) => total + action.steps, 0);
          const reachesHome = option.some(({ pawn, steps }) => state.pawns[color][pawn] + steps === FINISH);
          return { index, score: progress + (reachesHome ? 100 : 0) + Math.random() };
        }).sort((left, right) => right.score - left.score);
        state = applyMove(state, moves[0].index);
      }
      render();
    }
  }, 720);
}

function connectOnline(action) {
  if (onlineSocket) {
    const previousSocket = onlineSocket;
    onlineSocket = null;
    previousSocket.close();
  }
  if (action.type !== "resume") {
    onlineIdentity = null;
    sessionStorage.removeItem("parchisOnlineSession");
  }
  closeIntentionally = false;
  expectedOnlineAction = action;
  $("#create-room").disabled = true;
  $("#join-room").disabled = true;
  announce("Conectando a la mesa…");
  const protocol = location.protocol === "https:" ? "wss:" : "ws:";
  onlineSocket = new WebSocket(`${protocol}//${location.host}`);
  onlineSocket.addEventListener("open", () => {
    if (!expectedOnlineAction) return;
    onlineSocket.send(JSON.stringify(expectedOnlineAction));
    expectedOnlineAction = null;
  });
  onlineSocket.addEventListener("message", (event) => {
    let message;
    try {
      message = JSON.parse(event.data);
    } catch {
      showOnlineError("El servidor envió una respuesta que no se pudo leer.");
      return;
    }
    handleOnlineMessage(message);
  });
  onlineSocket.addEventListener("error", () => showOnlineError("No se pudo conectar. Verifica que el servidor esté encendido."));
  const socket = onlineSocket;
  onlineSocket.addEventListener("close", () => {
    $("#create-room").disabled = false;
    $("#join-room").disabled = false;
    if (onlineSocket === socket && !closeIntentionally && onlineIdentity) {
      $("#lobby-status").textContent = "Se perdió la conexión. Volviendo a conectar…";
      const identity = onlineIdentity;
      window.setTimeout(() => {
        if (!closeIntentionally) connectOnline({ type: "resume", ...identity });
      }, 1800);
    }
  });
}

function closeOnlineConnection(intentional) {
  closeIntentionally = intentional;
  if (intentional) {
    onlineIdentity = null;
    sessionStorage.removeItem("parchisOnlineSession");
  }
  if (onlineSocket) {
    onlineSocket.close();
    onlineSocket = null;
  }
}

function sendOnline(message) {
  if (!onlineSocket || onlineSocket.readyState !== WebSocket.OPEN) {
    $("#game-message").textContent = "Sin conexión con la sala. Reconectando…";
    return;
  }
  onlineSocket.send(JSON.stringify(message));
}

function showOnlineError(message) {
  if (!$("#online-screen").classList.contains("hidden")) announce(message, true);
  else $("#lobby-status").textContent = message;
}

function handleOnlineMessage(message) {
  if (message.type === "error") {
    showOnlineError(message.message || "No se pudo completar esa acción.");
    $("#create-room").disabled = false;
    $("#join-room").disabled = false;
    return;
  }
  if (message.type === "room") {
    onlineRoom = message.room;
    selectedRuleset = onlineRoom.ruleset || RULESETS.classic;
    updateFormatPicker();
    onlineColor = message.self?.color || onlineColor;
    if (message.self?.id && message.self?.token) {
      onlineIdentity = { roomCode: message.room.code, playerId: message.self.id, token: message.self.token };
      sessionStorage.setItem("parchisOnlineSession", JSON.stringify(onlineIdentity));
    }
    $("#lobby-code").textContent = onlineRoom.code;
    $("#lobby-status").textContent = onlineRoom.started ? "Partida en curso" : `${onlineRoom.players.length} de 4 jugadores`;
    $("#lobby-players").innerHTML = "";
    for (const player of onlineRoom.players) {
      const row = document.createElement("div");
      row.className = "lobby-player";
      row.innerHTML = `<span class="player-color" style="background:${colors[player.color]}"></span><span></span><small>${player.connected ? "Conectado" : "Reconectando…"}</small>`;
      row.children[1].textContent = player.name;
      $("#lobby-players").append(row);
    }
    const everyoneConnected = onlineRoom.players.every((player) => player.connected);
    const canStart = onlineRoom.hostId === onlineRoom.selfId && onlineRoom.players.length >= 2 && everyoneConnected && !onlineRoom.started;
    $("#start-online").classList.toggle("hidden", !canStart);
    $("#lobby-hint").classList.toggle("hidden", canStart || onlineRoom.started);
    if (!everyoneConnected && !onlineRoom.started) $("#lobby-hint").textContent = "Espera a que todos los jugadores vuelvan a conectarse.";
    else $("#lobby-hint").textContent = "Se necesitan al menos dos jugadores.";
    $("#create-room").disabled = false;
    $("#join-room").disabled = false;
    announce("");
    showScreen(onlineRoom.started ? "#game-screen" : "#lobby-screen");
    $("#board-caption").textContent = "PARTIDA EN CURSO";
    if (onlineRoom.state) state = onlineRoom.state;
    if (state && onlineRoom.started) render();
    return;
  }
  if (message.type === "state") {
    state = message.state;
    onlineRoom = message.room || onlineRoom;
    mode = "online";
    showScreen("#game-screen");
    render();
  }
}

function startOnline(action) {
  const name = $("#player-name").value.trim().slice(0, 18) || "Jugador";
  localStorage.setItem("parchisPlayerName", name);
  connectOnline({
    ...action,
    name,
    ...(action.type === "create" ? { ruleset: selectedRuleset } : {}),
  });
}

$("#player-name").value = localStorage.getItem("parchisPlayerName") || "Jugador";
const invitedRoom = SAFE_URL.searchParams.get("room");
if (invitedRoom) {
  $("#room-code").value = invitedRoom.toUpperCase().slice(0, 6);
  showScreen("#online-screen");
}
$("#room-code").addEventListener("input", (event) => {
  event.target.value = event.target.value.toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 6);
});
document.querySelectorAll("[data-mode]").forEach((button) => {
  button.addEventListener("click", () => {
    if (button.dataset.mode === "local") beginGame("local");
    if (button.dataset.mode === "computer") beginGame("computer");
    if (button.dataset.mode === "online") {
      announce("");
      showScreen("#online-screen");
    }
  });
});
document.querySelectorAll("[data-ruleset]").forEach((button) => {
  button.addEventListener("click", () => {
    selectedRuleset = button.dataset.ruleset;
    localStorage.setItem("parchisRuleset", selectedRuleset);
    updateFormatPicker();
  });
});
$("#back-home").addEventListener("click", () => showScreen("#home-screen"));
$("#create-room").addEventListener("click", () => startOnline({ type: "create" }));
$("#join-room").addEventListener("click", () => {
  const code = $("#room-code").value.trim();
  if (code.length !== 6) {
    announce("Escribe un código de sala de 6 caracteres.", true);
    return;
  }
  startOnline({ type: "join", roomCode: code });
});
$("#start-online").addEventListener("click", () => sendOnline({ type: "start" }));
$("#copy-room").addEventListener("click", async () => {
  const invite = new URL(location.href);
  invite.search = "";
  invite.searchParams.set("room", onlineRoom?.code || "");
  try {
    await navigator.clipboard.writeText(invite.toString());
    $("#copy-room").textContent = "¡Copiado!";
    window.setTimeout(() => { $("#copy-room").textContent = "Copiar enlace"; }, 1600);
  } catch {
    $("#copy-room").textContent = `Código: ${onlineRoom?.code || ""}`;
  }
});
$("#roll-button").addEventListener("click", roll);
$("#pass-button").addEventListener("click", passTurn);
$("#game-home").addEventListener("click", () => {
  closeOnlineConnection(true);
  state = null;
  onlineRoom = null;
  $("#winner-overlay").classList.add("hidden");
  showScreen("#home-screen");
});
$("#winner-home").addEventListener("click", () => {
  $("#winner-overlay").classList.add("hidden");
  closeOnlineConnection(true);
  state = null;
  onlineRoom = null;
  showScreen("#home-screen");
});
$("#share-result").addEventListener("click", async () => {
  const captureCount = state?.captures?.[state.winner] ?? 0;
  const captureLabel = captureCount === 1 ? "captura" : "capturas";
  const format = state?.ruleset === RULESETS.previa ? "La Previa" : "el Parchís clásico";
  const text = `🏆 ${names[state?.winner]} ganó ${format} con ${captureCount} ${captureLabel}. ¿Quién se apunta a la revancha? #ParchísDelParche`;
  const url = location.protocol === "https:" ? new URL(location.pathname, location.origin).toString() : "";
  try {
    if (navigator.share) {
      await navigator.share({ title: "Parchís del Parche", text, ...(url ? { url } : {}) });
    } else {
      const message = url ? `${text}\n${url}` : text;
      window.open(`https://wa.me/?text=${encodeURIComponent(message)}`, "_blank", "noopener,noreferrer");
    }
  } catch (error) {
    if (error.name !== "AbortError") {
      $("#winner-message").textContent = "No se pudo abrir la opción para compartir. ¡Puedes invitar a la revancha desde el inicio!";
    }
  }
});
const openRules = () => $("#rules-dialog").classList.remove("hidden");
const closeRules = () => $("#rules-dialog").classList.add("hidden");
$("#help-button").addEventListener("click", openRules);
$("#close-rules").addEventListener("click", closeRules);
$("#rules-ok").addEventListener("click", closeRules);
$("#rules-dialog").addEventListener("click", (event) => {
  if (event.target === $("#rules-dialog")) closeRules();
});
$("#leave-lobby").addEventListener("click", () => {
  closeOnlineConnection(true);
  onlineRoom = null;
  showScreen("#home-screen");
});
window.addEventListener("beforeunload", () => {
  if (onlineSocket) onlineSocket.close();
});

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/sw.js").catch((error) => {
    console.warn("No se pudo habilitar el modo sin conexión:", error);
  });
}
updateFormatPicker();

if (!invitedRoom) {
  try {
    const savedSession = JSON.parse(sessionStorage.getItem("parchisOnlineSession") || "null");
    if (savedSession?.roomCode && savedSession?.playerId && savedSession?.token) {
      showScreen("#online-screen");
      $("#online-error").textContent = "Recuperando tu mesa…";
      connectOnline({ type: "resume", ...savedSession });
    }
  } catch (error) {
    sessionStorage.removeItem("parchisOnlineSession");
    console.warn("No se pudo recuperar la sesión en línea:", error);
  }
}
