import pickle

saved_array = "test"

pickle_file = "test.pkl"

input_array = [0, 1, 2, 3]

try:
    with open(pickle_file, "rb") as f:
        pickle_array = pickle.load(f)
except:
    pass

pickle_array = [0, 1]
for x in pickle_array:
    print(x)
    for y in input_array:
        if x == y:
            continue
        else:
            pickle_array.append(y)
            continue

with open(pickle_file, "wb") as f:
    pickle.dump(pickle_array, f)

