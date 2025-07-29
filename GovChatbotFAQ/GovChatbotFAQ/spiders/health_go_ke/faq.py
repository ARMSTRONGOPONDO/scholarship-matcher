import scrapy
from GovChatbotFAQ.items import GovChatbotFAQItem
import re
from scrapy_playwright.page import PageMethod

class HealthFAQSpider(scrapy.Spider):
    name = 'health_faq_spider'

    def start_requests(self):
        yield scrapy.Request(
            url='https://sha.go.ke/',
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod('wait_for_selector', 'div#faqs ul li[id^="faq_"]', timeout=30000)
                ],
                errback=self.errback,
            ),
            callback=self.parse_sha
        )

    async def parse_sha(self, response):
        page = response.meta["playwright_page"]
        await page.close()
        """
        A dedicated parser for the sha.go.ke website.
        It extracts data from the 'aria-label' attribute which is more reliable.
        """
        for faq in response.css('div#faqs ul li[id^="faq_"]'):
            item = GovChatbotFAQItem()
            aria_label = faq.css('button span::attr(aria-label)').get()

            if aria_label:
                # Use regex to reliably split the question and answer
                match = re.search(r'Question:\s*(.*?)\s*,\s*Answer:\s*(.*)', aria_label, re.DOTALL)
                if match:
                    question = match.group(1).strip()
                    answer = match.group(2).strip()
                else:
                    # Fallback if regex fails
                    question = faq.css('button span::text').get()
                    answer = "Could not parse answer from aria-label."
            else:
                # Fallback if there is no aria-label
                question = faq.css('button span::text').get()
                answer = "Could not find aria-label."

            if question and answer:
                item['question'] = question.strip()
                item['answer'] = answer.strip()
                item['category'] = 'Social Health Authority'
                item['tags'] = ['SHA', 'health', 'Kenya']
                item['date_posted'] = None
                item['date_updated'] = None
                yield item

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

