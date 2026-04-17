# 🚀 Asynchronous Web Health Checker

A high-performance, command-line utility built with Python to monitor the status of multiple web endpoints concurrently.
This tool leverages modern asynchronous patterns to provide speed, resilience, and safety.

## ✨ Features

- **Blazing Fast Concurrency**: Powered by `asyncio` and `aiohttp` for non-blocking I/O.
- **Modern CLI**: Built with `Typer` for a beautiful, type-safe command-line interface with automatic help
  documentation.
- **Structured Concurrency**: Uses Python 3.11+ `TaskGroup` to ensure tasks are managed and cleaned up safely.
- **Smart Rate Limiting**: Implements `asyncio.Semaphore` to prevent overwhelming target servers or triggering DDoS
  protection.
- **Resilient Retries**: Includes automatic retry logic with **Exponential Backoff** for handling transient network
  blips.
- **Threaded Data Export**: Offloads blocking CSV file writing to background threads using `asyncio.to_thread` to keep
  the event loop responsive.

## 🛠️ Built With

- [Python 3.11+](https://www.python.org/)
- [uv](https://github.com/astral-sh/uv) - Fast Python package management.
- [aiohttp](https://docs.aiohttp.org/) - Asynchronous HTTP client.
- [Typer](https://typer.tiangolo.com/) - Modern CLI library.

## 🚀 Getting Started

### Prerequisites

Ensure you have [uv](https://github.com/astral-sh/uv) installed.

### Installation

1. Clone the repository:

    ```bash
    git clone git@github.com:Harry-s10/url_health_checker.git 
    cd health_checker
    ```

2. Install dependencies:

    ```bash
    uv sync
    ```

### 📖 Usage

1. Create a `urls.txt` file with one URL per line:
    ```plaintext
    https://www.google.com
    https://www.github.com 
    https://www.python.org
    ```

2. Run the checker:

    ```bash
    uv run python cli.py check urls.txt
    ```

**Command options**

| Option          | Shorthand | Default       | Description                               |
|-----------------|-----------|---------------|-------------------------------------------|
| `--output`      | `-o`      | `results.csv` | The filename for the CSV report.          |
| `--concurrency` | `-c`      | `5`           | Maximum number of concurrent connections. |
| `--help`        |           |               | Show the help menu.                       |

**Example with custom settings:**

```bash
uv run python cli.py check urls.txt -c 20 -o weekly_report.csv
```