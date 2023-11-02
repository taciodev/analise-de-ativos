import requests
import matplotlib.pyplot as plt

baseUrl = "https://brapi.dev/api/v2/crypto"
params = {
    "coin": "BTC,ETC",
    "currency": "BRL",
    "token": "eJGEyu8vVHctULdVdHYzQd",
}

response = requests.get(baseUrl, params=params)

if response.status_code == 200:
    data = response.json()

    coins = [coin["coinName"] for coin in data["coins"]]
    prices = [coin["regularMarketPrice"] for coin in data["coins"]]

    plt.figure(figsize=(8, 6))
    plt.bar(coins, prices, color="skyblue")
    plt.xlabel("Moedas")
    plt.ylabel("Preço (em USD)")
    plt.title("Preço das Moedas em Relação ao Dólar")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()
else:
    print(f"Request failed with status code {response.status_code}")
