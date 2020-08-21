import json
import pysftp

with open('credentials.json') as creds_file:
    creds = json.load(creds_file)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    creds['cnopts'] = cnopts
    print(creds)
    with pysftp.Connection(**creds) as sfpt:
        print('Connected...')
