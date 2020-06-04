import numpy

input_array = [0, 1, 2, 3]

pickle_array = [0, 1]


to_add = set(input_array) - set(pickle_array)

print(to_add)

pickle_array += to_add

print(pickle_array)
