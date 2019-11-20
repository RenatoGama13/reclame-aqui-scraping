# reclame-aqui-scraping

Para fazer o scraping do site estou usando:
- python 3.6.3;
- beautifulsoup4 4.8.1 (Use o pip para instalar);
- pandas 0.25.1 (Use o pip para instalar);
- geckodriver (Pode ser obtido no repositório https://github.com/mozilla/geckodriver/releases).

# O que fazer antes de rodar o código:
- Procure pela empresa que você quer obter as reclamações aqui https://www.reclameaqui.com.br/;
 <br>Copie o identificador da empresa entre as últimas duas barras. Será algo parecido com: https://www.reclameaqui.com.br/empresa/COMPANY-IDENTIFIER/;
 <br>Copie o resultado e cole  na variável "company";
- Escolha o local onde deseja salvar o arquivo. Basta especificar o local na variável "dest_path", por exemplo C:\\Workspace\\file.csv;
- A variável "headless" está setada como True. Isso quer dizer que o browser não será aberto. Caso queira ver o robô funcionando, passe essa variável para False;
- Rode o código e aproveite =)
