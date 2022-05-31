import os
import csv
import bs4
import requests
from logs import logger
from config import Config
# from scraping_manager.automate import Web_scraping

jobs_ids = []

def main (): 

    # Read categories, keywords and locations from json
    page = "Compu Trabajo"
    credentials = Config()
    keywords_categories = credentials.get("keywords")
    locations = credentials.get("locations")

    for keywords_category, keywords in keywords_categories.items():

        # Create and open csv / database file
        csv_path = os.path.join (os.path.dirname(__file__), f"{page}.csv")
        csv_file = open(csv_path, "a", encoding="utf-8", newline="")
        csv_writter = csv.writer(csv_file)

        # Search each keyword
        for keyword in keywords:

            # Search location
            for location in locations:

                logger.info (f"Scraping data {keyword} - {location}")

                # generate url with keyword and location
                location_formated = location.lower().replace(' ', '-')
                keyword_formated = keyword.lower().replace(' ', '-')
                url = f"https://www.computrabajo.com.mx/trabajo-de-{keyword_formated}-en-{location_formated}"
                
                # Get page data page
                res = requests.get (url)
                
                # Get jobs from current page

                # Generate css selectors for get data
                selector_article = "#p_ofertas article"
                selector_title = f"{selector_article} h1"
                selector_company = f"{selector_article} .fs16.fc_base.mt5.mb10"
                selector_details = f"{selector_article} .fc_aux.t_word_wrap.mb10.hide_m"
                selector_date = f"{selector_article} .fs13.fc_aux"

                # Get number of articles in the current page
                soup = bs4.BeautifulSoup (res.text, "html.parser")
                articles = soup.select (selector_article)
                
                # Get data from each article
                for article in articles:

                    # Skeip duplicated jobs
                    id = article.get ("id")
                    if id in jobs_ids:
                        continue
                    else:
                        jobs_ids.append (id)

                    # Get job data
                    title = article.select (selector_title)[0].getText()
                    company = article.select (selector_company)[0].getText()
                    details = article.select (selector_details)[0].getText()
                    date = article.select (selector_date)[0].getText().strip()
                    
                    # Clean data
                    title = title.strip().replace("\n", "").replace (",", "").replace ("\r\r", " ").replace ("\r", "")
                    company = company.strip().replace("\n", "").replace (",", "").replace ("\r\r", " ").replace ("\r", "")
                    details = details.strip().replace("\n", "").replace (",", "").replace ("\r\r", " ").replace ("\r", "")
                    date = date.strip().replace("\n", "").replace (",", "").replace ("\r\r", " ").replace ("\r", "")

                    # Add data to csv
                    row_data = [keywords_category, location, title, company, details, date]
                    csv_writter.writerow (row_data)

            # Debug lines
            break

        # Debug lines
        break


    # Close and save data in csv file
    csv_file.close ()




if __name__ == "__main__":

    main()