# reclame-aqui-scraping

Para fazer o scraping do site estou usando:
- python 3.6.3;
- beautifulsoup4 4.8.1 (Use o pip para instalar);
- pandas 0.25.1 (Use o pip para instalar);
- geckodriver (Pode ser obtido no repositório https://github.com/mozilla/geckodriver/releases).

# O que fazer antes de rodar o código:
- Procure pela empresa que você quer obter as reclamações aqui https://www.reclameaqui.com.br/;
- Copie o identificador da empresa entre as últimas duas barras;
Será algo parecido com: https://www.reclameaqui.com.br/empresa/COMPANY-IDENTIFIER/;
- Copie o resultado na variável "company";
- Um arquivo Complaints.csv será salvo em C:\Workspace. Mas você pode trocar o caminho na variável "dest_path";
- Rode o código e aproveite =)
