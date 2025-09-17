const express = require("express");
const multer = require("multer");
const Resume = require("../models/Resume");
const auth = require("../middleware/authMiddleware");

const router = express.Router();

const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, "uploads/"),
  filename: (req, file, cb) => cb(null, Date.now() + "-" + file.originalname),
});

const upload = multer({ storage });

// Upload resume
router.post("/upload", auth, upload.single("resume"), async (req, res) => {
  try {
    const resume = new Resume({
      user: req.user.id,
      filePath: req.file.path,
      skills: req.body.skills ? req.body.skills.split(",") : [],
      experience: req.body.experience || ""
    });

    await resume.save();
    res.json({ msg: "Resume uploaded successfully", resume });
  } catch (err) {
    res.status(500).send("Server error");
  }
});

module.exports = router;
