import json
import pysftp

with open('credentials.json') as creds_file:
    creds = json.load(creds_file)
    print(creds)
    with pysftp.Connection(**creds) as sfpt:
        print('Connected...')
