const express = require("express");
const TestResult = require("../models/TestResult");
const auth = require("../middleware/authMiddleware");

const router = express.Router();

// Submit test result
router.post("/submit", auth, async (req, res) => {
  const { score } = req.body;
  try {
    const passed = score >= 60; // Passing score condition

    const testResult = new TestResult({
      user: req.user.id,
      score,
      passed,
    });

    await testResult.save();
    res.json({ msg: "Test submitted successfully", passed });
  } catch (err) {
    res.status(500).send("Server error");
  }
});

// Get user result
router.get("/myresult", auth, async (req, res) => {
  try {
    const result = await TestResult.findOne({ user: req.user.id });
    res.json(result);
  } catch (err) {
    res.status(500).send("Server error");
  }
});

module.exports = router;
