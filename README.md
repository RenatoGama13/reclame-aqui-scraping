# reclame-aqui-scraping

To scrape the Reclame Aqui page I'm using:
- python 3.6.3
- beautifulsoup4 4.8.1 (Use pip for installing)
- pandas 0.25.1 (Use pip for installing)
- geckodriver (Get from this repository https://github.com/mozilla/geckodriver/releases)

# What to do before running the code:
- Search for company you want to get the complaints in https://www.reclameaqui.com.br/
- Copy the company identifier name between the last two bars.
It will look like this https://www.reclameaqui.com.br/empresa/COMPANY-IDENTIFIER-NAME/
- Paste the result in the variable "company".
- A .CSV file will be saved in C:\Workspace. But you can change the path in variable "dest_path".
- Run and enjoy =)
