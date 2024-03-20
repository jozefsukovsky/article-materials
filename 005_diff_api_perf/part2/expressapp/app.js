const express = require("express");
const fs = require("fs");

const app = express();
const port = 8004;

const jsonData = JSON.parse(fs.readFileSync("./test_data.json", "utf8"));

app.get("/children", async (req, res) => {
  res.json(jsonData);
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
