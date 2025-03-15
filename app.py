from flask import Flask, jsonify, request, render_template, session, redirect, url_for, flash
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv
from services.data_fetcher import DataFetcher
from ml.models.lstm_predictor import LSTMPredictor
from ml.models.pattern_detector import PatternDetector
from ml.models.portfolio_optimizer import PortfolioOptimizer
from ml.models.risk_analyzer import RiskAnalyzer
from ml.models.sentiment_analyzer import SentimentAnalyzer
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dj39dj3k2jd92jd92j9d2j9d29jd92jd92')
CORS(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize components
data_fetcher = DataFetcher()
lstm_predictor = LSTMPredictor()
pattern_detector = PatternDetector()
portfolio_optimizer = PortfolioOptimizer()
risk_analyzer = RiskAnalyzer()
sentiment_analyzer = SentimentAnalyzer()

# Initialize scheduler for background tasks
scheduler = BackgroundScheduler()
scheduler.start()

# Cache for storing computed results
prediction_cache = {}
analysis_cache = {}

# Mock user database (replace with real database in production)
users = {}

class User(UserMixin):
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

@app.route('/')
def index():
    featured_stocks = get_featured_stocks()
    market_news = get_market_news()
    return render_template('index.html', 
                         featured_stocks=featured_stocks,
                         market_news=market_news,
                         current_user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find user by email (mock implementation)
        user = next((u for u in users.values() if u.email == email), None)
        
        if user and check_password_hash(users[user.id]['password'], password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        
        flash('Invalid email or password', 'danger')
    return redirect(url_for('index'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if next((u for u in users.values() if u.email == email), None):
        flash('Email already registered', 'danger')
        return redirect(url_for('index'))
    
    user_id = str(len(users) + 1)
    user = User(user_id, username, email)
    users[user_id] = {
        'username': username,
        'email': email,
        'password': generate_password_hash(password),
        'portfolio': [],
        'watchlist': [],
        'first_name': '',
        'last_name': '',
        'display_name': '',
        'phone': '',
        'experience': '',
        'goals': [],
        'bio': '',
        'avatar_url': ''
    }
    
    login_user(user)
    flash('Registration successful!', 'success')
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/portfolio')
@login_required
def portfolio():
    if current_user.id in users:
        portfolio_data = users[current_user.id].get('portfolio', [])
        # Get current prices and calculate portfolio value
        total_value = 0
        for stock in portfolio_data:
            current_price = data_fetcher.get_stock_price(stock['symbol'])
            stock['current_price'] = current_price
            stock['value'] = current_price * stock['shares']
            total_value += stock['value']
        
        return render_template('portfolio.html',
                             portfolio=portfolio_data,
                             total_value=total_value)
    return render_template('portfolio.html', portfolio=[], total_value=0)

@app.route('/watchlist')
@login_required
def watchlist():
    if current_user.id in users:
        watchlist_data = users[current_user.id].get('watchlist', [])
        # Get current prices and analysis
        for stock in watchlist_data:
            current_price = data_fetcher.get_stock_price(stock['symbol'])
            stock['current_price'] = current_price
            stock['analysis'] = get_stock_analysis(stock['symbol'])
        
        return render_template('watchlist.html', watchlist=watchlist_data)
    return render_template('watchlist.html', watchlist=[])

@app.route('/profile')
@login_required
def profile():
    if current_user.id in users:
        user_data = users[current_user.id]
        portfolio_value = sum(stock['shares'] * data_fetcher.get_stock_price(stock['symbol'])
                            for stock in user_data.get('portfolio', []))
        return render_template('profile.html',
                             user=user_data,
                             portfolio_value=portfolio_value)
    return redirect(url_for('index'))

@app.route('/news')
def news():
    market_news = get_market_news()
    return render_template('news.html', news=market_news)

@app.route('/api/stock/<symbol>')
def get_stock_data(symbol):
    """Get comprehensive stock data including predictions and analysis"""
    try:
        # Get basic stock data
        price = data_fetcher.get_stock_price(symbol)
        hist_data = data_fetcher.get_historical_data(symbol)
        
        if price and hist_data is not None:
            # Calculate daily change
            daily_change = (hist_data['Close'].iloc[-1] - hist_data['Close'].iloc[-2]) / hist_data['Close'].iloc[-2] * 100
            
            # Get AI predictions
            predictions = get_stock_predictions(symbol, hist_data)
            
            # Get technical analysis
            technical_analysis = get_technical_analysis(symbol, hist_data)
            
            # Get sentiment analysis
            sentiment = sentiment_analyzer.analyze(symbol)
            
            return jsonify({
                'symbol': symbol,
                'price': price,
                'change': daily_change,
                'predictions': predictions,
                'technical': technical_analysis,
                'sentiment': sentiment,
                'history': [
                    {'date': date.strftime('%Y-%m-%d'), 'price': float(row['Close'])}
                    for date, row in hist_data.iterrows()
                ]
            })
        return jsonify({'error': 'Failed to fetch stock data'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/portfolio/add', methods=['POST'])
@login_required
def add_to_portfolio():
    data = request.json
    symbol = data.get('symbol')
    shares = data.get('shares', 0)
    
    if not symbol or shares <= 0:
        return jsonify({'error': 'Invalid input'}), 400
    
    if current_user.id in users:
        portfolio = users[current_user.id].get('portfolio', [])
        # Check if stock already in portfolio
        for stock in portfolio:
            if stock['symbol'] == symbol:
                stock['shares'] += shares
                break
        else:
            portfolio.append({
                'symbol': symbol,
                'shares': shares,
                'purchase_date': datetime.now().strftime('%Y-%m-%d')
            })
        users[current_user.id]['portfolio'] = portfolio
        return jsonify({'message': 'Stock added to portfolio'})
    
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/watchlist/add', methods=['POST'])
@login_required
def add_to_watchlist():
    data = request.json
    symbol = data.get('symbol')
    
    if not symbol:
        return jsonify({'error': 'Invalid input'}), 400
    
    if current_user.id in users:
        watchlist = users[current_user.id].get('watchlist', [])
        if not any(stock['symbol'] == symbol for stock in watchlist):
            watchlist.append({
                'symbol': symbol,
                'added_date': datetime.now().strftime('%Y-%m-%d')
            })
            users[current_user.id]['watchlist'] = watchlist
            return jsonify({'message': 'Stock added to watchlist'})
        return jsonify({'message': 'Stock already in watchlist'})
    
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/profile/update', methods=['POST'])
@login_required
def update_profile():
    if current_user.id in users:
        try:
            # Handle file upload
            avatar = request.files.get('avatarInput')
            if avatar:
                # Save avatar to static/images/avatars/
                avatar_dir = os.path.join(app.static_folder, 'images', 'avatars')
                os.makedirs(avatar_dir, exist_ok=True)
                avatar_path = os.path.join(avatar_dir, f'{current_user.id}.jpg')
                avatar.save(avatar_path)
                users[current_user.id]['avatar_url'] = f'/static/images/avatars/{current_user.id}.jpg'
            
            # Update user data
            users[current_user.id].update({
                'first_name': request.form.get('first_name'),
                'last_name': request.form.get('last_name'),
                'display_name': request.form.get('display_name'),
                'phone': request.form.get('phone'),
                'experience': request.form.get('experience'),
                'goals': request.form.getlist('goals[]'),
                'bio': request.form.get('bio')
            })
            
            flash('Profile updated successfully!', 'success')
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    return jsonify({'success': False, 'error': 'User not found'}), 404

@app.route('/settings')
@login_required
def settings():
    if current_user.id in users:
        user_data = users[current_user.id]
        return render_template('settings.html',
                             user=user_data)
    return redirect(url_for('index'))

@app.route('/api/portfolio/remove', methods=['POST'])
@login_required
def remove_from_portfolio():
    data = request.json
    symbol = data.get('symbol')
    
    if not symbol:
        return jsonify({'error': 'Invalid input'}), 400
    
    if current_user.id in users:
        portfolio = users[current_user.id].get('portfolio', [])
        users[current_user.id]['portfolio'] = [stock for stock in portfolio if stock['symbol'] != symbol]
        return jsonify({'message': 'Stock removed from portfolio'})
    
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/watchlist/remove', methods=['POST'])
@login_required
def remove_from_watchlist():
    data = request.json
    symbol = data.get('symbol')
    
    if not symbol:
        return jsonify({'error': 'Invalid input'}), 400
    
    if current_user.id in users:
        watchlist = users[current_user.id].get('watchlist', [])
        users[current_user.id]['watchlist'] = [stock for stock in watchlist if stock['symbol'] != symbol]
        return jsonify({'message': 'Stock removed from watchlist'})
    
    return jsonify({'error': 'User not found'}), 404

def get_featured_stocks():
    """Get data for featured stocks with AI insights"""
    featured_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    stocks_data = []
    
    for symbol in featured_symbols:
        try:
            price = data_fetcher.get_stock_price(symbol)
            if price:
                hist_data = data_fetcher.get_historical_data(symbol)
                if hist_data is not None:
                    daily_change = (hist_data['Close'].iloc[-1] - hist_data['Close'].iloc[-2]) / hist_data['Close'].iloc[-2] * 100
                    predictions = get_stock_predictions(symbol, hist_data)
                    stocks_data.append({
                        'symbol': symbol,
                        'price': price,
                        'change': daily_change,
                        'predictions': predictions
                    })
        except Exception as e:
            print(f"Error processing {symbol}: {str(e)}")
            continue
    
    return stocks_data

def get_stock_predictions(symbol, hist_data):
    """Get stock predictions using multiple ML models"""
    cache_key = f"{symbol}_{datetime.now().strftime('%Y-%m-%d')}"
    
    # Check cache
    if cache_key in prediction_cache:
        return prediction_cache[cache_key]
    
    try:
        # Get LSTM predictions
        lstm_pred = lstm_predictor.predict(hist_data)
        
        # Get technical patterns
        patterns = pattern_detector.detect_patterns(hist_data)
        
        # Get sentiment
        sentiment = sentiment_analyzer.analyze(symbol)
        
        predictions = {
            'price_target': lstm_pred['price_target'],
            'confidence': lstm_pred['confidence'],
            'patterns': patterns,
            'sentiment': sentiment
        }
        
        # Cache predictions
        prediction_cache[cache_key] = predictions
        return predictions
    except Exception as e:
        print(f"Error getting predictions for {symbol}: {str(e)}")
        return None

def get_stock_analysis(symbol):
    """Get comprehensive stock analysis"""
    try:
        hist_data = data_fetcher.get_historical_data(symbol)
        if hist_data is not None:
            predictions = get_stock_predictions(symbol, hist_data)
            technical = get_technical_analysis(symbol, hist_data)
            sentiment = sentiment_analyzer.analyze(symbol)
            
            return {
                'predictions': predictions,
                'technical': technical,
                'sentiment': sentiment
            }
    except Exception as e:
        print(f"Error analyzing {symbol}: {str(e)}")
    return None

def cleanup_cache():
    """Clean up old cache entries"""
    current_date = datetime.now().strftime('%Y-%m-%d')
    prediction_cache.clear()
    analysis_cache.clear()

# Schedule cache cleanup daily
scheduler.add_job(cleanup_cache, 'cron', hour=0)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
