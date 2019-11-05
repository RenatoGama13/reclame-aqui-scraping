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

class ReclameAqui:
    def __init__(self, company):
        self.base_url = "https://www.reclameaqui.com.br"
        self.url_site = f'{self.base_url}/empresa/{company}/lista-reclamacoes/?pagina='
        self.complaint_url = f'{self.base_url}/{company}'
        self.complaints_links = []
        self.page_number = 77
        self.first_page = 77
        self.is_the_first_page = True
        self.options = Options()
        self.options.headless = False
        self.fire_fox = webdriver.Firefox(options=self.options)

    def go_to_the_next_page(self):
        element = WebDriverWait(self.fire_fox, 15).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "pagination-next")))
        element.click()

    def go_to_the_first_page(self):
        self.fire_fox.get(self.url_site + str(self.first_page))
        self.is_the_first_page = False

    def increment_page_number(self):
        global page_number
        self.page_number+=1

    def is_there_next_page(self):
        url_page_number = re.search('\d*$', self.fire_fox.current_url).group()
        pagination = self.fire_fox.find_element_by_class_name('custom-pagination').find_elements_by_class_name('pagination-page')
        elements = []
        for page in pagination:
            elements.append(page.text)

        if elements[-1] == '...':
            return True
        else:
            if int(elements[-1]) > int(url_page_number):
                return True
            else:
                print("Não existe uma próxima página")
                return False

    def get_complaints_links(self):
        WebDriverWait(self.fire_fox, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "complain-list")))
        print(f'Capturando os hrefs da página={self.fire_fox.current_url}')
        html = BeautifulSoup(self.fire_fox.page_source, 'html.parser')
        for li_tag in html.find('ul', {'class':'complain-list'}).find_all('li',{'class':'ng-scope'}):
            self.complaints_links.append(li_tag.find('a').get('href'))

    # def scrape_the_page(self):
    #     while True:
    #         if self.is_the_first_page:
    #             go_to_the_first_page()
    #         else:
    #             if is_there_next_page(fire_fox.current_url):
    #                 go_to_the_next_page()
    #                 get_complaints_links()
    #             else:
    #                 break

    def add_general_data(self, bs_page, dados):
        dados.id = re.sub("[^0-9]", "", bs_page.find('ul', {'class':'local-date'}).find('li', {'class':'ng-scope'}).text)
        dados.local = bs_page.find('ul', {'class':'local-date'}).findAll('li', {'class':'ng-binding'})[0].text.strip()
        dados.company = self.company
        dados.url = self.fire_fox.current_url
        dados.status = bs_page.find('div', {'class':'upshot-seal'}).find('img').get('title')
        if bs_page.find('div', {'class':'col-md-9'}).findAll('div', {'class':['user-upshot-green', 'user-upshot-purple']}):
            dados.faria_acordo_novamente = bs_page.find('div', {'class':['green-circle img-circle ng-scope', 'red-circle img-circle ng-scope']}).text
            dados.nota = int(bs_page.findAll('div', {'class':'col-sm-12 col-sm-pull-0 col-xs-5 col-xs-pull-7'})[-1].text.strip())
        save_dados_in_dictionary(dados)

    def add_replies_to_data_frame  (self, bs_page, dados):
        class_of_considerations = ['user-upshot-green', 'user-upshot-purple']
        replies = bs_page.find('div', {'class':'col-md-9'}). \
            findAll('div', {'class':['ng-scope business-reply','ng-scope business-reply', class_of_considerations]})
        for i in range(len(replies)):
            dados.titulo = replies[i].find('div', {'class':'header-date'}).find('p', {'class':'title'}).text
            dados.texto = replies[i].find('div', {'class':'reply-content'}).find('p').text
            dados.data = replies[i].find('div', {'class':'header-date'}).find('p', {'class':'date'}).text.split(sep=' às ')[0]
            dados.hora = replies[i].find('div', {'class':'header-date'}).find('p', {'class':'date'}).text.split(sep=' às ')[1]
            if replies[i].get('class')[1] in class_of_considerations:
                dados.tipo = 'Consideração'
            else:
                dados.tipo = 'Replica'
            add_general_data(bs_page, dados)

    def add_the_complaint(self, bs_page, dados):
        dados.tipo = 'Reclamação'
        dados.titulo = bs_page.find('h1', {'class':'ng-binding'}).text
        dados.texto = bs_page.find('div', {'class':'complain-body'}).find('p',).text
        dados.data = bs_page.find('ul', {'class':'local-date'}).findAll('li', {'class':'ng-binding'})[1].text.strip().split(sep=' às ')[0]
        dados.hora = bs_page.find('ul', {'class':'local-date'}).findAll('li', {'class':'ng-binding'})[1].text.strip().split(sep=' às ')[1]
        self.add_general_data(bs_page, dados)

    def save_data(self, urls):
        for url in urls:
            self.save_data_from_each_page(url)
        return self.dados

    def save_dados_in_dictionary(self, dados):
        self.dados_df['tipo'].append(dados.tipo)
        self.dados_df['titulo'].append(dados.titulo)
        self.dados_df['texto'].append(dados.texto)
        self.dados_df['data'].append(dados.data)
        self.dados_df['hora'].append(dados.hora)
        self.dados_df['id'].append(dados.id)
        self.dados_df['local'].append(dados.local)
        self.dados_df['empresa'].append(dados.company)
        self.dados_df['url'].append(dados.url)
        self.dados_df['status'].append(dados.status)
        self.dados_df['faria_acordo_novamente'].append(dados.faria_acordo_novamente)
        self.dados_df['nota'].append(dados.nota)


    def save_data_from_each_page(self, url, numero_tentativas=2):
        try:
            print(f'Salvando dados da página={url}')
            self.fire_fox.get(url)
            bs_page = BeautifulSoup(self.fire_fox.page_source, 'html.parser')
            dados = Dados()
            self.add_the_complaint(bs_page, dados)
            self.add_replies_to_data_frame(bs_page, dados)
        except Exception as e:
            print(f'Erro ao tentar salvar dados da página={url}', e)
            if numero_tentativas > 0:
                sleep(3)
                self.save_data_from_each_page(url, numero_tentativas - 1)
            else:
                return None

    def build_urls(self):
        print(f'Montando as urls')
        return [f'{self.complaint_url}{href}' for href in self.complaints_links]

    def quit(self):
        self.fire_fox.quit()