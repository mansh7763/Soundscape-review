# Soundscape Review Web Application

## Overview

Soundscape Review is a web application designed to collect human feedback on AI-generated soundscapes. The feedback is used to improve soundscape generation models through Reinforcement Learning from Human Feedback (RLHF). Users listen to various soundscape audio clips, rate their quality and realism, and submit reviews. The application stores these reviews in a PostgreSQL database for further analysis and model training.

---

## Features

- 🎵 **Audio Review Interface:**
  - Listen to soundscape audio files directly on the web page.
  - Each audio has a title, play button, 0-5 star rating, and a submit button.
- 📝 **Instructions Section:**
  - Clear instructions for users about the review process and its purpose.
- ⭐ **Rating System:**
  - Interactive star-based rating for each audio file.
- 💾 **Database Storage:**
  - Stores each review (audio file, title, rating, timestamp, user info) in a PostgreSQL database.
- 📊 **Admin Endpoints:**
  - View all reviews and basic statistics via `/reviews` and `/stats` endpoints.
- 🌐 **Responsive Design:**
  - Modern, mobile-friendly UI using HTML and CSS.

---

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Database:** PostgreSQL
- **Deployment:** Railway (recommended), or any Python-friendly host

---

## Project Structure

```
Soundscape-review/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── Procfile              # For deployment (Gunicorn)
├── README.md             # Project documentation
├── .env                  # Environment variables (not committed)
├── static/
│   └── audio/            # Audio files for review
├── templates/
│   └── index.html        # Main HTML template
└── vercel.json           # (Optional) For Vercel deployment
```

---
