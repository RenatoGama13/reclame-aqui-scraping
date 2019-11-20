import time
import pandas as pd
from reclame_aqui_navegacao import ReclameAqui

company = 'COMPANY-IDENTIFIER'
dest_path = 'DESTINATION-PATH'
headless = True

navigation = ReclameAqui(company, headless)

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

print('Salvando os dados em um data frame')
start_time = time.time()
dados = navigation.save_data(urls)
elapsed_time = time.time() - start_time
print(f'Dados salvos - tempo=\'{elapsed_time}\'')

data_frame = pd.DataFrame(dados)

data_frame.to_csv(dest_path, sep=';', index=False)

navigation.quit()