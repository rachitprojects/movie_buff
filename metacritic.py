import requests
from bs4 import BeautifulSoup


print("Enter the movie name : ")
movie_name  = input()

url = "https://www.metacritic.com/search/all/" + movie_name + "/results"
headers = {"User-Agent":"Mozilla/5.0"}

search_page = BeautifulSoup(requests.get(url, headers=headers).text, 'lxml')

first_result =  search_page.find('li', {"class":"result first_result"})

link = first_result.find('a').get('href')
link = "https://www.metacritic.com/" + link

print(link)
# print(first_result)
hey = first_result.find_all('h3')
movie_name = ''.join(hey[0].findAll(text=True))
movie_name = movie_name.rstrip()
movie_name = movie_name.lstrip()

print(movie_name)
