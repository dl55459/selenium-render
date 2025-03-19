from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time
import csv
import os
import sys

# Configure Firefox options
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)

# Initialize WebDriver with enhanced settings
try:
    service = Service(
        executable_path="/usr/local/bin/geckodriver",
        service_args=["--marionette-port", "2828"]
    )
    
    driver = webdriver.Firefox(
        service=service,
        options=options,
        service_log_path=os.path.devnull  # Disable geckodriver logs
    )
    wait = WebDriverWait(driver, 30)  # Increased timeout for cloud environment
except Exception as e:
    print(f"WebDriver initialization failed: {str(e)}")
    sys.exit(1)

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
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'});",
                element
            )
            time.sleep(1)
            element.click()
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error clicking - {str(e)}")
            time.sleep(2)
    return False

def extract_coordinates(url):
    try:
        if "dir//" in url:
            coords_part = url.split("dir//")[1].split("&")[0]
            return tuple(map(float, coords_part.split(",")))
        return (None, None)
    except Exception as e:
        print(f"Coordinate error: {str(e)}")
        return (None, None)

def generate_filename(parent, child):
    clean = lambda s: s.replace(" ", "_").replace("/", "_").lower()[:50]
    return f"{clean(parent)}_{clean(child)}.csv"

try:
    # Navigate to target URL
    driver.get("https://www.google.com/maps/d/viewer?mid=1UUfwmW5YntQiVznItYrXwHYn1D9eGkgU&femb=1&ll=5.008162640544454%2C-68.52131693613987&z=1")
    print("Loaded initial map page")

    # Process parent folders
    for folder_name, folder_data in xpaths["parent_folders"].items():
        print(f"\n=== Processing folder: {folder_name} ===")
        
        try:
            # Open parent folder
            closed_folder = wait.until(EC.element_to_be_clickable(
                (By.XPATH, folder_data["closed"])
            ))
            if safe_click(closed_folder):
                print(f"Successfully opened {folder_name}")
                time.sleep(2.5)  # Allow content to load
                
                # Process subfolders
                for sub_name, sub_data in folder_data["subfolders"].items():
                    print(f"\n  -> Subfolder: {sub_name}")
                    pins = []
                    
                    try:
                        # Open subfolder
                        sub_element = wait.until(EC.element_to_be_clickable(
                            (By.XPATH, sub_data['xpath'])
                        ))
                        if safe_click(sub_element):
                            time.sleep(2.5)  # Allow pins to load
                            
                            # Process pins
                            for idx in range(1, sub_data['pins'] + 1):
                                try:
                                    # Click pin
                                    loc_xpath = f"{sub_data['location_base']}[{idx}]"
                                    location = wait.until(EC.element_to_be_clickable(
                                        (By.XPATH, loc_xpath)
                                    ))
                                    
                                    if safe_click(location):
                                        time.sleep(1.5)  # Wait for details panel
                                        
                                        # Extract details
                                        name = wait.until(EC.visibility_of_element_located(
                                            (By.XPATH, xpaths["name"])
                                        )).text
                                        desc = wait.until(EC.visibility_of_element_located(
                                            (By.XPATH, xpaths["description"])
                                        )).text
                                        
                                        # Get coordinates
                                        nav_btn = wait.until(EC.element_to_be_clickable(
                                            (By.XPATH, xpaths["navigation_button"])
                                        ))
                                        if safe_click(nav_btn):
                                            # Switch to new tab
                                            driver.switch_to.window(driver.window_handles[1])
                                            time.sleep(2)
                                            
                                            # Extract coordinates
                                            current_url = driver.current_url
                                            lat, lon = extract_coordinates(current_url)
                                            
                                            # Close tab and return
                                            driver.close()
                                            driver.switch_to.window(driver.window_handles[0])
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
                                            
                                            # Return to list view
                                            back_btn = wait.until(EC.element_to_be_clickable(
                                                (By.XPATH, xpaths["back_button"])
                                            ))
                                            safe_click(back_btn)
                                            time.sleep(1)
                                            
                                except Exception as e:
                                    print(f"  Error processing pin {idx}: {str(e)}")
                                    continue
                                    
                            # Save subfolder data
                            if pins:
                                filename = generate_filename(folder_name, sub_name)
                                with open(filename, "w", newline="", encoding="utf-8") as f:
                                    writer = csv.DictWriter(f, fieldnames=pins[0].keys())
                                    writer.writeheader()
                                    writer.writerows(pins)
                                print(f"  Saved {len(pins)} entries to {filename}")
                                
                    except Exception as e:
                        print(f"  Subfolder error: {str(e)}")
                        continue
                        
        except Exception as e:
            print(f"Folder error: {str(e)}")
            continue

except Exception as e:
    print(f"\nCritical error: {str(e)}")
    driver.save_screenshot("error_screenshot.png")

finally:
    driver.quit()
    print("\nBrowser closed. Script execution completed.")
