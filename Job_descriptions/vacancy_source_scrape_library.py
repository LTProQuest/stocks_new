
import os
import sys
import random
import requests
import datetime
import time
import re

import pickle
import browser_cookie3
from bs4 import BeautifulSoup


path = r"C:\Users\luket\Desktop\test_space\libraries"
sys.path.insert(0, path)

from library_webscrape import classes, outlook, edit_docx, os_lib, pickle_lib



def scrape(url,soup):
    #template_pickle = r"C:\Users\luket\Desktop\test_space\Job_descriptions\vacancy_source_scrape_pickle.pkl"
    template_pickle = r"C:\Users\luket\Desktop\test_space\selected_sources.pkl"

    pickle_array = pickle_lib.load_pickle(template_pickle)
    template_found_no_selector = False

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    headers = {"user-agent": USER_AGENT}

    if url.find("reed") != -1:
        with requests.session() as s:
            r = s.get(url, headers=headers)
            plain_text = r.text
            soup = BeautifulSoup(plain_text)
            description = soup.find("div", {"class": "description"})
            job_description = description.find("span").getText()
            job_expired = False
        return job_description, job_expired

    if url.find("glassdoor") != -1:
        with requests.session() as s:
            r = s.get(url, headers=headers)
            plain_text = r.text
            soup = BeautifulSoup(plain_text)
            description = soup.find("div", {"id": "JobDescriptionContainer"})
            job_description = description.find("div").getText()
            job_expired = False
        return job_description, job_expired
    
    
    for i, scrape_template in enumerate(pickle_array):   
        if url.find(scrape_template["website_title"]) != -1:
            if scrape_template["selector_found"] == True:
                description_selector = scrape_template["description_selector"]
                job_description = soup.find('div', {description_selector["attribute"]:description_selector["attribute_value"]}).getText()#{"description__text description__text--rich"}})
                job_expired = False  
            else:
                 template_found_no_selector = True
                 retry_template = scrape_template
                 template_index = i
                 break        
            try:
                expired_selector = scrape_template["job_expired_selector"]
                job_expired_warning = soup.find(expired_selector["parent"], {expired_selector["attribute"]:expired_selector["attribute_value"]}).getText()
                if type(job_expired_warning) == str:
                    job_expired = True
                    job_description = ""
                else:
                    pass    
            except KeyError:
                pass
            except UnboundLocalError:
                pass 
            return job_description, job_expired

    


    if template_found_no_selector == True:
        print('template_found_no_selector: ', template_found_no_selector, " - retrying template search")
    else:
        print("found new vacancy source - ", url)
    
    #FORMING A SCRAPING TEMPLATE FOR NEW VACANCY SOURCE
    webscraper = classes.webscraper(cookie_browser="firefox")
    soup, plain_text = webscraper.get_soup(url, return_plain_text=True)
    
    base_url = webscraper.base_url
    site = base_url
    # try:
    #     site = base_url.split("www.")[1].split(".")[0]
    # except IndexError:    
    #     site = base_url.split(".")[0]
    pickle_append_dict = {"website_title":site}
    
    expired_finder_terms = ["no longer available", "has expired", "has been filled","no longer accepting"]
    job_description_selector_finder_terms = ["job-description", "job_description", "job-details", "description__text", "jobDescription","jobdesc"]
    
    for split_number, line in enumerate(plain_text.split("<")):
        #print('line: ', line)
        for selector_finder in job_description_selector_finder_terms:
            if (line.find('="' + selector_finder) != -1):#if  (line.find("div") != -1) and (line.find('="' + selector_finder) != -1):
                description_selector_line = line #carries through and assigns furthest down the tree
                print('description_selector_line: ', description_selector_line)
                
        for expired_finder in expired_finder_terms:         
            if  (line.find(expired_finder) != -1):
                expired_selector_line = line #carries through and assigns furthest down the tree
                parent_line = plain_text.split("<")[split_number]
                print("expired vacancy found - ", line)

    
    try:
        attribute = description_selector_line.split("div ")[1].split("=")[0]
        attribute_value = description_selector_line.split('"')[1]
        pickle_append_dict["description_selector"] = {"attribute":attribute, "attribute_value":attribute_value}
        pickle_append_dict["selector_found"] = True
    except:
        pickle_append_dict["description_selector"] = {"attribute":"attribute", "attribute_value":"attribute_value"}
        pickle_append_dict["selector_found"] = False
        pass
    try:
        parent = expired_selector_line.split(" ")[0]
        attribute = expired_selector_line.split(" ")[1].split("=")[0]
        attribute_value = expired_selector_line.split('"')[1]
        pickle_append_dict["expired_selector"] = {"parent":parent, "attribute":attribute, "attribute_value":attribute_value}
    except:
        pass
    

    if template_found_no_selector == True:
        print('pickle_array: ', pickle_array[template_index])
        pickle_array[template_index] = pickle_append_dict
        print('Edited pickle_array: ', pickle_array[template_index])
        pickle_lib.save_pickle(template_pickle, pickle_array)
        #could overwrite good expiry selector so far
    else:
        pickle_lib.append_pickle(template_pickle, pickle_append_dict,print_pickle=False)


    log_file = "job_descriptions/vacancy_source_new_log.txt"
    append_to_log = 'url - r"'  + url + '" \n' + str(pickle_append_dict) + "\n"*2
    os_lib.file_append(log_file, append_to_log)

    job_description = None
    job_expired = True
    
    return job_description, job_expired


# url = r"https://www.glassdoor.co.uk/job-listing/JV.htm?jl=3600711345"
# job_decription, job_expired = scrape(url,"hi")
# print(job_decription)
