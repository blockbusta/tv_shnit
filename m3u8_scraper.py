import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Links to process
links = [
    "https://example1.com",
    "https://example2.com",
    "https://example3.com",
]

# Chrome options to avoid bot detection
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# Enable network logs
capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

# Path to ChromeDriver
driver_path = "/path/to/chromedriver"  # Update this with your ChromeDriver path
service = Service(driver_path)

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options, desired_capabilities=capabilities)

def get_m3u8_link(url):
    try:
        driver.get(url)
        time.sleep(5)  # Allow the page to load fully
        
        # Retrieve browser logs
        logs = driver.get_log("performance")
        
        m3u8_links = []
        for entry in logs:
            message = entry["message"]
            if "m3u8" in message:
                m3u8_links.append(message)
        
        # Extract only URLs
        return [line.split('"url":"')[1].split('"')[0] for line in m3u8_links if "url" in line]
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return []
    finally:
        # Slow down between requests to avoid detection
        time.sleep(10)

# Process each link
for link in links:
    print(f"Processing: {link}")
    m3u8_links = get_m3u8_link(link)
    if m3u8_links:
        print(f"Found m3u8 links for {link}:")
        for m3u8 in m3u8_links:
            print(m3u8)
    else:
        print(f"No m3u8 links found for {link}.")

# Clean up
driver.quit()
