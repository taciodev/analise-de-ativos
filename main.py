import requests
import matplotlib.pyplot as plt

TICKERS_URL = "https://brapi.dev/api/available"
BASE_URL = "https://brapi.dev/api/"
ENDPOINT = "quote/"
API_TOKEN = "oFtEvw4GaKhPbbHs7Zgvij"


def get_tickers(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("indexes", []), data.get("stocks", [])
    except requests.RequestException as e:
        print(f"A requisição falhou: {e}")
        return [], []


def choose_tickers(indexes, stocks):
    if indexes or stocks:
        user_choice = input(
            "\nEscolha qual conjunto de dados deseja usar (índices/ações/ambos): "
        ).lower()

        if user_choice == "índices":
            return ",".join(indexes)
        elif user_choice == "ações":
            return ",".join(stocks)
        elif user_choice == "ambos":
            return ",".join([f"{a},{b}" for a, b in zip(indexes, stocks)])
        else:
            print("Escolha inválida. Por favor, digite 'índices', 'ações' ou 'ambos'.")
            return None
    else:
        print("Nenhum dado disponível.")
        return None


def fetch_data(url):
    print(f"\nCarregando dados de {url}...")

    params = {
        "range": "6mo",
        # "interval": "1m",
        # "fundamental": "true",
        # "dividends": "true",
        "token": API_TOKEN,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        print(f"Carregamento bem-sucedido para {url}.")
        return response.json()
    else:
        print(f"Falha na solicitação com código de status {response.status_code}")
        return None


def find_working_combination(tickers_list):
    successful_data = []

    for i in range(len(tickers_list)):
        modified_tickers = tickers_list[i:] + tickers_list[:i]
        modified_url = BASE_URL + ENDPOINT + ",".join(modified_tickers)

        data = fetch_data(modified_url)

        if data:
            successful_data.append(data)

    return successful_data


def try_single_tickers(tickers_list):
    successful_data = []

    for ticker in tickers_list:
        url = BASE_URL + ENDPOINT + ticker
        data = fetch_data(url)

        if data:
            successful_data.append(data)

    return successful_data


def main():
    tickers_indexes, tickers_stocks = get_tickers(TICKERS_URL)
    tickers = choose_tickers(tickers_indexes, tickers_stocks)

    if tickers:
        tickers_list = tickers.split(",")

        successful_data_combination = find_working_combination(tickers_list)

        if successful_data_combination:
            print("\nDados das tentativas em combinação que foram bem-sucedidas:")
            print(successful_data_combination)
        else:
            print(
                "\nErro: Todas as tentativas em combinação falharam. Tentando novamente com tickers individuais.\n"
            )

            successful_data_single = try_single_tickers(tickers_list)

            if successful_data_single:
                print("\nDados das tentativas individuais que foram bem-sucedidas:")
                print(successful_data_single)
            else:
                print(
                    "\nErro: Todas as tentativas individuais também falharam. Verifique os tickers."
                )


if __name__ == "__main__":
    main()
