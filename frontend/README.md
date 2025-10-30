# DetoxifyAI Frontend

A beautiful web interface for real-time toxicity detection using the DetoxifyAI ML model.

## Quick Start

### 1. Start the FastAPI Backend

```bash
# From the root directory
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 2. Open the Frontend

Simply open `frontend/index.html` in your web browser, or serve it with a simple HTTP server:

```bash
# Option 1: Open directly
# Just double-click index.html

# Option 2: Python HTTP server
cd frontend
python -m http.server 3000
# Then visit http://localhost:3000
```

## Features

- **Real-time Analysis**: Enter text and get instant toxicity predictions
- **Confidence Scores**: See how confident the model is in its prediction
- **Toxicity Probability**: View the raw probability score
- **Example Buttons**: Quick test with pre-written examples
- **API Status Indicator**: See if the API and model are loaded
- **Responsive Design**: Works on desktop and mobile

## API Endpoints

The frontend connects to these FastAPI endpoints:

- `GET /health` - Check API and model status
- `POST /predict` - Analyze text for toxicity

## How It Works

1. User enters text in the textarea
2. Frontend sends POST request to `/predict` endpoint
3. Backend:
   - Preprocesses the text (lowercase, remove URLs, etc.)
   - Transforms text using TF-IDF vectorizer
   - Runs prediction using trained model
   - Returns prediction + confidence scores
4. Frontend displays results with visual indicators

## Mock Mode

If the model files are not found, the API runs in "mock mode" and returns placeholder predictions. This allows you to test the frontend before training your model.

## Screenshots

The frontend includes:
- Clean, modern gradient design
- Visual confidence meters
- Color-coded predictions (red for toxic, green for non-toxic)
- Example buttons for quick testing

## Tech Stack

- **Frontend**: Vanilla HTML, CSS, JavaScript
- **Backend**: FastAPI + Python
- **ML**: Scikit-learn (Logistic Regression) + TF-IDF
- **Styling**: Custom CSS with gradient backgrounds
