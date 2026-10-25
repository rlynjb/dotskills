// Evaluator-only: establish fixture truth, not model or skill performance.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { createUser: guarded } = require('./fixtures/case-01/create-user.cjs');
const { createUser: unguarded } = require('./fixtures/case-02/create-user.cjs');

for (const filename of ['save-user.cjs', 'requirements.md']) {
  const read = (id) => fs.readFileSync(path.join(__dirname, 'fixtures', id, filename));
  assert.deepEqual(read('case-01'), read('case-02'), filename + ' must match');
}

for (const createUser of [guarded, unguarded]) {
  for (const name of ['Ada', '  Ada  ', '0']) {
    const users = [];
    const input = { name, extra: 'ignored' };
    const result = createUser(input, users);
    assert.deepEqual(users, [{ name }]);
    assert.equal(result, users[0]);
    assert.deepEqual(input, { name, extra: 'ignored' });
  }
}

const invalidInputs = [
  null, false, 7, 'Ada', [], {}, { name: null }, { name: 7 },
  { name: '' }, { name: '   ' }, { name: '\t\n' },
];
for (const input of invalidInputs) {
  const users = [];
  assert.throws(() => guarded(input, users), TypeError);
  assert.deepEqual(users, []);
}

for (const input of [{ name: '   ' }, { name: '' }, { name: 7 }, {}]) {
  const users = [];
  const result = unguarded(input, users);
  assert.deepEqual(users, [{ name: input.name }]);
  assert.equal(result, users[0]);
}

console.log('PASS: fixture behavior matches the evaluator answer key.');
console.log('No model reviews were run; no skill-quality score was produced.');
