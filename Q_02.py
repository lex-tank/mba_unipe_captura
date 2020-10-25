from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json


def finds(browser, by, expression):
    try:
        return browser.find_elements(by, expression)
    except NoSuchElementException as nse:
        return None

def find(browser, by, expression):
    try:
        return browser.find_element(by, expression)
    except NoSuchElementException as nse:
        return None


busca = input('O que deseja buscar?')


# Conferindo os parametros passados
if  len(busca.strip()) > 1:
    print('Pesquisando por ' + busca)

else:
    print('Você não passou um parâmetro de busca válido :(')
    exit()


# Criando o arquivo de saida JSON
output  = open('Mercado_Livre.json', 'w', encoding='utf-8')

driver = webdriver.Firefox()

# URL de busca + parâmetro 
url_main = "https://lista.mercadolivre.com.br/" + busca


# Variaveis para paginação
next_page = True 
pagina = 0

while next_page:    
    pagina += 1
    
    
    print('Coletando da página \033[4m'+ str(pagina) + '\033[0m utilizando o link ' + str(url_main) + '\n')
   
    # iniciando a busca 
    driver.get(url_main)

    items = finds(driver, By.CLASS_NAME, 'ui-search-result__content') 
    for item in items:
        print('=============')        
        try:
            # Tratamento devido alguns pordutos vir fora do padrao esperado na DIV             
            descricao = find(item, By.CLASS_NAME, 'ui-search-item__title').get_property("textContent")
            frete =  find(item, By.CLASS_NAME, 'ui-search-item__shipping--free')
            # if frete:
            #     frete = frete.get_property("textContent")
            # else: 
            #     frete = 'Não possui frete grátis'     

            frete = frete.get_property("textContent") if frete else 'Não possui frete grátis'
                             
            fraction = find(item, By.CLASS_NAME, 'price-tag-fraction').get_property("textContent").strip()             
            fraction = fraction.replace('.', '')
            percent_ = find(item, By.CLASS_NAME, 'price-tag-cents')
            percent = '00'
            if percent_:
                percent = percent_.get_property("textContent").strip()
                percent = percent.replace('.', '')
        
        except Exception as err:
            print('EROOO -->', str(err))
            continue
           
        # Formatando o valor de preco
        preco = str(fraction)+ '.' + str(percent)
        preco = preco.strip()

        
        
        print(descricao) 
        print(preco)
        print(frete)

        # criando o dicionário 
        item = {'descricao': descricao, 'preco': preco, 'frete': frete}

        # Salvando o dicionário no arquivo JSON 
        output.write(json.dumps(item))
        output.write('\n')

    # Buscando a caixa que aponta se há próxima página
    proxima_pag = find(driver, By.CLASS_NAME, 'andes-pagination__button--next')
        
    if proxima_pag != None:
        print('Coleta da página \033[4m'+ str(pagina) + '\033[0m concluída, mas ainda existem produtos na próxima página.'+ '\n' )        
   
        # Coleta a url da página seguinte
        url_main = find(proxima_pag, By.CLASS_NAME, 'andes-pagination__link').get_attribute('href')                
    else:
        # Se não há mais páginas, a pesquisa é encerrada
        print("Pesquisa concluída! \n")         

        next_page = False

driver.close()
