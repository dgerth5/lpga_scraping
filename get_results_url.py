import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_urls(year):

  url = f"https://www.lpga.com/statistics/scoring/scoring-average?year={year}"

  # Make the HTTP request to get the page content
  response = requests.get(url)
  response.raise_for_status()  # Ensure the request was successful

  # Parse the HTML
  soup = BeautifulSoup(response.text, 'html.parser')

  # Find all <a> tags within the table
  a_tags = soup.find('div', class_='table-wrapper').find_all('a')

  # Extract href and text from each <a> tag
  links = [{'href': a.get('href'), 'text': a.text.strip()} for a in a_tags]

  df = pd.DataFrame(links)
  df.columns = ['Link', 'Name']

  # add in results link
  df["results"] = "https://www.lpga.com" + df["Link"].str[:-8] + f"/results?filters={year}&archive="

  return df
