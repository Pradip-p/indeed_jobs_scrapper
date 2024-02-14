BOT_NAME = "indeed"

SPIDER_MODULES = ["indeed.spiders"]
NEWSPIDER_MODULE = "indeed.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 5  # Set the delay to 5 seconds (adjust as needed)


# Set settings whose default value is deprecated to a future-proof value
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}


TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_LAUNCH_OPTIONS = {
    "slow_mo": 300,
    "headless": True,
    "timeout": 30 * 10000,  # 200 seconds
}
# settings.py

DEFAULT_REQUEST_HEADERS = {
    'Accept-Language': 'en-US,en;q=0.9',
}



# PLAYWRIGHT_CDP_KWARGS = {
#     "slow_mo": 1000,
#     "timeout": 10 * 1000
# }