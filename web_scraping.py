import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL to scrape
URL = "https://en.wikipedia.org/wiki/List_of_helicopter_prison_escapes"

# Headers to make the request look like it's coming from a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Safari/537.36"
}

def fetch_page(url):
    try:
        print("Fetching page...")
        session = requests.Session()
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        print("Page fetched successfully!")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def parse_table(html_content):
    try:
        print("Parsing the table...")
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', {'class': 'wikitable'})
        if not table:
            print("Table not found on the page.")
            return None, None
        
        data = []
        headers = [th.get_text(strip=True) for th in table.find_all('th')]
        print(f"Found headers: {headers}")
        
        for row in table.find_all('tr')[1:]:
            cells = row.find_all(['td', 'th'])
            if len(cells) != len(headers):
                print("Skipping row due to mismatch in columns.")
                continue
            row_data = [cell.get_text(strip=True) for cell in cells]
            data.append(row_data)
        
        print(f"Parsed {len(data)} rows.")
        return headers, data
    except Exception as e:
        print(f"Error parsing the table: {e}")
        return None, None

def save_to_csv(headers, data, filename="helicopter_prison_escapes.csv"):
    try:
        print("Saving data to CSV...")
        df = pd.DataFrame(data, columns=headers)
        df.to_csv(filename, index=False)
        print(f"Data successfully saved to {filename}")
        return df
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return None

def main():
    print("Starting script...")

    # Check internet connection with headers
    try:
        test_response = requests.get("https://www.wikipedia.org", headers=HEADERS, timeout=5)
        test_response.raise_for_status()
        print("Internet connection is working!")
    except Exception as e:
        print(f"Internet connection failed: {e}")
        return

    html_content = fetch_page(URL)
    if html_content:
        headers, data = parse_table(html_content)
        if headers and data:
            df = save_to_csv(headers, data)
            if df is not None:
                print("\nHere is the scraped data:\n")
                print(df)
        else:
            print("No data found to save.")
    else:
        print("Failed to fetch page content.")
    print("Script finished.")

if __name__ == "__main__":
    main()
