import asyncio
from urllib.parse import urlsplit


async def check_url(url: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        try:
            url_parsed = urlsplit(url)
            port: int = 443 if url_parsed == "https" else 80
            use_ssl: bool = url_parsed == "https"

            return await asyncio.wait_for(perform_request(url_parsed.hostname, port, use_ssl), timeout=5.0)
        except TimeoutError:
            return f"{url}: ❌ Failed"
        except Exception as e:
            return f"{url}: ❌ Error: {e}"


async def perform_request(hostname, port, use_ssl):
    reader, writer = await asyncio.open_connection(hostname, port, ssl=use_ssl)
    query = f"GET / HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
    writer.write(query.encode())
    await writer.drain()

    response = await reader.readline()
    writer.close()
    await writer.wait_closed()

    return f"{hostname}: ✅ {response.decode().strip()}"


async def main():
    urls = ["https://www.google.com", "https://www.python.org", "https://www.github.com"]
    sem = asyncio.Semaphore(5)
    tasks = []
    async with asyncio.TaskGroup() as tg:
        for url in urls:
            task = tg.create_task(check_url(url, sem))
            tasks.append(task)

    for task in tasks:
        print(task.result())


if __name__ == "__main__":
    asyncio.run(main())
