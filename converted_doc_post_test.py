import sys
import time
edited_document_storage = "storage/edited_cv_storage"


path = r"C:\Users\luket\Desktop\work\cv_library_workspace\libraries"
sys.path.insert(0, path)
from library_webscrape import classes, outlook, edit_docx, edit_pdf

webscraper = classes.webscraper(debug=True)
#desired_fields = ["title", "id", "jobType", "city"]

def get_vacancy_payloads():
    vacancy_api_url = "https://api.pro-quest.co.uk/api/importjobs/getlatest?sector=it&qty=1"
    vacancy_payloads = webscraper.api_get_dictionaries_from_json(vacancy_api_url, desired_fields)
    return vacancy_payloads
vacancy_payloads = get_vacancy_payloads()
#print(vacancy_payloads[0])  

payload = webscraper.api_get_response()

"""
payload = {
    "VacancyId": 767522,
    "NoMatch": False,
    "Town": "hayes",
    "County": "Middlesex",
    "MainPhone": "447807938521",
    "OptionalPhone": "447807938521",
    "Email": "ejazhameed2912@gmail.com",
    "Age": "55",
    "DateAvailable": "01-02-19",
    "CurrentJobTitle": "ElectronicRF Test software test web developer",
    "DesiredJobTitle": "software and hardware test",
    "JobType": "Contract Permanent Temporary",
    "WillingtoTravel": "Upto20miles",
    "WillingtoRelocate": "No",
    "UKDrivingLicence": "Yes",
    "ExpectedSalary": "25001-30000",
    "Name": "test",
    "DesiredIndustry": "Electronic",
    "MainSkills": "software test electronic test RF test, PCB test Set top box test  vb.netjunior web developer Web Based Cloud Testing Fault Management  Fault finding, Troubleshooting ",
    "CVFileExtension": "docx",
    "CVFile": "dGVzdA==",
    "DepersonalisedCVFile": "dGVzdA=="
    }




candidate_post_url = "https://api.pro-quest.co.uk/api/candidates/PostJobCandidate"

cv_file_path = r"C:\Users\luket\Desktop\work\cv_library_workspace\storage\cv_storage\Vijayaraghavan Kesariraman_14962042_cv-library.pdf"
edit_pdf.convert_pdf_to_docx(cv_file_path)
cv_file_path = cv_file_path.replace(".pdf", ".docx")
time.sleep(2)
texts_to_hide = [""]
edited_cv_file_path = edit_docx.docx_replace_multiple_strings(cv_file_path, texts_to_hide, edited_document_storage)
payload["DepersonalisedCVFile"] = webscraper.encode_cv(edited_cv_file_path)
payload["CVFile"] = webscraper.encode_cv(cv_file_path)

webscraper.api_post_payload(candidate_post_url, payload)


"""

