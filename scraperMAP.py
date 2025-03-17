from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Set Chrome options for headless mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")  

# Ensure ChromeDriver is correctly detected
chrome_options.binary_location = "/usr/bin/google-chrome"
chrome_driver_path = "/usr/local/bin/chromedriver"


# Start ChromeDriver service
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


# Open the Google My Maps link
url = "https://www.google.com/maps/d/viewer?mid=1UUfwmW5YntQiVznItYrXwHYn1D9eGkgU&femb=1&ll=5.008162640544454%2C-68.52131693613987&z=1"
driver.get(url)

# Wait for the map to load
wait = WebDriverWait(driver, 20)  # Increased timeout for slow loading

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
                # Add other subfolders here
            }
        },
        # Add other parent folders here
    },
    # Name and description in the details panel
    "name": '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div[1]/div[2]',
    "description": '//*[@id="featurecardPanel"]/div/div/div[4]/div[1]/div[2]/div[2]',

    # Navigation button in the details panel
    "navigation_button": '//*[@id="featurecardPanel"]/div/div/div[3]/div[3]/div',

    # Back button to return to the main side panel
    "back_button": '//*[@id="featurecardPanel"]/div/div/div[3]/div[1]/div'
}

# Function to safely click an element with retries
def safe_click(element, max_retries=3):
    for attempt in range(max_retries):
        try:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(1)  # Wait for the element to be in view
            element.click()
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error clicking element - {str(e)}")
            time.sleep(2)  # Wait before retrying
    print("Max retries reached. Skipping this element.")
    return False

# Function to extract coordinates from the URL
def extract_coordinates(url):
    try:
        if "dir//" in url:
            # Extract the part of the URL between "dir//" and "&"
            coords_part = url.split("dir//")[1].split("&")[0]
            lat, lon = coords_part.split(",")
            return float(lat), float(lon)
        else:
            return None, None
    except Exception as e:
        print(f"Error extracting coordinates from URL: {str(e)}")
        return None, None

# Function to generate a valid filename
def generate_filename(parent_folder, child_folder):
    # Replace spaces and special characters with underscores
    parent_folder = parent_folder.replace(" ", "_").replace("/", "_").lower()
    child_folder = child_folder.replace(" ", "_").replace("/", "_").lower()
    return f"{parent_folder}_{child_folder}.csv"

# Extract data from all parent folders and their subfolders
try:
    # Loop through each parent folder
    for folder_name, folder_data in xpaths["parent_folders"].items():
        print(f"Processing parent folder: {folder_name}")

        # Locate and expand the parent folder
        closed_folder = wait.until(EC.element_to_be_clickable((By.XPATH, folder_data["closed"])))
        safe_click(closed_folder)
        print(f"Expanded parent folder: {folder_name}")
        time.sleep(1)  # Wait for the folder to expand

        # Loop through each subfolder in the parent folder
        for subfolder_name, subfolder_data in folder_data["subfolders"].items():
            try:
                print(f"Processing subfolder: {subfolder_name}")

                # Locate and click the subfolder
                subfolder = wait.until(EC.element_to_be_clickable((By.XPATH, subfolder_data['xpath'])))
                safe_click(subfolder)
                print(f"Clicked subfolder: {subfolder_name}")
                time.sleep(1)  # Wait for the subfolder to load

                # Initialize a list to store pins for this subfolder
                pins = []

                # Loop through all location elements in the subfolder
                for index in range(1, subfolder_data['pins'] + 1):  # Loop from 1 to number of pins
                    try:
                        # Generate the XPath for the current location element
                        location_xpath = f'{subfolder_data["location_base"]}[{index}]'
                        print(f"Processing location {index} with XPath: {location_xpath}")

                        # Locate the location element
                        location = wait.until(EC.element_to_be_clickable((By.XPATH, location_xpath)))
                        if not safe_click(location):
                            print(f"Skipping location {index} due to click failure")
                            continue
                        print(f"Clicked location {index}")
                        time.sleep(1)  # Wait for the details panel to load

                        # Extract name and description
                        name = driver.find_element(By.XPATH, xpaths["name"]).text
                        description = driver.find_element(By.XPATH, xpaths["description"]).text

                        # Click the navigation button to get coordinates
                        nav_button = driver.find_element(By.XPATH, xpaths["navigation_button"])
                        safe_click(nav_button)
                        print("Clicked navigation button")

                        # Switch to the new tab
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(2)  # Wait for the tab to load

                        # Extract coordinates from the URL
                        current_url = driver.current_url
                        lat, lon = extract_coordinates(current_url)

                        print(f"Extracted coordinates: {lat}, {lon}")

                        # Save the data
                        pins.append({
                            "Name": name,
                            "Description": description,
                            "Type": subfolder_name,
                            "Latitude": lat,
                            "Longitude": lon,
                            "Index": index
                        })

                        # Close the new tab and switch back to the main tab
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(1)

                        # Click the back button to return to the main side panel
                        back_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpaths["back_button"])))
                        safe_click(back_button)
                        print("Clicked back button")
                        time.sleep(1)  # Wait for the side panel to reload
                    except Exception as e:
                        print(f"Error extracting location data in {subfolder_name} (index {index}): {str(e)}")

                # Save the data for this subfolder to a CSV file
                filename = generate_filename(folder_name, subfolder_name)
                with open(filename, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=["Name", "Description", "Type", "Latitude", "Longitude", "Index"])
                    writer.writeheader()
                    writer.writerows(pins)

                print(f"Data saved to {filename}")
            except Exception as e:
                print(f"Error accessing subfolder {subfolder_name}: {str(e)}")
except Exception as e:
    print(f"Error accessing parent folder or subfolder: {str(e)}")

# Close the browser
driver.quit()
