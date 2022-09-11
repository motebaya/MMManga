from .functions import Base, re, json

class Manhwadesu(Base):
    host = "https://manhwadesu.me"
    def search(self, query: str):
        page = self.session.get(
            self.host + f"/?s={query}"
        ).text
        soup = self.parse(page)
        if (li := soup.find_all(class_="bsx")):
            for i in li:
                a = i.find("a")
                yield {
                    "id": self.getPath(a.get("href")),
                    "title": a.get("title")
                }
        return None
    
    def getchapter(self, chap: str):
        page = self.session.get(
            self.host + chap
        ).text
        soup = self.parse(page)
        if (cap := soup.find_all(class_="eph-num")):
            for i in cap[1:]:
                yield {
                    "id": self.getPath(i.find("a").attrs.get("href"))
                }
        return None
    
    def getImage(self, chap: str):
        page = self.session.get(
            self.host + chap
        ).text
        soup = self.parse(page)
        if (data := re.search(r"(?<=ts_reader\.run\()([^']+?)(?=\);)", page)):
            return (soup.find(class_="entry-title").text, json.loads(
                data.group(1)
            )["sources"][0]["images"])
        return False

# testing

# m = Manhwadesu()
# m1 = list(m.search("teach"))
# print(m1)

# m2 = list(m.getchapter(m1[0]["id"]))
# print(m2)

# m3 = m.getImage(m2[0]["id"])
# print(m3)