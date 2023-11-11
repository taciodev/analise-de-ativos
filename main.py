import requests
import matplotlib.pyplot as plt


def get_tickers(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("indexes", []), data.get("stocks", [])
    except requests.RequestException as e:
        print(f"A requisição falhou: {e}")
        return [], []


tickers_url = "https://brapi.dev/api/available"
tickers_indexes, tickers_stocks = get_tickers(tickers_url)

tickers = "null"

if tickers_indexes or tickers_stocks:
    user_choice = input(
        "Escolha qual conjunto de dados deseja usar (índices/ações/ambos): "
    ).lower()

    if user_choice == "índices":
        tickers = ",".join(tickers_indexes)
    elif user_choice == "ações":
        tickers = ",".join(tickers_stocks)
    elif user_choice == "ambos":
        tickers = ",".join(
            [f"{a},{b}" for a, b in zip(tickers_indexes, tickers_stocks)]
        )
    else:
        print("Escolha inválida. Por favor, digite 'índices', 'ações' ou 'ambos'.")
else:
    print("Nenhum dado disponível.")

base_url = "https://brapi.dev/api/"
endpoint = f"quote/{tickers}"

full_url = base_url + endpoint
params = {
    "range": "6mo",
    "interval": "1m",
    "fundamental": "true",
    "dividends": "true",
    "token": "oFtEvw4GaKhPbbHs7Zgvij",
}

response = requests.get(full_url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code {response.status_code}")
