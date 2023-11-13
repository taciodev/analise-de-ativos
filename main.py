import requests
import matplotlib.pyplot as plt
import time

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
            "\nEscolha qual conjunto de dados deseja usar (índices/ações): "
        ).lower()

        if user_choice == "índices":
            return ",".join(indexes), user_choice
        elif user_choice == "ações":
            return ",".join(stocks), user_choice
        else:
            print("Escolha inválida. Por favor, digite 'índices' ou 'ações'.")
            return None, None
    else:
        print("Nenhum dado disponível.")
        return None, None


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


# def find_working_combination(tickers_list):
#     url = BASE_URL + ENDPOINT + ",".join(tickers_list)

#     data = fetch_data(url)

#     if data:
#         return data


def try_single_tickers(tickers_list):
    successful_data = []

    for ticker in tickers_list:
        url = BASE_URL + ENDPOINT + ticker
        data = fetch_data(url)

        if data:
            successful_data.append(data)

    return successful_data


def plot_paginated_index_data(data, items_per_page=10):
    # Extrair resultados de todos os conjuntos de dados
    all_results = [
        result for index_data in data for result in index_data.get("results", [])
    ]

    total_items = len(all_results)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    page = 1
    while page <= total_pages:
        start_index = (page - 1) * items_per_page
        end_index = min(page * items_per_page, total_items)
        page_results = all_results[start_index:end_index]

        # Ordenar os resultados com base no regularMarketPrice em ordem decrescente
        sorted_results = sorted(
            page_results, key=lambda x: x.get("regularMarketPrice", 0), reverse=True
        )

        # Pegar os top 10 resultados
        top_indices = sorted_results[:10]

        # Preparar dados para o gráfico
        symbols = [index.get("symbol", "") for index in top_indices]
        prices = [index.get("regularMarketPrice", 0) for index in top_indices]

        # Plotar o gráfico
        plt.bar(symbols, prices)
        plt.xlabel("Índices")
        plt.ylabel("Preço de Mercado Regular")
        plt.title(
            f"Página {page}/{total_pages}: Top 10 Índices por Preço de Mercado Regular"
        )
        plt.show()

        user_input = input(
            "\nPressione Enter para avançar para a próxima página (ou 'c' para sair): "
        )
        if user_input.lower() == "c":
            break

        page += 1


def plot_paginated_stock_data(data, items_per_page=10):
    # Extrair resultados de todos os conjuntos de dados
    all_results = [
        result for stock_data in data for result in stock_data.get("results", [])
    ]

    total_items = len(all_results)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    page = 1
    while page <= total_pages:
        start_index = (page - 1) * items_per_page
        end_index = min(page * items_per_page, total_items)
        page_results = all_results[start_index:end_index]

        # Ordenar os resultados com base no regularMarketPrice em ordem decrescente
        sorted_results = sorted(
            page_results, key=lambda x: x.get("regularMarketPrice", 0), reverse=True
        )

        # Pegar os top 10 resultados
        top_stocks = sorted_results[:10]

        # Preparar dados para o gráfico
        symbols = [stock.get("symbol", "") for stock in top_stocks]
        prices = [stock.get("regularMarketPrice", 0) for stock in top_stocks]

        # Plotar o gráfico
        plt.bar(symbols, prices)
        plt.xlabel("Ações")
        plt.ylabel("Preço de Mercado Regular")
        plt.title(
            f"Página {page}/{total_pages}: Top 10 Ações por Preço de Mercado Regular"
        )
        plt.show()

        user_input = input(
            "\nPressione Enter para avançar para a próxima página (ou 'c' para sair): "
        )
        if user_input.lower() == "c":
            break

        page += 1


def main():
    tickers_indexes, tickers_stocks = get_tickers(TICKERS_URL)
    tickers, user_choice = choose_tickers(tickers_indexes, tickers_stocks)

    if tickers:
        tickers_list = tickers.split(",")

        print("\nCarregando dados individuais...")

        successful_data_single = try_single_tickers(tickers_list)

        if successful_data_single:
            print(
                "\nPressione a tecla 'q' ao visualizar o gráfico para acessar as opções seguintes: pressione Enter para avançar para a próxima página ou 'c' para sair."
            )

            time.sleep(10)

            if user_choice == "índices":
                plot_paginated_index_data(successful_data_single)
            else:
                plot_paginated_stock_data(successful_data_single)

            # successful_tickers = [
            #     result["symbol"]
            #     for data in successful_data_single
            #     for result in data.get("results", [])
            # ]

            # print("\nCarregando dados combinados...")

            # successful_data_combination = find_working_combination(successful_tickers)

            # if successful_data_combination:
            #     print("\nDados das tentativas em combinação que foram bem-sucedidas:")
            #     print(successful_data_combination)
            # else:
            #     print(
            #         "\nErro: A tentativa de combinação falhou. Verifique os tickers ou parâmetros."
            #     )
        else:
            print(
                "\nErro: Todas as tentativas individuais falharam. Verifique os tickers e/ou os parâmetros."
            )


if __name__ == "__main__":
    main()
