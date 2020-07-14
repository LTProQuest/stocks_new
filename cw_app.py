
"""
process: 
get vacancy info, call produce candidate search URL app
Send each candidate URL to scrape app
"""
#try:

import re
import time
import datetime
import requests
import random
import sys
import os
from bs4 import BeautifulSoup


import browser_cookie3 


import cw_scrape


path = r"C:\Users\luket\Desktop\work\cv_library_workspace\libraries"
sys.path.insert(0, path)
from library_webscrape import classes, os_lib


root_url = "https://recruiter.cwjobs.co.uk"
#a

candidate_scrape_attempts = 0
candidate_scrape_limit = 400
candidates_per_minute = 6
post_candidate = True
debug_on = False
    
webscraper = classes.webscraper(debug = debug_on, cookie_browser = "firefox")

location = "London"
key_words = "database OR file OR php OR sql OR java OR a OR python OR ruby OR c+ OR html OR design OR web"

page_limit = 50

candidates_posted = 0 

try:
    for page_number in range(page_limit):
        print('page_number: ', page_number)
        
        
        candidate_search_url = r"https://recruiter.cwjobs.co.uk/CandidateSearchWebMvc/CandidateSearch/Results?FreeText=" + key_words + r"&ShowUnspecifiedSalary=False&QuestionAnswerIds=%7b1%2c2%7d%7b2%2c2%7d&LastActivityId=6&CurrentLocation=" + location + r"&TravelTime=45&SalaryFacetsType=99&PreRegStatusFacet=0%2c1&HideCandidatesSinceDays=7&SearchId=aa1b08b3-ff85-4d49-b429-c4efcbec789f&scr=1&PageNumber=" + str(page_number + 1) + "#search-results"

        soup = webscraper.get_soup(candidate_search_url)
        view_candidate_links = soup.findAll("a", {"class": "candidate-lnk"})
        print("length candidate links", len(view_candidate_links))
        result_soup = soup.find("p",{"id": ["searchSummary"]}).getText()
        result_soup = result_soup.split("of")[1]
        result_soup = result_soup.split("candidates")[0].strip()
        number_of_results = int(result_soup)
        if page_number == 0:
            print(number_of_results)

        time.sleep(4)

        for link in view_candidate_links:

            if candidate_scrape_attempts == number_of_results:
                print("all results scraped")
                break


            if candidate_scrape_attempts < candidate_scrape_limit:
                candidate_scrape_attempts += 1
                pass
            else:
                break

            time.sleep(60/candidates_per_minute)

            candidate_url = root_url + link.get('href')
            print("candidate url: " , candidate_url)

            try: #omit no uploaded cv exceptions
                payload, download_path, eligible_to_work = cw_scrape.get_candidate_payload(candidate_url, webscraper)
            except:
                continue
            
            if eligible_to_work == False:
                print("Not eligible to work, continuing")
                continue
            else:
                pass
            
            

            payload["NoMatch"] = True
            #print(payload)

            #candidate_post_url = "https://api.pro-quest.co.uk/api/candidates/PostContractor"
            candidate_post_url = "https://data.prestigeumbrella.co.uk/api/candidates/postcontractor"


            payload["CVSummary"] = "test"

            first_name = link.find("span", {"class": "firstName"}).getText().strip()
            last_name = link.find("span", {"class": "lastName"}).getText().strip()
            print(first_name)
            
            print(last_name)
            payload["Name"] = first_name + " " + last_name
            
            if debug_on == True:
                print(payload)
            
            
            if post_candidate == True:
                response = webscraper.api_post_payload(candidate_post_url, payload, assign_response_as_variable=True)
                print(response[0:10])
                if response.lower().find('id":') != -1:
                    candidates_posted += 1
                    print(candidates_posted, " of 250 candidates posted")
                elif response.lower().find("duplicate") != -1:
                    print("moving to next page")
                    break #move to next page
                else:
                    pass

            else:
                pass

            if candidates_posted >= 250:
                break
    print("\n"*4 + "Posting complete, ", candidates_posted, " of 250 candidates posted")

except Exception as e: 
    print("An error has occured and it's description displayed below." + "\n"*2)
    print("Error description - ", str(e))
    if e is ModuleNotFoundError():
        print("Application files not found, please check the application is installed correctly by referring to 'installation.txt' in the application folder and that no files have been moved")
    
    
    print("Please check you are signed into CWJobs on Firefox and that you are able to search for candidate information manually before restarting the application \n\n  If this is a reoccuring error and cannot be resolved, please copy the error description above and email it to 'luke.turner@pro-quest.co.uk'")



input("press enter to exit")
        

    








        
  


