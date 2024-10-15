# Importa o módulo json para manipulação de dados JSON
import json
# Importa o módulo os para acessar variáveis de ambiente
import os
# Importa o módulo requests para fazer requisições HTTP
import requests
# Importa o decorator tool da biblioteca langchain para criar ferramentas
from langchain.tools import tool

# Define uma classe chamada SearchTools
class SearchTools():

    # Define um método da classe com o decorator @tool, nomeado "Search the internet"
    @tool("Search the internet")
    def search_internet(query):
        """Useful to search the internet about a given topic and return relevant results"""
        # Imprime uma mensagem indicando que a pesquisa está sendo realizada
        print("Searching the internet...")
        # Define a quantidade máxima de resultados a serem retornados
        top_result_to_return = 5
        # URL do serviço de busca Serper
        url = "https://google.serper.dev/search"
        # Cria um payload JSON com a consulta e o número de resultados
        payload = json.dumps(
            {"q": query, "num": top_result_to_return, "tbm": "nws"})
        # Define os cabeçalhos da requisição, incluindo a chave da API Serper
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        # Faz uma requisição POST à URL com os cabeçalhos e o payload
        response = requests.request("POST", url, headers=headers, data=payload)
        # Verifica se a chave 'organic' está presente na resposta JSON
        if 'organic' not in response.json():
            # Retorna uma mensagem de erro se a chave 'organic' não estiver presente
            return "Sorry, I couldn't find anything about that, there could be an error with your Serper API key."
        else:
            # Extrai os resultados da chave 'organic' da resposta JSON
            results = response.json()['organic']
            # Inicializa uma lista para armazenar as strings dos resultados
            string = []
            # Imprime os resultados (limite definido por top_result_to_return)
            print("Results:", results[:top_result_to_return])
            # Itera sobre os resultados, até o limite definido
            for result in results[:top_result_to_return]:
                try:
                    # Tenta extrair a data do resultado
                    date = result.get('date', 'Date not available')
                    # Adiciona os detalhes do resultado à lista como uma string formatada
                    string.append('\n'.join([
                        f"Title: {result['title']}",
                        f"Link: {result['link']}",
                        f"Date: {date}",  # Inclui a data no resultado
                        f"Snippet: {result['snippet']}",
                        "\n-----------------"
                    ]))
                except KeyError:
                    # Continua para o próximo resultado se houver uma KeyError
                    continue

            # Retorna a lista de strings dos resultados como uma única string
            return '\n'.join(string)
