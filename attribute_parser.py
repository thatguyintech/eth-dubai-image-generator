from os import path, walk
from json import dumps

def weights(length):
    return [len(x) for x in split(range(100), length)]

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

# 1. parsing script
def parse_attributes_directory(dir_path):
    attributes = {}
    directories = next(walk(dir_path, (None, None, [])))[1]  # [] if no file
    for category in directories:
        attributes[category] = {}
        groups = next(walk("{}/{}".format(dir_path, category), (None, None, [])))[1]
        for group in groups:
            filepaths = next(walk("{}/{}/{}".format(dir_path, category, group), (None, None, [])))[2]
            files = ["{}".format(filepath[:len(filepath)-4]) for filepath in filepaths] # remove the .png
            attributes[category][group] = {
                "files": sorted(files, key=str.casefold),
                "weights": weights(len(files))
            }
    return attributes

dir_path = "./attributes"

def write_to_attributes_config():
    f = open("attributes_config.json", "w")
    f.write(dumps(parse_attributes_directory(dir_path), sort_keys=True, indent=4))
    f.close()


print("writing to attributes_config.json ..")

write_to_attributes_config()

# print(dumps(parse_attributes_directory("/Users/alberthu/Documents/co/nft-image-generator/attributes"), sort_keys=False, indent=4))