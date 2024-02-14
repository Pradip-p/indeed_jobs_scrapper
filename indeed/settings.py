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
    "headless": True,
    "timeout": 20 * 10000,  # 200 seconds
}