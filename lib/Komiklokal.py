#!/usr/bin/python

from .functions import Base, re

class Komiklokal(Base):
    host = "https://komiklokal.me"

    def search(self, query: str, page: int = 1):
        page = self.session.get(
            self.host + f"/?s={query}"
        ).text
        soup = self.parse(page)
        if (li := soup.find_all(class_="bsx")):
            for l in li:
                a = l.find("a").attrs
                yield {
                    "id": self.getPath(
                        a.get("href")
                    ),
                    "title": a.get("title")
                }
        return None

    def getchapter(self, id: str):
        page = self.session.get(
            self.host + id
        ).text
        soup = self.parse(page)
        if (chap := soup.find_all(class_="eph-num")):
            for ca in chap[1:]:
                yield {
                    "id": self.getPath(
                        ca.find("a").attrs.get("href")
                    )
                }

    def getImage(self, chap: str):
        page = self.session.get(
            self.host + chap
        ).text
        soup = self.parse(page)
        if (data := re.search(r"(?<=\"images\"\:)([^']+?)(?=\})", page)):
            return (
                soup.find(class_="entry-title").text.strip(),
                eval(
                    data.group(1).replace("\\", "")
                )
            )
        return None

# # # testing

# m = Komiklokal()
# res = list(m.search("teach"))
# print(res)

# cap = list(m.getchapter(res[0]["id"]))
# print(cap)

# imgs = m.getImage(cap[0]["id"])
# print(imgs)