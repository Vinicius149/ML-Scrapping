import requests
from bs4 import BeautifulSoup
import re

# USER AGENT
headers = {
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

# SELECIONAR PRODUTO
produto = input('Digite o produto: ')
produto = produto.replace(' ', '-')

# URL BASE
url = f'https://lista.mercadolivre.com.br/{produto}'

# Lista para armazenar os resultados
resultados = []

# LOOP DE RASPAGEM (agora com limite para evitar loops infinitos)
for start in range(1, 2): #testar 5 paginas, aumentar caso necessario
    url_final = url + '_Desde_' + str(start*50+1) #paginação do ML é de 50 em 50
    print(f'Acessando: {url_final}') #adicionado para debug
    # FAZER A REQUISIÇÃO
    r = requests.get(url_final, headers=headers)

    if r.status_code == 200:  # Check for successful response
        site = BeautifulSoup(r.content, 'html.parser')

        # ENCONTRAR OS RESULTADOS (Seletores atualizados)
        itens = site.find_all('li', class_='ui-search-layout__item') #seleciona cada item da lista

        if not itens:
            print(f'Nenhum item encontrado na página {start}')
            break

        # CAPTURAR DADOS
        for item in itens:
            descricao = item.find('h2', class_='poly-box poly-component__title')
            preco = item.find('span', class_='andes-money-amount__fraction')
            link = item.find_all('a', attrs= {'href' : re.compile("^https://produto")})

            try:
                resultados.append({ #adiciona um dicionario na lista
                    "Descrição": descricao.text.strip() if descricao else 'Não encontrado',  # Remove espaços em branco
                    "Preço": preco.text.strip() if preco else 'Não encontrado',
                    "Link": link.get('href') if link else 'Não encontrado'
                })
            except AttributeError as e:
                print(f"Erro ao acessar atributos do elemento: {e}")

    else:
        print(f"Erro ao acessar a página {start}: Código de status {r.status_code}")
        break #para o loop se der erro na pagina

# Imprimir os resultados após o loop
if resultados: #verifica se a lista nao esta vazia
    for resultado in resultados:
        print(resultado)
else:
    print("Nenhum resultado encontrado.")

print('Raspagem concluída.')