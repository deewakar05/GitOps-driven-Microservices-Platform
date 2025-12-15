const express = require('express');

const app = express();

app.get('/', (_req, res) => {
  res.json({ message: 'Hello, DevOps! CI/CD Pipeline Working Successfully' });
});

module.exports = app;
