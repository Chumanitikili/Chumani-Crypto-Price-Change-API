import os
import logging
from flask import Flask, render_template, jsonify
from crypto_service import CryptoService
from apscheduler.schedulers.background import BackgroundScheduler

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

# Initialize crypto service
crypto_service = CryptoService()

# Schedule update job to run every 15 minutes
scheduler = BackgroundScheduler()
scheduler.add_job(crypto_service.update_crypto_data, 'interval', minutes=15)
scheduler.start()

@app.route('/')
def index():
    """Renders the homepage with current crypto data"""
    crypto_data = crypto_service.get_all_crypto_data()
    return render_template('index.html', crypto_data=crypto_data)

@app.route('/api/crypto/all')
def get_all_crypto():
    """API endpoint to get all crypto data"""
    try:
        data = crypto_service.get_all_crypto_data()
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error getting all crypto data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/crypto/<coin>')
def get_crypto(coin):
    """API endpoint to get specific cryptocurrency data"""
    try:
        data = crypto_service.get_crypto_data(coin.lower())
        if data:
            return jsonify(data)
        return jsonify({"error": "Cryptocurrency not found"}), 404
    except Exception as e:
        logger.error(f"Error getting crypto data for {coin}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/braze')
def get_braze_data():
    """API endpoint that formats data for Braze integration"""
    try:
        data = crypto_service.get_braze_formatted_data()
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error getting Braze formatted data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/documentation')
def documentation():
    """Renders the API documentation page"""
    return render_template('documentation.html')

@app.route('/api/update', methods=['POST'])
def force_update():
    """Endpoint to manually trigger data update"""
    try:
        crypto_service.update_crypto_data()
        return jsonify({"status": "success", "message": "Data updated successfully"})
    except Exception as e:
        logger.error(f"Error updating crypto data: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Initialize data on startup
with app.app_context():
    try:
        crypto_service.update_crypto_data()
        logger.info("Initial crypto data update completed")
    except Exception as e:
        logger.error(f"Failed to update crypto data on startup: {str(e)}")
