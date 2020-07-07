

# headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

# headers = {
# "Host": 'www.imdb.com',
# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
# "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
# "Accept-Language": "en-US,en;q=0.5",
# "Accept-Encoding": "gzip, deflate, br",
# "Connection": "keep-alive",
# "Referer": "https://www.imdb.com/title/tt1979376/?ref_=nv_sr_srsg_0",
# 'Cookie' : "uu=BCYuGnO8a6nkIfLm44bOdOwuZxuVELeptwePjIkj3O0RvuRCVgb5bz0-b3niuTu7Fm0IGf6Z_TNs%0D%0A-FjYtQxzIVlM9ERKUosyXm_y6kl1u4ZOR_b7o9Z9ux4ZHtzs2b2Yo9MLuBGi_GDqslXTh-efcQD2%0D%0AiQ%0D%0A; session-id=132-8892320-2399452; session-id-time=2082787201l; csm-hit=tb:1NGWCGFTG7H97JY5ZTXG+s-3TETBRQ647WV637VJYS1|1594104582351&t:1594104582351&adb:adblk_no; adblk=adblk_no; ubid-main=130-9889388-2112132; session-token=z06dJOAkQBVpd+FYCGqFuB5LyKuE5MxT6tqEwJxAPWGkSKYMRcK3NUMUGr/sdih9P+WzWCKwawP3L+/UxWa+CBqrucT16Vp84xUab4vVzl1LE5FQPjj2m6bn8RrOqcnH5/+LzxZtcYhFmie+7SBX2DBOhNNjqq/qOTP8G3FnxzrrZIgY/GJgYWfgQ1G14Pau; as=%7B%22n%22%3A%7B%22t%22%3A%5B970%2C250%5D%2C%22tr%22%3A%5B300%2C250%5D%2C%22in%22%3A%5B0%2C0%5D%2C%22ib%22%3A%5B0%2C0%5D%7D%7D",
# 'Upgrade-Insecure-Requests': '1',
# 'TE': 'Trailers'
# }

# with open("search_res.html", 'wb') as search_res:
#     search_res.write(bytes(page.prettify(), 'utf-8'))

import requests 
from bs4 import BeautifulSoup


print("Enter movie name, for imdb search")
movie_name = input()

query = {'q' : movie_name, 'ref_' : 'nv_sr_sm'}


"""
    Took these headers from Firefox's dev tools
"""

headers2 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    'Cookie' : "uu=BCYuGnO8a6nkIfLm44bOdOwuZxuVELeptwePjIkj3O0RvuRCVgb5bz0-b3niuTu7Fm0IGf6Z_TNs%0D%0A-FjYtQxzIVlM9ERKUosyXm_y6kl1u4ZOR_b7o9Z9ux4ZHtzs2b2Yo9MLuBGi_GDqslXTh-efcQD2%0D%0AiQ%0D%0A; session-id=132-8892320-2399452; session-id-time=2082787201l; csm-hit=tb:1NGWCGFTG7H97JY5ZTXG+s-3TETBRQ647WV637VJYS1|1594104582351&t:1594104582351&adb:adblk_no; adblk=adblk_no; ubid-main=130-9889388-2112132; session-token=z06dJOAkQBVpd+FYCGqFuB5LyKuE5MxT6tqEwJxAPWGkSKYMRcK3NUMUGr/sdih9P+WzWCKwawP3L+/UxWa+CBqrucT16Vp84xUab4vVzl1LE5FQPjj2m6bn8RrOqcnH5/+LzxZtcYhFmie+7SBX2DBOhNNjqq/qOTP8G3FnxzrrZIgY/GJgYWfgQ1G14Pau; as=%7B%22n%22%3A%7B%22t%22%3A%5B970%2C250%5D%2C%22tr%22%3A%5B300%2C250%5D%2C%22in%22%3A%5B0%2C0%5D%2C%22ib%22%3A%5B0%2C0%5D%7D%7D",
    "Referer": "https://www.imdb.com/title/tt1979376/?ref_=nv_sr_srsg_0"

}

page = BeautifulSoup(requests.get("https://www.imdb.com/find", params=query, headers=headers2).content, features="lxml")



"""
    Checks search results, finds appropriate link
"""



links_list = []
for row in page.find("table", {'class' : 'findList'}).find_all("tr"):
    item_title = row.find("td", {'class' : 'result_text'})
    if "(TV" not in str(item_title):
        for hlink in item_title.find_all("a"):
            # movie_link = hlink["href"]
            links_list.append(hlink["href"])
            # break

review_page = BeautifulSoup(requests.get("https://imdb.com" + links_list[0], headers = headers2).content, features="lxml")

review_link = ""
for div in review_page.find_all("div", {"class" : "user-comments"}):
    review_location = list(div.find_all("a"))[-1]
    review_link = review_location["href"]

user_reviews = BeautifulSoup(requests.get("https://imdb.com" + review_link, headers = headers2).content, features="lxml")
with open("imdb_reviews.txt", 'w') as review_file:
    num_review = 1
    for div in user_reviews.find_all("div", {"class" : "review-container"}):
        for review in div.find("div", {"class", "text show-more__control"}):
            if str(review).replace("<br/>", ""):
                review_file.write(str(review.encode("utf-8")))
                review_file.write("\n")
                review_file.write(str(num_review))
                num_review += 1
    

