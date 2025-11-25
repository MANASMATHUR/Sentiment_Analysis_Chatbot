# Chatbot with Sentiment Analysis

This is a Python-based chatbot that performs sentiment analysis on user conversations. It features a modern Web UI, a robust FastAPI backend, and impressive visual analytics.

## Features

- **Tier 1**: Analyzes the overall conversation sentiment (Positive, Negative, Neutral) and detects mood trends.
- **Tier 2**: Real-time sentiment analysis for each user message with on-screen labels.
- **Real-time Chart**: Live visualization of the conversation's sentiment trend using Chart.js.
- **Dark Mode**: Fully supported dark theme for a premium experience.
- **Typing Indicators**: Realistic interaction cues.
- **Web Interface**: Responsive UI with glassmorphism design.

## Technologies

- **Python 3**
- **FastAPI**: Web framework.
- **vaderSentiment**: Sentiment analysis engine.
- **Chart.js**: Data visualization.
- **Vanilla JS & CSS**: Frontend logic and styling.

## Setup & Running

1. **Clone the repository** (if applicable).

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   uvicorn src.app:app --reload
   ```

5. **Open in Browser**:
   Go to `http://127.0.0.1:8000`

6. **Optional CLI mode** *(useful for demos/tests)*:
   ```bash
   python -m src.main
   ```
   Type `exit` or `quit` to end the session and view the overall sentiment summary.

## Project Structure

```
.
├── src/
│   ├── app.py         # FastAPI backend
│   ├── analyzer.py    # Sentiment logic
│   ├── chatbot.py     # Conversation manager
│   ├── templates/
│   │   └── index.html # Frontend HTML
│   └── static/
│       ├── style.css  # Premium styling
│       └── script.js  # Frontend logic
├── tests/             # Unit tests
├── requirements.txt
└── README.md
```

## Sentiment Logic

- **Engine**: [VADER Sentiment](https://github.com/cjhutto/vaderSentiment) via `SentimentIntensityAnalyzer`.
- **Per-message (Tier 2)**:
  - `compound >= 0.05` → Positive
  - `compound <= -0.05` → Negative
  - otherwise Neutral
- **Conversation-level (Tier 1)**:
  - Every exchange in the history (user + bot) is rescored and averaged.
  - Trend detection compares the first and second half of the score timeline to classify the trajectory as *Improving*, *Declining*, or *Stable*.
  - A natural language direction string (e.g., “Negative – general dissatisfaction detected. Mood declined...”) is generated to clearly state the emotional direction of the whole conversation.

## Tier Status

- **Tier 1**  Implemented (conversation summary endpoint + UI/CLI modal).
- **Tier 2** ✔️ Implemented (per message sentiment labels, chart, API responses).
- **Enhancements**: Mood trend summary, optional CLI mode, live visualization, dark mode, typing indicators.

## Tests

Unit and API tests are included under `tests/`.

```bash
pytest
```
