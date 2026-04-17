import asyncio
import csv
from pathlib import Path

import aiohttp
import typer

# CLI App
app = typer.Typer(help="🚀 Modern Async Web Health Checker")


def save_to_csv(file: Path, data: list):
    with file.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file.exists():
            writer.writerow(["URL", "Status"])
        writer.writerows(data)


async def check_url(url: str, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore):
    async with semaphore:
        try:
            async with session.get(url, timeout=5) as response:
                return url, response.status
        except Exception as e:
            return url, f"❌ Error: {e}"


async def run_checks(urls: list[str], concurrency: int, output: Path):
    sem = asyncio.Semaphore(concurrency)
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(check_url(url, session, sem)) for url in urls]
        results = [task.result() for task in tasks]
    for url, status in results:
        typer.echo(f"{url:40} {status}")

    await asyncio.to_thread(save_to_csv, output, results)
    typer.secho(f"Results saved to {output}", fg=typer.colors.GREEN, bold=True)


@app.command()
def check(
    file: Path = typer.Argument(..., help="Path to text file with URLs"),
    output: str = typer.Option("result.csv", "--output", "-o", help="Output CSV file"),
    concurrency: int = typer.Option(5, "--concurrency", "-c", help="Number of concurrent requests"),
):
    """
    Check the health of a list of URLs asynchronously.
    """
    if not file.exists():
        typer.secho(f"Error: File {file} not found.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    urls = [line.strip() for line in file.read_text().splitlines() if line.strip()]
    asyncio.run(run_checks(urls, concurrency, Path(output)))


if __name__ == "__main__":
    app()
