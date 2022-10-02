#!/usr/bin/env python3

from lib import Base, MangaSearch
import asyncio

async def test_all():
    module = MangaSearch.Mangasearch() # call class
    module.host = module.host.format('manhwaland.guru') # set host
    print(module.host)
    search = await module.search('lea') # search result list type(map)
    search = list(search)
    print(search)
    print()
    chapter = await module.get_chapter(search[0]['a']) # chapter list
    chapter = list(chapter)
    print(chapter)
    print()
    images = await module.get_images(chapter[0]['a']) # tuple output with title & images list
    # or
    title, images_list = images # unpack tuple values
    print(images)

if __name__=='__main__':
    asyncio.run(test_all())
