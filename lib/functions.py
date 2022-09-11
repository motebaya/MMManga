#!/usr/bin/python

import requests, re, os, json
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
from PIL import Image
from io import BytesIO

class Base:
    def __init__(self):
        self.session = self.make_session()
    
    def make_session(self) -> requests.Session:
        session = requests.Session()
        session.headers["User-Agent"] = "Mozilla/5.0 (Linux; Android 11; Infinix X6810) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"
        return session
    
    def parse(self, raw):
        return BeautifulSoup(raw, "html.parser")
    
    def getPath(self, url):
        return urlparse(url).path

class HandlePdf:
    def __init__(self):
        self.name = None

    def getImage(self, Listurl: str):
        for index, url in enumerate(Listurl, 1):
            print(f"\r ~! Fetching Image: {index} Of {len(Listurl)}        ", end="")
            content = requests.get(url).content
            yield Image.open(
                BytesIO(content)
            )

    def adjustImage(self, imgList: list) -> list:
        listSize = list(map(
            (lambda s: s.size), imgList
        ))
        size = max(set(listSize), key=listSize.count)
        return list(map(
            (lambda imgs: imgs.resize(
                (size[0], imgs.size[1])
            )), imgList
        ))
