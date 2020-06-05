''''
TO DO 
initial search vacancy may differ to much to add to the class itself 

actually may be cleaner that each site is defined by subclasses
as the session needs to be initiated
maybe doesnt matter multiple sessions
'''
import requests
from random import randint
import time
import re
import json
import base64
import random

from PyPDF2 import PdfFileReader, PdfFileWriter



import browser_cookie3 as browsercookie
from bs4 import BeautifulSoup


#problem - if add new settings input then those not classified relative to the default settings dont remain
class webscraper:
    s = requests.session()
    
    def __init__(self, requests_per_minute = 30, current_url=None, base_url=None, values = None, debug = False, cookie_browser = "chrome", cookies = None): 
        
        default_settings = {
            "download_cv": False,
            "send_logger_results_to_email": False,  # when False, prints results to terminal
            "download_storage": None,
        }


        


        self.requests_per_minute = requests_per_minute
        self.current_url = current_url
        self.base_url = base_url
        if values == None:
            self.values = default_settings
        else:
            self.values = values
        self.debug = debug
       
        self.cookie_browser = cookie_browser
        if cookie_browser == "chrome":
            cj = browsercookie.chrome()
        if cookie_browser == "firefox":
            cj = browsercookie.firefox()
        self.cookies = cj    


    def sleep(self):
        requests_per_minute = 30
        lower_wait_limit = int((60/(self.requests_per_minute))*0.8)
        upper_wait_limit = int((60/(self.requests_per_minute))*1.2)
        time.sleep(randint(lower_wait_limit,upper_wait_limit))
        
    def get_soup(self, url, find_in_soup=None, return_plain_text=False):
        
        sleep_value = random.randint(5,15)
        time.sleep(sleep_value)
        r = webscraper.s.get(url, cookies=self.cookies)
        plain_text = r.text    
        soup = BeautifulSoup(plain_text,   "lxml")
        self.current_url = url
        webscraper.sleep(self)
        if self.debug == True:
            print("current_url - ", url)
            #print("start of page soup: ", str(soup)[0:1000], "\n"*4, "source URL: ", url) #prints first number of characters of soup
            #if find_in_soup not None: *Task generate portion of soup about keywords
            #    soup.find
            #    print("soup search for ", find_in_soup, )

        base_url = url.split("/")[0:3]
        base_url = "/".join(base_url)
        self.base_url = base_url
        if return_plain_text == True:
            return soup,plain_text
        return soup

    def get_candidate_page_soup(self, url):
        webscraper.get_soup(url)
        webscraper.sleep(self)
        return soup
    
    def find_candidate_urls(self):
        pass
   
    def find_attribute_list_get_payload(self,soup):
            criteria = soup.findAll("div", {"class": ["vcvdp-left","vcvdj-left"]})
            info = soup.findAll("div", {"class": ["vcvdp-right","vcvdj-right"]})           
            payload = {}
            for i in range(len(criteria)):                                          
                try:
                    payload[criteria[i].getText()] = info[i].getText().split(">")[1].split("<")[0]
                except:
                    payload[criteria[i].getText()] = info[i].getText().split("<")[0].strip().replace("\n","").replace(" ","")
            if self.debug == True:
                print("candidate CV payload:", payload)
            return payload

    def get_download_path_from_partial_text(self, hyper_link_soup, hyper_link_text):

        """
        hyper_links = hyper_link_soup.findAll("a")
        print("hyperlinks found - ", len(hyper_links))
        for link in hyper_links:
            print(link)
            if link.get('href').find(hyper_link_text) != -1:
                download_path = self.base_url + link.get('href')
                break
        return download_path
        """
        return "hi"        

    def download_file_from_url(self, download_url, file_directory=None, depersonalise=False):
        if self.debug == True:
            print("download_url - ", download_url)
        file_directory = self.values["download_storage"]
        if self.values["download_cv"] == True:
            pass

        def get_filename_from_cd(cd):     
            if not cd:
                return None
            fname = re.findall('filename=(.+)', cd)
            if len(fname) == 0:
                return None
            return fname[0]
        response = webscraper.s.get(download_url, cookies=self.cookies ,allow_redirects=True)
        filename = get_filename_from_cd(response.headers.get('content-disposition'))
        if depersonalise == False:
            file_path = file_directory + "/" +  filename[1:-1]
        else:
            file_path = file_directory + "/" +  filename[1:-1].split("(")[1]
            


        with  open(file_path,'wb') as f:
            f.write(response.content)
        time.sleep(2)
        if file_path.endswith("pdf") == True:
            """
            print("pdf found")
            fin = open(file_path, 'rb')
            reader = PdfFileReader(fin)
            writer = PdfFileWriter()

            writer.appendPagesFromReader(reader)
            metadata = reader.getDocumentInfo()
            writer.addMetadata(metadata)

            # Write your custom metadata here:
            writer.addMetadata({
                '/Title': filename[1:-1].split("(")[1]
            })

            fout = open(file_path, 'ab') #ab is append binary; if you do wb, the file will append blank pages
            writer.write(fout)

            fin.close()
            fout.close()
            """
            from pdfrw import PdfReader, PdfWriter, PdfDict
            try:
                pdf_reader = PdfReader(file_path)
                metadata = PdfDict(Author='Someone', Title='PDF in Python')
                pdf_reader.Info.update(metadata)
                PdfWriter().write(file_path, pdf_reader)
            except:
                pass #in case no metadata to begin with        
        return file_path    

    def api_post_payload(self, api_url, payload, assign_response_as_variable = False, put=False):       
        with requests.Session() as s:
            
            if put == False:
                r = s.post(api_url ,json=payload,verify=False, headers = {'Content-type': 'application/json', 'Accept': 'text/plain'})
            else:
                r = s.put(api_url ,json=payload,verify=False, headers = {'Content-type': 'application/json', 'Accept': 'text/plain'})
            print(r.status_code)
            response = r.text
            if self.debug == True:
                print("posted payload: ", response)
            if assign_response_as_variable == True:
                return response    

    def api_get_response(self, api_url, print_reponse=False):       
        with requests.Session() as s:    
            r = s.get(api_url, verify=False, headers = {'Content-type': 'application/json', 'Accept': 'text/plain'})
            print(r.status_code)
            response = r.text
            if print_reponse == True:
                print(response)
            return response

    def api_get_dictionaries_from_json(self, api_url, desired_fields_dict):
        response = self.api_get_response(api_url)
        json_data = json.loads(response)
        payloads = []
        for line in json_data:
            payload = {}
            for key, value in line.items():
                for field in desired_fields_dict:
                    if field == key:
                        payload[key] = value     
            payloads.append(payload)

        #if self.debug == True:
        #    print("got payloads - 1st payload: ", payloads[0])
        return(payloads)     

    def encode_cv(self, file_path):
        """this app encodes cv to base64 and returns extension"""

        with open(file_path, "rb") as file:
                        
            encoded_string = base64.b64encode(file.read())
            #decoded_string = base64.b64decode(encoded_string).decode('utf-8', errors='ignore')               
            encoded_document =  str(encoded_string)[2:-1]
        return encoded_document
       
        
                            




