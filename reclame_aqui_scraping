from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

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
options.headless = True
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

def add_replies_to_data_frame(replies, complaint_id):
    for i in range(len(replies)):
        dados_df['title'].append(replies[i].find('div', {'class':'header-date'}).find('p', {'class':'title'}).text)
        dados_df['text'].append(replies[i].find('div', {'class':'reply-content'}).find('p').text)
        dados_df['id'].append(complaint_id)
        dados_df['local'].append("")
        dados_df['date'].append(replies[i].find('div', {'class':'header-date'}).find('p', {'class':'date'}).text.split(sep=' às ')[0])
        dados_df['time'].append(replies[i].find('div', {'class':'header-date'}).find('p', {'class':'date'}).text.split(sep=' às ')[1])

def add_the_complaint(bs_page, complaint_id):
    dados_df['title'].append(bs_page.find('h1', {'class':'ng-binding'}).text)
    dados_df['text'].append(bs_page.find('div', {'class':'complain-body'}).find('p',).text)
    dados_df['local'].append(bs_page.find('ul', {'class':'local-date'}).findAll('li', {'class':'ng-binding'})[0].text.strip())
    dados_df['id'].append(complaint_id)
    dados_df['date'].append(bs_page.find('ul', {'class':'local-date'}).findAll('li', {'class':'ng-binding'})[1].text.strip().split(sep=' às ')[0])
    dados_df['time'].append(bs_page.find('ul', {'class':'local-date'}).findAll('li', {'class':'ng-binding'})[1].text.strip().split(sep=' às ')[1])

def save_data_in_df():
    for page_link in page_links:
        print(f'Saving data from=\'{page_link}\'')
        fire_fox.get(page_link)
        bs_page = BeautifulSoup(fire_fox.page_source, 'html.parser')
        complaint_id = re.sub("[^0-9]", "", bs_page.find('ul', {'class':'local-date'}).find('li', {'class':'ng-scope'}).text)
        business_replies = bs_page.find('div', {'class':'col-md-9'}).findAll('div', {'class':'ng-scope business-reply'})
        user_replies = bs_page.find('div', {'class':'col-md-9'}).findAll('div', {'class':'ng-scope user-reply'})
        add_the_complaint(bs_page, complaint_id)
        add_replies_to_data_frame(business_replies, complaint_id)
        add_replies_to_data_frame(user_replies, complaint_id)


print('Scraping the page')
start_time = time.time()
scrape_the_page()
elapsed_time = time.time() - start_time
print(f'Scraping finished - elapsedTime=\'{elapsed_time}\'')

page_links = [f'{complaint_url}{href}' for href in complaints_links]

dados_df = {
    'title':[],
    'text':[],
    'local':[],
    'id':[],
    'date':[],
    'time':[]
}

print('Saving the complaints data in the data frame')
start_time = time.time()
save_data_in_df()
elapsed_time = time.time() - start_time
print(f'Data saved in the data frame- elapsedTime=\'{elapsed_time}\'')

data_frame = pd.DataFrame(dados_df)

data_frame.to_csv(dest_path, sep=';')

fire_fox.quit()
