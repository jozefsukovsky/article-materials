require("dotenv").config({ path: "../.env" });

const express = require("express");
const app = express();
const port = 8004;

const { PrismaClient } = require("@prisma/client");
const prisma = new PrismaClient({
  // log: ["query"],
});

app.get("/children", async (req, res) => {
  const page = req.query.page ? parseInt(req.query.page) : 1;
  const perPage = 30;
  const offset = (page - 1) * perPage;
  try {
    const count = await prisma.child.count({});
    const children = await prisma.child.findMany({
      relationLoadStrategy: "join", // test feature enabled in schema.prisma
      skip: offset,
      take: perPage,
      select: {
        title: true,
        created: true,
        modified: true,
        json_field: true,
        long_text: true,
        parent: {
          select: {
            title: true,
            description: true,
            created: true,
            modified: true,
          },
        },
      },
    });

    const pages = count / perPage;
    const baseUrl = `${req.protocol}://${req.hostname}:${port}${req.path}`;
    const nextPage = page < pages ? `${baseUrl}?page=${page + 1}` : null;
    const previousPage = page > 1 ? `${baseUrl}?page=${page - 1}` : null;

    res.json({
      results: children,
      count,
      next: nextPage,
      previous: previousPage,
    });
  } catch (error) {
    console.error("Error fetching children:", error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
