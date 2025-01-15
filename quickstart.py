from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Embedded service account credentials
service_account_credentials = {
    "type": "service_account",
    "project_id": "card-fetcher-447813",
    "private_key_id": "82576e61135f877e4aa02679918bc89cbab5edfe",
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDFHutzfUyrEik9
JCNZzgRbNcRjhPCqqJSt1WpOU2jHZd2FvHZcjNvncX5WpoaGsdr9YqwmZlkqCV8x
TVj0ZJOqGLP4FzWaQfEp/YtbR7zmG4ToWyIewwmU1IMhGWz/zrjVxliY5HaLbfsv
WmA5HtYpLAft8aadkxkFyMD2bCoN3w6ScS8Jd2F6Lh6oOQj2rEpcq3onegOHyhf6
+0a9s06CYnEU1A0M3qJO5Nt3GAZPn5hN51hBUhYee+UUz7IkOet2vWg2KJ7IDFC0
ceWeyIxx8v2Dsy+Eb15mMs4rF5s9xkHYchQMY6x6WnL1nIZ89OTSYc4G4o4bBl8t
pLhaE447AgMBAAECggEAGyDvv5O5hvu3YDpGgTgIwnLKZfXoV1xfJfNur3vsOjEL
RToUQhWCuD4W6J7/ea8ll+TKE3jXgaELkFH4UZ478ld3AUhUcLftlF1YHgZn+XVF
G+Na9UfbXDfJGjeRGD2fk5A6JkSfCf5naPNztbjIOZ9dMgKlbx9M/M5NvDxTp1fT
F/3oiofOIuXr9EgoIUWNVdltRCHIQ4GwLgOZFwYN6YC3G+8M3hAfv6nxrr6mY0pB
pWDyIhxWCFHqrK97xDC+RUrkErrG1HHEavpAKp6HyDh8v/CGUONkpfXBM03kjenT
7ZnK0Wb7iUGBTP1VbrLC9W0hr+YYX843TUAmtOPXVQKBgQDrQ2bU8sWbycKCLS6c
82OyjqHHlh/dV6DihkpMFRDWP0nN4KoUPfvC5J4mP4uXkx+Jrn3SCy8YNHg97LGs
+fNtIY1EnNsQ3/vXxo3iVVs2DHSOvXk5CMHmoEX0x64/YqGyr3WV5t1sT7JiOHVg
gKgROKq82FzfVLuDKQ5NOibhzwKBgQDWftn45JpWXY4AWrzeNrGxJ1K83n7hMfbz
lmNgkHLChkLIc8BdVlu37SFcOyhviGKRrVh63vH0zHu2he6/7ydF+jdS4aQig2po
XGF2HR2gdGMksmhGy44z+G92g8BUA34VYpVPEWRyxEOLqmNSi73038aeJRAKtbM0
0J6mlffD1QKBgGk0o/iYdAvdprDF+bFQGgZQSEJTfP5jYFvMR89MIFJezOdXD1er
/DjEOYDLK+ZlcVYFhNh4DeBaHmc6wJ2kzNnBhkXniwM51opAjVRobTh3S2xFiL8b
jnJOu9nhradEuSCJ3CBjtCLqZNANhVfZUM8asydt7eIlJxFZO78HQTn7AoGBAIop
b3HYnmlfHaawy9M+27pGoA60KnoX2wAQMLb0lFckcEP5+0Cj7bRNdB2apXMiIIvB
YqrSjHuoc0+geab7/woeICCs4zKv/4x1ZPnVy02dancqy+w+Fbz4G6P1PZ9gGIjh
1Vb21wLt1KxT9mInTRY8Rg17xhd/7ozojCi1lMB5AoGAFUCWEaqDLvRaAboqFvm4
am9dxGMyv51R39xOQrT6nCyU4qnkmGEawUWSQapj6rTr3LbDEoIKPMe2Z6ulxJV+
gB2G3CLWbtLC15wOT0hFrq2xs5NdmQ0w7JRlfwit/Z7ilk3lBw+LiquR1QjOo+OW
jsLESLVUeP+QYKOGEgCQZ7k=
-----END PRIVATE KEY-----""",
    "client_email": "card-fetching-person@card-fetcher-447813.iam.gserviceaccount.com",
    "client_id": "102641126073155786750",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/card-fetching-person%40card-fetcher-447813.iam.gserviceaccount.com"
}

# Step 1: Web Scraping with Total Card Count
# (Your scrape_card_data function here remains unchanged)
def scrape_card_data():
    # Configure Selenium WebDriver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://nattobot.com/inventory/724868037706252379#cards")

    # Extract card data
    cards = driver.find_elements(By.CSS_SELECTOR, "div.card[data-type][data-element]")
    scraped_data = []

    for card in cards:
        try:
            # Get card name
            card_name_element = card.find_element(By.TAG_NAME, "h4")
            card_name = card_name_element.text.strip() if card_name_element else ""

            # Skip cards without a name
            if not card_name:
                continue

            # Get card element
            element_img = card.find_element(By.CSS_SELECTOR, "img.cardelement")
            element_src = element_img.get_attribute("src")
            element_name = element_src.split('/')[-1].split('.')[0] if element_src else ""

            # Skip cards without an element
            if not element_name:
                continue

            # Calculate total number of cards
            # Extract advancement stars
            try:
                stars_img = card.find_element(By.CSS_SELECTOR, "img.advancementstarsbottom")
                stars_src = stars_img.get_attribute("src")
                stars_count = int(stars_src.split('_')[1].split('.')[0]) if stars_src else 0
            except Exception:
                stars_count = 0

            # Extract extra amount
            try:
                extra_amount_div = card.find_element(By.CLASS_NAME, "card_topleft")
                extra_amount_text = extra_amount_div.text.strip()
                extra_amount = int(extra_amount_text.split(":")[1].strip()) if extra_amount_text else 0
            except Exception:
                extra_amount = 0

            # Calculate total amount
            total_amount = stars_count + extra_amount +1

            # Append the card data
            scraped_data.append([card_name, element_name, total_amount])
        except Exception as e:
            print(f"Error processing card: {e}")
            continue

    driver.quit()
    return scraped_data
# Step 2: Update Google Sheets
def update_google_sheet(data):
    # Authenticate with embedded credentials
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_credentials, ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)

    # Open the spreadsheet
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/12emjQPQGtP74aDjAikeP7Y1-dF4vIHw5ag5bYIxoACA/edit?usp=sharing").sheet1

    # Insert data into the spreadsheet
    sheet.clear()  # Clear existing data
    sheet.update("A1", [["Name", "Element", "Total Cards"]] + data)  # Add headers and data

    print("Data added successfully!")

# Main Execution
if __name__ == "__main__":
    # Step 1: Scrape data
    scraped_data = scrape_card_data()

    # Step 2: Update the spreadsheet
    if scraped_data:
        update_google_sheet(scraped_data)
    else:
        print("No data was scraped from the website.")
