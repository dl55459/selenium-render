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

# Define all functions FIRST
def safe_click(element, max_retries=2):
    for attempt in range(max_retries):
        try:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
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
            lat, lon = coords_part.split(",")
            return float(lat), float(lon)
        return None, None
    except Exception as e:
        print(f"Coordinate error: {str(e)}")
        return None, None

def generate_filename(parent, child):
    clean_parent = parent.replace(" ", "_").replace("/", "_").lower()
    clean_child = child.replace(" ", "_").replace("/", "_").lower()
    return f"{clean_parent}_{clean_child}.csv"

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


# Correct paths for Render
FIREFOX_BIN = os.path.expandvars("$FIREFOX_BIN")
GECKODRIVER_PATH = os.path.expandvars("$GECKODRIVER_PATH")

# Firefox configuration - ADD ERROR HANDLING
try:
    from selenium.webdriver.firefox.service import Service
    service = Service(
        executable_path=GECKODRIVER_PATH,
        log_path=os.devnull
    )
    
    options = Options()
    options.binary_location = FIREFOX_BIN
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=800,600")

    # Before driver initialization
    print("\nSystem verification:")
    print("Current directory:", os.getcwd())
    print("Geckodriver path:", GECKODRIVER_PATH)
    print("Firefox path:", FIREFOX_BIN)
    print("Geckodriver exists:", os.path.exists(GECKODRIVER_PATH))
    print("Firefox exists:", os.path.exists(FIREFOX_BIN))

    # If paths are wrong, show alternatives
    if not os.path.exists(GECKODRIVER_PATH):
        print("Searching for geckodriver...")
        os.system("find / -name geckodriver 2>/dev/null")

    if not os.path.exists(FIREFOX_BIN):
        print("Searching for Firefox...")
        os.system("find / -name firefox* 2>/dev/null")
        
    driver = webdriver.Firefox(
        service=service,
        options=options
    )
    print("Driver capabilities:", driver.capabilities)
    print("Firefox version:", driver.capabilities['browserVersion'])
    print("Geckodriver version:", driver.capabilities['moz:geckodriverVersion'])
    
except Exception as e:
    print(f"DRIVER INIT ERROR: {str(e)}")
    print("Potential solutions:")
    print("1. Verify geckodriver exists:", os.path.exists(GECKODRIVER_PATH))
    print("2. Verify Firefox exists:", os.path.exists(FIREFOX_BIN))
    sys.exit(1)
    
# Add after driver initialization
print("\nSystem verification:")
print("Geckodriver exists:", os.path.exists(GECKODRIVER_PATH))
print("Firefox exists:", os.path.exists(FIREFOX_BIN))
print("Current PATH:", os.environ["PATH"])

# Test basic navigation
try:
    service = Service(
        executable_path=GECKODRIVER_PATH,
        log_path=os.devnull
    )
    driver = webdriver.Firefox(
        service=service,
        options=options
    )
    print("\nDriver initialized successfully!")
    print("Browser version:", driver.capabilities['browserVersion'])
    
    # Rest of your scraping code...
    
except Exception as e:
    print(f"\nDRIVER INIT ERROR: {str(e)}")
    sys.exit(1)
    
    # Main scraping logic
    driver.get("https://www.google.com/maps/d/viewer?mid=1UUfwmW5YntQiVznItYrXwHYn1D9eGkgU&femb=1&ll=5.008162640544454%2C-68.52131693613987&z=1")

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
                time.sleep(3.75)  # Allow content to load
                
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
                            time.sleep(3.75)  # Allow pins to load
                            
                            # Process pins
                            for idx in range(1, sub_data['pins'] + 1):
                                try:
                                    # Click pin
                                    loc_xpath = f"{sub_data['location_base']}[{idx}]"
                                    location = wait.until(EC.element_to_be_clickable(
                                        (By.XPATH, loc_xpath)
                                    ))
                                    
                                    if safe_click(location):
                                        time.sleep(2.25)  # Wait for details panel
                                        
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
                                            time.sleep(3)
                                            
                                            # Extract coordinates
                                            current_url = driver.current_url
                                            lat, lon = extract_coordinates(current_url)
                                            
                                            # Close tab and return
                                            driver.close()
                                            driver.switch_to.window(driver.window_handles[0])
                                            time.sleep(1.5)
                                            
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
                                            time.sleep(1.5)
                                            
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
    print(f"Error: {str(e)}")
    sys.exit(1)

finally:
    if 'driver' in locals():
        driver.quit()
    print("Process completed")
