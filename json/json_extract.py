import json

DIR_NAME = "json_patterns/"
FILE_LIST_NAME = "names.txt"
OUTPUT_NAME = "all_patterns.json"

names = []
patterns = []


with open(FILE_LIST_NAME, 'r') as fh:
    line = fh.readline()
    while line != "":
        line = line.rstrip()
        names.append(line)
        line = fh.readline()

for name in names:
    with open(DIR_NAME + name, 'r') as fh:
        s = fh.read()
        x = json.loads(s)
        if x["life"] == [[0, 0, 0],
                         [0, 1, 0],
                         [0, 0, 0]] or len(x["title"]) > 20:
            pass
        else:
            patterns.append(x)

with open(OUTPUT_NAME, "w") as fh:
    s = json.dumps(patterns)
    fh.write(s)
