import json
import datetime


def get_files(cat):
    today = datetime.date.today()
    tg_file_date = today + datetime.timedelta(days=cat['tigo']['day'])
    ot_file_date = today + datetime.timedelta(days=cat['other']['day'])
    tigo_date = tg_file_date.strftime(cat['tigo']['dateFmt'])
    other_date = ot_file_date.strftime(cat['other']['dateFmt'])
    tigo_dir = cat['tigo']['directory']
    other_dir = cat['other']['directory']
    tigo_tmpl = cat['tigo']['tmpl']
    other_tmpl = cat['other']['tmpl']
    tigo_file = f'{tigo_dir}{tigo_tmpl.replace("[DATE]", tigo_date)}'
    other_file = f'{other_dir}{other_tmpl.replace("[DATE]", other_date)}'
    return (tigo_file, other_file, tg_file_date, ot_file_date)
