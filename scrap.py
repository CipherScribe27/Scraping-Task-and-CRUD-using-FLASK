import requests
from bs4 import BeautifulSoup
import csv
import re
from prettytable import PrettyTable

def scrape_website():
    i = 0
    
    csv_file = 'vulnerabilities.csv'
    fieldnames = ['Vulnerability', 'Published Date' , 'Severity']    
    with open(csv_file, 'a', newline='') as file:
        if file.tell() == 0:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
        while True:
            url = f"https://www.rapid7.com/db/?q=&type=nexpose&page={i}"
            response = requests.get(url)

            if response.status_code != 200:
                print(f"Failed to retrieve the website. Error code: {response.status_code}")
                break

            soup = BeautifulSoup(response.content, 'html.parser')

            vulnerability = soup.find_all('div',{'class':'resultblock__info-title'})
            publish_severity = soup.find_all('div',{'class':'resultblock__info-meta'})
            v = str(vulnerability)
            s = str(publish_severity)
        
            pattern1 = r'<div class="resultblock__info-title">\s*(.*?)\s*</div>'
            pattern2 = r'Published:\s*(.*?)\s*\| Severity:\s*(\d+)'
            matches1 = re.findall(pattern1, v)
            matches2 = re.findall(pattern2, s)

            table = PrettyTable(fieldnames)
            for vuln, pub_severity in zip(matches1, matches2):
                pub_date, severity = pub_severity
                table.add_row([vuln, pub_date, severity])

            print(table)
            writer = csv.writer(file)
            writer.writerows(table)

            i += 1

    print("Data extraction complete. The data is stored in vulnerabilities.csv")

scrape_website()




# import requests
# from bs4 import BeautifulSoup
# import csv
# import re

# def scrape_website():
#     i = 0
    
#     csv_file = 'vulnerabilities.csv'
#     fieldnames = ['Vulnerability', 'Published Date' , 'Severity']    
#     with open(csv_file, 'a', newline='') as file:
#         if file.tell() == 0:
#             writer = csv.DictWriter(file, fieldnames=fieldnames)
#             writer.writeheader()
#         while True:
#             url = f"https://www.rapid7.com/db/?q=&type=nexpose&page={i}"
#             response = requests.get(url)

#             if response.status_code != 200:
#                 print(f"Failed to retrieve the website. Error code: {response.status_code}")
#                 break
                


#             soup = BeautifulSoup(response.content, 'html.parser')

#             vulnerability = soup.find_all('div',{'class':'resultblock__info-title'})
#             publish_severity = soup.find_all('div',{'class':'resultblock__info-meta'})
#             v = str(vulnerability)
#             s = str(publish_severity)
        
#             pattern1 = r'<div class="resultblock__info-title">\s*(.*?)\s*</div>'
#             pattern2 = r'Published:\s*(.*?)\s*\| Severity:\s*(\d+)'
#             matches1 = re.findall(pattern1, v)
#             matches2 = re.findall(pattern2, s)

#             for vulnerability, publish_severity in zip(matches1,matches2):
#                 writer.writerow({'Vulnerability':vulnerability,'Published Date':publish_severity[0],'Severity':publish_severity[1]})
                
#             i += 1

#     print("Data extraction complete. The data is stored in vulnerabilities.csv")

# scrape_website()


