import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataStore:
    """
    Class for handling data persistence for cryptocurrency information
    """
    def __init__(self, data_file="data/crypto_data.json"):
        self.data_file = data_file
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """
        Ensures the data directory exists
        """
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        # Create empty data file if it doesn't exist
        if not os.path.exists(self.data_file):
            self._write_empty_data()
    
    def _write_empty_data(self):
        """
        Writes an empty data structure to the file
        """
        try:
            with open(self.data_file, 'w') as file:
                json.dump({
                    "bitcoin": {
                        "name": "Bitcoin",
                        "symbol": "BTC",
                        "current_price": 0,
                        "price_change_24h": 0,
                        "price_change_formatted": "0.00%",
                        "direction": "up",
                        "last_updated": datetime.now().isoformat()
                    },
                    "ethereum": {
                        "name": "Ethereum",
                        "symbol": "ETH",
                        "current_price": 0,
                        "price_change_24h": 0,
                        "price_change_formatted": "0.00%",
                        "direction": "up",
                        "last_updated": datetime.now().isoformat()
                    },
                    "solana": {
                        "name": "Solana",
                        "symbol": "SOL",
                        "current_price": 0,
                        "price_change_24h": 0,
                        "price_change_formatted": "0.00%",
                        "direction": "up",
                        "last_updated": datetime.now().isoformat()
                    },
                    "cardano": {
                        "name": "Cardano",
                        "symbol": "ADA",
                        "current_price": 0,
                        "price_change_24h": 0,
                        "price_change_formatted": "0.00%",
                        "direction": "up",
                        "last_updated": datetime.now().isoformat()
                    }
                }, file, indent=2)
        except Exception as e:
            logger.error(f"Error creating initial data file: {str(e)}")
    
    def save_crypto_data(self, data):
        """
        Saves cryptocurrency data to the JSON file
        
        Args:
            data (dict): Dictionary containing cryptocurrency data
        """
        try:
            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=2)
            logger.debug(f"Data saved to {self.data_file}")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            raise Exception(f"Failed to save data: {str(e)}")
    
    def load_crypto_data(self):
        """
        Loads cryptocurrency data from the JSON file
        
        Returns:
            dict: Dictionary containing cryptocurrency data
        """
        try:
            with open(self.data_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.warning(f"Data file not found: {self.data_file}")
            self._write_empty_data()
            return self.load_crypto_data()
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in data file: {self.data_file}")
            self._write_empty_data()
            return self.load_crypto_data()
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise Exception(f"Failed to load data: {str(e)}")
