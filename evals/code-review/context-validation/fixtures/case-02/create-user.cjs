const { saveUser } = require('./save-user.cjs');

function createUser(input, users) {
  return saveUser(input, users);
}

module.exports = { createUser };
