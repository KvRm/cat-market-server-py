def omit(d, keys):
    return {x: d[x] for x in d if x not in keys}