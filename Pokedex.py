
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
 
import json
import time

from Pokemon import Pokemon

class Pokedex:

    default_structure = {
        'id': -1,
        'species': "",
        'baseSpecies': None,
        'form': None,
        'formLetter': None,
        'otherForms': None,
        'types': [],
        'genderRatio': {'M': 0.0, 'F': 0.0},
        'baseStats': { "HP": 0, "Attack": 0, "Defense": 0, "SpAtk": 0, "SpDef": 0, "Speed": 0 },
        'abilities': [],
        'heightm': 0.0,
        'weightkg': 0.0,
        'tier': None
    }

    def __init__(self):
        self.poke_dict = {}
        self.json_file = "Pokedex.json"
        
        self.from_json()

        self.id_to_mon = {}

    def get_pokemon(self, species):
        pokemon_dict = self.poke_dict[species]
        pokemon = Pokemon(pokemon_dict)
        return pokemon

    def to_json(self):
        with open(self.json_file, 'w') as write_file:
            json.dump(self.poke_dict, write_file)

    def from_json(self):
        with open(self.json_file, 'r') as read_file:
            self.poke_dict = json.load(read_file)

    def scrape_showdown_dex(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://dex.pokemonshowdown.com/pokemon/")
        wait = WebDriverWait(driver, 30)

        time.sleep(15)
        # Can't scroll, manual scroll

        mon_list = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "a[data-entry^='pokemon|']")))
        
        for mon in mon_list:

            tier = mon.find_element_by_css_selector("span[class='col numcol']").get_attribute("innerText")
            species = mon.find_element_by_css_selector("span[class='col pokemonnamecol']").get_attribute("innerText")
            
            type_list = mon.find_elements_by_css_selector("img[width='32']")
            types = [t.get_attribute("alt") for t in type_list]

            ability_list = mon.find_elements_by_css_selector("span[class='col abilitycol']")
            abilities = [a.get_attribute("innerText") for a in ability_list if a.get_attribute("innerText") != '']
            
            twoability_list = mon.find_elements_by_css_selector("span[class='col twoabilitycol']")
            for ta in twoability_list:
                ta_temp = ta.get_attribute("innerText").split('\n')
                for abil in ta_temp:
                    abilities.append(abil)
            
            stat_list = mon.find_elements_by_css_selector("span[class='col statcol']")
            baseStats = {}
            for s in stat_list:
                stat, val = s.get_attribute("innerText").split('\n')
                baseStats[stat] = int(val)
            
            mon.click()
            id = int(wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "code"))).get_attribute("innerText")[1:])
            
            height_weight = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "dl[class='sizeentry']"))).get_attribute("innerText").split('\n')[1]
            hw_list = height_weight.split()
            heightm = float(hw_list[0])
            weightkg = float(hw_list[2])

            gender_ratio_html = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "dl[class='colentry']")))[1]
            gr_str = gender_ratio_html.find_element_by_css_selector("dd").get_attribute("innerText")
            if "genderless" in gr_str:
                gender_ratio = None
            else:
                gr_list = gr_str.split()
                if len(gr_list) == 4:
                    mpercent = float(gr_list[0][:-1])
                    fpercent = float(gr_list[2][:-1])
                    gender_ratio = {'M': mpercent, 'F': fpercent}
                else:
                    if gr_list[1] == "male":
                        gender_ratio = {'M': 100}
                    else:
                        gender_ratio = {'F': 100}

            
            if id in self.id_to_mon:
                baseSpecies = self.id_to_mon[id]
                form = species.replace(baseSpecies, '')[1:]
                formLetter = form[0]
                self.poke_dict[baseSpecies]["otherForms"].append(species)
            else:
                self.id_to_mon[id] = species
                baseSpecies = None
                form = None
                formLetter = None

            mon_dict = {
                'id': id,
                'species': species,
                'baseSpecies': baseSpecies,
                'form':form,
                'formLetter': formLetter,
                'otherForms': [],
                'types': types,
                'genderRatio': gender_ratio,
                'baseStats': baseStats,
                'abilities': abilities,
                'heightm': heightm,
                'weightkg': weightkg,
                'tier': tier
            }

            self.poke_dict[species] = mon_dict
            print(id, end='\r')

            if id == 807:
                break


def main():
    dex = Pokedex()
    # dex.scrape_showdown_dex()
    # dex.to_json()
    
    dex.from_json()

    while True:
        mon = input("Pokemon: ")
        if mon in dex.poke_dict:
            print(dex.poke_dict[mon])
        else:
            print("Invalid mon")
    


if __name__ == "__main__":
    main()