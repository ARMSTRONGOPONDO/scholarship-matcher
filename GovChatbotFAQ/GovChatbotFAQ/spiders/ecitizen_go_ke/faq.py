import scrapy
from GovChatbotFAQ.items import GovChatbotFAQItem

class ECitizenFAQSpider(scrapy.Spider):
    name = 'ecitizen_faq_spider'
    allowed_domains = ['ecitizen.go.ke']
    start_urls = [
        'https://ecitizen.go.ke/en/help-and-support'
    ]

    def parse(self, response):
        # Select each list item that contains a question and answer pair.
        # These are identified by an ID that starts with "faq_".
        # This selector is accurate based on the HTML structure.
        for faq in response.css('li[id^="faq_"]'):
            item = GovChatbotFAQItem()

            # Select the question text more specifically using the span's class
            question = faq.css('button span.text-lg.font-medium::text').get()

            # Select the answer container div and extract all text content within it.
            # This is more robust than targeting just <p> tags, in case the structure changes.
            answer_parts = faq.css('div.relative.overflow-hidden.transition-all ::text').getall()
            # Join all text parts, stripping whitespace and filtering out empty strings
            answer = " ".join(part.strip() for part in answer_parts if part.strip())

            item['question'] = question.strip() if question else None
            item['answer'] = answer.strip() if answer else None # Also strip the final answer
            item['category'] = 'eCitizen General' # Category is static for this page
            item['tags'] = ['eCitizen']
            item['date_posted'] = None
            item['date_updated'] = None

            yield item
