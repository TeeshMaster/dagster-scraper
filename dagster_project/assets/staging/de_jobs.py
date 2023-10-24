import pandas as pd
from bs4 import BeautifulSoup
import requests
import googlemaps

from dagster import asset, EnvVar 

from datetime import datetime
import logging


def geocoder(geocode_search):

    try:
        geolocator = googlemaps.Client(key=EnvVar("GOOGLE_GEO_API_KEY"))
        locator = geolocator.geocode(geocode_search)
        coordinates = locator[0]['geometry']['location']
        return {'latitude' : coordinates['lat'], 'longitude' : coordinates['lng'] }

    except ValueError as error_message:
        logging.error("Error: geocode failed on input {} with message {}".format(geocode_search, error_message))
        return False

@asset(io_manager_key="snowflake_io_manager", compute_kind="pandas")
def data_engineer_jobs_stg() -> pd.DataFrame:
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    headers = {'user-agent':agent}

    search_job_title='data engineer'
    search_job_location='melbourne'

    all_rows = []
    page_count = 1
    while True:
        try:
            print('page:', page_count)
            url = ('https://www.seek.com.au/{}-jobs/in-{}?page={}').format(search_job_title, search_job_location, page_count)
            response = requests.get(url, headers=headers)
            html_soup = BeautifulSoup(response.text, 'html.parser')
            jobs = html_soup.find_all("article", {"data-automation": "normalJob"})
            if len(jobs) < 1:
                logging.info(f'{len(all_rows)} {search_job_title} jobs found')
                break
            
            for soup in jobs:
            
                published_date = soup.find("span", {"data-automation": "jobListingDate"}).text.strip()
                job_title = soup.find("a", {"data-automation": "jobTitle"}).text.strip()
                company_name = soup.find("a", {"data-automation": "jobCompany"})
                if company_name != None:
                    company_name = soup.find("a", {"data-automation": "jobCompany"}).text.strip()

                location = soup.find("a", {"data-automation": "jobLocation"}).text.strip()
                salary = soup.find("span", {"data-automation": "jobSalary"})
                if salary != None:
                    salary = soup.find("span", {"data-automation": "jobSalary"}).text.strip()
                    
                category = soup.find("a", {"data-automation": "jobClassification"}).text.strip()
                short_description = soup.find("span", {"data-automation": "jobShortDescription"}).text.strip()
                featured = soup.find("a", {"data-automation": "jobPremium"})

                geo_search = str(company_name) + " " + str(location) + ", Australia"
                geocode_result = geocoder(geo_search)

                if geocode_result:
                    latitude = geocode_result['latitude']
                    longitude = geocode_result['longitude']
                else:
                    latitude = None
                    longitude = None

                job_url = 'https://www.seek.com.au/' + soup.find("a", {"data-automation": "jobTitle"})["href"]
                run_datetime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                row = [run_datetime, published_date, job_title, company_name, location, salary, category, short_description, featured, latitude, longitude, job_url, search_job_title, search_job_location]
                all_rows.append(row)
            page_count = page_count + 1
        except Exception as e:
            logging.error(f'An error occured while scraping jobs: {e}')
            break

    df = pd.DataFrame(all_rows, columns = ['run_datetime', 'published_date', 'job_title', 'company_name', 'location', 'salary', 'category', 'short_description', 'featured', 'latitude', 'longitude', 'job_url', 'search_job_title', 'search_job_location'])
    return df
    
    