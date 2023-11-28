import requests
import json
import pprint
from bs4 import BeautifulSoup

BASE_URL = "https://www.auto-data.net"
brands_url = BASE_URL + "/en/allbrands"

brands_page = requests.get(brands_url)
soup = BeautifulSoup(brands_page.content, "html.parser")
brands_elements = soup.find_all("a", {"class": "marki_blok"})

specs_set = set()

for brand_elements in brands_elements:
    brand_name = brand_elements.find("strong")
    
    print('Parsing {}...'.format(brand_name.text.strip()))

    brand_url = brand_elements["href"]
    
    brand_page = requests.get(BASE_URL + brand_url)
    soup = BeautifulSoup(brand_page.content, "html.parser")
    models_elements = soup.find_all("a", {"class": "modeli"})

    for model_elements in models_elements:
        model_url = model_elements["href"]

        model_page = requests.get(BASE_URL + model_url)
        soup = BeautifulSoup(model_page.content, "html.parser")
        gens_elements = soup.find_all("a", {"class": "position"})
    
        for gen_elements in gens_elements:
            gen_name = gen_elements.find("strong", {"class": "tit"})
            
            if gen_name is None:
                continue
            
            gen_url = gen_elements["href"]
            gen_page = requests.get(BASE_URL + gen_url)
            soup = BeautifulSoup(gen_page.content, "html.parser")
            mods_elements = soup.find_all("th", {"class": "i"})
            
            for mod_elements in mods_elements:
                mod_a = mod_elements.find("a")
                
                mod_url = mod_a["href"]
                
                mod_page = requests.get(BASE_URL + mod_url)
                soup = BeautifulSoup(mod_page.content, "html.parser")
                table = soup.find("table", {"class": "cardetailsout car2"})
                if table is None:
                    continue
                table_rows = table.find_all("tr")

                for table_row in table_rows:
                    key = table_row.find("th")
                    if key is None:
                        continue
                    
                    value = table_row.find("td")
                    if value is None:
                        continue

                    specs_set.add(key.text.strip())    

with open("specs.txt", "w") as file:
    file.write(str(specs_set))

print("Parsing finished: Result was written into specs.txt file.")
print(specs_set)

