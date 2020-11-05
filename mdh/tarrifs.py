import csv
lookup = []
lookup_other = []


def get_co_fee_other(orig_amt):
    for band in lookup_other:
        lower, upper, co = band
        if orig_amt >= lower and orig_amt <= upper:
            return co
    return 0


def get_co_fee(amount):
    for band in lookup:
        lower, upper, co = band
        orig_amt = amount - co
        if orig_amt >= lower and orig_amt <= upper:
            return (orig_amt, co)
    return (orig_amt, 0)


def read_tarrifs():
    with open("inputs/tarrif.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            lookup.append((int(row['LOWER']), int(row['UPPER']), int(row['CO'])))


def read_tarrifs_other():
    with open("inputs/tarrif_old.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            lookup_other.append((int(row['LOWER']), int(row['UPPER']), int(row['CO'])))


if __name__ == "__main__":
    read_tarrifs()
    read_tarrifs_other()
    # print(lookup)
    output = []
    with open("inputs/mdh_trans.csv") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            org_amt, co = get_co_fee(int(row['transaction_amount']))
            output.append({
                'trans_date': row['trans_date'],
                'transaction_amount': row['transaction_amount'],
                'co_fee': co,
                'org_amount': org_amt,
                'co_fee_other': get_co_fee_other(org_amt)
            })
    with open("mdh/mdh_output.csv", 'w', newline='') as csv_file:
        header = ['trans_date', 'transaction_amount', 'co_fee', 'org_amount', 'co_fee_other']
        writer = csv.DictWriter(csv_file, header)
        writer.writeheader()
        writer.writerows(output)
