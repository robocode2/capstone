# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class WeatherscraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class WeatherscraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
        

from urllib.parse import urlencode
from random import randint
import random
import requests

class ScrapeOpsFakeBrowserHeaderAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT', 'http://headers.scrapeops.io/v1/browser-headers') 
        self.scrapeops_fake_browser_headers_active = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED', True)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self._get_headers_list()
        self._scrapeops_fake_browser_headers_enabled()

    def _get_headers_list(self):
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.headers_list = json_response.get('result', [])

    def _get_random_browser_header(self):
        random_index = randint(0, len(self.headers_list) - 1)
        return self.headers_list[random_index]

    def _scrapeops_fake_browser_headers_enabled(self):
        if self.scrapeops_api_key is None or self.scrapeops_api_key == '' or self.scrapeops_fake_browser_headers_active == False:
            self.scrapeops_fake_browser_headers_active = False
        else:
            self.scrapeops_fake_browser_headers_active = True
    
    def process_request(self, request, spider):        
        random_browser_header = self._get_random_browser_header()
        
        fallback_headers = {
            'accept-language': 'en-US,en;q=0.9',
            'sec-fetch-user': '?1',
            'sec-fetch-mode': random.choice(['navigate', 'cors', 'no-cors']),
            'sec-fetch-site': random.choice(['same-origin', 'cross-site', 'none']),
            'sec-ch-ua-platform': random.choice(['Windows', 'Linux', 'macOS']),
            'sec-ch-ua-mobile': random.choice(['?0', '?1']),
            'sec-ch-ua': random.choice([
                            '"Google Chrome";v="95", "Not A;Brand";v="99", "Chromium";v="95"',
                            '"Mozilla";v="5.0", "Not A;Brand";v="99", "Chromium";v="95"',
                            '"Microsoft Edge";v="94", "Chromium";v="94", "Not A;Brand";v="99"'
                        ]),
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'user-agent': random.choice([
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
                            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15'
                        ]),
            'upgrade-insecure-requests': '1'
        }

        request.headers['accept-language'] = random_browser_header.get('accept-language', fallback_headers['accept-language'])
        request.headers['sec-fetch-user'] = random_browser_header.get('sec-fetch-user', fallback_headers['sec-fetch-user']) 
        request.headers['sec-fetch-mode'] = random_browser_header.get('sec-fetch-mode', fallback_headers['sec-fetch-mode']) 
        request.headers['sec-fetch-site'] = random_browser_header.get('sec-fetch-site', fallback_headers['sec-fetch-site']) 
        request.headers['sec-ch-ua-platform'] = random_browser_header.get('sec-ch-ua-platform', fallback_headers['sec-ch-ua-platform']) 
        request.headers['sec-ch-ua-mobile'] = random_browser_header.get('sec-ch-ua-mobile', fallback_headers['sec-ch-ua-mobile']) 
        request.headers['sec-ch-ua'] = random_browser_header.get('sec-ch-ua', fallback_headers['sec-ch-ua']) 
        request.headers['accept'] = random_browser_header.get('accept', fallback_headers['accept']) 
        request.headers['user-agent'] = random_browser_header.get('user-agent', fallback_headers['user-agent']) 
        request.headers['upgrade-insecure-requests'] = random_browser_header.get('upgrade-insecure-requests', fallback_headers['upgrade-insecure-requests'])

    