import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

# LinkedIn credentials (store securely, consider environment variables)
linkedin_username = "2002ehsansoltani@gmail.com"
linkedin_password = "Vqi+x0!wnB)%C57"


# Set up Chrome driver with options
chrome_options = Options()
driver = webdriver.Chrome(options=chrome_options)

# Ignore StaleElementReferenceException
ignored_exceptions = (StaleElementReferenceException)
wait = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions)

# Maximize the browser window
driver.maximize_window()

# Open the LinkedIn link
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=4049236704&geoId=105080838&keywords=python%20developer&origin=JOBS_HOME_KEYWORD_AUTOCOMPLETE&refresh=true")
# driver.get("https://www.linkedin.com/authwall?trk=qf&original_referer=&sessionRedirect=https%3A%2F%2Fwww.linkedin.com%2Fjobs%2Fsearch%2F%3FcurrentJobId%3D4049236704%26geoId%3D105080838%26keywords%3Dpython%2520developer%26origin%3DJOBS_HOME_KEYWORD_AUTOCOMPLETE%26refresh%3Dtrue")

# Wait for the page to load
time.sleep(5)

# Handle different login scenarios
try:
    # Attempt to find the sign-in button on the main content page
    sign_in_btn = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[1]/form/p/button')
    driver.execute_script("arguments[0].click()", sign_in_btn)

    # Wait for the page to load and enter credentials
    time.sleep(3)

    username_input = driver.find_element(By.ID, "session_key")
    driver.execute_script(f"arguments[0].value='{linkedin_username}'", username_input)

    password_input = driver.find_element(By.XPATH, '//*[@id="session_password"]')
    driver.execute_script(f"arguments[0].value='{linkedin_password}'", password_input)

    time.sleep(5)
    # Submit the login form and handle potential CAPTCHA
    submit_btn = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[1]/div[2]/form/div[2]/button')
    driver.execute_script("arguments[0].click()", submit_btn)

    input("Captcha Done? Press Enter to continue...")
    # waiting for the page to load
    time.sleep(3)

    # Navigate to the jobs section and search for Python developer jobs
    job_btn = driver.find_element(By.XPATH, '//*[@id="global-nav"]/div/nav/ul/li[3]/a')
    driver.execute_script("arguments[0].click()", job_btn)

    if wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.jobs-search-box__inner input"))):

        # entering the python developer into search input field
        search_input_1 = driver.find_elements(By.CSS_SELECTOR, "div.jobs-search-box__inner div.relative input")[0]
        search_input_1.click()
        search_input_1.send_keys("Python Developer")
        search_input_1.send_keys(Keys.ENTER)



    else:
        print("Search input not visible")

    # Wait for search results and iterate through job listings
    time.sleep(10)

    if wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.scaffold-layout__list"))):
        li_elements = driver.find_elements(By.CSS_SELECTOR, "div.scaffold-layout__list div ul li.ember-view")

    for company in li_elements:
        time.sleep(2)
        # checking if that li is a job application through checking if it has an attribute named data-occludable-job-id if yes so we sure that li is job application
        company_id = company.get_attribute("data-occludable-job-id")
        if company_id != None:
            # Click on the job listing
            wait.until(EC.element_to_be_clickable(company)).click()

            # Check for save and follow buttons and click if available
            wait.until(EC.visibility_of_element_located((By.XPATH,
                                                         '//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[5]/div/button'))).click()
            # checking the visibility of follow button
            if wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.follow"))):
                # finding follow button
                follow_btn = driver.find_element(By.CSS_SELECTOR, "button.follow")
                # clicking on follow button
                driver.execute_script("arguments[0].click()", follow_btn)


except NoSuchElementException:
    try:
        # Check for sign-in modal and click the button if visible
        if wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div/div[2]/button'))):
            sign_in_btn = driver.find_element(By.XPATH, '//*[@id="base-contextual-sign-in-modal"]/div/section/div/div/div/div[2]/button')
            driver.execute_script("arguments[0].click()", sign_in_btn)

        # Wait for page to load after clicking sign-in
        time.sleep(3)


        # Enter LinkedIn credentials
        username_input = driver.find_element(By.ID, "base-sign-in-modal_session_key")
        driver.execute_script(f"arguments[0].value='{linkedin_username}'", username_input)


        password_input = driver.find_element(By.ID, "base-sign-in-modal_session_password")
        driver.execute_script(f"arguments[0].value='{linkedin_password}'", password_input)

        time.sleep(2)
        # Submit login form
        submit_btn = driver.find_element(By.XPATH, '//*[@id="base-sign-in-modal"]/div/section/div/div/form/div[2]/button')
        driver.execute_script("arguments[0].click()", submit_btn)

        # Handle potential CAPTCHA (pause script execution until user confirms completion)
        input("Captcha Done? ")

        # Check for job listings after login
        if wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.scaffold-layout__list"))):
            li_elements = driver.find_elements(By.CSS_SELECTOR, "div.scaffold-layout__list div ul li.ember-view")

        # Loop through job listings, saving and following if clickable
        for company in li_elements:
            company_id = company.get_attribute("data-occludable-job-id")
            if company_id != None:
                wait.until(EC.element_to_be_clickable(company)).click()
                time.sleep(2)

                # Check and click save button if available
                if wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[5]/div/button'))):
                    save_btn = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[5]/div/button')
                    save_btn.click()
                else:
                    pass
                # Check for and click follow button if available
                if wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.follow"))):
                    follow_btn = driver.find_element(By.CSS_SELECTOR, "button.follow")
                    driver.execute_script("arguments[0].click()", follow_btn)
                else:
                    pass

    except NoSuchElementException:
        try:
            # Find and click the "Sign in with email" button
            sign_in_btn = driver.find_element(By.LINK_TEXT, "Sign in with email")
            driver.execute_script("arguments[0].click()", sign_in_btn)

            # Enter LinkedIn credentials
            username_input = driver.find_element(By.ID, "username")
            username_input.send_keys(linkedin_username)

            password_input = driver.find_element(By.ID, "password")
            password_input.send_keys(linkedin_password)

            # Click the submit button to log in
            submit_btn = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[4]/button')
            driver.execute_script("arguments[0].click()", submit_btn)

            # Handle potential CAPTCHA (pause script execution until user confirms completion)
            input("Captcha Done? ")

            # Click the "Jobs" button
            job_btn = driver.find_element(By.XPATH, '//*[@id="global-nav"]/div/nav/ul/li[3]/a')
            driver.execute_script("arguments[0].click()", job_btn)

            # Check for search field visibility and enter search terms
            if wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.jobs-search-box__inner input"))):

                search_input_1 = driver.find_elements(By.CSS_SELECTOR, "div.jobs-search-box__inner div.relative input")[
                    0]
                search_input_1.click()
                search_input_1.send_keys("Python Developer")
                search_input_1.send_keys(Keys.ENTER)



            else:
                print("Search input not visible")

            # Wait for search results and find job listings
            time.sleep(10)
            if wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.scaffold-layout__list"))):
                li_elements = driver.find_elements(By.CSS_SELECTOR, "div.scaffold-layout__list div ul li.ember-view")
                print(len(li_elements))

            # Loop through job listings, saving and following if clickable
            for company in li_elements:
                time.sleep(2)
                company_id = company.get_attribute("data-occludable-job-id")
                if company_id != None:
                    # Click save button if available
                    wait.until(EC.element_to_be_clickable(company)).click()
                    wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                 '//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[5]/div/button'))).click()

                    # Click follow button if available
                    if wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button.follow"))):
                        follow_btn = driver.find_element(By.CSS_SELECTOR, "button.follow")
                        driver.execute_script("arguments[0].click()", follow_btn)

        except NoSuchElementException:
            raise NoSuchElementException