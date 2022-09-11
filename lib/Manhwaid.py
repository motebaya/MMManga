from .functions import Base

class Manhwaid(Base):
    host = "https://manhwaid.club"
    def search(self, query: str):
        page = self.session.get(
            self.host + f"/?s={query}&post_type=wp-manga"
        ).text
        soup = self.parse(page)
        if (li := soup.find_all(class_="tab-thumb")):
            for l in li:
                a = l.find("a").attrs
                yield {
                    "id": self.getPath(a.get("href")),
                    "title": a.get("title")
                }
        return None

    def getchapter(self, id: str):
        page = self.session.post(
            f"{self.host}{id}ajax/chapters/"
        ).text
        soup = self.parse(page)
        if (chap := soup.find_all(class_="wp-manga-chapter")):
            for cap in chap:
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
        if (data := soup.find_all(class_="page-break")):
            return (soup.find(id="chapter-heading").text.strip(),
                list(map(
                    (lambda s: s.find("img").attrs.get("src").strip()), 
                data
            )))
        return None

# # testing
# m = Manhwaid()
# m1 = list(m.search("doki"))
# print(m1)

# m2 = list(m.getchapter(m1[0]["id"]))
# print(m2)

# m3 = list(m.getImage(m2[0]["id"]))
# print(m3)