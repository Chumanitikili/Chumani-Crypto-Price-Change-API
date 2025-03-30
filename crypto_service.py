import os
import logging
import requests
from datetime import datetime
from data_store import DataStore

logger = logging.getLogger(__name__)

class CryptoService:
    """
    Service for retrieving and managing cryptocurrency data
    """
    def __init__(self):
        self.data_store = DataStore()
        self.api_key = os.environ.get("COINGECKO_API_KEY", "")
        self.supported_coins = {
            "bitcoin": "btc",
            "ethereum": "eth",
            "solana": "sol",
            "cardano": "ada"
        }
        
    def update_crypto_data(self):
        """
        Updates cryptocurrency data by fetching from the CoinGecko API
        """
        logger.info("Updating cryptocurrency data...")
        
        # Determine API endpoint based on whether we have an API key
        if self.api_key:
            url = "https://pro-api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": "usd",
                "ids": ",".join(self.supported_coins.keys()),
                "price_change_percentage": "24h",
                "x_cg_pro_api_key": self.api_key
            }
        else:
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": "usd",
                "ids": ",".join(self.supported_coins.keys()),
                "price_change_percentage": "24h"
            }
        
        try:
            # Make API request with timeout
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            coin_data = response.json()
            logger.debug(f"Received data for {len(coin_data)} coins")
            
            updated_data = {}
            for coin in coin_data:
                coin_id = coin["id"]
                symbol = coin["symbol"].upper()
                price = coin["current_price"]
                price_change_24h = coin["price_change_percentage_24h"]
                
                # Format the price change for display
                price_change_formatted = f"{price_change_24h:.2f}%"
                # Determine if price is up or down
                direction = "up" if price_change_24h >= 0 else "down"
                
                updated_data[coin_id] = {
                    "name": coin_id.capitalize(),
                    "symbol": symbol,
                    "current_price": price,
                    "price_change_24h": price_change_24h,
                    "price_change_formatted": price_change_formatted,
                    "direction": direction,
                    "last_updated": datetime.now().isoformat()
                }
            
            # Store the updated data
            self.data_store.save_crypto_data(updated_data)
            logger.info("Cryptocurrency data updated successfully")
            
            return updated_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching crypto data: {str(e)}")
            raise Exception(f"Failed to fetch crypto data: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error updating crypto data: {str(e)}")
            raise Exception(f"Unexpected error: {str(e)}")
    
    def get_all_crypto_data(self):
        """
        Retrieves all stored cryptocurrency data
        """
        return self.data_store.load_crypto_data()
    
    def get_crypto_data(self, coin_id):
        """
        Retrieves data for a specific cryptocurrency
        """
        if coin_id not in self.supported_coins:
            return None
        
        data = self.data_store.load_crypto_data()
        return data.get(coin_id)
    
    def get_braze_formatted_data(self):
        """
        Formats cryptocurrency data for Braze integration using Liquid-compatible format
        """
        data = self.data_store.load_crypto_data()
        braze_data = {}
        
        for coin_id, coin_data in data.items():
            symbol = self.supported_coins.get(coin_id, coin_id)
            
            # Format for Braze's Liquid templating
            braze_data[f"{symbol}_change"] = coin_data["price_change_formatted"]
            braze_data[f"{symbol}_direction"] = coin_data["direction"]
        
        # Add a timestamp for caching purposes
        braze_data["last_updated"] = datetime.now().isoformat()
        
        return braze_data
