#!/usr/bin/python
"""
just for learn, so sorry if my code so bad
created = ctime(
    Monday Oct 3 03:32:58 2022
)
credits t.me/dvinchii / github.com/motebaya
"""
from argparse import ArgumentParser, RawTextHelpFormatter
from lib import (
    CreatePdf,
    MangaSearch,
    Manhwaid,
    exists
)
import asyncio

class Main(CreatePdf):
    """
    main class for CLI and handle Module
    """
    async def _main(self, query: str, site: str):
        site_choice = [
            i for i in self.site_list if i.startswith(
                site.lower()
            )
        ]
        if site_choice:
            host = site_choice[0] if site.lower() != 'manhwaid' else 'manhwaid.club'
            module = MangaSearch.Mangasearch() if 'manhwaid' not in host else Manhwaid.Manhwaid()
            module.host = module.host.format(host)
            self.debug(host)
            if (s_result := await module.search(query)):
                s_result = list(s_result)
                title = list(i.get('t') for i in s_result)
                if (chap := await self.choice(title, message=f"found ({len(s_result)}) results for query")):
                    chap = s_result[title.index(chap)]
                    self.check_dirs(
                        chap.get('t')
                    )
                    if (chapters := await module.get_chapter(chap.get('a'))):
                        chapters = list(chapters)[::-1]
                        self.debug(f"found ({len(chapters)}) chapters in {chap.get('t')}")
                        self.debug('Select chapters follow min and max range')
                        s_chap = await self.choice(
                            list(), 
                            message='Input in range ({})-({})'.format(
                                min(range(len(chapters)))+1,
                                max(range(len(chapters)))+1
                            )
                        )
                        if (c_list := self.get_range(s_chap, chapters)):
                            for index, chaps in enumerate(c_list, 1):
                                p_chapter = chapters.index(chaps) + 1 # chapter index position 
                                self.debug(f"getting all images on chapter: ({p_chapter}) of ({len(c_list)})")
                                f_output = "./{}/{}".format(chap.get('t'), f"{c_title}.pdf")
                                if not exists(f_output): # check if chapter exist on dir or not
                                    if (m_list := await module.get_images(chaps.get('a'))):
                                        c_title, m_list = m_list
                                        images_data = await self.req_images(m_list)
                                        _pdf = await self.adjust_image(images_data)
                                        self.debug(f"converting ({len(_pdf)}) images to pdf")
                                        _pdf[0].save(
                                            "./{}/{}".format(
                                                chap.get('t'), f"{c_title}.pdf"
                                            ), save_all=True, append_images=_pdf[1:]
                                        )
                                        self.debug(f"saved {c_title}.pdf")
                                    else:
                                        self.debug(f"skip chapters {p_chapter}", mode='red')
                                else:
                                    self.debug(f"skip chapters {p_chapter} alrdy downloaded", mode='yellow')
                            self.debug(f"success downloading total {len(c_list)} chapters")
                        return None # no need ?
                return None
            return None
        return None

    async def _cli(self):
        parser = ArgumentParser(
            description="\tNSFW Manhwa downloader\n    Author: @github.com/motebaya",
            formatter_class=RawTextHelpFormatter
        )
        parser.add_argument('-s', '--site', help='chose site host .eg: sekaikomik', metavar='', type=str)
        parser.add_argument('-q', '--query', help='query for search, read readme.md!', metavar='', type=str, nargs="*")
        group = parser.add_argument_group('additional', description='example usage')
        group.add_argument('-i', '--info', help='info or show example', action='store_true')
        arg = parser.parse_args()
        if arg.site and arg.query:
            if any(x.startswith(arg.site) for x in self.site_list):
                print(f"\n{parser.description}\n")
                await self._main(
                    '+'.join(arg.query), arg.site
                )
            else:
                self.debug(f'site {arg.site} not exists in website list')
                self.debug('usage -i for show info/example')
                exit(1)
        elif arg.info:
            exit(" example usage: main.py -q doki doki -s sekaikomik")
        else:
            parser.print_help()

if __name__=="__main__":
    try:
        asyncio.run(Main()._cli())
    except Exception as e:
        exit(str(e))
