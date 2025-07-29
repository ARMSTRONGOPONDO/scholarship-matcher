import scrapy
import re
from googleapiclient.discovery import build
from google.oauth2 import service_account
from GovChatbotFAQ.items import GovChatbotFAQItem

class SlideExtractorSpider(scrapy.Spider):
    name = 'slide_extractor'
    presentation_id = '1mY68zOIQBUHkht2wiKgzkIQpPuxh1Oihj2rn4AlMcDM'

    async def start(self):
        SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']
        SERVICE_ACCOUNT_FILE = self.settings.get('GOOGLE_SERVICE_ACCOUNT_FILE')
        
        if not SERVICE_ACCOUNT_FILE:
            self.logger.error("GOOGLE_SERVICE_ACCOUNT_FILE setting missing")
            return

        try:
            creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        except Exception as e:
            self.logger.error(f"Credential error: {e}")
            return

        slides_service = build('slides', 'v1', credentials=creds)
        
        try:
            presentation = slides_service.presentations().get(
                presentationId=self.presentation_id
            ).execute()
        except Exception as e:
            self.logger.error(f"API error: {e}")
            return

        slides = presentation.get('slides', [])
        
        for slide in slides:
            # Collect all text elements with their position
            text_elements = []
            for element in slide.get('pageElements', []):
                if 'shape' in element and 'text' in element['shape']:
                    text = ''.join([
                        te.get('textRun', {}).get('content', '')
                        for te in element['shape']['text'].get('textElements', [])
                    ]).strip()
                    
                    if text:
                        # Get element vertical position
                        transform = element.get('transform', {})
                        translateY = transform.get('translateY', 0)
                        text_elements.append({
                            'text': text,
                            'translateY': translateY,
                            'is_title': self.is_title_element(element)
                        })
            
            # Sort text elements by vertical position (top to bottom)
            text_elements.sort(key=lambda x: x['translateY'])
            
            # Identify question from the first title-like element
            title = next((t['text'] for t in text_elements if t['is_title']), None)
            
            # If no title found, use the first non-trivial text element
            if not title and text_elements:
                title = next(
                    (t['text'] for t in text_elements if len(t['text'].split()) > 1),
                    text_elements[0]['text'] if text_elements else "Untitled"
                )
            
            # Clean and format the title
            title = self.clean_title(title)
            
            # Build answer from remaining text elements
            description = self.build_description(text_elements, title)
            
            # Find image if exists
            image_url = next((
                e['image']['contentUrl'] for e in slide.get('pageElements', [])
                if 'image' in e and 'contentUrl' in e.get('image', {})
            ), None)

            if title or description or image_url:
                item = GovChatbotFAQItem()
                item['question'] = title
                item['answer'] = description
                item['category'] = 'Google Slide Presentation'
                item['tags'] = ['google', 'slide', 'extracted']
                item['image'] = image_url
                yield item

    def is_title_element(self, element):
        """Improved title detection heuristic"""
        try:
            text_style = element['shape']['text']['textElements'][0].get('textRun', {}).get('style', {})
            font_size = text_style.get('fontSize', {}).get('magnitude', 12)
            is_bold = text_style.get('bold', False)
            return is_bold and font_size >= 18
        except (KeyError, IndexError):
            return False
            
    def clean_title(self, title):
        """Clean and format title text"""
        if not title:
            return "Untitled"
            
        # Remove redundant prefixes/suffixes
        title = re.sub(r'^[0-9]+[\.\)\s]*', '', title)  # Remove numbering
        title = re.sub(r'[\:\-\—]+$', '', title)  # Remove trailing punctuation
        title = title.strip()
        
        # Capitalize first letter
        if title and title[0].islower():
            title = title[0].upper() + title[1:]
            
        return title or "Untitled"
    
    def build_description(self, text_elements, title):
        """Build well-formatted description from text elements"""
        # Exclude title and other short text elements
        description_parts = []
        for t in text_elements:
            text = t['text'].strip()
            # Skip if this is the title or very short text
            if text == title or len(text.split()) < 2:
                continue
            description_parts.append(text)
        
        if not description_parts:
            return "No description available"
            
        # Join with proper punctuation
        description = ". ".join(description_parts)
        
        # Ensure it ends with a period
        if not description.endswith('.'):
            description += '.'
            
        # Remove duplicate spaces and line breaks
        description = re.sub(r'\s+', ' ', description)
        
        return description