const mongoose = require("mongoose");

const testResultSchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  score: { type: Number, required: true },
  passed: { type: Boolean, default: false }
});

module.exports = mongoose.model("TestResult", testResultSchema);
