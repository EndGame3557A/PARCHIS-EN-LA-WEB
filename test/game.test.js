import test from "node:test";
import assert from "node:assert/strict";
import {
  FINISH,
  TRACK_LENGTH,
  RULESETS,
  createGame,
  currentPlayer,
  rollDice,
  applyMove,
  skipMove,
} from "../public/game.js";

test("the game rejects dice outside the valid range", () => {
  const state = createGame();
  assert.throws(() => rollDice(state, [0, 7]), /valores entre 1 y 6/);
});

test("a double releases one pawn and grants another roll", () => {
  const state = rollDice(createGame(), [4, 4]);
  assert.equal(state.pawns.green[0], 0);
  assert.equal(state.phase, "roll");
  assert.equal(state.turn, 0);
});

test("a player who fails three jail attempts loses the turn", () => {
  let state = createGame();
  state = rollDice(state, [1, 2]);
  state = rollDice(state, [2, 3]);
  state = rollDice(state, [1, 6]);
  assert.equal(currentPlayer(state), "red");
  assert.equal(state.jailAttempts.green, 0);
});

test("moving both dice applies each move and passes to the next team", () => {
  let state = createGame();
  state.pawns.green[0] = 0;
  state.pawns.green[1] = 0;
  state = rollDice(state, [1, 2]);
  const split = state.options.findIndex((option) => option.length === 2);
  assert.notEqual(split, -1);
  state = applyMove(state, split);
  assert.deepEqual(state.pawns.green.slice(0, 2), [1, 2]);
  assert.equal(currentPlayer(state), "red");
});

test("a token must roll the exact remaining distance to finish", () => {
  const state = createGame();
  state.pawns.green = [FINISH - 2, FINISH, FINISH, FINISH];
  const rolled = rollDice(state, [1, 1]);
  const completed = applyMove(rolled, 0);
  assert.equal(completed.pawns.green[0], FINISH);
  assert.equal(completed.winner, "green");

  const tooFar = createGame();
  tooFar.pawns.green = [FINISH - 1, FINISH, FINISH, FINISH];
  const blockedRoll = rollDice(tooFar, [1, 1]);
  assert.equal(blockedRoll.options.length, 0);
  assert.equal(blockedRoll.phase, "move");
});

test("a lone opponent is sent home on an unsafe square", () => {
  const state = createGame();
  state.pawns.green[0] = 2;
  state.pawns.red[0] = 56;
  const rolled = rollDice(state, [1, 2]);
  const moved = applyMove(rolled, 0);
  assert.equal(moved.pawns.green[0], 5);
  assert.equal(moved.pawns.red[0], null);
  assert.equal(moved.captures.green, 1);
});

test("safe squares protect an opponent from capture", () => {
  const state = createGame();
  state.pawns.green[0] = 2;
  state.pawns.red[0] = 58;
  const rolled = rollDice(state, [2, 3]);
  const moved = applyMove(rolled, 0);
  assert.equal(moved.pawns.green[0], 7);
  assert.equal(moved.pawns.red[0], 58);
});

test("the third consecutive double sends the furthest pawn home", () => {
  let state = createGame();
  state.pawns.green = [1, 10, FINISH, FINISH];
  for (const dice of [[2, 2], [3, 3], [4, 4]]) {
    state = rollDice(state, dice);
    state = applyMove(state, 0);
  }
  assert.equal(state.pawns.green[1], FINISH);
});

test("a team wins after all four tokens reach home", () => {
  const state = createGame();
  state.pawns.green = [FINISH, FINISH, FINISH, FINISH - 2];
  state.phase = "move";
  state.dice = [1, 1];
  state.options = [[{ pawn: 3, steps: 2 }]];
  const completed = applyMove(state, 0);
  assert.equal(completed.winner, "green");
  assert.equal(completed.phase, "over");
});

test("a turn can only be passed when no legal move exists", () => {
  const state = createGame();
  state.phase = "move";
  state.dice = [1, 2];
  state.options = [];
  assert.equal(currentPlayer(skipMove(state)), "red");
  state.options = [[{ pawn: 0, steps: 3 }]];
  assert.throws(() => skipMove(state), /no hay movimientos legales/);
});

test("a double gives another roll even when it has no legal move", () => {
  const state = createGame();
  state.phase = "move";
  state.dice = [3, 3];
  state.options = [];
  const next = skipMove(state);
  assert.equal(currentPlayer(next), "green");
  assert.equal(next.phase, "roll");
});

test("La Previa starts with one pawn on the track and doubles movement", () => {
  const state = createGame(undefined, RULESETS.previa);
  assert.equal(state.tokensPerPlayer, 1);
  assert.deepEqual(state.pawns.green, [0, FINISH, FINISH, FINISH]);
  const rolled = rollDice(state, [1, 2]);
  assert.equal(rolled.options.length, 1);
  assert.deepEqual(rolled.options[0], [{ pawn: 0, steps: 6 }]);
  assert.equal(applyMove(rolled, 0).pawns.green[0], 6);
});

test("La Previa ends when its single active pawn reaches the goal", () => {
  const state = createGame(undefined, RULESETS.previa);
  state.pawns.green[0] = FINISH - 6;
  const rolled = rollDice(state, [1, 2]);
  const completed = applyMove(rolled, 0);
  assert.equal(completed.winner, "green");
  assert.equal(completed.phase, "over");
});

test("board constants define a complete outer path and home lane", () => {
  assert.equal(TRACK_LENGTH, 68);
  assert.equal(FINISH, 76);
});
