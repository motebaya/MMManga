#!/usr/bin/python
"""
just simpl code, use it for learn 
i also still learn in python

"""
from importlib import import_module
from lib.functions import *
from concurrent.futures import ThreadPoolExecutor

sitelist = [
    "mangadop.net",
    "sekaikomik.live",
    "manhwaid.club",
    "manhwadesu.me",
    "komiklokal.me",
]

def to_menu(t: list):
    for index, value in enumerate(t, 1):
        print(
            f" [{index:02d}] {value.title()}"
        )

def select(min: int, max: int, q: str):
    print()
    while True:
        try:
            s = int(input(f" [#] {q.title()}: "))
            if s in list(range(min, max + 1)):
                return s
            else:
                continue
        except ValueError:
            continue

def ask_query(s):
    while True:
        query = input(f" [#] {s.title()}: ")
        if (query := query.strip()):
            return query
        else:
            continue

def get_range(i: str, t: list):
    if i.lower() == "all":
        return t[:]

    if i.isdigit() and len(t) >= (int(i) - 1):
        return t[int(i)-1]

    i = list(map(int, i.split("-")))
    i[-1] = i[-1] + 1
    ranges = list(range(*i))
    start, end = ranges[0] -1, ranges[-1]
    if len(t) >= (start):
        return t[start: end]

def _main():
    print()
    to_menu(sitelist)
    site = select(1, len(sitelist), "chosee")
    filename = sitelist[site -1].split(".")[0].title()
    Base = import_module(f"lib.{filename}")
    module = eval(
        "Base.{}()".format(
            filename
        )
    )
    query = ask_query("query")
    if (result := module.search(query)):
        result = list(result)
        print(
            f"\n ~! Found {len(result)} result \n"
        )
        to_menu(list(
            map(lambda v: v["title"], result)
        ))
        chapter = select(1, len(result), "chapter")
        chapter = result[chapter-1]
        if (chapterlist := module.getchapter(chapter["id"])):

            chapterlist = list(chapterlist)[::-1]
            print(
                f"\n ~! Found Total Chapter {len(chapterlist)}\n    Input Range if wanna download batch!\n    Type All if wanna download all chapter\n"
            )
            dlist = get_range(ask_query("Chapter (eg:1-10):"), chapterlist)
            if not os.path.isdir(chapter["title"]):
                os.mkdir(chapter["title"])

            for index, img in enumerate(dlist, 1):
                title, images = module.getImage(img["id"])
                output = "./{}/{}.pdf".format(chapter["title"], title)
                if not os.path.exists(output):
                    print(f"\r ~! Downloading : {index} Of {len(dlist)} chapter", end="")
                    pdf = HandlePdf()
                    pdf = pdf.adjustImage(
                        list(pdf.getImage(images))
                    )
                    pdf[0].save(output, save_all=True, append_images=pdf[1:])
                    print(
                        f"\n [%] Saved: {title}.pdf"
                    )
                else:
                    continue

if __name__=="__main__":
    _main()
