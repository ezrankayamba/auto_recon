import json
import pysftp
import pandas as pd

BASE_REMOTE_DIR = '/data/exchangefiles/'
with open('credentials.json') as creds_file:
    creds = json.load(creds_file)
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    creds['cnopts'] = cnopts
    print(creds)
    with pysftp.Connection(**creds) as sfpt:
        print('Connected...')
        f_name = f'tigo_disbursement_rpt_21082020_065354_001.csv'
        r_file = f'airtelmoney/AIRTEL/{f_name}'
        with sfpt.open(r_file) as csv_file:
            print(csv_file)
            data = pd.read_csv(csv_file)
            print(data.head())
