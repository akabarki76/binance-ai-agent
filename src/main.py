import yaml
import os
from src.binance_data import BinanceDataManager
from binance.enums import KLINE_INTERVAL_1MINUTE
from src.ai_engine import analyze_log, optimize_trade_strategy # Import optimize_trade_strategy

def load_config(config_path="config/config.yaml"):
    script_dir = os.path.dirname(__file__)
    absolute_config_path = os.path.join(script_dir, '..', config_path)
    try:
        with open(absolute_config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Config file not found at {absolute_config_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing config file: {e}")
        return None

def main():
    config = load_config()
    if config:
        print("Configuration loaded successfully:")
        binance_api_key = config['api_keys']['binance_key']
        binance_api_secret = config['api_keys']['binance_secret']
        log_level = config['settings']['log_level']

        print(f"Binance API Key (first 5 chars): {binance_api_key[:5]}...")
        print(f"Log Level: {log_level}")

        # Initialize Binance Data Manager
        data_manager = BinanceDataManager(binance_api_key, binance_api_secret)

        # Fetch some sample klines data
        try:
            # Fetch enough data for SMA calculation (e.g., limit=30 for 5 and 20 period SMAs)
            klines = data_manager.get_klines("BTCUSDT", KLINE_INTERVAL_1MINUTE, limit=30)
            print(f"Successfully fetched {len(klines)} klines.")

            if klines:
                # Process klines with AI engine for trade optimization
                print("Passing klines data to AI engine for trade optimization...")
                trade_signal = optimize_trade_strategy(klines)
                print(f"Trade Signal: {trade_signal['signal']} - Reason: {trade_signal['reason']}")

                # Placeholder for AI engine processing (analyze_log)
                sample_log_entry = f"Fetched {len(klines)} BTCUSDT 1-minute klines. Trade signal: {trade_signal['signal']}"
                ai_insight = analyze_log(sample_log_entry)
                print(f"AI Engine Insight (Log Analysis): {ai_insight['insight']}")

        except Exception as e:
            print(f"Error fetching klines or processing with AI engine: {e}")

    else:
        print("Failed to load configuration.")

if __name__ == "__main__":
    main()