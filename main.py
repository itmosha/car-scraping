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
brands = []
brand_id = 1

for brand_elements in brands_elements:
    brand_name = brand_elements.find("strong")
    
    print('Parsing {}...'.format(brand_name.text.strip()))

    brand_url = brand_elements["href"]

    brand = dict()
    brand["id"] = brand_id
    brand["name"] = brand_name.text.strip()
    
    brand_page = requests.get(BASE_URL + brand_url)
    soup = BeautifulSoup(brand_page.content, "html.parser")
    models_elements = soup.find_all("a", {"class": "modeli"})

    models = []
    model_id = 1
    
    for model_elements in models_elements:
        model_name = model_elements.find("strong")
        model_url = model_elements["href"]

        model = dict()
        model["id"] = model_id
        model["name"] = model_name.text.strip()
        
        model_page = requests.get(BASE_URL + model_url)
        soup = BeautifulSoup(model_page.content, "html.parser")
        gens_elements = soup.find_all("a", {"class": "position"})
    
        gens = []
        gen_id = 1

        for gen_elements in gens_elements:
            gen_name = gen_elements.find("strong", {"class": "tit"})
            
            if gen_name is None:
                continue
            
            gen = dict()

            gen["id"] = gen_id
            gen["name"] = gen_name.text.strip()
            gen_url = gen_elements["href"]
            
            gen_page = requests.get(BASE_URL + gen_url)
            soup = BeautifulSoup(gen_page.content, "html.parser")
            mods_elements = soup.find_all("th", {"class": "i"})

            mods = []
            mod_id = 1
            
            for mod_elements in mods_elements:
                mod_a = mod_elements.find("a")
                
                mod = dict()

                mod["id"] = mod_id
                mod["name"] = mod_a.find("span", {"class": "tit"}).text.strip()
                mod_url = mod_a["href"]
                
                mod_page = requests.get(BASE_URL + mod_url)
                soup = BeautifulSoup(mod_page.content, "html.parser")
                
                table = soup.find("table", {"class": "cardetailsout car2"})
                table_rows = table.find_all("tr")
                specs = dict()

                for table_row in table_rows:
                    key = table_row.find("th")
                    if key is None:
                        continue
                    
                    value = table_row.find("td")
                    if value is None:
                        continue
                    specs_set.add(key.text.strip())    
                    specs[key.text.strip()] = value.text.strip()
                
                specs.pop('Brand', None)
                specs.pop('Model', None)
                specs.pop('Generation', None)
                specs.pop('Modification (Engine)', None)
                specs.pop('Engine oil specification', None)
                
                specs['start_of_production'] = specs.pop('Start of production', None)
                specs['end_of_production'] = specs.pop('End of production', None)
                specs['powertrain_architecture'] = specs.pop('Powertrain Architecture', None)
                specs['body_type'] = specs.pop('Body type', None)
                specs['seats'] = specs.pop('Seats', None)
                specs['doors'] = specs.pop('Doors', None)
                specs['fuel_consumption_urban'] = specs.pop('Fuel consumption (economy) - urban', None)
                specs['fuel_consumption_extra_urban'] = specs.pop('Fuel consumption (economy) - extra urban', None)
                specs['fuel_consumption_combined'] = specs.pop('Fuel consumption (economy) - combined', None)
                specs['co2_emissions'] = specs.pop('CO2 emissions', None)
                specs['fuel_type'] = specs.pop('Fuel Type', None)
                specs['0-100_kmh_acceleration'] = specs.pop('Acceleration 0 - 100 km/h', None)
                specs['0-62_mph_acceleration'] = specs.pop('Acceleration 0 - 62 mph', None)
                specs['maximum_speed'] = specs.pop('Maximum speed', None)
                specs['weight_to_power_ratio'] = specs.pop('Weight-to-power ratio', None)
                specs['weight_to_torque_ratio'] = specs.pop('Weight-to-torque ratio', None)
                specs['power'] = specs.pop('Power', None)
                specs['power_per_litre'] = specs.pop('Power per litre', None)
                specs['torque'] = specs.pop('Torque', None)
                specs['engine_layout'] = specs.pop('Engine layout', None)
                specs['engine_model'] = specs.pop('Engine Model/Code', None)
                specs['engine_displacement'] = specs.pop('Engine displacement', None)
                specs['number_of_cylinders'] = specs.pop('Number of cylinders', None)
                specs['engine_configuration'] = specs.pop('Engine configuration', None)
                specs['cylinder_bore'] = specs.pop('Cylinder Bore', None)
                specs['piston_stroke'] = specs.pop('Piston Stroke', None)
                specs['compression_ratio'] = specs.pop('Compression ratio', None)
                specs['number_of_valves_per_cylinder'] = specs.pop('Number of valves per cylinder', None)
                specs['engine_aspiration'] = specs.pop('Engine aspiration', None)
                specs['engine_oil_capacity'] = specs.pop('Engine oil capacity', None)
                specs['coolant'] = specs.pop('Coolant', None)
                specs['kerb_weight'] = specs.pop('Kerb Weight', None)
                specs['fuel_tank_capacity'] = specs.pop('Fuel tank capacity', None)
                specs['length'] = specs.pop('Length', None)
                specs['width'] = specs.pop('Width', None)
                specs['height'] = specs.pop('Height', None)
                specs['wheelbase'] = specs.pop('Wheelbase', None)
                specs['front_track'] = specs.pop('Front track', None)
                specs['rear_track'] = specs.pop('Rear (Back) track', None)
                specs['drivetrain_achitecture'] = specs.pop('Drivetrain Architecture', None)
                specs['drive_wheel'] = specs.pop('Drive wheel', None)
                specs['number_of_gears_and_gearbox_type'] = specs.pop('Number of gears and type of gearbox', None)
                specs['front_suspension'] = specs.pop('Front suspension', None)
                specs['rear_suspension'] = specs.pop('Rear suspension', None)
                specs['front_brakes'] = specs.pop('Front brakes', None)
                specs['rear_brakes'] = specs.pop('Rear brakes', None)
                specs['assisting_systems'] = specs.pop('Assisting systems', None)
                specs['steering_type'] = specs.pop('Steering type', None)
                specs['power_steering'] = specs.pop('Power steering', None)
                specs['tires_size'] = specs.pop('Tires size', None)
                specs['wheel_rims_size'] = specs.pop('Wheel rims size', None)
                
                mod["specs"] = specs
                mods.append(mod)
                mod_id += 1
            
            gen["modifications"] = mods

            gens.append(gen)
            gen_id += 1
                
        models.append({"name": model_name.text.strip(), "generations": gens})
        model_id += 1
    
    brand["models"] = models
    brands.append(brand)

    brand_id += 1
    if brand_id > 1:
        break

with open("cars.json", "w") as file:
    json.dump(brands, file, indent=4)

print("Parsing finished: Result was written into cars.json file.")
print(specs_set)

