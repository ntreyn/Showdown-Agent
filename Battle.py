

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from AI import Agent
from BattleMask import Mask

import time
import re

class Battle:

    def __init__(self, driver, pokedex, agent_team):
        self.driver = driver
        self.pokedex = pokedex

        self.done = False
        self.turn = 0

        self.agent_team = agent_team
        self.opponent_team = {}
    
    def battle(self):

        wait = WebDriverWait(self.driver, 20)
        self.set_teams(wait)

        rightbar = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='rightbar']")))
        self.opponent = rightbar.find_element_by_css_selector("strong").get_attribute("innerText").strip()

        # turn0_battle_history = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='battle-history']")))

        # for tbh in turn0_battle_history:
            # print(tbh.get_attribute("innerText"))

        time.sleep(10)

        self.mask = Mask()
        self.agent = Agent(self.mask)

        self.agent.lead()

        self.update_mask(wait)

        self.turn += 1

        while not self.done:
            print("here")
            time.sleep(20)
            self.execute_turn(wait)

    def execute_turn(self, wait):

        # Speed and damage calcs
        # Assess switches (both sides)

        # Assess following turns

        # Choose action
        # Attack or switch

        # Update info

        action = self.agent.get_action()
        self.execute_action(action, wait)

    

        self.turn += 1
        self.done = True


    def execute_action(self, action, wait):




        
        self.update_mask(wait)    

    def update_mask(self, wait):

        set_update = self.get_set_changes(wait)
        field_update = self.get_field_changes(wait)

        self.mask.update(set_update, field_update)
        

    def get_set_changes(self, wait):

        # Update sets
        """
        Set updates

        Nickname
        Ability
        Moveset
        Item
        Form change
        
        Lasting conditions:
        
        HP / Fainted
        PP
        Status
        
        In play conditions:

        Substitute
        Perish Song
        Leech Seed
        Ingrain
        Confusion
        Boosts / Drops
        """

        updated_sets = {}

        for mon in self.opponent_team.values():
            n = getattr(mon.set, "team_number")
            species = mon.species
            updated_sets[mon.species] = {}

            pokemon_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-tooltip='pokemon|1|{}']".format(n))))
            hover = ActionChains(self.driver).move_to_element(pokemon_icon)
            hover.perform()

            pokemon_tooltip = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='tooltip']")))
            inner_text = pokemon_tooltip.get_attribute("innerText")

            # print("************")
            # print(inner_text)
            # print("xxxxxxxxxxxxx")

            it_list = [x for x in inner_text.splitlines() if x != '']

            for line in it_list:
                
                # Update nickname
                if mon.set.nickname is None:
                    nick_re = re.search('\({}\)'.format(mon.species), line)
                    if nick_re is not None:
                        print(species, line.replace(nick_re.group(), "").strip())
                        updated_sets[species]["nickname"] = line.replace(nick_re.group(), "").strip()
                
                # Update ability 
                if mon.set.ability is None:
                    ability_re = re.search('Ability:', line)
                    if ability_re is not None:
                        print(species, line.replace(ability_re.group(), "").strip())
                        updated_sets[species]["ability"] = line.replace(ability_re.group(), "").strip()
                

                # Update item
                if mon.set.item is None:
                    if line[:4] == "Item" and line[6:].strip() != "(exists)":
                        print(species, line[6:].strip())
                        updated_sets[species]["item"] = line[6:].strip()


            

            """
            set_dict = {
                "species": name,
                "nickname": None,
                "gender": gender,
                "item": item,
                "ability": None,
                "level": level,
                "shiny": None,
                "happiness": None,
                "EVs": {},
                "nature": None,
                "IVs": {},
                "moves": None
            }
            """

        # <span class="status brn">BRN</span>
        # Look for class^='status' innerText
        """
        <div class="status">
            <span class="bad">Leech&nbsp;Seed</span> 
        </div>
        """
        # Look for class='status'
        # find_element_by_css_select "span[class='bad']" innerText
        """
        <div class="status">
            <span class="brn">BRN</span>
            <span class="bad">Confused</span> 
        </div>
        """

        return {}

    def get_field_changes(self, wait):

        field = {}
        
        # Get field conditions
        field_conditions = {}
        feild_condition_list = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class^='weather']")))

        fc_it_list = [h.get_attribute("innerText") for h in feild_condition_list if h.get_attribute("innerText") != '']

        for fc_it in fc_it_list:
            fcs = fc_it.split('\n')
            for fc in fcs:
                turns_re = re.search('\(([^)]+)\)', fc)
                if turns_re is not None:
                    turns_str = turns_re[0].strip()
                    turns = [int(c) for c in turns_str if c.isdigit()]
                    condition = fc.replace(turns_str, "").strip()

                    field_conditions[condition] = {
                        "condition": condition,
                        "turns": turns,
                        "starter": None
                    }

        for fc in field_conditions:
            if fc in self.mask.field["conditions"]:
                field_conditions[fc]["starter"] = self.mask.field["conditions"][fc]["starter"]
            else:
                turn_battle_log = self.get_battle_log(wait)
                for log in turn_battle_log:
                    x = log.get_attribute("innerText")
                    y = re.search('{}'.format(self.mask.ConditionCauses[fc]["move"]), x)
                    if y is not None:
                        print(x)
                        print(self.mask.ConditionCauses[fc]["move"])
                        break
                    z = re.search('{}'.format(self.mask.ConditionCauses[fc]["ability"]), x)
                    if z is not None:
                        print(x)
                        print(self.mask.ConditionCauses[fc]["ability"])
                        break
                        
                


        # Get hazards from img src or log

        field["conditions"] = field_conditions

        return field

    def get_battle_log(self, wait):
        if self.turn == 0:
            turn_battle_log = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[./following-sibling::h2[.='Turn {}']]".format(self.turn + 1))))
        elif self.done:
            turn_battle_log = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[./preceding-sibling::h2[.='Turn {}']]".format(self.turn))))
        else:
            turn_battle_log = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[./preceding-sibling::h2[.='Turn {}']][./following-sibling::h2[.='Turn {}']]".format(self.turn, self.turn + 1))))
        return turn_battle_log   

    def set_teams(self, wait):
        for a in self.agent_team.values():
            if a.set.gender is None:
                i = getattr(a.set, "team_number")
                gender = self.get_agent_team_gender(wait, i)
                a.set.update_set({ "gender": gender })
        
        self.get_opposing_team(wait)

    def set_opposing_team(self, team_list):
        
        for d in team_list:
            species = d["species"]
            pokemon = self.pokedex.get_pokemon(species)
            pokemon.create_set(d)
            self.opponent_team[species] = pokemon

    def get_opposing_team(self, wait):

        team_list = []

        for n in range(6):

            try:
                pokemon_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-tooltip='pokemon|1|{}']".format(n))))
                hover = ActionChains(self.driver).move_to_element(pokemon_icon)
                hover.perform()

                pokemon_tooltip = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='tooltip']")))
                inner_text = pokemon_tooltip.get_attribute("innerText")
            except TimeoutException:
                break

            gender = ' '
            for g in ['M', 'F']:
                try:
                    pokemon_tooltip.find_element_by_css_selector("img[alt='{}']".format(g))
                    gender = g
                except NoSuchElementException:
                    continue
            if gender == ' ':
                gender = None

            text_list = inner_text.splitlines()
            
            temp = text_list[0].split()
            if temp[-1][0] == 'L' and temp[-1][1].isnumeric():
                name = text_list[0][:-3]
                level_str = (text_list[0][-3:]).strip()
                level = int(level_str[1:])
            else:
                name = name = text_list[0]
                level = 100
            name = name.strip()

            text_list = inner_text.split()

            if "Item:" in text_list:
                item = None
            else:
                item = False

            set_dict = {
                "team_number": n,
                "species": name,
                "nickname": None,
                "gender": gender,
                "item": item,
                "ability": None,
                "level": level,
                "shiny": None,
                "happiness": None,
                "EVs": {},
                "nature": None,
                "IVs": {},
                "moves": None
            }

            team_list.append(set_dict)
            
            # print("Name: {}, Level: {}, Gender: {}, Item: {}".format(name, level, gender, item))
        
        self.set_opposing_team(team_list)

    def get_agent_team_gender(self, wait, n):
        try:
            pokemon_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-tooltip='pokemon|0|{}']".format(n))))
            hover = ActionChains(self.driver).move_to_element(pokemon_icon)
            hover.perform()

            pokemon_tooltip = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='tooltip']")))
        except TimeoutException:
            return None

        gender = ' '
        for g in ['M', 'F']:
            try:
                pokemon_tooltip.find_element_by_css_selector("img[alt='{}']".format(g))
                gender = g
            except NoSuchElementException:
                continue
        if gender == ' ':
            gender = None
        
        return gender
