const cluster = require("cluster");
const express = require("express");
const fs = require("fs");

const port = 8004;

const jsonData = JSON.parse(fs.readFileSync("./test_data.json", "utf8"));
const cpus = require("os").cpus().length;

if (cluster.isMaster) {
  console.log(`Master pid ${process.pid}`);
  for (let i = 0; i < cpus; i++) {
    cluster.fork();
  }

  cluster.on("exit", (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`);
    console.log("Restarting worker...");
    cluster.fork();
  });
} else {
  console.log(`Worker pid ${process.pid}`);
  const app = express();
  app.get("/children", async (req, res) => {
    res.json(jsonData);
  });

  app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
  });
}
