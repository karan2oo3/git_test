from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Function to scrape data
def scrape_card_data():
    # Your scraping logic
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get("https://nattobot.com/inventory/724868037706252379#cards")

    scraped_data = []
    # Add scraping logic here

    driver.quit()
    return scraped_data

# Flask route to scrape data and update Google Sheets
@app.route("/scrape-and-update", methods=["GET"])
def scrape_and_update():
    data = scrape_card_data()

    # Authenticate with Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    # Open Google Sheet
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/12emjQPQGtP74aDjAikeP7Y1-dF4vIHw5ag5bYIxoACA/edit").sheet1
    sheet.clear()
    sheet.update("A1", [["Name", "Element", "Total Cards"]] + data)

    return jsonify({"message": "Data updated successfully!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
