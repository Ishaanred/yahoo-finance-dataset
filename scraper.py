import yfinance as yf
import pandas as pd
import time
import csv
import os

# --- Configuration ---
TICKER_CSV_FILE = "tickers.csv"
OUTPUT_CSV_FILE = "yahoo_finance_output.csv"
PROCESSED_LOG_FILE = "processed_tickers.log"
REQUEST_DELAY_SECONDS = 2
WAIT_ON_TIMEOUT_MINUTES = 30
CONSECUTIVE_TIMEOUT_LIMIT = 3

DATA_POINTS = [
    'symbol', 'displayName', 'longName', 'country', 'website',
    'industryDisp', 'sectorDisp', 'longBusinessSummary',
    'fullTimeEmployees', 'marketCap', 'totalRevenue',
    'financialCurrency', 'fullExchangeName'
]


def read_tickers_from_csv(filename):
    tickers = []
    try:
        with open(filename, mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            first_row = next(reader)
            if first_row and first_row[0].strip().lower() not in ['ticker', 'tickers', 'symbol', 'symbols']:
                tickers.append(first_row[0].strip())
            for row in reader:
                if row:
                    tickers.append(row[0].strip())
    except FileNotFoundError:
        print(f"ERROR: Ticker file not found at '{filename}'.")
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['tickers'])
            writer.writerow(['AAPL'])
            writer.writerow(['MSFT'])
        print(f"A sample '{filename}' has been created for you.")
    except Exception as e:
        print(f"An error occurred while reading '{filename}': {e}")
    return tickers


def load_processed_tickers(filename):
    if not os.path.exists(filename):
        return set()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    except Exception as e:
        print(f"Could not read processed tickers log: {e}")
        return set()


def log_processed_ticker(ticker, filename):
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"{ticker}\n")
    except Exception as e:
        print(f"Failed to log processed ticker {ticker}: {e}")


def append_to_csv(data, filename):
    file_exists = os.path.exists(filename)
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=DATA_POINTS)
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
    except IOError as e:
        print(f"Error writing to CSV file '{filename}': {e}")


def main():
    all_tickers = read_tickers_from_csv(TICKER_CSV_FILE)
    if not all_tickers:
        return

    processed_tickers = load_processed_tickers(PROCESSED_LOG_FILE)
    tickers_to_process = [t for t in all_tickers if t not in processed_tickers]

    if not tickers_to_process:
        print("All tickers already processed. Nothing to do.")
        return

    print(f"Found {len(all_tickers)} total tickers.")
    print(f"{len(processed_tickers)} already processed.")
    print(f"Processing remaining {len(tickers_to_process)} tickers.")

    consecutive_timeouts = 0

    for i, ticker_symbol in enumerate(tickers_to_process):
        print(f"\nProcessing {ticker_symbol} ({i + 1}/{len(tickers_to_process)})...")
        try:
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info

            if not info or 'symbol' not in info:
                print(f"--> No data for '{ticker_symbol}'. Skipping.")
                log_processed_ticker(ticker_symbol, PROCESSED_LOG_FILE)
                continue

            consecutive_timeouts = 0
            stock_data = {point: info.get(point, 'N/A') for point in DATA_POINTS}
            append_to_csv(stock_data, OUTPUT_CSV_FILE)
            log_processed_ticker(ticker_symbol, PROCESSED_LOG_FILE)
            print(f"--> Saved '{ticker_symbol}'.")

        except Exception as e:
            error_message = str(e).lower()
            print(f"--> ERROR for '{ticker_symbol}': {error_message}")
            if "timeout" in error_message or "timed out" in error_message:
                consecutive_timeouts += 1
                if consecutive_timeouts >= CONSECUTIVE_TIMEOUT_LIMIT:
                    print(f"    Waiting {WAIT_ON_TIMEOUT_MINUTES} minutes after repeated timeouts...")
                    time.sleep(WAIT_ON_TIMEOUT_MINUTES * 60)
                    consecutive_timeouts = 0
            else:
                consecutive_timeouts = 0
        finally:
            time.sleep(REQUEST_DELAY_SECONDS)

    print("\nAll tickers processed.")


if __name__ == "__main__":
    main()
