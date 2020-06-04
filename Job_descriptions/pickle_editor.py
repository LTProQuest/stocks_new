import sys
path = r"C:\Users\luket\Desktop\test space\libraries"
sys.path.insert(0, path)

from library_webscrape import pickle_lib
import pickle

pickle_file = "vacancy_source_scrape_pickle.pkl"
with open(pickle_file, "rb") as f:
    pickle_array = pickle.load(f)

#append_dict = {"website_title":"linkedin","selector_attribute":"class","selector_attribute_value":"description__text"}
#pickle_lib.append_pickle(pickle_file, append_dict, print_pickle=True)  