from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from time import sleep
import re
import pandas as pd
import numpy

company = 'COMPANY-IDENTIFIER-NAME'
base_url = "https://www.reclameaqui.com.br"
url_site = f'{base_url}/empresa/{company}/lista-reclamacoes/?pagina='
complaint_url = f'{base_url}/{company}'
complaints_links = []
page_number = 0
first_page = 1
is_the_first_page = True
dest_path = 'C:\\Workspace\\Complaints.csv'

options = Options()
options.headless = False
fire_fox = webdriver.Firefox(options=options)

def go_to_the_next_page():
    element = WebDriverWait(fire_fox, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "pagination-next")))
    element.click()
    increment_page_number()

def go_to_the_first_page():
    fire_fox.get(url_site + str(first_page))
    global is_the_first_page
    is_the_first_page = False

def increment_page_number():
    global page_number
    page_number+=1

def is_there_next_page(url):
    url_page_number = re.search('\d*$', url).group()
    pagination = fire_fox.find_element_by_class_name('custom-pagination').find_elements_by_class_name('pagination-page')
    elements = []
    for page in pagination:
        elements.append(page.text)

    if elements[-1] == '...':
        return True
    else:
        if int(elements[-1]) > int(url_page_number):
            return True
        else:
            print("There isn't next page")
            return False

def get_complaints_links():
    WebDriverWait(fire_fox, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "complain-list")))
    print(f'Geting all hrefs from={fire_fox.current_url}')
    html = BeautifulSoup(fire_fox.page_source, 'html.parser')
    for li_tag in html.find('ul', {'class':'complain-list'}).find_all('li',{'class':'ng-scope'}):
        complaints_links.append(li_tag.find('a').get('href'))

def scrape_the_page():
    while True:
        if is_the_first_page:
            go_to_the_first_page()
        else:
            if is_there_next_page(fire_fox.current_url):
                go_to_the_next_page()
                get_complaints_links()
            else:
                break

def add_general_data(bs_page):
    dados_df['id'].append(re.sub("[^0-9]", "", bs_page.find('ul', {'class':'local-date'}).find('li', {'class':'ng-scope'}).text))
    dados_df['local'].append(bs_page.find('ul', {'class':'local-date'}).findAll('li', {'class':'ng-binding'})[0].text.strip())
    dados_df['company'].append(company)
    dados_df['page_link'].append(fire_fox.current_url)
    dados_df['status'].append(bs_page.find('div', {'class':'upshot-seal'}).find('img').get('title'))
    if bs_page.find('div', {'class':'col-md-9'}).findAll('div', {'class':['user-upshot-green', 'user-upshot-purple']}):
        dados_df['deal_again'].append(bs_page.find('div', {'class':['green-circle img-circle ng-scope', 'red-circle img-circle ng-scope']}).text)
        dados_df['note'].append(int(bs_page.findAll('div', {'class':'col-sm-12 col-sm-pull-0 col-xs-5 col-xs-pull-7'})[-1].text.strip()))
    else:
        dados_df['deal_again'].append(numpy.nan)
        dados_df['note'].append(numpy.nan)        

def add_replies_to_data_frame  (bs_page):
    class_of_considerations = ['user-upshot-green', 'user-upshot-purple']
    replies = bs_page.find('div', {'class':'col-md-9'}).\
        findAll('div', {'class':['ng-scope business-reply','ng-scope business-reply', class_of_considerations]})
    for i in range(len(replies)):
        dados_df['title'].append(replies[i].find('div', {'class':'header-date'}).find('p', {'class':'title'}).text)
        dados_df['text'].append(replies[i].find('div', {'class':'reply-content'}).find('p').text)
        dados_df['date'].append(replies[i].find('div', {'class':'header-date'}).find('p', {'class':'date'}).text.split(sep=' às ')[0])
        dados_df['time'].append(replies[i].find('div', {'class':'header-date'}).find('p', {'class':'date'}).text.split(sep=' às ')[1])
        if replies[i].get('class')[1] in class_of_considerations:
            dados_df['type'].append('Consideration')
        else:
            dados_df['type'].append('Reply')
        add_general_data(bs_page)

def add_the_complaint(bs_page):
    dados_df['type'].append('Complaint')
    dados_df['title'].append(bs_page.find('h1', {'class':'ng-binding'}).text)
    dados_df['text'].append(bs_page.find('div', {'class':'complain-body'}).find('p',).text)
    dados_df['date'].append(bs_page.find('ul', {'class':'local-date'}).findAll('li', {'class':'ng-binding'})[1].text.strip().split(sep=' às ')[0])
    dados_df['time'].append(bs_page.find('ul', {'class':'local-date'}).findAll('li', {'class':'ng-binding'})[1].text.strip().split(sep=' às ')[1])
    add_general_data(bs_page)  

def save_data():
    for url in page_links:
        save_data_from_each_page(url)
        
        
def save_data_from_each_page(url, numero_tentativas=2):
    try:
        print(f'Saving data from=\'{url}\'')
        fire_fox.get(url)
        bs_page = BeautifulSoup(fire_fox.page_source, 'html.parser')
        add_the_complaint(bs_page)
        add_replies_to_data_frame(bs_page)
    except Exception as e:
        print(f'Error saving data from:{url}', e)
        if numero_tentativas > 0:
            sleep(5)
            save_data_from_each_page(url, numero_tentativas - 1) 
        else:
            return None
        


print('Scraping the page')
start_time = time.time()
scrape_the_page()
elapsed_time = time.time() - start_time
print(f'Scraping finished - elapsedTime=\'{elapsed_time}\'')

page_links = [f'{complaint_url}{href}' for href in complaints_links]

dados_df = {
    'type':[],
    'title':[],
    'text':[],
    'local':[],
    'id':[],
    'date':[],
    'time':[],
    'company':[],
    'page_link':[],
    'status':[],
    'note':[],
    'deal_again':[]
}

print('Saving the complaints data in the data frame')
start_time = time.time()
save_data()
elapsed_time = time.time() - start_time
print(f'Data saved in the data frame- elapsedTime=\'{elapsed_time}\'')

data_frame = pd.DataFrame(dados_df)

data_frame.to_csv(dest_path, sep=';')

fire_fox.quit()
