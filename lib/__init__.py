#!/usr/bin/env python3
"""
module created : ctime(
    Monday Oct 3, 03:32:58 2022
)
readme on github.com/motebaya
"""
from urllib.parse import urlparse
from httpx import AsyncClient
from bs4 import BeautifulSoup
from time import ctime
from PIL import Image, UnidentifiedImageError
from tqdm import tqdm
from io import BytesIO
from questionary import select, text
from os.path import abspath, exists
from os import mkdir
import asyncio, aiohttp, re

class Base(AsyncClient):
    def __init__(self) -> None:
        super().__init__()
        self.headers.update({
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        })
        self.times = lambda : ctime().split()[-2]
        self.site_list = [
            "mangadop.net",
            "manhwadesu.me",
            "sekaikomik.live",
            "komiklokal.me",
            "manhwaland.guru",
            "komik18.art",
            "komikdewasa.me",
            "manhwaid.club"
        ]
        self.color = {
            'green': '\x1b[32m',
            'red': '\x1b[31m',
            'yellow': '\x1b[33m'
        }

    def parse(self, raw):
        return BeautifulSoup(
            raw.text if hasattr(raw, 'text') else raw,
            "html.parser"
        )

    def getPath(self, url: str):
        return urlparse(url).path.removeprefix('/')

    def debug(self, string: str, mode: str= 'green'):
        print(" \x1b[0m[{}{}\x1b[0m] {}".format(
            self.color[mode], self.times(),string.title()
        ))
    
    def check_dirs(self, name: str):
        fullpath = abspath(name)
        if not exists(fullpath):
            mkdir(fullpath)
    
    def _format(self, list_: list):
        return list(map(
            (lambda x: (
                f"{x[0]:02d}. {x[1].title()}"
            )), enumerate(
                list_, 1
            )
        ))

    def get_range(self, num: str, listr: list):
        """
        parse range chapter eg. when input 12-34
        then will slice with that range 
        """
        total = range(1, len(listr) + 1)
        if (rn := re.findall(r"(\d+)-(\d+)", num)):
            if len(rn[0]) == 2:
                if all(int(i) in total for i in rn[0]):
                    return listr[
                        int(rn[0][0])-1:
                        int(rn[0][1])
                    ]
                return list()
            return list()
        else:
            if (snum := int(num)-1) in total:
                return [listr[
                    snum
                ]]
            return list()

    # async ask
    async def choice(self, question: list, message: str = 'chosee'):
        if question:
            question.append('Exit')
            answer = await select(
                message.title(), self._format(question)
            ).ask_async()
            if (rn := re.search(r"^(\d+)\.", answer)):
                rn = rn.group(1)
                if (int(rn)-1) in range(len(question)-1):
                    return question[int(rn)-1]
                return None
            return None

        # single ask
        answer = await text(message.title()).ask_async()
        return answer


class CreatePdf(Base):
    async def req_images(self, list_url: list):
        image_data = []
        for index, value in enumerate(list_url, 1):
            print(value)
            self.debug(f'downloading images {index} of {len(list_url)}')
            try:
                content = await self.download(value)
                if content:
                    image_data.append(content)
            except UnidentifiedImageError:
                self.debug(f"skip {value} image corrupted!", mode='red')
                continue
        return image_data

    async def download(self, image_url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                t = tqdm(asyncio.as_completed(session), total=int(response.headers.get('content-length', 0)), unit='B', unit_scale=True)
                image_bytes = BytesIO()
                async for i in response.content.iter_chunks():
                    image_bytes.write(i[0])
                    t.update(len(i[0]))
                t.close()
                return Image.open(
                    image_bytes
                )

    async def adjust_image(self, image_list: list) -> list:
        sizes = list(map(
            lambda x: x.size, image_list
        ))
        size = max(set(sizes), key=sizes.count)
        return list(map(
            lambda x: x.resize(
                (size[0], x.size[1])
            ), image_list
        ))
