const app = require('./app');

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  // Keep the log minimal to avoid noisy CI output.
  console.log(`Server running on port ${PORT}`);
});
