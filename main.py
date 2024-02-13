# import functions_framework
from indeed import IndeedScraper



# @functions_framework.http
# def indeed_scraper(request):
def indeed_crawler(event, context):
    # Create a CrawlerRunner with your project settings
    collection_name = 'nurse'
    # Create an instance of the scraper
    scraper = IndeedScraper(collection_name)
    # Run the scraper to save the scraped data into MongoDB
    scraper.run()
    print('Successfully scraped.....')



# Uncomment the following lines if running this code outside of a Cloud Function environment
if __name__ == "__main__":
    indeed_crawler('','')
