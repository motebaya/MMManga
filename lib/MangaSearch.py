#!/usr/bin/env python3

from . import Base
import re, json, regex

class Mangasearch(Base):
    """
    site_list = [
        mangadop.net
        manhwadesu.com
        sekaikomik.live
        komiklokal.me
        manhwaland.guru
        komik18.art (indo lang)
        komikdewasa.me (indo lang)
    ]
    """
    host = "https://{}"

    async def search(self, query: str):
        assert "{}"  not in self.host
        page = await self.get(
            f"{self.host}/?s={query}"
        )
        soup = self.parse(page.text)
        if (li := soup.find_all(class_='bsx')):
            return map(
                (lambda x: {
                    't': x.a.get('title'),
                    'a': self.getPath(
                        x.a.get('href'))
                }), li
            )
        return None

    async def get_chapter(self, id: str):
        page = await self.get(
            f"{self.host}/{id}", follow_redirects=True
        )
        soup = self.parse(page.text)
        if (li := soup.find_all(class_='eph-num')):
            return map(
                (lambda x: {'a': self.getPath(
                    x.find('a').get('href')
                )}), li[1:]
            )
        return None
    
    async def get_images(self, chapter: str):
        page = await self.get(f"{self.host}/{chapter}", follow_redirects=True)
        soup = self.parse(page.text)
        if (raw := re.search(r"(?<=ts_reader\.run\()([^']+?)(?=\);)", page.text)):
            if (raw_json := regex.search(r'\{(?:[^{}]|(?R))*\}', raw.group(1))):
                return (soup.find(class_='entry-title'
                    ).text.strip(), json.loads(
                        re.sub(r"(?:!(\d|\w)|null)",
                            r'""', raw_json.group())
                    )['sources'][0]['images'])
            return None
        return None

# test method
