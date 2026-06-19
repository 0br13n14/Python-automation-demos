# Python-demos

### email_sender.py
Sends a single email via Gmail SMTP using environment variables for credentials.

### bulk_email_sender.py
Reads customer data from a CSV file and sends personalized emails to each 
recipient — core automation pattern: read data, loop, act per row.

### ContactManagerCLI.py
Command-line contact manager — add, view, and search contacts stored locally.

### web_scraper.py
**Professional 8-function web scraper** — input validation, defensive fetch
with retries, HTML parsing, data extraction, unicode cleaning, pagination,
and CSV save. Scraped 100 quotes across 10 pages from **quotes.toscrape.com.**

> Note: currently configured for quotes.toscrape.com. Structure can be adapted for other sites by updating the parse() and extract() functions.
