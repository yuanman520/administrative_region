#!/usr/bin/env python3

import asyncio
import re

import aiohttp
from pyquery import PyQuery as pq

from config import REGION_URL, REGION_COLLECTION, MONGODB_NAME
from db_motor import BaseMotor


async def crawl_administrative_region():

    async with aiohttp.ClientSession() as session:
        async with session.get(REGION_URL) as r:
            content = await r.text()
            doc = pq(content)
            html = doc('tr[height="19"] td.xl702087').text()
            if not html:
                return False
            region_list = html.split(' ')
            data = []
            for k, v in enumerate(region_list):
                if k % 2 == 0 and v:

                    if re.match('[1-9][0-9]0000', v):
                        depth = 1

                    elif re.match('[1-9][0-9]{3}00', v):
                        depth = 2

                    else:
                        depth = 3

                    data.append({
                        '_id': v,
                        'name': region_list[k+1],
                        'depth': depth
                    })

            coll = BaseMotor().client[MONGODB_NAME][REGION_COLLECTION]
            res = await coll.insert_many(data)
            if res.inserted_ids:
                return True
            else:
                return False


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(crawl_administrative_region())
