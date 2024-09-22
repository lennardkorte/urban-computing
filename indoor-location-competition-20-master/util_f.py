from os import path, getenv
from glob import iglob

def data_floors(data_dir):
    for res in iglob(path.join(data_dir, '*', '*')):
        if not path.isdir(res):
            continue
        head, floor = path.split(res)
        _, site = path.split(head)
        yield site, floor

