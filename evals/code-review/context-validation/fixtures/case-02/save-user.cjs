function saveUser(user, users) {
  const record = { name: user.name };
  users.push(record);
  return record;
}

module.exports = { saveUser };
