import csv


def csv_to_dict_list(csv_file_path: str):
    data_list = []
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            data_list.append(dict(row))
    return data_list

def dict_list_to_file(csv_file_path: str,data_list: list[dict]):
    with open(csv_file_path, mode='w', encoding='utf-8', newline='') as csv_file:
        fieldnames = data_list[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_list)