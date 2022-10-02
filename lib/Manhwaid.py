#!/usr/bin/env python3

from . import Base

class Manhwaid(Base):
    """
    different page template, just create different file 
    for more easy to use.
    """
    host = "https://{}"
    async def search(self, query: str):
        page = await self.get(
            self.host + f"/?s={query}&post_type=wp-manga"
        )
        soup = self.parse(page.text)
        if (li := soup.find_all(class_="tab-thumb")):
            return map(
                (lambda x: {
                    't': x.a.get('title'),
                    'a': self.getPath(
                        x.a.get('href')
                    )
                }), li
            )
        return None

    async def get_chapter(self, id: str):
        page = await self.post(
            f"{self.host}/{id}ajax/chapters/"
        )
        soup = self.parse(page.text)
        if (chap := soup.find_all(class_="wp-manga-chapter")):
            return map(
                (lambda x: {
                    'a': self.getPath(
                        x.a.get('href')
                    )
                }), chap
            )
        return None

    async def get_images(self, chap: str):
        page = await self.get(
            f"{self.host}/{chap}"
        )
        soup = self.parse(page.text)
        if (data := soup.find_all(class_="page-break")):
            return (soup.find(id="chapter-heading").text.strip(),
                list(map(
                    (lambda s: s.find("img").attrs.get("src").strip()), 
                data
            )))
        return None
