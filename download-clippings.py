import requests
from time import sleep
import json


url_pageless = "https://api.clippings.io/api/UserRecords/?RecordFilterTypeId=1&BookMarks=false&Clippings=true&Highlights=true&Notes=true&SortOrder=BookTitle+Asc&ThenByOrder=LocationDecimal+Asc&Page="

page=1

payload = {}
headers = {
          'Authorization': 'Bearer base64 bearer would be here',
            'Cookie': 'ARRAffinity=f52cee243400e98c109f08cf421244231e9bb2346d6d2220d1c264843b8e1f56; ARRAffinitySameSite=f52cee243400e98c109f08cf421244231e9bb2346d6d2220d1c264843b8e1f56'
            }


bearer = input("Enter new Authorization bearer of the following form: Bearer <base64 bearer token>")
headers['Authorization'] = bearer

only_booktitle_and_highlights = list()
full_json_str = b'' 
for i in range(1, 110):

    url_page = url_pageless + str(i)
    response = requests.request("GET", url_page, headers=headers, data = payload)
    if response.status_code != 200:
        print("response code is: %d\nExiting. if status is 401 make sure you have used the correct bearer?" % response.status_code)
        exit(1)
    res_text = response.text.encode('utf8')
    if res_text == b'[]':
        print("finished\nlast page is: " + str(i-1))
        break
    full_json_str += res_text
    page_json = json.loads(res_text)
    for j in range(len(page_json)):
        title = page_json[j]["BookTitle"].encode('utf-8')
        content = page_json[j]["Content"].encode('utf-8')
        author = page_json[j]["BookAuthor"].encode('utf-8')
        only_booktitle_and_highlights.append({"title": title, "author": author, "content": content})
    print("page %d processed." % i)
    sleep(0.5)


with open("full_json_all_pages", "wb") as all_json:
    all_json.write(full_json_str)

#reconstruct clippings from booktitle and highlights
clippings_text = b'' 
for i in only_booktitle_and_highlights:
    clippings_text += i["title"] + ' ('.encode('utf-8') + i["author"] + ')'.encode('utf-8') + '\r\n- Your Highlight on Location 249-250 | Added on Sunday, February 12, 2023 10:51:38 PM'.encode('utf-8') + "\r\n\r\n".encode('utf-8') + i["content"] + "\r\n==========\r\n".encode('utf-8') 

with open("My Clippings.txt", "wb") as clippings:
    clippings.write(clippings_text)
