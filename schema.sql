CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE,
  password TEXT,
  backup TEXT

);


CREATE TABLE secrets (
  id SERIAL PRIMARY KEY,
  owner TEXT REFERENCES users(username),
  secret TEXT
);
