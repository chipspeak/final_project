from selenium_functions import *
import time
from guideframe_utils import get_env_settings  # Importing the guide_step and get_env_settings functions from guideframe_utils.py

# Setup the driver and perform automation tests
def selenium_automation_tests():
    env_settings = get_env_settings()  # Getting the environment settings
    driver_location = env_settings["driver_location"]  # Getting the driver location from the settings
    driver = driver_setup(driver_location)  # Initializing driver
    
    set_window_size(driver)
    open_url(driver, "https://magento.softwaretestingboard.com/")
    time.sleep(2)  # Give the page time to load

    # Clicking the agree button for the privacy policy
    click_button_by_span_text(driver, "AGREE")

    # Click on the 'Sign In' link
    click_element(driver, ".authorization-link > a")
    time.sleep(2)
    
    # Enter email and password
    type_into_field(driver, "email", "test-user@email.com")
    type_into_field(driver, "pass", "testuser-1")
    
    # Click the sign-in button
    click_element(driver, "button[name='send']")
    time.sleep(3)

    # First, hover over the "Gear" menu
    hover_over_element(driver, "https://magento.softwaretestingboard.com/gear.html")
    time.sleep(2)

    # Then, click on "Fitness Equipment"
    click_element(driver, "a[href='https://magento.softwaretestingboard.com/gear/fitness-equipment.html']")
    time.sleep(2)

    # Hover over the Yoga companion kit product
    hover_over_element(driver, "https://magento.softwaretestingboard.com/sprite-yoga-companion-kit.html")
    time.sleep(2)

    # Hover over the yoga straps product
    hover_over_element(driver, "https://magento.softwaretestingboard.com/set-of-sprite-yoga-straps.html")
    time.sleep(2)

    # Return to the straps product and click on it
    hover_and_click(driver, "https://magento.softwaretestingboard.com/harmony-lumaflex-trade-strength-band-kit.html")
    time.sleep(2)

    # Hover over the reviews link
    hover_over_element(driver, "https://magento.softwaretestingboard.com/harmony-lumaflex-trade-strength-band-kit.html#reviews")
    time.sleep(2)

    # Open the reviews link in a new tab
    open_link_in_new_tab(driver, "https://magento.softwaretestingboard.com/harmony-lumaflex-trade-strength-band-kit.html#reviews")
    time.sleep(2)
    
    # Close the browser
    driver.quit()

# Run the automation test
if __name__ == "__main__":
    selenium_automation_tests()
