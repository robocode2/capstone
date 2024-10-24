from shutil import which
import os
from dotenv import load_dotenv

load_dotenv()
# Scrapy settings for weatherscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "weatherscraper"

SPIDER_MODULES = ["weatherscraper.spiders"]
NEWSPIDER_MODULE = "weatherscraper.spiders"
LOG_LEVEL = 'ERROR'

LOCATIONS_JSON_PATH = 'weatherScraper/locations.json'

SCRAPEOPS_API_KEY = os.getenv('SCRAPEOPS_API_KEY')

SCRAPEOPS_PROXY_ENABLED = True


SCRAPEOPS_NUM_RESULTS = 50

CONCURRENT_REQUESTS = 1 
DOWNLOAD_DELAY = 2

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "weatherscraper.middlewares.WeatherscraperSpiderMiddleware": 543,
#}

""" SELENIUM_DRIVER_NAME = 'chrome'
SELENIUM_DRIVER_EXECUTABLE_PATH = which("chromedriver")
SELENIUM_DRIVER_ARGUMENTS = [] 
 """

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,
    'scrapeops_scrapy.middleware.retry.RetryMiddleware': 900,
    'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
    'weatherscraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware': 400,
}

ROBOTSTXT_OBEY = False


EXTENSIONS = {
        'scrapeops_scrapy.extension.ScrapeOpsMonitor': 500, 
        }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'weatherscraper.pipelines.PostgreSQLPipeline': 200,

}
DATABASE_URL = os.getenv('PROD_DATABASE_URL')



# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"



