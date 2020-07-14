import pickle


def append_pickle(pickle_file, element_to_append,print_pickle=False):
    try:
        with open(pickle_file, "rb") as f:
            pickle_array = pickle.load(f)
    except FileNotFoundError:
        print("pickle not found - '", pickle_file, "' created")
        pickle_array = []
        with open(pickle_file, "wb") as f:
            pickle.dump(pickle_array, f)

    pickle_array.append(element_to_append)
    
    with open(pickle_file, "wb") as f:
        pickle.dump(pickle_array, f)

    if print_pickle == True:
        print("pickle: ", pickle_array)


def create_blank_pickle(pickle_file):
    pickle_array = []
    with open(pickle_file, "wb") as f:
        pickle.dump(pickle_array, f)

def load_pickle(pickle_file):
    with open(pickle_file, "rb") as f:
        pickle_array = pickle.load(f)
    return pickle_array



def create_copy_pickle(pickle_file):
    with open(pickle_file, "rb") as f:
        pickle_array = pickle.load(f)
    
    with open(pickle_file + "_original", "wb") as f:
        pickle.dump(pickle_array, f)

 
def replace_dictionary(pickle_file, indentifier_key, identifier_value, new_dict):
    array = load_pickle(pickle_array)
    for index,element in enumerate(array):
        if array[indentifier_key] == identifier_value:
            array[index] = new_dict
        else:
            pass
       
def save_pickle(pickle_file, pickle_array):
    with open(pickle_file, "wb") as f:
            pickle.dump(pickle_array, f)

# #editor for vacancy scrape templates
# scrape_template_pickle = r"C:\Users\luket\Desktop\test_space\Job_descriptions\vacancy_source_scrape_pickle.pkl"
# indentifier_key = "website_title"
# identifier_value = ""
# new_dict = ""
# replace_dictionary(scrape_template_pickle, indentifier_key, identifier_value, new_dict)

            