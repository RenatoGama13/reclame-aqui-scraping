from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
from time import sleep
from dados import Dados
from reclame_aqui_navegacao import ReclameAqui

# company = 'COMPANY-IDENTIFIER-NAME'
company = 'acordo-certo'
# base_url = "https://www.reclameaqui.com.br"
# url_site = f'{base_url}/empresa/{company}/lista-reclamacoes/?pagina='
# complaint_url = f'{base_url}/{company}'
# complaints_links = []
# page_number = 77
# first_page = 77
# is_the_first_page = True
dest_path = 'C:\\Workspace\\Complaints.csv'

# options = Options()
# options.headless = True
# fire_fox = webdriver.Firefox(options=options)
#
# def go_to_the_next_page():
#     element = WebDriverWait(fire_fox, 15).until(
#         EC.element_to_be_clickable((By.CLASS_NAME, "pagination-next")))
#     element.click()
#     increment_page_number()
#
# def go_to_the_first_page():
#     fire_fox.get(url_site + str(first_page))
#     global is_the_first_page
#     is_the_first_page = False
#
# def increment_page_number():
#     global page_number
#     page_number+=1
#
# def is_there_next_page(url):
#     url_page_number = re.search('\d*$', url).group()
#     pagination = fire_fox.find_element_by_class_name('custom-pagination').find_elements_by_class_name('pagination-page')
#     elements = []
#     for page in pagination:
#         elements.append(page.text)
#
#     if elements[-1] == '...':
#         return True
#     else:
#         if int(elements[-1]) > int(url_page_number):
#             return True
#         else:
#             print("There isn't next page")
#             return False
#
# def get_complaints_links():
#     WebDriverWait(fire_fox, 10).until(
#         EC.element_to_be_clickable((By.CLASS_NAME, "complain-list")))
#     print(f'Capturando os hrefs da página={fire_fox.current_url}')
#     html = BeautifulSoup(fire_fox.page_source, 'html.parser')
#     for li_tag in html.find('ul', {'class':'complain-list'}).find_all('li',{'class':'ng-scope'}):
#         complaints_links.append(li_tag.find('a').get('href'))
#
# def scrape_the_page():
#     while True:
#         if is_the_first_page:
#             go_to_the_first_page()
#         else:
#             if is_there_next_page(fire_fox.current_url):
#                 go_to_the_next_page()
#                 get_complaints_links()
#             else:
#                 break
#
# def add_general_data(bs_page, dados):
#     dados.id = re.sub("[^0-9]", "", bs_page.find('ul', {'class':'local-date'}).find('li', {'class':'ng-scope'}).text)
#     dados.local = bs_page.find('ul', {'class':'local-date'}).findAll('li', {'class':'ng-binding'})[0].text.strip()
#     dados.company = company
#     dados.url = fire_fox.current_url
#     dados.status = bs_page.find('div', {'class':'upshot-seal'}).find('img').get('title')
#     if bs_page.find('div', {'class':'col-md-9'}).findAll('div', {'class':['user-upshot-green', 'user-upshot-purple']}):
#         dados.faria_acordo_novamente = bs_page.find('div', {'class':['green-circle img-circle ng-scope', 'red-circle img-circle ng-scope']}).text
#         dados.nota = int(bs_page.findAll('div', {'class':'col-sm-12 col-sm-pull-0 col-xs-5 col-xs-pull-7'})[-1].text.strip())
#     save_dados_in_dictionary(dados)
#
# def add_replies_to_data_frame  (bs_page, dados):
#     class_of_considerations = ['user-upshot-green', 'user-upshot-purple']
#     replies = bs_page.find('div', {'class':'col-md-9'}). \
#         findAll('div', {'class':['ng-scope business-reply','ng-scope business-reply', class_of_considerations]})
#     for i in range(len(replies)):
#         dados.titulo = replies[i].find('div', {'class':'header-date'}).find('p', {'class':'title'}).text
#         dados.texto = replies[i].find('div', {'class':'reply-content'}).find('p').text
#         dados.data = replies[i].find('div', {'class':'header-date'}).find('p', {'class':'date'}).text.split(sep=' às ')[0]
#         dados.hora = replies[i].find('div', {'class':'header-date'}).find('p', {'class':'date'}).text.split(sep=' às ')[1]
#         if replies[i].get('class')[1] in class_of_considerations:
#             dados.tipo = 'Consideração'
#         else:
#             dados.tipo = 'Replica'
#         add_general_data(bs_page, dados)
#
# def add_the_complaint(bs_page, dados):
#     dados.tipo = 'Reclamação'
#     dados.titulo = bs_page.find('h1', {'class':'ng-binding'}).text
#     dados.texto = bs_page.find('div', {'class':'complain-body'}).find('p',).text
#     dados.data = bs_page.find('ul', {'class':'local-date'}).findAll('li', {'class':'ng-binding'})[1].text.strip().split(sep=' às ')[0]
#     dados.hora = bs_page.find('ul', {'class':'local-date'}).findAll('li', {'class':'ng-binding'})[1].text.strip().split(sep=' às ')[1]
#     add_general_data(bs_page, dados)
#
# def save_data():
#     for url in page_links:
#         save_data_from_each_page(url)
#
# def save_dados_in_dictionary(dados):
#     dados_df['tipo'].append(dados.tipo)
#     dados_df['titulo'].append(dados.titulo)
#     dados_df['texto'].append(dados.texto)
#     dados_df['data'].append(dados.data)
#     dados_df['hora'].append(dados.hora)
#     dados_df['id'].append(dados.id)
#     dados_df['local'].append(dados.local)
#     dados_df['empresa'].append(dados.company)
#     dados_df['url'].append(dados.url)
#     dados_df['status'].append(dados.status)
#     dados_df['faria_acordo_novamente'].append(dados.faria_acordo_novamente)
#     dados_df['nota'].append(dados.nota)
#
#
# def save_data_from_each_page(url, numero_tentativas=2):
#     try:
#         print(f'Salvando dados da página={url}')
#         fire_fox.get(url)
#         bs_page = BeautifulSoup(fire_fox.page_source, 'html.parser')
#         dados = Dados()
#         add_the_complaint(bs_page, dados)
#         add_replies_to_data_frame(bs_page, dados)
#     except Exception as e:
#         print(f'Erro ao tentar salvar dados da página={url}', e)
#         if numero_tentativas > 0:
#             sleep(3)
#             save_data_from_each_page(url, numero_tentativas - 1)
#         else:
#             return None

navigation = ReclameAqui(company)

print('Realizando scraping de todas as páginas')
start_time = time.time()
while True:
    if navigation.is_the_first_page:
        navigation.go_to_the_first_page()
    else:
        if navigation.is_there_next_page():
            navigation.go_to_the_next_page()
            navigation.increment_page_number()
            navigation.get_complaints_links()
        else:
            break
elapsed_time = time.time() - start_time
print(f'Scraping finalizado - tempo=\'{elapsed_time}\'')

urls = navigation.build_urls()

dados_df = {
    'tipo':[],
    'titulo':[],
    'texto':[],
    'local':[],
    'id':[],
    'data':[],
    'hora':[],
    'empresa':[],
    'url':[],
    'status':[],
    'nota':[],
    'faria_acordo_novamente':[]
}

print('Salvando os dados em um data frame')
start_time = time.time()
dados = navigation.save_data(urls)
elapsed_time = time.time() - start_time
print(f'Dados salvos - tempo=\'{elapsed_time}\'')

data_frame = pd.DataFrame(dados)

data_frame.to_csv(dest_path, sep=';')

navigation.quit()