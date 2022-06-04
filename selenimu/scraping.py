import time

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By


def get_jobs(keyword, num_jobs, verbose):
    """Gathers jobs as a dataframe, scraped from Glassdoor"""

    # Initializing the webdriver
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(
        executable_path="C:/Users/39320\Desktop/myProjects_python/jobSalaryPrediction/chromedriver",
        options=options
    )
    driver.set_window_size(1120, 600)

    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" + keyword + "&sc.keyword=" + keyword + "&locT=&locId=&jobType="
    driver.get(url)
    jobs = []
    first_time = True
    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(4)

        # Test for the "Sign Up" prompt and get rid of it.
        if first_time:
            try:
                driver.find_element(by=By.XPATH, value=".//*[@id='onetrust-accept-btn-handler']").click()
            except ElementClickInterceptedException:
                pass

        time.sleep(.1)

        try:
            driver.find_element(by=By.CLASS_NAME, value="ModalStyle__xBtn___29PT9").click()  # clicking to the X.
        except NoSuchElementException:
            pass

        # Going through each job in this page
        job_buttons = driver.find_elements(by=By.XPATH, value='.//*[@id= "MainCol"]//a[@class= "jobLink"]')
        try:
            for job_button in job_buttons:
                print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
                if len(jobs) >= num_jobs:
                    break

                job_button.click()  # You might
                time.sleep(5)
                if first_time:
                    try:
                        driver.find_element(by=By.XPATH, value='.//span[@alt="Close"]').click()
                    except ElementClickInterceptedException:
                        pass
                    first_time = False
                collected_successfully = 0
                while collected_successfully < 100:
                    try:
                        company_name = driver.find_element(by=By.XPATH,
                                                           value='.//div[@class="css-xuk5ye e1tk4kwz5"]').text
                        job_title = driver.find_element(by=By.XPATH,
                                                        value='.//div[@class="css-1j389vi e1tk4kwz2"]').text
                        location = driver.find_element(by=By.XPATH,
                                                       value='.//div[@class="css-56kyx5 e1tk4kwz1"]').text  # could be remote
                        job_description = driver.find_element(by=By.XPATH,
                                                              value='.//div[@class="jobDescriptionContent desc"]').text
                        try:
                            top_company = driver.find_element(by=By.XPATH,
                                                              value='.//span[@class="css-1cqhqxf eqj3y11"]').text
                        except NoSuchElementException:
                            top_company = 0
                        collected_successfully = 100
                    except:
                        collected_successfully = collected_successfully + 1

                try:
                    salary_estimate = driver.find_element(by=By.XPATH,
                                                          value='.//span[@class="css-1hbqxax e1wijj240" and @data-test="detailSalary"]').text
                except NoSuchElementException:
                    salary_estimate = -1  # You need to set a "not found value. It's important."

                try:
                    rating = driver.find_element(by=By.XPATH,
                                                 value='.//span[@class="css-1m5m32b e1tk4kwz4" and @data-test="detailRating"]').text
                except NoSuchElementException:
                    rating = -1  # You need to set a "not found value. It's important."

                try:
                    company_overview = driver.find_element(by=By.XPATH, value='.//div[@id="EmpBasicInfo"]').text
                except NoSuchElementException:
                    company_overview = -1

                try:
                    recommend_friend = driver.find_element(by=By.XPATH, value='.//div[@class="css-vkhqai"]').text
                    ceo_app = driver.find_element(by=By.XPATH, value='.//div[@class="css-vkhqai ceoApprove"]').text
                    other_info = driver.find_element(by=By.XPATH, value='.//ul[@class="css-1t3mcrv erz4gkm2"]').text
                except NoSuchElementException:
                    recommend_friend = -1
                    ceo_app = -1
                    other_info = -1

                # Printing for debugging
                if verbose:
                    print("Company Name: {}".format(company_name))
                    print("Job Title: {}".format(job_title))
                    print("Location: {}".format(location))
                    print("Job Description: {}".format(job_description[:100]))
                    print("Top Company: {}".format(top_company))
                    print("Salary Estimate: {}".format(salary_estimate))
                    print("Rating: {}".format(rating))
                    print("Comapany overview: {}".format(company_overview))
                    print("Recommend to a friend: {}".format(recommend_friend))
                    print("Ceo approve: {}".format(ceo_app))
                    print("Other info: {}".format(other_info))
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

                jobs.append({"Company Name": company_name,
                             "Job Title": job_title,
                             "Location": location,
                             "Job Description": job_description,
                             "Top Company": top_company,
                             "Salary Estimate": salary_estimate,
                             "Rating": rating,
                             "Comapany overview": company_overview,
                             "Recommend to a friend": recommend_friend,
                             "Ceo approve": ceo_app,
                             "Other info": other_info})

        # Clicking on the "next page" button
        except:
            driver.find_element(by=By.XPATH, value='.//span[@alt="next-icon"]').click()
            time.sleep(5)

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.


#for test
# df_scraping = get_jobs("data scientist", 5, True)
