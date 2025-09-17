const mongoose = require("mongoose");

const resumeSchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: "User", required: true },
  filePath: { type: String }, // uploaded file path
  skills: [String], // structured skill data extracted
  experience: String
});

module.exports = mongoose.model("Resume", resumeSchema);
