# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 20:01:40 2018

@author: luket
"""
import re
import win32com.client, datetime, time

class outlook_object:
    outlook= None
    inbox = None
    default_email = "luke.turner@pro-quest.co.uk"
    def __init__(self, email=default_email, debug_mode=False):
        self.debug_mode = debug_mode
        self.email = email
        global outlook
        global inbox
        outlook=win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = outlook.GetDefaultFolder(6)


    #identifies Folder_name as object
    def print_inbox_sub_folders(self):
        folders = inbox.Folders
        for i, folder in enumerate(folders):
            print(i, folder.Name)
            
    def send_email(self, recipient_email, result_string):
        if recipient_email == None:
            recipient_emaail = self.email    
        now = datetime.datetime.today()
        o = win32com.client.Dispatch("Outlook.Application")
        Msg = o.CreateItem(0)
        Msg.Importance = 0
        Msg.SentOnBehalfOfName = self.email
        Msg.ReadReceiptRequested = False
        Msg.OriginatorDeliveryReportRequested = False

        Msg.Subject = 'Results ' + str(now)
        Msg.HTMLBody = result_string
        Msg.To = recipient_email
        Msg.CC = ""
        Msg.BCC = ""
        Msg.Send()

    def get_folder_by_name(self, folder_name):
        folders = inbox.Folders
        for folder in folders:
            if folder.Name == folder_name:
                found_folder = folder
                break
        try:    
            return found_folder
        except:
            exception_message = ("folder not found \n available folders: \n")
            for folder in folders:
                exception_message += folder.Name + "\n"
            print(exception_message)        

    def get_last_message_body(self, folder):
        messages = folder.Items
        message = messages.GetLast()
        return message.body         


    def search_six_digit_code(self, email_body):
        six_digit_regex = re.compile(r"[0-9]{6}")
        verification_code = re.search(six_digit_regex, email_body, flags=0)[0]
        return verification_code



def get_cv_library_verification_code():
    print("waiting for verfication email")
    time.sleep(30) #wait for email
    outlook = outlook_object()
    folder = outlook.get_folder_by_name("cv_library_verification_codes")
    verification_email_text = outlook.get_last_message_body(folder)
    verification_code = outlook.search_six_digit_code(verification_email_text)
    print("verification code: ", verification_code)
    return verification_code


class WebscrapeLogger(outlook_object):
    payload_log_limit = 3
    
    def __init__(self, send_email_enabled=False, payload_log=[]):   
        self.send_email_enabled = send_email_enabled
        self.payload_log = payload_log
            
    def append_payload_to_logging(self, payload, scrape_attempts):
        if scrape_attempts < webscrapingLogger.payload_log_limit: 
            self.payload_log.append(payload)

    def email_or_print_log(self, scrape_attempts, error_message):
        if email_results == True:
            outlook.email_string_to_outlook( "Attempts: " + str(scrape_attempts) +  "\n"*4 + str(self.payload_log) + "\n*4 +  Errors: " + str(error_message))
        else:
            print("Attempts: " + {} + "\n"*4 + {} + "\n*4  Errors: " + {}).format(str(scrape_attempts), str(self.payload_log), error_message)   
