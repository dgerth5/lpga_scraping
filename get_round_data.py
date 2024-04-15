# needs url from get_results_url

def get_round_data(url):

  # URL from which to fetch data
  url = url

  # Make the HTTP request to get the page content
  response = requests.get(url)
  response.raise_for_status()  # This will raise an error if the request failed

  # Parse the HTML
  soup = BeautifulSoup(response.text, 'html.parser')

  # Find the table
  table = soup.find('table', class_='table')

  # Extract rows from the table body
  rows = table.find('tbody').find_all('tr')

  # Data storage for table
  data = []

  # Process each row in the table
  for row in rows:
      cols = row.find_all('td')
      date = cols[0].text.strip() if len(cols) > 0 else None
      event = cols[1].text.strip() if len(cols) > 1 else None
      r1 = cols[2].text.split()[0].strip() if len(cols) > 2 else None
      r2 = cols[3].text.split()[0].strip() if len(cols) > 3 else None
      r3 = cols[4].text.split()[0].strip() if len(cols) > 4 else None
      r4 = cols[5].text.split()[0].strip() if len(cols) > 5 else None

      data.append({
          'Date': date,
          'Event': event,
          'R1': r1,
          'R2': r2,
          'R3': r3,
          'R4': r4
      })

  # Extract additional information: Player Name, Rookie Year, Age
  player_info_section = soup.find('div', class_='player-banner-info')
  player_name = player_info_section.find('div', class_='name').text.strip()
  rookie_year = player_info_section.find('div', class_='player-banner-box-item-rookieyear').find_next_sibling('div').text.strip()
  age = player_info_section.find('div', class_='player-banner-box-item-height').find_next_sibling('div').text.strip()

  # Adding extracted details to each row of data
  for d in data:
      d.update({
          'Player_Name': player_name,
          'Rookie_Year': rookie_year,
          'Age': age
      })

  # Create DataFrame
  df = pd.DataFrame(data)

  # Specify the order of columns
  column_order = ['Player_Name', 'Rookie_Year', 'Age', 'Date', 'Event', 'R1', 'R2', 'R3', 'R4']
  df = df[column_order]

  return df

