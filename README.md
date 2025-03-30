# Chumani Crypto Price Change API

A Python-based API service that retrieves, stores, and serves cryptocurrency price changes for integration with Braze marketing platform.

## Features

- Real-time cryptocurrency data for Bitcoin, Ethereum, Solana, and Cardano
- Focus on 24-hour price changes with formatted display
- Automatic updates every 15 minutes
- Braze-ready integration with Liquid template format
- Clean, responsive UI built with Bootstrap
- Comprehensive API documentation

## API Endpoints

- `/api/crypto/all` - Get data for all cryptocurrencies
- `/api/crypto/{coin_id}` - Get data for a specific cryptocurrency
- `/api/braze` - Get data formatted for Braze integration
- `/api/update` - Force a manual update of the data

## Technologies Used

- Python/Flask
- CoinGecko API for cryptocurrency data
- Bootstrap for responsive UI
- APScheduler for automated updates
- JSON-based data storage

## Getting Started

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt`
3. Run with `gunicorn --bind 0.0.0.0:5000 main:app`

## Optional: CoinGecko API Key

For higher rate limits, you can add a CoinGecko API key as an environment variable:
```
export COINGECKO_API_KEY="your_api_key_here"
```