import json

names = []
patterns = []
DIR_NAME = "json_patterns/"
FILE_LIST_NAME = "names.txt"
OUTPUT = "patterns.json"


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
        patterns.append([x])

with open(OUTPUT, "w") as fh:
    s = json.dumps(patterns)
    fh.write(s)
