import asyncio

import aiohttp


async def check_url(url: str, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore):
    async with semaphore:
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(url, timeout=timeout) as response:
                status = response.status
                if status == 200:
                    return f"{url:30}: ✅ Active"
                return f"{url:30}: ❌ Unable to reach"
        except TimeoutError:
            return f"{url:30}: ❌ Timeout"
        except Exception as e:
            return f"{url:30}: ❌ Error: {e}"


async def main():
    urls = ["https://www.google.com", "https://www.python.com", "https://www.github.com"]
    sem = asyncio.Semaphore(5)
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(check_url(url, session, sem)) for url in urls]
        print("Health Check result")
        for task in tasks:
            print(task.result())


if __name__ == "__main__":
    asyncio.run(main())
