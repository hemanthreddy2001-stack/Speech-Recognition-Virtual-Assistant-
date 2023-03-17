import csv
def find_phNo(name):
    with open("contacts.csv", 'r') as file:
            csvfile=csv.DictReader(file)
            for r in csvfile:
                    if name.lower()==dict(r)['Names']:
                            return dict(r)['Phone_numbers']
    return None
print(find_phNo(input()))

