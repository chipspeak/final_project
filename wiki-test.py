import subprocess
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to open a URL
def open_url(driver, target):
    driver.get("https://www.wikipedia.org" + target)

# Function to set window size
def set_window_size(driver):
    driver.maximize_window()
    
# Function to click an element using a CSS selector with error handling
def click_element(driver, css_selector):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        element.click()
    except Exception as e:
        print(f"Error clicking element with selector '{css_selector}': {e}")

# Function to type into an input field using an ID with error handling
def type_into_field(driver, element_id, text):
    try:
        input_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, element_id))
        )
        input_field.send_keys(text)
    except Exception as e:
        print(f"Error typing into field with ID '{element_id}': {e}")

# Function to start FFmpeg to record the screen
def start_ffmpeg_recording(output_file):
    # Command to start recording using FFmpeg
    command = [
        'ffmpeg',
        '-f', 'x11grab',             # Capture X11 screen
        '-video_size', '1920x1080',           # Set resolution; consider using '$(xdpyinfo | grep dimensions)' for dynamic resolution
        '-i', ':1.0',                # Input display (change this if necessary)
        '-c:v', 'libxvid',           # Video codec
        '-preset', 'fast',           # Preset for encoding speed
        '-framerate', '30',          # Frame rate; increase for smoother video
        '-b:v', '3000k',             # Set bitrate for better quality
        '-pix_fmt', 'yuv420p',       # Pixel format
        output_file                  # Output file
    ]
    
    # Start the FFmpeg process
    return subprocess.Popen(command)

# Function to run the entire test sequence
def run_selenium_test():
    # Set up Chrome options with the user profile
    options = Options()
    options.add_argument("/home/paoconno/.config/google-chrome/Default") 

    # Disable the "Chrome is being controlled by automated test software" banner
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Specify the path to ChromeDriver
    service = Service('/usr/bin/chromedriver')

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Step 1: Set window size
        set_window_size(driver)

        # Step 2: Open URL
        open_url(driver, "/")

        time.sleep(5)

        # Step 3: Type "Red Hat" into the search input
        type_into_field(driver, "searchInput", "Red Hat")

        # Step 4: Wait for the suggestion list to appear, then click the first suggestion
        try:
            suggestion = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".suggestion-text"))
            )
            suggestion.click()

            time.sleep(5)

        except Exception as e:
            print(f"Error clicking suggestion: {e}")

        # Step 5: Click the link for "Fedora Project"
        click_element(driver, ".hatnote:nth-child(39) > a")

        time.sleep(10)

    finally:
        print("Test complete")

if __name__ == "__main__":
    output_file = "screen_recording.avi"
    
    # Start FFmpeg recording in a separate thread
    ffmpeg_process = threading.Thread(target=start_ffmpeg_recording, args=(output_file,))
    ffmpeg_process.start()

    try:
        run_selenium_test()
    finally:
        # Stop FFmpeg process
        subprocess.call(['pkill', 'ffmpeg'])
        ffmpeg_process.join()
