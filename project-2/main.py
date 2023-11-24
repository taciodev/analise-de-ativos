from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from colorama import Fore, Style


def download_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def calculate_metrics(stock_data):
    metrics = {}

    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()
    stock_data['Daily_Return'] = stock_data['Adj Close'].pct_change()

    metrics['Volatility'] = stock_data['Daily_Return'].std()

    delta = stock_data['Adj Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    stock_data['RSI'] = rsi

    metrics['Last_Close'] = stock_data['Close'].iloc[-1]
    metrics['Last_SMA_50'] = stock_data['SMA_50'].iloc[-1]
    metrics['Last_SMA_200'] = stock_data['SMA_200'].iloc[-1]
    metrics['Last_RSI'] = stock_data['RSI'].iloc[-1]

    return metrics

def plot_data(stock_data, ticker):
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Close'], label=f'{ticker} Close Price (USD)')
    plt.plot(stock_data['SMA_50'], label='SMA 50 days (USD)')
    plt.plot(stock_data['SMA_200'], label='SMA 200 days (USD)')
    plt.title(f'{ticker} Stock Analysis')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.show()

def market_direction(sma_50, sma_200):
    if sma_50 > sma_200:
        return 'Buy'
    elif sma_50 < sma_200:
        return 'Sell'
    else:
        return 'Hold'

def get_user_choice():
    print("\n" + Style.BRIGHT + "Escolha uma ação para analisar:" + Style.RESET_ALL)
    print(Fore.BLUE + "1. Apple (AAPL)")
    print("2. Motorola (MSI)")
    print("3. Xiaomi (XIACF)")
    print("4. Amazon (AMZN)")
    print("5. Positivo (POSI3.SA)" + Style.RESET_ALL)
    choice = input(Fore.YELLOW + "Digite o número da sua escolha (ou 'q' para sair): " + Style.RESET_ALL)
    return choice

def get_ticker_from_choice(choice):
    stocks = ['AAPL', 'MSI', 'XIACF', 'AMZN', 'POSI3.SA']
    if choice.isdigit() and 1 <= int(choice) <= len(stocks):
        return stocks[int(choice) - 1]
    else:
        return None

if __name__ == "__main__":
    start_date = '2020-01-01'
    end_date = datetime.today().strftime('%Y-%m-%d')

    while True:
        user_choice = get_user_choice()
        if user_choice.lower() == 'q':
            break

        ticker = get_ticker_from_choice(user_choice)
        if ticker:
            stock_data = download_stock_data(ticker, start_date, end_date)
            metrics = calculate_metrics(stock_data)
            direction = market_direction(metrics['Last_SMA_50'], metrics['Last_SMA_200'])

            print(f"\n" + Style.BRIGHT + f"Análise para {ticker} (Até {end_date}):" + Style.RESET_ALL)
            print(f"Último Preço de Fechamento: ${metrics['Last_Close']:.2f}")
            print(f"Última Média Móvel Simples de 50 dias: ${metrics['Last_SMA_50']:.2f}")
            print(f"Última Média Móvel Simples de 200 dias: ${metrics['Last_SMA_200']:.2f}")
            print(f"Volatilidade: {metrics['Volatility']:.4f}")
            print(f"Índice de Força Relativa (RSI): {metrics['Last_RSI']:.2f}")
            print(f"Direção do Mercado: {direction}")

            plot_data(stock_data, ticker)
        else:
            print(Fore.RED + "Escolha inválida. Por favor, digite um número válido ou 'q' para sair." + Style.RESET_ALL)

