
"""
process: 
get vacancy info, call produce candidate search URL app
Send each candidate URL to scrape app
"""
import sys

path = r"C:\Users\luket\Desktop\test_space\depersonalisation"
sys.path.insert(0, path)
import redact_template
import cw_scrape
import win32com.client
import browser_cookie3
from bs4 import BeautifulSoup
import os
import random
import requests
import datetime
import time
import re

#import doc_to_docx

path = r"C:\Users\luket\Desktop\test_space\libraries"
sys.path.insert(0, path)

from library_webscrape import classes, outlook, edit_docx, os_lib

# Settings
#depersonalise_cv = False
logger = outlook.WebscrapeLogger()
candidate_pages_per_vacancy = 1
vacancy_search_limit = 100
vacancy_start_from = 62  # default = 1
root_url = 'https://recruiter.cwjobs.co.uk'
candidate_scrape_limit = 300  # per vacancy


settings = {
    "download_cv": True,
    "download_storage": r"C:\Users\luket\Desktop\test_space\storage\cv_storage",
    "email_logging": False
}

edited_document_storage = r"C:\Users\luket\Desktop\test_space\storage\edited_cv_storage"
candidates_per_minute = 3
candidate_post_url = "https://api.pro-quest.co.uk/api/candidates/PostJobCandidate"
#candidate_post_url = "https://api.pro-quest.co.uk/api/candidates/PostContractor"
post_candidate = True
debug_on = True
clean_storage = True  # before app execution


if clean_storage == True:
    os_lib.delete_folder_content(edited_document_storage)
    os_lib.delete_folder_content(settings["download_storage"])

webscraper = classes.webscraper(debug=debug_on, cookie_browser="firefox", values=settings)
desired_fields = ["title", "id", "jobType", "city", "importJobDescription"]


def get_vacancy_payloads():
    vacancy_api_url = "https://api.pro-quest.co.uk/api/importjobs/getlatest?sector=it&qty=" + str(vacancy_search_limit)
    vacancy_payloads = webscraper.api_get_dictionaries_from_json(
        vacancy_api_url, desired_fields)
    return vacancy_payloads


vacancy_payloads = get_vacancy_payloads()


for i, vacancy in enumerate(vacancy_payloads):
    print("vacancy number - ", i + 1)
    if i < (vacancy_start_from - 1):
        continue
    else:
        pass

    candidate_scrape_attempts = 0

    print("beginning candidate search for vacancy")
    for page_number in range(candidate_pages_per_vacancy):

        print("page number - ", page_number)

        if vacancy["city"].lower() == "unknown":
            vacancy["city"] = ""    
        
        vacancy["title"] = vacancy["title"].replace("&","")

        
        print(vacancy["city"])

        candidate_search_url = r"https://recruiter.cwjobs.co.uk/CandidateSearchWebMvc/CandidateSearch/Results?FreeText=" + vacancy["title"].split("-")[0].split(",")[0] + r"&ShowUnspecifiedSalary=False&QuestionAnswerIds=%7b1%2c2%7d%7b2%2c2%7d&LastActivityId=6&CurrentLocation=" + vacancy["city"] + r"&TravelTime=45&SalaryFacetsType=99&PreRegStatusFacet=0%2c1&HideCandidatesSinceDays=7&SearchId=aa1b08b3-ff85-4d49-b429-c4efcbec789f&scr=1&PageNumber=" + str(page_number + 1) + "#search-results"
        print("candidate search url = " + candidate_search_url)
        soup = webscraper.get_soup(candidate_search_url)
        view_candidate_links = soup.findAll("a", {"class": "candidate-lnk"})
        time.sleep(2)
        print("length candidate links", len(view_candidate_links))
        no_match = False
        if len(view_candidate_links) < 9:
            no_match = True
            continue

        result_soup = soup.find("p", {"id": ["searchSummary"]}).getText()
        result_soup = result_soup.split("of")[1]
        result_soup = result_soup.split("candidates")[0].strip()
        number_of_results = int(result_soup)
        if page_number == 0:
            print(number_of_results)
        time.sleep(4)

        print("candidate links found - ", len(view_candidate_links))

       

        for link in view_candidate_links:

            if candidate_scrape_attempts < candidate_scrape_limit:
                candidate_scrape_attempts += 1
                pass
            else:
                continue

            time.sleep(60/candidates_per_minute)

            candidate_url = root_url + link.get('href')
            try:  # omit no uploaded cv exceptions
                print("attempting to scrape url - ", candidate_url)
                payload, cv_download_url, eligible_to_work = cw_scrape.get_candidate_payload(candidate_url, webscraper)
            except:
                print("scrape failed")
                continue
            
            print(payload)
            if eligible_to_work == False:
                print("Not eligible to work, continuing")
                continue

            if debug_on == True:
                print("cv_download_url - ", cv_download_url)

            payload["VacancyId"] = vacancy["id"]
            payload["NoMatch"] = no_match
            cv_file_path = webscraper.download_file_from_url(cv_download_url, depersonalise=True)
            
            first_name = link.find("span", {"class": "firstName"}).getText().strip()
            last_name = link.find("span", {"class": "lastName"}).getText().strip()
            texts_to_hide = [first_name, last_name]
            print("texts_to_hide - ", texts_to_hide)
            
            filename, file_extension = os.path.splitext(cv_file_path)
            payload["CVFile"] = webscraper.encode_cv(cv_file_path)


            try:
                if file_extension == ".docx":
                    edited_cv_file_path = edit_docx.docx_replace_multiple_strings(
                        cv_file_path, texts_to_hide, edited_document_storage)
                    payload["DepersonalisedCVFile"] = webscraper.encode_cv(
                        edited_cv_file_path)
                    payload["CVFileExtension"] = "docx"
        
                elif file_extension == ".pdf":
                    edited_cv_file_path = redact_template.pdf_redact(
                        cv_file_path, edited_document_storage, texts_to_hide)
                    time.sleep(2)
                    payload["DepersonalisedCVFile"] = webscraper.encode_cv(
                        edited_cv_file_path)
                    payload["CVFileExtension"] = "pdf"

                else:
                    continue
                    print("oh dear, new file extension found - ", file_extension)

            except:
                print("depersonalisation error, conrinuing")
                continue

                

                  
            """
            elif file_extension == ".doc":
                print("doc found")
                doc_to_docx.save_as_docx(cv_file_path)
                edited_cv_file_path = edit_docx.docx_replace_multiple_strings(
                    cv_file_path + "x", texts_to_hide, edited_document_storage)
                payload["DepersonalisedCVFile"] = webscraper.encode_cv(
                    edited_cv_file_path)
           
            """
            


            if debug_on == True:
                print(payload["CVFileExtension"])

           
            if post_candidate == True:
                webscraper.api_post_payload(
                    candidate_post_url, payload, put=False)
                print("posting")
            else:
                pass


# logger.append_payload_to_logging(payload)

# logger.email_or_print_log()

#template = "An exception of type {0} occurred. Arguments:\n{1!r}"
#error_message = template.format(type(ex).__name__, ex.args)


#logger.email_log(scrape_attempts, error_message)
