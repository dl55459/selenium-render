from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv
import os

# Configure Chrome options
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.binary_location = "/usr/bin/google-chrome-stable"

# Initialize Chrome driver with Service
service = Service(executable_path="/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=options)

# Open the Google My Maps link
url = "https://www.google.com/maps/d/viewer?mid=1UUfwmW5YntQiVznItYrXwHYn1D9eGkgU&femb=1&ll=5.008162640544454%2C-68.52131693613987&z=1"
driver.get(url)

# Wait for the map to load
wait = WebDriverWait(driver, 20)

# Define all XPaths at the beginning for better visibility
xpaths = {
    # Parent folders and their subfolders
    "parent_folders": {
        "Ghost Towns": {
            "closed": '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[2]/div/div',
            "subfolders": {
                "Archaeological Site": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[3]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[3]/div[2]/div',
                    'pins': 95
                },
                "Dammed": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[4]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[4]/div[2]/div',
                    'pins': 60
                },
                "Abandoned Due to Disaster": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[5]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[5]/div[2]/div',
                    'pins': 29
                },
                "Unbuilt Developments": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[6]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[6]/div[2]/div',
                    'pins': 16
                },
                "Ghost Towns": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[7]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[7]/div[2]/div',
                    'pins': 1196
                }
            }
        },
        "Abandoned/Historic Places": {
            "closed": '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[2]/div/div',
            "subfolders": {
                "Abandoned Buildings": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[3]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[3]/div[2]/div',
                    'pins': 88
                },
                "Abandoned Military Property": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[4]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[4]/div[2]/div',
                    'pins': 75
                },
                "Historical Marker": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[5]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[5]/div[2]/div',
                    'pins': 64
                },
                "Abandoned Mine": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[6]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[6]/div[2]/div',
                    'pins': 54
                },
                "Abandoned Place": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[7]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[7]/div[2]/div',
                    'pins': 50
                },
                "Theme Park": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[8]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[8]/div[2]/div',
                    'pins': 41
                },
                "Abandoned Industrial Plant": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[9]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[9]/div[2]/div',
                    'pins': 35
                },
                "Memorial": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[10]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[10]/div[2]/div',
                    'pins': 28
                },
                "Abandoned Bridge": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[11]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[11]/div[2]/div',
                    'pins': 22
                },
                "Historical Site": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[12]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[12]/div[2]/div',
                    'pins': 17
                },
                "Abandoned Power Plant": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[13]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[13]/div[2]/div',
                    'pins': 11
                },
                "Abandoned Mine2": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[14]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[14]/div[2]/div',
                    'pins': 2
                },
                "Abandoned Bridge (Demolished)": {
                    'xpath': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[15]/div[1]/div/div[2]/div',
                    'location_base': '//*[@id="legendPanel"]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[15]/div[2]/div',
                    'pins': 1
                }
            }
        }
    },
    # Name and description in the details panel
    "name": '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div[1]/div[2]',
    "description": '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div[2]/div[2]',

    # Navigation button in the details panel
    "navigation_button": '//*[@id="featurecardPanel"]/div/div/div[3]/div[3]/div',

    # Back button to return to the main side panel
    "back_button": '//*[@id="featurecardPanel"]/div/div/div[3]/div[1]/div'
}

def safe_click(element, max_retries=3):
    for attempt in range(max_retries):
        try:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(1)
            element.click()
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error clicking element - {str(e)}")
            time.sleep(2)
    print("Max retries reached. Skipping this element.")
    return False

def extract_coordinates(url):
    try:
        if "dir//" in url:
            coords_part = url.split("dir//")[1].split("&")[0]
            lat, lon = coords_part.split(",")
            return float(lat), float(lon)
        return None, None
    except Exception as e:
        print(f"Coordinate extraction error: {str(e)}")
        return None, None

def generate_filename(parent_folder, child_folder):
    parent = parent_folder.replace(" ", "_").replace("/", "_").lower()
    child = child_folder.replace(" ", "_").replace("/", "_").lower()
    return f"{parent}_{child}.csv"

def switch_to_new_tab(timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            return True
        time.sleep(0.5)
    return False

try:
    for folder_name, folder_data in xpaths["parent_folders"].items():
        print(f"Processing parent folder: {folder_name}")
        closed_folder = wait.until(EC.element_to_be_clickable((By.XPATH, folder_data["closed"])))
        safe_click(closed_folder)
        time.sleep(1)

        for subfolder_name, subfolder_data in folder_data["subfolders"].items():
            try:
                print(f"Processing subfolder: {subfolder_name}")
                subfolder = wait.until(EC.element_to_be_clickable((By.XPATH, subfolder_data['xpath'])))
                safe_click(subfolder)
                time.sleep(1)

                pins = []
                for index in range(1, subfolder_data['pins'] + 1):
                    try:
                        location_xpath = f'{subfolder_data["location_base"]}[{index}]'
                        location = wait.until(EC.element_to_be_clickable((By.XPATH, location_xpath)))
                        
                        if not safe_click(location):
                            continue
                        
                        time.sleep(1)
                        name = driver.find_element(By.XPATH, xpaths["name"]).text
                        description = driver.find_element(By.XPATH, xpaths["description"]).text

                        nav_button = driver.find_element(By.XPATH, xpaths["navigation_button"])
                        safe_click(nav_button)

                        if switch_to_new_tab():
                            current_url = driver.current_url
                            lat, lon = extract_coordinates(current_url)
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                        else:
                            lat, lon = None, None

                        pins.append({
                            "Name": name,
                            "Description": description,
                            "Type": subfolder_name,
                            "Latitude": lat,
                            "Longitude": lon,
                            "Index": index
                        })

                        back_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["back_button"])))
                        safe_click(back_button)
                        time.sleep(1)

                    except Exception as e:
                        print(f"Error processing pin {index}: {str(e)}")

                filename = generate_filename(folder_name, subfolder_name)
                with open(filename, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=["Name", "Description", "Type", "Latitude", "Longitude", "Index"])
                    writer.writeheader()
                    writer.writerows(pins)

                print(f"Saved {len(pins)} entries to {filename}")
                
            except Exception as e:
                print(f"Subfolder error: {str(e)}")

except Exception as e:
    print(f"Main error: {str(e)}")
finally:
    driver.quit()
    print("Browser closed")
