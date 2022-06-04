"""
Source: https://mersakarya.medium.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905
"""

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
        executable_path="C:/Users/39320\Desktop/myProjects_python/jobSalaryPrediction/chromedriver", options=options)
    driver.set_window_size(1120, 1000)

    # url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" + keyword + "&sc.keyword=" + keyword + "&locT=&locId=&jobType="
    driver.get(url)
    jobs = []
    first_time = True
    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(4)

        # Test for the "Sign Up" prompt and get rid of it.
        if first_time == True:
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
                if first_time == True:
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
                        location = driver.find_element(by=By.XPATH, value=
                        './/div[@class="css-56kyx5 e1tk4kwz1"]').text  # could be remote
                        job_description = driver.find_element(by=By.XPATH, value=
                        './/div[@class="jobDescriptionContent desc"]').text
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
                    rating = driver.find_element(by=By.XPATH, value='.//span[@class="css-1m5m32b e1tk4kwz4" and @data-test="detailRating"]').text
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

                # Going to the Company tab...
                # clicking on this:
                # <div class="tab" data-tab-type="overview"><span>Company</span></div>
                try:
                    driver.find_element(by=By.XPATH, value='.//div[@class="tab" and @data-tab-type="overview"]').click()

                    try:
                        # <div class="infoEntity">
                        #    <label>Headquarters</label>
                        #    <span class="value">San Francisco, CA</span>
                        # </div>
                        headquarters = driver.find_element(by=By.XPATH, value=
                        './/div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                    except NoSuchElementException:
                        headquarters = -1

                    try:
                        size = driver.find_element(by=By.XPATH, value=
                        './/div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                    except NoSuchElementException:
                        size = -1

                    try:
                        founded = driver.find_element(by=By.XPATH, value=
                        './/div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                    except NoSuchElementException:
                        founded = -1

                    try:
                        type_of_ownership = driver.find_element(by=By.XPATH, value=
                        './/div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                    except NoSuchElementException:
                        type_of_ownership = -1

                    try:
                        industry = driver.find_element(by=By.XPATH, value=
                        './/div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                    except NoSuchElementException:
                        industry = -1

                    try:
                        sector = driver.find_element(by=By.XPATH, value=
                        './/div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                    except NoSuchElementException:
                        sector = -1

                    try:
                        revenue = driver.find_element(by=By.XPATH, value=
                        './/div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                    except NoSuchElementException:
                        revenue = -1

                    try:
                        competitors = driver.find_element(by=By.XPATH, value=
                        './/div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                    except NoSuchElementException:
                        competitors = -1

                except NoSuchElementException:  # Rarely, some job postings do not have the "Company" tab.
                    headquarters = -1
                    size = -1
                    founded = -1
                    type_of_ownership = -1
                    industry = -1
                    sector = -1
                    revenue = -1
                    competitors = -1

                if verbose:
                    print("Headquarters: {}".format(headquarters))
                    print("Size: {}".format(size))
                    print("Founded: {}".format(founded))
                    print("Type of Ownership: {}".format(type_of_ownership))
                    print("Industry: {}".format(industry))
                    print("Sector: {}".format(sector))
                    print("Revenue: {}".format(revenue))
                    print("Competitors: {}".format(competitors))
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
                # "Salary Estimate": salary_estimate,
                # "Job Description": job_description,
                # "Rating": rating,
                # "Company Name": company_name,
                # "Location": location,
                # "Headquarters": headquarters,
                # "Size": size,
                # "Founded": founded,
                # "Type of ownership": type_of_ownership,
                # "Industry": industry,
                # "Sector": sector,
                # "Revenue": revenue,
                # "Competitors": competitors}
                # add job to jobs

                # Clicking on the "next page" button
        except:
            driver.find_element(by=By.XPATH, value='.//span[@alt="next-icon"]').click()
            time.sleep(5)
        # except NoSuchElementException:
        #     print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
        #                                                                                                      len(jobs)))
        #     break

    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.


df_scraping = get_jobs("data scientist", 5, True)
