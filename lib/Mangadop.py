from .functions import Base, datetime, re

class Mangadop(Base):
    
    host = "https://mangadop.net"

    def search(self, query: str):
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
            for cap in chap[1:]:
                yield {
                    "id": self.getPath(
                        cap.find("a").attrs.get("href")
                    )
                }
        return None
    
    def getImage(self, chap: str):
        page = self.session.get(
            self.host + chap
        ).text
        soup = self.parse(page)
        if (imageList := re.findall(r"(?<=<img\ssrc\=\")([^']*?)(?=\")", page)):
             return (soup.find(class_="entry-title").text,
              list(dict.fromkeys(
                imageList
             )))
        return None

# testing

# m = Mangadop()
# res = list(m.search("teach"))
# print(res)

# chap = list(m.getchapter(res[0]["id"]))
# print(chap)

# imgs = m.getImage(chap[0]["id"])
# print(imgs)

