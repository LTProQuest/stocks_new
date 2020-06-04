import pickle


def append_pickle(pickle_file, element_to_append,print_pickle=False):
    try:
        with open(pickle_file, "rb") as f:
            pickle_array = pickle.load(f)
    except:
        pickle_array = []
        with open(pickle_file, "wb") as f:
            pickle.dump(pickle_array, f)

    pickle_array.append(element_to_append)
    
    with open(pickle_file, "wb") as f:
        pickle.dump(pickle_array, f)

    if print_pickle == True:
        print("pickle: ", pickle_array)