import sys
path = r"C:\Users\luket\Desktop\test_space\libraries"
sys.path.insert(0, path)

from library_webscrape import pickle_lib
import pickle

pickle_file = "selected_sources.pkl"
pickle_lib.create_blank_pickle(pickle_file)

#append_dict = {"website_title":"linkedin","selector_attribute":"class","selector_attribute_value":"description__text"}
#pickle_lib.append_pickle(pickle_file, append_dict, print_pickle=True)  


string = """  
    if url.find("indeed.co.uk") != -1:
        job_description = soup.find("div", {"class":"jobsearch-jobDescriptionText"}).getText()   
        try: 
            job_expired_warning = soup.find('h3', {"class":"icl-Alert-headline"}).getText()
        except:
            pass  
    elif url.find("linkedin.com") != -1:
        job_description = soup.find('div', {"class":{"description__text description__text--rich"}})
        job_expired_warning = soup.find('span', {"class":"inline-notification__text"}).getText()        
    
    elif url.find("irishjobs") != -1:
        job_description = soup.find('div', {"class":"job-details"})
        try:    
            job_expired_warning = soup.find('p', {"class":{"expiredClass alert-expired"}}).getText()
        except:
            pass
    elif url.find("cityjobs") != -1: #Totaljobs
        job_description = soup.find('div', {"id":"job-description"})
        
    elif url.find("workinstartups") != -1:
        job_description = soup.find('div', {"id":"job-description"})
        
    elif url.find("independentjobs") != -1:
        job_description = soup.find('div', {"class":"block fix-text job-description"})
        try:
            job_expired_warning = soup.find('p', {"class":"message message--warning icon-before"}).getText()
        except:
            pass
    elif url.find("simplyhired") != -1:
        job_description = soup.find('div', {"class":{"viewjob-description ViewJob-description"}})
    
    elif url.find("jobstoday") != -1:
        job_description = soup.find('div', {"class":"block fix-text job-description"})
        try:
            job_expired_warning = soup.find('p', {"class":"message message--warning icon-before"}).getText()
        except:
            pass
    elif url.find("leaps.emid") != -1:
        job_description = soup.find('div', {"class":"job_description"})
        
    elif url.find("postjobsfree") != -1:
        job_description = soup.find('div', {"id":"descriptionDiv"})
            
    elif url.find("totaljobs") != -1:
        job_description = soup.find('div', {"class":"job-description"})
"""



template_array = []
try:
    for code_block in string.split("elif"):
        scrape_template = {"selector_found": True}
        for line in code_block.splitlines():
            if line.find("url.find") != -1:
                scrape_template["website_title"] = line.split('find("')[1].split('"')[0]
            if line.find("job_description") != -1:
                description_template = {}
                description_template["attribute"] = line.split('{"')[1].split('"')[0]
                try:
                    description_template["attribute_value"] =  line.split('":"')[1].split('"')[0]
                except:
                    description_template["attribute_value"] =  line.split(':{"')[1].split(' ')[0]
                    

                scrape_template["description_selector"] = description_template
            if line.find("expired_warning") != -1:
                expiry_template = {}
                expiry_template["parent"] = line.split("find('")[1].split("'")[0]
                expiry_template["attribute"] = line.split('{"')[1].split('"')[0]
                try:
                    expiry_template["attribute_value"] = line.split('":"')[1].split('"')[0]
                except:
                    expiry_template["attribute_value"] = line.split('{"')[1].split(' ')[0]
                scrape_template["expired_selector"] = expiry_template

        pickle_lib.append_pickle(pickle_file, scrape_template)    
except:
    print(line)
                




