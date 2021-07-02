import json

names = []
patterns = []

with open('names.txt', 'r') as fh:
    line = fh.readline()
    while line != "":
        line = line.rstrip()
        names.append(line)
        line = fh.readline()

for name in names:
    with open(name, 'r') as fh:
        s = fh.read()
        x = json.loads(s)
        patterns.append([x])

with open("names.json", "w") as fh:
    s = json.dumps(patterns)
    fh.write(s)
