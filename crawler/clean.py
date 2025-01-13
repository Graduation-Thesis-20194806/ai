import csv
import os

headers = ["id", "owner","repo","number","title","body","state","created_at","updated_at","closed_at"]
def csv_to_dict_list(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data
def clean_body_prestashop(text: str):
    lines = text.splitlines()
    result = None
    for i in range(0,len(lines)):
        line = lines[i].strip().lower()
        if line.startswith('##'):
            if 'describe' in line and 'bug' in line:
                result = ""
                for j in range(i+1,len(lines)):
                    if lines[j].strip().startswith('##'):
                        break
                    result += (lines[j]+'\n')
            if 'expected' in line and 'behavior' in line:
                if not result:
                    result = ""
                    for j in range(i+1,len(lines)):
                        if lines[j].strip().startswith('##'):
                            break
                        result += (lines[j]+'\n')
    return result

def clean_body_prestashop_2(text: str):
    lines = text.splitlines()
    for i in range(0, len(lines)):
        line = lines[i].strip().lower()
        if line.startswith('| description? |'):
            return line[len('| description? |'):-1]
        if line.startswith('| description?  |'):
            return line[len('| description?  |'):-1]
        if line.startswith('| description?      | '):
            return line[len('| description?      | '):-1]
    return None

def clean_body_prestashop_3(text: str):
    lines = text.splitlines()
    result = None
    for i in range(0, len(lines)):
        line = lines[i].strip().lower()
        if line.startswith('**'):
            if 'describe' in line and 'bug' in line:
                result = ""
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().startswith('**'):
                        break
                    result += (lines[j] + '\n')
            if 'expected' in line and 'behavior' in line:
                if not result:
                    result = ""
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip().startswith('**'):
                            break
                        result += (lines[j] + '\n')
    return result

def clean_file_prestashop():
    file_path = os.path.join('crawler', 'result', f"PrestaShop_PrestaShop_raw_5.csv")
    clean_path = os.path.join('crawler', 'result', f"PrestaShop_PrestaShop_cleaned.csv")
    raw_path = os.path.join('crawler', 'result', f"PrestaShop_PrestaShop_raw_6.csv")

    data = csv_to_dict_list(file_path)
    for row in data:
        result = clean_body_prestashop_3(row['body'])
        if result:
            row['body'] = result
            with open(clean_path, mode='a', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writerow(row)
        elif row['body']:
            with open(raw_path, mode='a', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writerow(row)

def clean_body_magento(text: str):
    lines = text.splitlines()
    result = None
    for i in range(0, len(lines)):
        line = lines[i].strip().lower()
        if line.startswith('##'):
            if 'expected' in line and 'result' in line:
                if not result:
                    result = ""
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().startswith('##'):
                        break
                    if lines[j].strip().startswith('<!--- '):
                        continue
                    result += (lines[j] + '\n')
            if 'actual' in line and 'result' in line:
                if not result:
                    result = ""
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip().startswith('##'):
                            break
                        if lines[j].strip().startswith('<!--- '):
                            continue
                        result += (lines[j] + '\n')
    return result
def clean_body_magento_2(text: str):
    lines = text.splitlines()
    result = None
    for i in range(0, len(lines)):
        line = lines[i].strip().lower()
        if line.startswith('##'):
            if 'description' in line:
                result = ""
                for j in range(i + 1, len(lines)):
                    if lines[j].strip().startswith('##'):
                        break
                    if lines[j].strip().startswith('<!--- '):
                        continue
                    result += (lines[j] + '\n')
    return result
def clean_file_magento():
    file_path = os.path.join('crawler', 'result', f"magento_magento2_raw_3.csv")
    clean_path = os.path.join('crawler', 'result', f"magento_magento2_cleaned.csv")
    raw_path = os.path.join('crawler', 'result', f"magento_magento2_raw_4.csv")

    data = csv_to_dict_list(file_path)
    for row in data:
        result = clean_body_magento_2(row['body'])
        if result:
            row['body'] = result
            with open(clean_path, mode='a', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writerow(row)
        elif row['body']:
            with open(raw_path, mode='a', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writerow(row)
def clean_body_woocommerce(text: str):
    lines = text.splitlines()
    result = None
    for i in range(0,len(lines)):
        line = lines[i].strip().lower()
        if line.startswith('##'):
            if 'issue' in line and 'description' in line:
                result = ""
                for j in range(i+1,len(lines)):
                    if lines[j].strip().startswith('##'):
                        break
                    result += (lines[j]+'\n')
            if 'acceptance' in line and 'criteria' in line:
                if not result:
                    result = ""
                    for j in range(i+1,len(lines)):
                        if lines[j].strip().startswith('##'):
                            break
                        result += (lines[j]+'\n')
    return result
def clean_file_woocommerce():
    file_path = os.path.join('crawler', 'result', f"woocommerce_woocommerce_raw.csv")
    clean_path = os.path.join('crawler', 'result', f"woocommerce_woocommerce_cleaned.csv")
    raw_path = os.path.join('crawler', 'result', f"woocommerce_woocommerce_raw_2.csv")

    data = csv_to_dict_list(file_path)
    for row in data:
        result = clean_body_woocommerce(row['body'])
        if result:
            row['body'] = result
            with open(clean_path, mode='a', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writerow(row)
        elif row['body']:
            with open(raw_path, mode='a', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writerow(row)
if __name__ == "__main__":
    clean_file_woocommerce()