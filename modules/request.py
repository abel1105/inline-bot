import json
import os
import requests
import webbrowser
from bs4 import BeautifulSoup

cookies = {}

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}


def getHTML(url):
    r = requests.get(url, cookies=cookies, headers=headers)
    return BeautifulSoup(r.text, 'html.parser')


def getJSON(url):
    r = requests.get(url, cookies=cookies, headers=headers)
    return json.loads(r.text)


def getData(url):
    r = requests.get(url, cookies=cookies, headers=headers)
    return r


def postData(url, data):
    r = requests.post(url, data=data, cookies=cookies, headers=headers)
    return r


def postJson(url, data):
    json_headers = headers
    json_headers['content-type'] = 'application/json'
    json_data = json.dumps(data)
    r = requests.post(url, data=json_data, cookies=cookies, headers=json_headers)
    return r


def openImage(src):
    chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
    img_url = "https://tixcraft.com" + src
    webbrowser.get(chrome_path).open(img_url)
