import asyncio
import time


async def get_html(url):
    print("start get url")
    await asyncio.sleep(2)
    print("end get url")


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(get_html('http://www.baidu.com'))
    print(time.time() - start_time)
