
from selenium import webdriver  
# from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options 

movie_name = input()

# query = {'q' : movie_name}
# headers = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
# }

# rog_ebert = requests.get("https://www.rogerebert.com/search", params=query, headers

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get("https://www.rogerebert.com/search?utf8=%E2%9C%93&q=" + movie_name)
# element = driver.find_element_by_id("q")
# element.send_keys(movie_name)
# element.send_keys(Keys.RETURN)
page_html = BeautifulSoup(driver.page_source, features="lxml")

link_check = page_html.find_all("a", {'class' : 'gs-title'})
driver.get(link_check[0]["href"])
review_page = BeautifulSoup(driver.page_source, features="lxml")


review_data = review_page.find_all("section", {'class': 'page-content--block_editor-content js--reframe'})
with open("rogebert_rev.txt", "w") as final_rev:
    for section in review_data:
        para = section.find_all("p")
        final_rev.write(str(para))




