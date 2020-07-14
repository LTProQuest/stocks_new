
import os
import requests
import re
import time
import datetime
import sys
import bs4
import win32com
from bs4 import BeautifulSoup
import browser_cookie3 

path = r"C:\Users\luket\Desktop\test_space\libraries"
sys.path.insert(0, path)

from library_webscrape import classes, outlook, edit_docx, os_lib

debug_on = True


def get_candidate_payload(job_url, webscraper):
    payload = {}
    base_url = "https://recruiter.cwjobs.co.uk"
    cj = browser_cookie3.firefox()
    with requests.Session() as s:
        
        r = s.get(job_url, cookies=cj)  
        time.sleep(4) 
        plain_text = r.text
        soup = BeautifulSoup(plain_text, "lxml")

        hyperlink_soup = soup.select("#btnDownloadCV")
                             
        download_path = base_url + hyperlink_soup[0].get("href")
        

      

        #CONTACT DETAILS
        test = soup.find("a", {"id": "btnEmailCandidate"})
        contact_details_url = base_url + test.get("data-hiddendataurl")
        contact_details = s.get(contact_details_url, cookies=cj).text
        time.sleep(4)
        from ast import literal_eval
        contact_details = literal_eval(contact_details) # from string to array
        #SUMMARY
        summary = soup.find("div", {"class": "col-lg-12 basic-summary"})
        summary = summary.getText().strip().replace("  ", "").splitlines()        
        summary = list(filter(None, summary))
        for i in range(0,len(summary),2):
            payload[summary[i]] = summary[i+1]  

        if payload["Work eligibility:"] == "Eligible to work in the UK":
            eligible_to_work = True
        else:
            eligible_to_work = False          

        reformatted_payload = {
            "NoMatch": True,
            "Town": "test",
            "County": "test",
            "MainPhone": "test",
            "OptionalPhone": "test",
            "Email": contact_details["Email"],
            "Age": "test",
            #"DateAvailable": "10-10-10",
            "CurrentJobTitle": "test",
            "DesiredJobTitle": "test",
            "JobType": "Contract",
            "WillingtoTravel": "test",
            "WillingtoRelocate": "test",
            "UKDrivingLicence": "test",
            "ExpectedSalary": "test",
            "Name": "test",
            "DesiredIndustry": "test",
            "MainSkills": "test",
            "CVSummary": "test",
            #"CVFileExtension": "pdf",
            #"CVFile": "dGVzdA==",
            #"DepersonalisedCVFile": "dGVzdA==",
            }
        

        reformatted_payload["Town"] = payload["Residence:"]
        reformatted_payload["CurrentJobTitle"] = payload["Current job title:"]

        try:
            reformatted_payload["MainPhone"] = contact_details["MobilePhone"]
        except:
            pass
        try:    
            reformatted_payload["OptionalPhone"] = contact_details["HomePhone"]
        except:
            pass
            

       
    return reformatted_payload, download_path, eligible_to_work
        

# webscraper = classes.webscraper(debug=debug_on, cookie_browser="firefox")
# job_url = "https://recruiter.cwjobs.co.uk/CandidateSearchWebMVC/CandidateDetails/Show?FreeText=Front+End+Developer&ShowUnspecifiedSalary=False&QuestionAnswerIds=%7b1%2c2%7d%7b2%2c2%7d&LastActivityId=6&CurrentLocation=Birkenhead&TravelTime=45&SalaryFacetsType=99&PreRegStatusFacet=0%2c1&HideCandidatesSinceDays=7&SearchId=aa1b08b3-ff85-4d49-b429-c4efcbec789f&scr=1&PageNumber=1PageNumber=1&candidateId=GmFVAJcAMLs%3d&CandidateSearchAuditId=q2bZFy%2fA8Wda52wNhWo97Q%3d%3d&PagePosition=1&PageSize=10"
# payload = get_candidate_payload(job_url, webscraper)




