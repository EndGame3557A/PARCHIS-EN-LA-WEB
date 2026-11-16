export const PLAYERS = [
  { id: "green", name: "Esmeralda", color: "#21a67a", start: 0 },
  { id: "red", name: "Coral", color: "#ef6474", start: 17 },
  { id: "cream", name: "Marfil", color: "#e5aa3c", start: 34 },
  { id: "blue", name: "Índigo", color: "#6d7ce8", start: 51 },
];

export const TRACK_LENGTH = 68;
export const HOME_LENGTH = 8;
export const FINISH = TRACK_LENGTH + HOME_LENGTH;
export const SAFE_CELLS = new Set([0, 7, 12, 17, 24, 29, 34, 41, 46, 51, 58, 63]);
export const RULESETS = {
  classic: "classic",
  previa: "previa",
};

const clone = (value) => JSON.parse(JSON.stringify(value));

export function createGame(playerIds = PLAYERS.map((player) => player.id), ruleset = RULESETS.classic) {
  if (playerIds.length < 2 || playerIds.length > PLAYERS.length) {
    throw new RangeError("Una partida necesita entre 2 y 4 equipos.");
  }
  if (new Set(playerIds).size !== playerIds.length || playerIds.some((id) => !PLAYERS.some((player) => player.id === id))) {
    throw new RangeError("Los equipos de la partida no son válidos.");
  }
  if (!Object.values(RULESETS).includes(ruleset)) {
    throw new RangeError("El formato de partida no es válido.");
  }
  const tokensPerPlayer = ruleset === RULESETS.previa ? 1 : 4;
  const pawns = Object.fromEntries(playerIds.map((id) => [
    id,
    ruleset === RULESETS.previa ? [0, FINISH, FINISH, FINISH] : [null, null, null, null],
  ]));
  return {
    players: [...playerIds],
    ruleset,
    tokensPerPlayer,
    turn: 0,
    phase: "roll",
    pawns,
    captures: Object.fromEntries(playerIds.map((id) => [id, 0])),
    dice: null,
    options: [],
    jailAttempts: Object.fromEntries(playerIds.map((id) => [id, 0])),
    doublesInRow: Object.fromEntries(playerIds.map((id) => [id, 0])),
    winner: null,
    message: "Tira los dados para comenzar.",
  };
}

export function currentPlayer(state) {
  return state.players[state.turn];
}

function isInYard(state, color) {
  return state.pawns[color].every((position) => position === null || position === FINISH);
}

function nextPlayer(state) {
  state.turn = (state.turn + 1) % state.players.length;
  const color = currentPlayer(state);
  state.phase = "roll";
  state.dice = null;
  state.options = [];
  state.jailAttempts[color] = 0;
  state.message = `Turno de ${PLAYERS.find((player) => player.id === color).name}.`;
}

function putPawnInHome(state, color) {
  const candidates = state.pawns[color]
    .map((position, pawn) => ({ position, pawn }))
    .filter(({ position }) => position !== null && position < FINISH)
    .sort((left, right) => left.position - right.position);
  if (candidates.length === 0) return false;
  state.pawns[color][candidates[0].pawn] = FINISH;
  return true;
}

function releasePawn(state, color) {
  const pawn = state.pawns[color].findIndex((position) => position === null);
  if (pawn < 0) return false;
  state.pawns[color][pawn] = 0;
  return true;
}

function cellAt(color, progress) {
  const player = PLAYERS.find((entry) => entry.id === color);
  return (player.start + progress) % TRACK_LENGTH;
}

function canMovePawn(state, color, pawn, steps) {
  const current = state.pawns[color][pawn];
  if (!Number.isInteger(steps) || steps <= 0 || current === null || current >= FINISH) return false;
  const destination = current + steps;
  if (destination > FINISH) return false;
  if (destination >= TRACK_LENGTH) return true;

  const cell = cellAt(color, destination);
  const occupyingOpponents = [];
  for (const other of state.players) {
    if (other === color) continue;
    for (const position of state.pawns[other]) {
      if (position !== null && position < TRACK_LENGTH && cellAt(other, position) === cell) {
        occupyingOpponents.push(position);
      }
    }
  }
  if (occupyingOpponents.length >= 2) return false;
  return true;
}

function movePawn(state, color, pawn, steps) {
  if (!canMovePawn(state, color, pawn, steps)) return false;
  const destination = state.pawns[color][pawn] + steps;
  state.pawns[color][pawn] = destination;
  if (destination >= TRACK_LENGTH) return true;

  const cell = cellAt(color, destination);
  if (SAFE_CELLS.has(cell)) return true;
  for (const other of state.players) {
    if (other === color) continue;
    for (let index = 0; index < state.pawns[other].length; index += 1) {
      const position = state.pawns[other][index];
      if (position !== null && position < TRACK_LENGTH && cellAt(other, position) === cell) {
        state.pawns[other][index] = null;
        state.captures[color] += 1;
      }
    }
  }
  return true;
}

function optionIsLegal(state, color, actions) {
  const simulation = clone(state);
  for (const action of actions) {
    if (!movePawn(simulation, color, action.pawn, action.steps)) return false;
  }
  return true;
}

export function legalMoves(state) {
  if (state.phase !== "move" || !state.dice) return [];
  const color = currentPlayer(state);
  const pace = state.ruleset === RULESETS.previa ? 2 : 1;
  const [first, second] = state.dice.map((die) => die * pace);
  const options = [];
  for (let pawn = 0; pawn < 4; pawn += 1) {
    const actions = [{ pawn, steps: first + second }];
    if (optionIsLegal(state, color, actions)) options.push(actions);
  }
  for (let firstPawn = 0; firstPawn < 4; firstPawn += 1) {
    for (let secondPawn = 0; secondPawn < 4; secondPawn += 1) {
      if (firstPawn === secondPawn) continue;
      const actions = [
        { pawn: firstPawn, steps: first },
        { pawn: secondPawn, steps: second },
      ];
      if (optionIsLegal(state, color, actions)) options.push(actions);
    }
  }
  const unique = new Map(options.map((option) => [
    option.map(({ pawn, steps }) => `${pawn}:${steps}`).join("|"),
    option,
  ]));
  return [...unique.values()];
}

export function rollDice(state, dice) {
  if (state.phase !== "roll") throw new Error("Ahora no corresponde tirar los dados.");
  if (!Array.isArray(dice) || dice.length !== 2 || dice.some((value) => !Number.isInteger(value) || value < 1 || value > 6)) {
    throw new RangeError("Los dados deben ser dos valores entre 1 y 6.");
  }
  const next = clone(state);
  const color = currentPlayer(next);
  const [first, second] = dice;
  const isDouble = first === second;
  next.dice = [...dice];

  if (next.ruleset === RULESETS.classic && isDouble) next.doublesInRow[color] += 1;
  else next.doublesInRow[color] = 0;

  if (next.ruleset === RULESETS.classic && next.doublesInRow[color] === 3) {
    putPawnInHome(next, color);
    next.doublesInRow[color] = 0;
    if (next.pawns[color].every((position) => position === FINISH)) {
      next.winner = color;
      next.phase = "over";
      next.message = `¡${PLAYERS.find((player) => player.id === color).name} ganó la partida!`;
      return next;
    }
    next.message = "¡Tercer doble! Una ficha avanzada llega a casa.";
  }

  if (isDouble && next.pawns[color].includes(null)) {
    releasePawn(next, color);
    next.jailAttempts[color] = 0;
    next.phase = "roll";
    next.options = [];
    next.message = `¡Doble! Una ficha de ${PLAYERS.find((player) => player.id === color).name} sale a la pista.`;
    return next;
  }

  if (isInYard(next, color)) {
    next.jailAttempts[color] += 1;
    next.options = [];
    if (next.jailAttempts[color] >= 3) {
      next.jailAttempts[color] = 0;
      next.message = "No salió ningún doble en tres intentos. El turno pasa.";
      nextPlayer(next);
    } else {
      next.message = `Solo se sale con dobles. Intento ${next.jailAttempts[color]} de 3.`;
    }
    return next;
  }

  next.phase = "move";
  next.options = legalMoves(next);
  if (next.options.length === 0) next.message = "No hay movimientos legales. Puedes pasar el turno.";
  else next.message = `Dados: ${first} y ${second}. Elige una jugada.`;
  return next;
}

export function applyMove(state, optionIndex) {
  if (state.phase !== "move" || !Number.isInteger(optionIndex) || !state.options[optionIndex]) {
    throw new RangeError("El movimiento seleccionado no es válido.");
  }
  const next = clone(state);
  const color = currentPlayer(next);
  const option = next.options[optionIndex];
  for (const action of option) {
    if (!movePawn(next, color, action.pawn, action.steps)) {
      throw new Error("La posición cambió y el movimiento ya no es legal.");
    }
  }
  if (next.pawns[color].every((position) => position === FINISH)) {
    next.winner = color;
    next.phase = "over";
    next.options = [];
    next.message = `¡${PLAYERS.find((player) => player.id === color).name} ganó la partida!`;
    return next;
  }
  if (next.dice[0] === next.dice[1]) {
    next.phase = "roll";
    next.options = [];
    next.dice = null;
    next.message = `¡Doble! ${PLAYERS.find((player) => player.id === color).name} tira otra vez.`;
  } else {
    nextPlayer(next);
  }
  return next;
}

export function skipMove(state) {
  if (state.phase !== "move" || state.options.length !== 0) {
    throw new Error("Solo se puede pasar cuando no hay movimientos legales.");
  }
  const next = clone(state);
  if (next.dice[0] === next.dice[1]) {
    const color = currentPlayer(next);
    next.phase = "roll";
    next.dice = null;
    next.message = `¡Doble! ${PLAYERS.find((player) => player.id === color).name} tira otra vez.`;
  } else {
    nextPlayer(next);
  }
  return next;
}

export function describeMove(option) {
  return option.map(({ pawn, steps }) => `Ficha ${pawn + 1} · ${steps} casillas`).join("  +  ");
}
