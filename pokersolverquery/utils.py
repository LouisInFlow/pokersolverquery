
def nth_occurence(x, search,  n):
    found_indecies = [i for i, value in enumerate(x) if value == search]
    if n >= len(found_indecies):
        return None
    else:
        return found_indecies[n]

