# Presidency University - AI Smart Gate & Face Recognition System

> **Hackathon Solution**: Automated Real-Time Facial Recognition Gate Entry & Access Verification System for Presidency University Campus.

---

## Problem Statement & Objective
At **Presidency University**, student entry at main campus gates currently requires manual physical ID card checking, leading to:
- **Long queues and severe delays** during peak morning entry hours.
- **Manual overhead & security risks** (lost or misplaced ID cards, fake ID cards).
- **Lack of real-time digital access logs** for campus security administration.

### The AI Solution
**Presidency-GatePass-AI** is a high-speed, 100% Python-based facial recognition system built using **OpenCV**, **LBPH / Embedding Deep Recognition**, **SQLite**, and **Flask**. It delivers:
- **Instant sub-second face identification & verification**.
- **Anti-Spoofing & Liveness Detection** (liveness checks & eye cascade tracking to prevent photo/screen spoofing).
- **Automated Voice Greetings** & High-Tech HUD Overlays.
- **Real-Time Security Dashboard & Audit Logs** with CSV export functionality.
- **Dual Modes**: Web Dashboard UI for campus admins & Desktop Kiosk GUI for gate terminals.

---

## Architecture & Tech Stack
- **Language**: Python 3.10+
- **Computer Vision Engine**: OpenCV (`cv2`, Haar Cascade Face & Eye Detectors, LBPH Face Recognizer)
- **Backend & Database**: Flask, SQLite3, RESTful APIs
- **Web UI**: HTML5, Modern CSS3 (Dark-Mode Glassmorphism, Google Fonts), Vanilla JS (Web Speech API TTS)
- **Desktop UI**: Tkinter + Pillow (PIL)

---

## Project Directory Structure
```
presidency_gate_pass/
├── app.py                # Main Flask Web Server & Video Streaming
├── face_engine.py        # OpenCV Face Detection & Recognition AI Engine
├── database.py           # SQLite Database Manager (Students & Logs)
├── seed_demo_data.py     # Script to generate sample students & train AI
├── gui_app.py            # Standalone Desktop Kiosk Application
├── requirements.txt      # Python library dependencies
├── README.md             # Project documentation & setup
├── templates/
│   └── index.html        # Glassmorphism Web Dashboard Template
└── static/
    ├── css/style.css     # Dark mode UI styling & animations
    └── js/app.js         # Frontend polling, TTS voice alerts, JS logic
```

## Run Globally
