from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
import csv
import os

# Configure Firefox options
options = Options()
options.add_argument("-headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

print("Firefox version:", os.popen('firefox --version').read())
print("Geckodriver version:", os.popen('geckodriver --version').read())

# Configure service with error handling
try:
    service = Service(
        executable_path="/usr/local/bin/geckodriver",
        log_path=os.devnull  # Disable geckodriver logs
    )
    
    driver = webdriver.Firefox(
        service=service,
        options=options,
        service_log_path=os.devnull  # Disable additional logging
    )
except Exception as e:
    print(f"Failed to initialize WebDriver: {str(e)}")
    raise

print("WebDriver capabilities:", driver.capabilities)

# Open the Google My Maps link
url = "https://www.google.com/maps/d/viewer?mid=1UUfwmW5YntQiVznItYrXwHYn1D9eGkgU&femb=1&ll=5.008162640544454%2C-68.52131693613987&z=1"
driver.get(url)

# Define all XPaths
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
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(1)
            element.click()
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error clicking - {str(e)}")
            time.sleep(2)
    print("Max retries reached. Skipping element.")
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

def generate_filename(parent, child):
    clean_parent = parent.replace(" ", "_").replace("/", "_").lower()
    clean_child = child.replace(" ", "_").replace("/", "_").lower()
    return f"{clean_parent}_{clean_child}.csv"

try:
    for folder_name, folder_data in xpaths["parent_folders"].items():
        print(f"\nProcessing: {folder_name}")
        
        # Open parent folder
        closed_folder = wait.until(EC.element_to_be_clickable((By.XPATH, folder_data["closed"])))
        if safe_click(closed_folder):
            print(f"Opened: {folder_name}")
            time.sleep(2)

            for sub_name, sub_data in folder_data["subfolders"].items():
                print(f"\n>> Subfolder: {sub_name}")
                pins = []
                
                try:
                    sub_element = wait.until(EC.element_to_be_clickable((By.XPATH, sub_data['xpath'])))
                    if safe_click(sub_element):
                        time.sleep(2)
                        
                        for idx in range(1, sub_data['pins'] + 1):
                            try:
                                loc_xpath = f"{sub_data['location_base']}[{idx}]"
                                location = wait.until(EC.element_to_be_clickable((By.XPATH, loc_xpath)))
                                
                                if safe_click(location):
                                    time.sleep(1.5)
                                    
                                    # Get details
                                    name = driver.find_element(By.XPATH, xpaths["name"]).text
                                    desc = driver.find_element(By.XPATH, xpaths["description"]).text
                                    
                                    # Get coordinates
                                    nav_btn = driver.find_element(By.XPATH, xpaths["navigation_button"])
                                    if safe_click(nav_btn):
                                        main_window = driver.current_window_handle
                                        new_window = [w for w in driver.window_handles if w != main_window][0]
                                        driver.switch_to.window(new_window)
                                        time.sleep(2)
                                        
                                        current_url = driver.current_url
                                        lat, lon = extract_coordinates(current_url)
                                        
                                        driver.close()
                                        driver.switch_to.window(main_window)
                                        time.sleep(1)
                                        
                                        # Store data
                                        pins.append({
                                            "Name": name,
                                            "Description": desc,
                                            "Type": sub_name,
                                            "Latitude": lat,
                                            "Longitude": lon,
                                            "Index": idx
                                        })
                                        
                                        # Go back
                                        back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["back_button"])))
                                        safe_click(back_btn)
                                        time.sleep(1)
                                        
                            except Exception as e:
                                print(f"Error processing pin {idx}: {str(e)}")
                                continue
                                
                except Exception as e:
                    print(f"Subfolder error: {str(e)}")
                    continue
                
                # Save CSV
                if pins:
                    filename = generate_filename(folder_name, sub_name)
                    with open(filename, "w", newline="", encoding="utf-8") as f:
                        writer = csv.DictWriter(f, fieldnames=pins[0].keys())
                        writer.writeheader()
                        writer.writerows(pins)
                    print(f"Saved {len(pins)} entries to {filename}")

except Exception as e:
    print(f"Fatal error: {str(e)}")
    driver.save_screenshot("error_screenshot.png")

finally:
    driver.quit()
    print("\nBrowser closed. Script completed.")
