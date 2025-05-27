# StockWizard Project

A modern web-based stock trading platform with real-time tracking, portfolio management, and AI-powered insights.

## Features 🚀

- Real-time stock tracking and price updates
- Portfolio management and analysis
- Market news integration
- Machine Learning predictions and analysis
- User authentication and profile management
- Dark/light theme support
- Responsive modern UI with Bootstrap 5

## Prerequisites 📋

- Python 3.8+
- pip (Python package manager)
- Web browser (Chrome/Firefox recommended)
- API Keys (required):
  - Alpha Vantage API key
  - Finnhub API key
  - Twelve Data API key

## Installation 🛠️

1. Clone the repository:
```bash
git clone https://github.com/yourusername/StockWizard.git
cd StockWizard
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API keys:
```
FLASK_SECRET_KEY=your_secure_key_here
ALPHA_VANTAGE_KEY=your_key_here
FINNHUB_KEY=your_key_here
TWELVE_DATA_KEY=your_key_here
```

## Project Structure 📁

```
StockWizard/
├── app.py                 # Main Flask application
├── static/               # Static assets
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   └── images/          # Image assets
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── login.html       # Authentication pages
│   ├── portfolio.html   # Portfolio management
│   └── watchlist.html   # Stock watchlist
├── ml/                  # Machine Learning models
│   └── models/
│       ├── lstm_predictor.py
│       ├── pattern_detector.py
│       ├── portfolio_optimizer.py
│       ├── risk_analyzer.py
│       └── sentiment_analyzer.py
├── services/           # Backend services
│   └── data_fetcher.py # API integration
└── requirements.txt    # Python dependencies
```

## Running the Application 🚀

1. Ensure all API keys are set in `.env`
2. Start the Flask server:
```bash
python app.py
```
3. Open your browser and navigate to:
```
http://localhost:5000
```

## Machine Learning Features 🤖

- Stock Price Prediction (LSTM)
- Market Sentiment Analysis
- Portfolio Optimization
- Risk Analysis
- Pattern Detection

## Technical Details 💻

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend**: Python Flask
- **Data Sources**: Alpha Vantage, Finnhub, Twelve Data
- **ML Libraries**: TensorFlow, scikit-learn
- **Additional Features**:
  - Real-time data updates
  - Interactive charts
  - Responsive design
  - Error handling
  - Data caching
  - Input validation
  - API rate limiting

## Security Features 🔒

- Environment variables for sensitive data
- Secure authentication system
- Input validation and sanitization
- API rate limiting
- Error handling

## Contributing 🤝

Feel free to fork the repository and submit pull requests for any improvements.


