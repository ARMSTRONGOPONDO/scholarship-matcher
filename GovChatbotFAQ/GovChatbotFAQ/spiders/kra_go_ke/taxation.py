import scrapy
from GovChatbotFAQ.items import GovChatbotFAQItem

class GovChatbotFAQSpider(scrapy.Spider):
    name = 'kra_taxation_spider'
    allowed_domains = ['kra.go.ke']
    start_urls = [
        'https://www.kra.go.ke/helping-tax-payers/faqs',
    ]

    def parse(self, response):
        """
        This first parse method finds all the FAQ categories on the left-hand
        side menu and creates a new request to scrape each one.
        """
        # Find all links in the left-side navigation menu
        category_links = response.css('div.sticky-nav ul.nav li a::attr(href)').getall()
        for link in category_links:
            # For each category link, follow it and call 'parse_category' to handle it
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        """
        This method scrapes all the Q&A pairs from a single category page
        and then follows the pagination to the next page in that category.
        """
        # Extract the category name from the active link in the menu
        category_name = response.css('div.sticky-nav ul.nav li a.active::text').get()

        # Loop through each FAQ item on the page
        for faq in response.css('div.faq-grid div.grid-item'):
            item = GovChatbotFAQItem()

            # Extract the question and answer using the correct selectors
            # .get() gets the first match
            # .getall() gets all text within the element, which is good for answers with multiple paragraphs
            question = faq.css('p.title::text').get()
            answer_parts = faq.css('div.ui-accordion-content ::text').getall()

            # Join the answer parts into a single clean string
            answer = " ".join(part.strip() for part in answer_parts if part.strip())

            item['question'] = question.strip() if question else None
            item['answer'] = answer
            item['category'] = category_name.strip() if category_name else 'General'
            
            # These fields don't exist per item, so we can leave them blank or set a default
            item['tags'] = [category_name.strip()] if category_name else []
            item['date_posted'] = None
            item['date_updated'] = None

            yield item

        # Find the 'Next' button to go to the next page of the current category
        next_page = response.css('ul.pagination a.pagenav[title="Next"]::attr(href)').get()
        if next_page:
            # If a 'Next' page exists, follow it and call this same method again
            yield response.follow(next_page, callback=self.parse_category)