
"""
process: 
get vacancy info, call produce candidate search URL app
Send each candidate URL to scrape app
"""



import os
import sys
import random
import requests
import datetime
import time
import re

import win32com.client
import browser_cookie3
from bs4 import BeautifulSoup

import vacancy_source_scrape_library as vacancy_scrape

path = r"C:\Users\luket\Desktop\test_space\libraries"
sys.path.insert(0, path)

from library_webscrape import classes, outlook, edit_docx, os_lib, pickle_lib

#os_lib.print_after_terminal_stop()







vacancy_start_from = 1


post_job = True
debug_on = True
clean_logging_files = False
clean_scrape_templates = False
print_current_scrape_templates = True
override_skips = False
skips_override = str(5600)
#template_pickle = r"C:\Users\luket\Desktop\test_space\Job_descriptions\vacancy_source_scrape_pickle.pkl"
template_pickle = r"C:\Users\luket\Desktop\test_space\selected_sources.pkl"


logging_files = r"C:\Users\luket\Desktop\test_space\Job_descriptions\vacancy_source_new_log.txt"
if clean_logging_files == True:
    try:
        os.remove(logging_files)
    except:
        print("logging files not found")
        pass    



if print_current_scrape_templates == True:
    current_scrape_templates = pickle_lib.load_pickle(template_pickle)
    print('current_scrape_templates: ', current_scrape_templates)

if clean_scrape_templates == True:
    pickle_lib.create_blank_pickle(template_pickle)
    pickle_lib.load_pickle(template_pickle)

ignore_selected_sources = True
sources_to_ignore = ["independentjobs", "jobstoday","stepstone"]#["independentjobs","linkedin", "indeed", "irish","totaljobs"]#["linkedin","indeed","irish","cityjobs","workinstartups","independentjobs"] 

scrape_selected_sources = False
selected_sources = []
pickle_array = pickle_lib.load_pickle(template_pickle)
for template in pickle_array:
    selected_sources.append(template["website_title"])
print('selected_sources: ', selected_sources)


webscraper = classes.webscraper(debug=debug_on, cookie_browser="firefox")


desired_fields = ["jobadvert", "id", "jobDescription",
                  "importDate", "date", "modifiedBy"]


def get_vacancy_payloads(skips, vacancy_search_limit=1000):
    time.sleep(1)
    vacancy_api_url = "https://api.jobs4contractors.co.uk/api/j4cjob?skip=" + skips + "&take=" + str(vacancy_search_limit)
    vacancy_payloads = webscraper.api_get_dictionaries_from_json(
        vacancy_api_url, desired_fields)
    return vacancy_payloads

try:
    for i in range(5,100):
        vacancy_payloads = get_vacancy_payloads(skips=str(i*1000), vacancy_search_limit=100)
        if len(vacancy_payloads) == 0:
        
            for k in range(10):
                vacancy_payloads = get_vacancy_payloads(skips=str((i-1)*1000 + k*100), vacancy_search_limit=100)
                if len(vacancy_payloads) == 0:
                    for y in range(10):
                        vacancy_payloads = get_vacancy_payloads(skips=str((i-1)*1000 + (k-1)*100 + y*10), vacancy_search_limit = 10)
                        if len(vacancy_payloads) == 0:
                            skips = str(((i-1)*1000 + (k-1)*100 + (y-1)*10) - 1000)
                            

                            class found_skips(Exception):
                                pass
                            raise found_skips()
except found_skips:
    print('skips: ', skips)
    pass

if override_skips == True:
    print("overriding skips - ")
    skips = skips_override
    print('skips: ', skips)

vacancy_payloads = get_vacancy_payloads(skips, vacancy_search_limit=1000)
vacancy_payloads = list(reversed(vacancy_payloads))  # most recent first
print(vacancy_payloads)


job_descriptions_added = 0
for vacancy_number, vacancy in enumerate(vacancy_payloads):
    print('vacancy_number: ', vacancy_number)

    if vacancy["modifiedBy"] == "Description Updater":
        print("vacancy already modified, continuing")
        continue
    if vacancy_number < vacancy_start_from:
        continue
    if vacancy["jobDescription"] == None:
        pass
    else:
        print("Other user has already imported descriptions, continuing")
        continue


    job_url = vacancy["jobadvert"]
    print('job_url: ', job_url)

    with requests.Session() as s: 
        
        try:
            r = requests.get(job_url, timeout=10)
        except requests.exceptions.Timeout as err: 
            print(err, "continuing")
            continue
        plain_text = r.text
        soup = BeautifulSoup(plain_text, "lxml")
        time.sleep(3)
        #try:
        if job_url.find("suneese") != -1:
            try:
                url_redirect = plain_text.split("url=")[1].split('"')[0] #vacancy_url within sunnesse html
            except IndexError:
                continue    
        else:
            url_redirect = job_url    
        #except:
        #    print('url_redirect problem: ', url_redirect)
        #    continue    
        known_source = False
        if scrape_selected_sources == True:
            for selected_source in selected_sources:
                if url_redirect.find(selected_source) != -1:
                    known_source = True

            if known_source == True:
                pass
            else:
                print("unknown source - ", url_redirect, " continuing...")            
                continue
        
        if ignore_selected_sources == True:
            try:
                for source_to_ignore in sources_to_ignore:
                    if url_redirect.find(source_to_ignore) != -1:
                        print('ignoring source - ', source_to_ignore)

                        class ignoreSourceError(Exception):
                            pass
                        raise ignoreSourceError()
                        break
            except ignoreSourceError:
                continue



          
        try:
            soup, plain_text = webscraper.get_soup(url_redirect, return_plain_text=True)
        except requests.exceptions.ConnectionError as e:
            print("connection_error, continuing")
            continue
        
    
        try:
            job_description, job_expired = vacancy_scrape.scrape(url_redirect, soup)
            print(job_description)
        except:
            print("scrape failed")
            continue

        if job_expired == True:
            print('job_expired: ', job_expired, " continuing")   
            continue
        else:
            pass

        job_description = edit_docx.depersonalise_via_regex(job_description)
        #job_description = wrap(job_description, 70)


        post_url = r"https://api.jobs4contractors.co.uk/api/j4cjob"
        job_payload = {"id": vacancy["id"], "jobDescription" : job_description}
        print('job_payload: ', job_payload)

        if post_job == True:
            webscraper.api_post_payload(post_url, job_payload, put=True)
            job_descriptions_added += 1
        else:
            pass
                                  




"""
        def find_str(s, char):
            index = 0

            if char in s:
                c = char[0]
                for ch in s:
                    if ch == c:
                        if s[index:index+len(char)] == char:
                            return index

                    index += 1

            return -1
        
        term_to_find = "longer available"# OR EXPIRED
        available_index = find_str(plain_text, term_to_find) #if = -1, no substrings found
        print("available found at index ", available_index)
        if available_index != -1:
            print("substring ", term_to_find, " found - ", plain_text[available_index-20:available_index+20] )



#SOURCE URL MANAGEMENT
new_sources_found = []
if test_particular_source == True:
    source_to_ignore_found = False
    for source_to_ignore in sources_to_ignore:
        if url_redirect.find(source_to_ignore) != -1:
            source_to_ignore_found = True
            pass
        else:
            print("link from source being tested - vacancy number", x)
            print("source_url = ", url_redirect)
            pass
    if source_to_ignore_found == True:
        continue
    else:
        print("new source found - url_redirect")
        new_sources_found.append(url_redirect)
        pass
"""
                



    


job_descriptions_added = 0
for vacancy_number, vacancy in enumerate(vacancy_payloads):
    print('vacancy_number: ', vacancy_number)

    if vacancy["modifiedBy"] == "Description Updater":
        print("vacancy already modified, continuing")
        break
    if vacancy_number < vacancy_start_from:
        continue
    if vacancy["jobDescription"] == None:
        pass
    else:
        print("Other user has already imported descriptions, continuing")
        continue


    job_url = vacancy["jobadvert"]
    print('job_url: ', job_url)

    with requests.Session() as s: 
        
        try:
            r = requests.get(job_url, timeout=10)
        except requests.exceptions.Timeout as err: 
            print(err, "continuing")
            continue
        plain_text = r.text
        soup = BeautifulSoup(plain_text, "lxml")
        time.sleep(3)
        #try:
        if job_url.find("suneese") != -1:
            try:
                url_redirect = plain_text.split("url=")[1].split('"')[0] #vacancy_url within sunnesse html
            except IndexError:
                continue    
        else:
            url_redirect = job_url    
        #except:
        #    print('url_redirect problem: ', url_redirect)
        #    continue    
        known_source = False
        if scrape_selected_sources == True:
            for selected_source in selected_sources:
                if url_redirect.find(selected_source) != -1:
                    known_source = True

            if known_source == True:
                pass
            else:
                print("unknown source - ", url_redirect, " continuing...")            
                continue
        
        if ignore_selected_sources == True:
            try:
                for source_to_ignore in sources_to_ignore:
                    if url_redirect.find(source_to_ignore) != -1:
                        print('ignoring source - ', source_to_ignore)

                        class ignoreSourceError(Exception):
                            pass
                        raise ignoreSourceError()
                        break
            except ignoreSourceError:
                continue



          
        try:
            soup, plain_text = webscraper.get_soup(url_redirect, return_plain_text=True)
        except requests.exceptions.ConnectionError as e:
            print("connection_error, continuing")
            continue
        
    
        try:
            job_description, job_expired = vacancy_scrape.scrape(url_redirect, soup)
            print(job_description)
        except:
            print("scrape failed")
            continue

        if job_expired == True:
            print('job_expired: ', job_expired, " continuing")   
            continue
        else:
            pass

        post_url = r"https://api.jobs4contractors.co.uk/api/j4cjob"
        job_payload = {"id": vacancy["id"], "jobDescription" : job_description}
        print('job_payload: ', job_payload)

        if post_job == True:
            webscraper.api_post_payload(post_url, job_payload, put=True)
            job_descriptions_added += 1
        else:
            pass
                                  




"""
        def find_str(s, char):
            index = 0

            if char in s:
                c = char[0]
                for ch in s:
                    if ch == c:
                        if s[index:index+len(char)] == char:
                            return index

                    index += 1

            return -1
        
        term_to_find = "longer available"# OR EXPIRED
        available_index = find_str(plain_text, term_to_find) #if = -1, no substrings found
        print("available found at index ", available_index)
        if available_index != -1:
            print("substring ", term_to_find, " found - ", plain_text[available_index-20:available_index+20] )



#SOURCE URL MANAGEMENT
new_sources_found = []
if test_particular_source == True:
    source_to_ignore_found = False
    for source_to_ignore in sources_to_ignore:
        if url_redirect.find(source_to_ignore) != -1:
            source_to_ignore_found = True
            pass
        else:
            print("link from source being tested - vacancy number", x)
            print("source_url = ", url_redirect)
            pass
    if source_to_ignore_found == True:
        continue
    else:
        print("new source found - url_redirect")
        new_sources_found.append(url_redirect)
        pass
"""
                
