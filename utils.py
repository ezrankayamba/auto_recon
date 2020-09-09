import json
import datetime


def get_files(cat):
    today = datetime.date.today()
    yest = today - datetime.timedelta(days=cat['day'])
    tigo_date = yest.strftime(cat['tigo']['dateFmt'])
    other_date = yest.strftime(cat['other']['dateFmt'])
    tigo_dir = cat['tigo']['directory']
    other_dir = cat['other']['directory']
    tigo_tmpl = cat['tigo']['tmpl']
    other_tmpl = cat['other']['tmpl']
    tigo_file = f'{tigo_dir}{tigo_tmpl.replace("[DATE]", tigo_date)}'
    other_file = f'{other_dir}{other_tmpl.replace("[DATE]", other_date)}'
    return (tigo_file, other_file, yest)
