const { saveUser } = require('./save-user.cjs');

function createUser(input, users) {
  if (
    input === null ||
    typeof input !== 'object' ||
    Array.isArray(input) ||
    typeof input.name !== 'string' ||
    input.name.trim().length === 0
  ) {
    throw new TypeError('A nonblank name is required.');
  }

  return saveUser(input, users);
}

module.exports = { createUser };
