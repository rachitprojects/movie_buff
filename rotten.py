import requests
import re
import urllib, json
from bs4 import BeautifulSoup


print("Enter the movie name : ",end="")
movie_name  = input()

url = "https://www.rottentomatoes.com/search?search=" + movie_name
headers = {"User-Agent":"Mozilla/5.0"}

search_page = BeautifulSoup(requests.get(url, headers=headers).text, 'lxml')
all_scripts = search_page.find_all("script", {"id":"movies-json"})

soup=BeautifulSoup(str(all_scripts[0]),"html.parser")
res = soup.find('script')
json_object = json.loads(res.contents[0])
 
# print(json_object['items'])
for item in json_object['items']:
    movie_name = item['url']
    break

movie_name = movie_name.split('/')
movie_name = movie_name[-1]

print(movie_name)


r = requests.get("https://www.rottentomatoes.com/m/"+movie_name+"/reviews?type=user")
data = json.loads(re.search('movieReview\s=\s(.*);', r.text).group(1))

movieId = data["movieId"]

def getReviews(endCursor):
    r = requests.get(f"https://www.rottentomatoes.com/napi/movie/{movieId}/reviews/user",
    params = {
        "direction": "next",
        "endCursor": endCursor,
        "startCursor": ""
    })
    return r.json()

reviews = []
result = {}
for i in range(0, 5):
    print(f"[{i}] request review")
    result = getReviews(result["pageInfo"]["endCursor"] if i != 0  else "")
    for item in result['reviews']:
        reviews.append(item['review'])

with open("rotten_reviews.txt", 'w') as review_file:
    num_review = 1
    for r in reviews:
        r = ''.join(reviews[num_review-1])
        print(r)
        review_file.write(r)
        review_file.write("\n")
        review_file.write(str(num_review))
        num_review += 1


print(f"got {len(reviews)} reviews")
