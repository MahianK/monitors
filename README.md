# Best Buy Product Monitor

A Python availability monitor that checks Best Buy product pages and sends real-time Discord notifications when an item becomes available to purchase.

The monitor uses Requests and Beautiful Soup to inspect each product page for an active **Add to Cart** button. Results are printed to the terminal with timestamps, and in-stock products trigger a Discord embed containing the product name, link, SKU, and price.

> [!IMPORTANT]
> The current source contains a hard-coded Discord webhook URL. Revoke that webhook in Discord before using or publishing the project, then replace it with a new webhook loaded from an environment variable. Never commit webhook URLs or other credentials.

## Features

- Monitors multiple Best Buy product pages in sequence
- Parses HTML with Beautiful Soup
- Detects availability from the add-to-cart button
- Rotates browser user-agent strings between requests
- Prints timestamped, color-coded status updates
- Sends rich Discord webhook notifications
- Includes product links, SKUs, and prices in each alert
- Supports configurable products and polling intervals

## Tech stack

- Python
- [Requests](https://requests.readthedocs.io/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [discord-webhook](https://pypi.org/project/discord-webhook/)

## How it works

```text
Best Buy product page
        │
        ▼
Download page HTML with Requests
        │
        ▼
Find the add-to-cart element with Beautiful Soup
        │
        ├── “Add to Cart” found ──► Log in stock ──► Send Discord alert
        │
        └── Not found ────────────► Log out of stock
```

The script repeats this process for every product in the `stores` dictionary.

## Getting started

### Prerequisites

- Python 3.8 or 3.9
- A Discord server where you can create webhooks

The repository's dependency versions were originally pinned in 2022. Python 3.8 or 3.9 offers the best compatibility with those versions.

### 1. Clone the repository

```bash
git clone https://github.com/MahianK/monitors.git
cd monitors
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the repository's complete dependency snapshot:

```bash
python -m pip install -r requirements.txt
```

Only three third-party packages are required by the current script. If the older pinned dependencies do not install on your system, install these directly instead:

```bash
python -m pip install requests beautifulsoup4 discord-webhook
```

## Secure Discord webhook setup

1. In Discord, open your server settings and create a webhook for the channel that should receive stock alerts.
2. Revoke the webhook currently embedded in `BestBuyProductMonitor.py`.
3. Replace the hard-coded value in the script with an environment lookup:

```python
webhook_url = os.environ["DISCORD_WEBHOOK_URL"]
webhook = DiscordWebhook(url=webhook_url, username="Best Buy")
```

4. Set the environment variable before starting the monitor:

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/your-new-webhook"
```

On Windows PowerShell:

```powershell
$env:DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your-new-webhook"
```

## Configuring products

Products are defined in the `stores` dictionary inside `BestBuyProductMonitor.py`:

```python
stores = {
    "PRODUCT LABEL": [
        "https://www.bestbuy.com/site/example-product/0000000.p?skuId=0000000",
        ".add-to-cart-button",
        "Add to Cart",
        "Example Product Name",
        "0000000",
        "$99.99",
    ]
}
```

Each entry contains:

| Position | Value | Purpose |
| ---: | --- | --- |
| `0` | Product URL | Best Buy page to request |
| `1` | CSS selector | Element inspected for stock status |
| `2` | Expected text | Text that indicates availability |
| `3` | Product name | Title shown in terminal and Discord |
| `4` | SKU | SKU shown in the notification |
| `5` | Price | Price shown in the notification |

The repository includes example entries for PlayStation consoles, an NVIDIA graphics card, and a Samsung television. Product URLs, prices, and page markup can change, so verify each entry before running the monitor.

## Polling interval

The number passed to `runCheck` at the bottom of the script controls the delay, in seconds, after each product check:

```python
checkStock().runCheck(60)
```

Use a considerate interval and review Best Buy's applicable terms and policies before running automated requests. Very frequent polling can create unnecessary traffic or lead to rate limiting.

## Run the monitor

After configuring a new Discord webhook and verifying the products:

```bash
python BestBuyProductMonitor.py
```

The terminal will show a timestamped status for each product. When **Add to Cart** is detected, the configured Discord channel receives an embed with the purchasing link and product details.

Stop the monitor with `Ctrl+C`.

## Project structure

```text
monitors/
├── BestBuyProductMonitor.py  # Scraper, availability checks, and Discord alerts
├── requirements.txt          # Original pinned Python dependencies
└── azure-pipelines.yml       # Azure Pipelines placeholder configuration
```

## Current limitations

- Best Buy can change its HTML, CSS selectors, or anti-automation behavior at any time.
- Static HTML requests may not detect availability rendered only by JavaScript.
- The current implementation sends another alert on every successful polling cycle; it does not remember prior stock state.
- Product names, SKUs, and prices are manually configured rather than extracted from the page.
- Request timeouts, retries, and HTTP error handling are not yet implemented.
- The polling cycle currently restarts through recursion and should be changed to an iterative loop for reliable long-running use.
- The included dependency file contains more packages than the current script requires.

## Ideas for improvement

- Load products and webhook settings from a `.env` or configuration file
- Notify only when availability changes from out of stock to in stock
- Add request timeouts, retry limits, and exponential backoff
- Replace positional product lists with dictionaries or data classes
- Extract current names and prices from product pages
- Add structured logging and optional log files
- Add tests using saved HTML fixtures
- Simplify and update `requirements.txt`
- Add monitoring adapters for additional retailers

## Responsible use

This project is intended for personal notifications and educational use. Follow retailer terms, respect rate limits, and do not use the monitor to interfere with a website or gain unauthorized access.
