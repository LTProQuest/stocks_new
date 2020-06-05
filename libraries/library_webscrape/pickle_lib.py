import pickle


def append_pickle(pickle_file, element_to_append,print_pickle=False):
    try:
        with open(pickle_file, "rb") as f:
            pickle_array = pickle.load(f)
    except:
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

 