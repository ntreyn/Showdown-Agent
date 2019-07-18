

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

from misc_utils import StatusList, ConditionCauses, Afflictions, HazardsMap, change_hazards

import time
import re

class Battle:

    def __init__(self, driver, pokedex, agent_team):
        self.driver = driver
        self.pokedex = pokedex

        self.done = False
        self.turn = 0

        self.agent_team = agent_team
        self.agent_nicks = {}
        self.agent_active = None
        self.agent_alias = {}

        self.opponent_team = {}
        self.opponent_nicks = {}
        self.opponent_active = None
        self.opponent_alias = {}
    
    def battle(self):

        wait = WebDriverWait(self.driver, 15)
        self.set_teams(wait)

        rightbar = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='rightbar']")))
        self.opponent = rightbar.find_element_by_css_selector("strong").get_attribute("innerText").strip()

        # turn0_battle_history = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='battle-history']")))

        # for tbh in turn0_battle_history:
            # print(tbh.get_attribute("innerText"))

        self.mask = Mask()
        self.agent = Agent(self.mask)

        try:
            lead = self.agent.lead()
            lead_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[(@name='{}') and (@value='{}')]".format(lead["name"], lead["value"]))))
            lead_button.click()
        except TimeoutException:
            try:
                exit_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='closeAndMainMenu']")))
                exit_button.click()
                self.done = True
                return
            except TimeoutException:
                print("Error: no lead no exit")

        time.sleep(5)

        try:
            timer_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='openTimer']")))
            timer_button.click()

            timer_on = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='timerOn']")))
            timer_on.click()
        except (TimeoutException, StaleElementReferenceException) as e:
            print("failed timer")

        time.sleep(5)
        try:
            self.update_mask(wait)
        except TimeoutException:
            print("failed update")

        self.turn += 1

        while not self.done:
            self.execute_turn(wait)

    def execute_turn(self, wait):
        
        for attempts in range(2):
            try:
                #print("here3")
                action = self.agent.get_action()
                self.execute_action(action, wait)
                break
            except TimeoutException:
                print("failed action")
                continue

        count = 0
        #print("here0")
        
        for attempts in range(5):
            #print("here5")
            try:
                #print("here1")
                wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Turn {}')]".format(self.turn + 1))))
                break
            except TimeoutException:
                # check switch
                try:
                    #print("here2")
                    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "switchmenu")))
                    switch = self.agent.get_switch()
                    switch_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[(@name='{}') and (@value='{}')]".format(switch["name"], switch["value"]))))
                    switch_button.click()
                    time.sleep(5)
                    continue
                except TimeoutException:
                    pass

                try:
                    #print("here4")
                    exit_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='closeAndMainMenu']")))
                    exit_button.click()
                    self.done = True
                    return
                except TimeoutException:
                    count += 1
                    continue
        
        if count == 5:
            print("Error: no turn 'n' no close")
            exit()

        self.update_mask(wait) 
        self.turn += 1
        print(self.turn)


    def execute_action(self, action, wait):
        if action["mega"]:
            mega_checkbox = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='megaevo']")))
            mega_checkbox.click()
        if action["zmove"]:
            z_checkbox = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='zmove']")))
            z_checkbox.click()
            time.sleep(3)
            z_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[starts-with(@data-tooltip, 'zmove') and (@value='{}')]".format(action["value"]))))
            z_button.click()
        else:
            action_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[(@name='{}') and (@value='{}')]".format(action["name"], action["value"]))))
            action_button.click()

        time.sleep(10)   

    def update_mask(self, wait):

        self.update_opponent_set(wait)
        self.update_agent_set(wait)
        field_update = self.get_field_changes(wait)

        self.mask.update(self.opponent_team, self.opponent_active, self.agent_team, self.agent_active, field_update)
    
    def update_agent_set(self, wait):
        new_mons = {}

        for mon in self.agent_team.values():
            n = mon.set.team_number
            species = mon.species

            pokemon_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-tooltip='pokemon|0|{}']".format(n))))
            hover = ActionChains(self.driver).move_to_element(pokemon_icon)
            hover.perform()

            pokemon_tooltip = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='tooltip']")))
            inner_text = pokemon_tooltip.get_attribute("innerText")

            #print("************")
            #print(inner_text)
            #print("xxxxxxxxxxxxx")

            it_list = [x for x in inner_text.splitlines() if x != '']

            for line in it_list:

                # Update form
                if mon.form is None:
                    if species in self.agent_nicks.values():
                        nick = self.agent_team[species].set.nickname
                        if_nick_re = re.search('{} \(.*\)'.format(nick), line)
                        if if_nick_re is not None:
                            temp = re.search('\(.*\)', line).group()[1:-1]
                            if temp != species:
                                new_mons[species] = temp
                    else:
                        if_form_re = re.search('{} \(.*\)'.format(species), line)
                        if if_form_re is not None:
                            form_re = re.search('\(.*\)', line)
                            new_species = form_re.group()[1:-1]
                            new_mons[species] = new_species
                
                # Update nickname
                if mon.set.nickname is not None:
                    self.agent_nicks[mon.set.nickname] = species


                alias_re = re.search('\({}\)'.format(species), line)
                if alias_re is not None:
                    alias = line.replace(alias_re.group(), "").strip()
                    self.agent_alias[alias] = species

                # Update ability 
                ability_re = re.search('Ability:', line)
                if ability_re is not None:
                    abil = line.replace(ability_re.group(), "").strip()
                    if abil != self.agent_team[species].set.ability:
                        self.agent_team[species].set.temp_ability = abil

                # Item knock condition

                # Update item
                if line[:4] == "Item":
                    item_str = line[6:].strip()
                    if item_str[-12:] == "knocked off)":
                        self.agent_team[species].set.item = item_str[6:-17]
                        self.agent_team[species].set.knocked = True
                    elif (mon.set.item is None or mon.set.item != item_str) and item_str != "(exists)":
                        #print(species, line[6:].strip())
                        setattr(self.agent_team[species].set, "item", line[6:].strip())

                # Update moves
                if line[0] == "•":
                    pp_re = re.search('\(.*\)', line)
                    if pp_re is not None:
                        pp_remaining = int(pp_re.group()[1:-1].split('/')[0])
                        move = line.replace(pp_re.group(), "")[1:].strip()
                        if (move, pp_remaining) not in mon.set.moves:
                            getattr(self.agent_team[species].set, "moves").append((move, pp_remaining))

                # Probably needs to be modified
                if line[:2] == 'HP':
                    for status in StatusList:
                        if status in line:
                            self.agent_team[species].set.status = status
                            line = line.replace(status, "").strip()
                            break

                    fainted_re = re.search('\(fainted\)', line)
                    if fainted_re is not None:
                        self.agent_team[species].set.hp = 0.0
                        self.agent_team[species].set.fainted = True
                    else:
                        temp = line.replace('HP:', "").strip()
                        ind = temp.index('%')
                        self.agent_team[species].set.hp = float(line.replace('HP:', "").strip()[:ind])

        for species, new_species in new_mons.items():
            new_mon = self.pokedex.get_pokemon(new_species)

            set_dict = {}
            for key in self.agent_team[species].set.keys_total:
                set_dict[key] = getattr(self.agent_team[species].set, key)
            set_dict["species"] = new_species
            set_dict["ability"] = new_mon.abilities[0]
            set_dict["temp_ability"] = None

            new_mon.create_set(set_dict)

            if species in self.agent_nicks.values():
                self.agent_nicks[self.agent_team[species].set.nickname] = new_species

            self.agent_alias[species] = new_species

            del self.agent_team[species]
            self.agent_team[new_species] = new_mon
        
        opp_active = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='statbar rstatbar']")))

        type_list = opp_active.find_elements_by_css_selector("img.pixelated")
        new_types = [t.get_attribute("alt") for t in type_list]

        active_text_list = opp_active.get_attribute("innerText").split('\n')

        name_str = active_text_list[0].strip()

        if name_str in self.agent_nicks:
            self.agent_active = self.agent_nicks[name_str]
        elif name_str in self.agent_alias:
            self.agent_active = self.agent_alias[name_str]
        else:
            self.agent_active = name_str

        if len(active_text_list) > 2:
            status_str = active_text_list[2].replace(u'\xa0', u' ')
            status_list = status_str.split()

            if '+' in status_list:
                added_type = new_types.pop(-1)
            else:
                added_type = None

            self.agent_team[self.agent_active].set.new_types = new_types
            self.agent_team[self.agent_active].set.added_type = added_type

            for afflict in Afflictions:
                if afflict in status_str and afflict not in self.agent_team[self.agent_active].set.afflictions:
                    self.agent_team[self.agent_active].set.afflictions.append(afflict)
            
            for stat in self.agent_team[self.agent_active].set.stats_changes:
                if stat in status_list:
                    ind = status_list.index(stat)
                    mult = float(status_list[ind - 1][:-1])
                    add = self.stat_mult_to_add(stat, mult)
                    self.agent_team[self.agent_active].set.stats_changes[stat] = add

        #self.agent_team[self.agent_active].print_set()
        #for mon in self.agent_team.values():
        #    mon.print_set()

    def update_opponent_set(self, wait):
        new_mons = {}

        for mon in self.opponent_team.values():
            n = mon.set.team_number
            species = mon.species

            pokemon_icon = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-tooltip='pokemon|1|{}']".format(n))))
            hover = ActionChains(self.driver).move_to_element(pokemon_icon)
            hover.perform()

            pokemon_tooltip = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='tooltip']")))
            inner_text = pokemon_tooltip.get_attribute("innerText")

            #print("************")
            #print(inner_text)
            #print("xxxxxxxxxxxxx")

            it_list = [x for x in inner_text.splitlines() if x != '']

            for line in it_list:

                # Update form
                if mon.form is None:
                    if species in self.opponent_nicks.values():
                        nick = self.opponent_team[species].set.nickname
                        if_nick_re = re.search('{} \(.*\)'.format(nick), line)
                        if if_nick_re is not None:
                            temp = re.search('\(.*\)', line).group()[1:-1]
                            if temp != species:
                                new_mons[species] = temp
                    else:
                        if_form_re = re.search('{} \(.*\)'.format(species), line)
                        if if_form_re is not None:
                            form_re = re.search('\(.*\)', line)
                            new_species = form_re.group()[1:-1]
                            new_mons[species] = new_species
                
                # Update nickname
                if mon.set.nickname is None:

                    if species in new_mons:
                        temp_species = new_mons[species]
                    else:
                        temp_species = species

                    nick_re = re.search('\({}\)'.format(temp_species), line)
                    if nick_re is not None:
                        #print(species, line.replace(nick_re.group(), "").strip())
                        nick = line.replace(nick_re.group(), "").strip()
                        setattr(self.opponent_team[species].set, "nickname", nick)
                        self.opponent_nicks[nick] = species

                # Update ability 
                if mon.set.ability is None:
                    ability_re = re.search('Ability:', line)
                    if ability_re is not None:
                        #print(species, line.replace(ability_re.group(), "").strip())
                        setattr(self.opponent_team[species].set, "ability", line.replace(ability_re.group(), "").strip())
                else:
                    ability_re = re.search('Ability:', line)
                    if ability_re is not None:
                        abil = line.replace(ability_re.group(), "").strip()
                        if abil != self.opponent_team[species].set.ability:
                            self.opponent_team[species].set.temp_ability = abil

                # Item knock condition

                # Update item
                if line[:4] == "Item":
                    item_str = line[6:].strip()
                    if item_str[-12:] == "knocked off)":
                        self.opponent_team[species].set.item = item_str[6:-17]
                        self.opponent_team[species].set.knocked = True
                    elif (mon.set.item is None or mon.set.item != item_str) and item_str != "(exists)":
                        #print(species, line[6:].strip())
                        setattr(self.opponent_team[species].set, "item", line[6:].strip())


                # Update moves
                if line[0] == "•":
                    pp_re = re.search('\(.*\)', line)
                    if pp_re is not None:
                        pp_remaining = int(pp_re.group()[1:-1].split('/')[0])
                        move = line.replace(pp_re.group(), "")[1:].strip()
                        if (move, pp_remaining) not in mon.set.moves:
                            getattr(self.opponent_team[species].set, "moves").append((move, pp_remaining))

                if line[:2] == 'HP':

                    for status in StatusList:
                        if status in line:
                            self.opponent_team[species].set.status = status
                            line = line.replace(status, "").strip()
                            break

                    fainted_re = re.search('\(fainted\)', line)
                    if fainted_re is not None:
                        self.opponent_team[species].set.hp = 0.0
                        self.opponent_team[species].set.fainted = True
                    else:
                        self.opponent_team[species].set.hp = float(line.replace('HP:', "").strip()[:-1])

        for species, new_species in new_mons.items():
            new_mon = self.pokedex.get_pokemon(new_species)

            set_dict = {}
            for key in self.opponent_team[species].set.keys_total:
                set_dict[key] = getattr(self.opponent_team[species].set, key)
            set_dict["species"] = new_species
            set_dict["ability"] = new_mon.abilities[0]
            set_dict["temp_ability"] = None

            new_mon.create_set(set_dict)

            if species in self.opponent_nicks.values():
                self.opponent_nicks[self.opponent_team[species].set.nickname] = new_species

            self.opponent_alias[species] = new_species

            del self.opponent_team[species]
            self.opponent_team[new_species] = new_mon
        
        opp_active = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='statbar lstatbar']")))
        
        # type_list = opp_active.find_elements_by_css_selector("img[class='pixelated']")
        type_list = opp_active.find_elements_by_css_selector("img.pixelated")
        new_types = [t.get_attribute("alt") for t in type_list]

        active_text_list = opp_active.get_attribute("innerText").split('\n')

        name_str = active_text_list[0].strip()
        if name_str in self.opponent_nicks:
            self.opponent_active = self.opponent_nicks[name_str]
        elif name_str in self.opponent_alias:
            self.opponent_active = self.opponent_alias[name_str]
        else:
            self.opponent_active = name_str

        if len(active_text_list) > 2:
            status_str = active_text_list[2].replace(u'\xa0', u' ')
            status_list = status_str.split()

            if '+' in status_list:
                added_type = new_types.pop(-1)
            else:
                added_type = None

            self.opponent_team[self.opponent_active].set.new_types = new_types
            self.opponent_team[self.opponent_active].set.added_type = added_type

            for afflict in Afflictions:
                if afflict in status_str and afflict not in self.opponent_team[self.opponent_active].set.afflictions:
                    self.opponent_team[self.opponent_active].set.afflictions.append(afflict)
            
            for stat in self.opponent_team[self.opponent_active].set.stats_changes:
                if stat in status_list:
                    ind = status_list.index(stat)
                    mult = float(status_list[ind - 1][:-1])
                    add = self.stat_mult_to_add(stat, mult)
                    self.opponent_team[self.opponent_active].set.stats_changes[stat] = add

        #for mon in self.opponent_team.values():
        #    mon.print_set()

    def get_field_changes(self, wait):

        #The opposing Swampert used Substitute!
        #The opposing Swampert put in a substitute!  

        #Swampert's substitute faded!

        #The opposing Swampert used Substitute!
        #But it does not have enough HP left to make a substitute!

        field = {}
        
        # Get field conditions
        field_conditions = {}
        field_condition_list = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class^='weather']")))

        fc_it_list = [h.get_attribute("innerText") for h in field_condition_list if h.get_attribute("innerText") != '']

        for fc_it in fc_it_list:
            fcs = fc_it.split('\n')
            for fc in fcs:
                if fc[:5] == "Foe's":
                    fc = fc[5:].strip()

                turns_re = re.search('\(([^)]+)\)', fc)
                if turns_re is not None:
                    turns_str = turns_re[0].strip()
                    turns = [int(c) for c in turns_str if c.isdigit()]
                    condition = fc.replace(turns_str, "").strip()

                    field_conditions[condition] = {
                        "condition": condition,
                        "turns": turns,
                        "starter": None,
                        "side": None
                    }
                elif fc.strip() in ConditionCauses:
                    field_conditions[fc.strip()] = {
                        "condition": fc.strip(),
                        "turns": None,
                        "starter": None,
                        "side": None
                    }

        for fc in field_conditions:
            if fc[:5] == "Foe's":
                fc = fc[5:].strip()

            if fc in self.mask.field["conditions"]:
                field_conditions[fc]["starter"] = self.mask.field["conditions"][fc]["starter"]
                field_conditions[fc]["side"] = self.mask.field["conditions"][fc]["side"]
            else:
                turn_battle_log = self.get_battle_log(wait)
                for log in turn_battle_log:
                    log_it = log.get_attribute("innerText")
                    fc_move_re = re.search('{}'.format(ConditionCauses[fc]["move"]), log_it)
                    if fc_move_re is not None:
                        fc_line = log_it.split('\n')[0]
                        if fc_line[0:12] == "The opposing":
                            starter_str = fc_line[13:].split()[0]

                            if starter_str in self.opponent_nicks:
                                starter = self.opponent_nicks[starter_str]
                            elif starter_str in self.opponent_alias:
                                starter = self.opponent_alias[starter_str]
                            else:
                                starter = starter_str

                            field_conditions[fc]["starter"] = starter
                            field_conditions[fc]["side"] = 'O'
                        else:
                            starter_str = fc_line.split()[0]

                            if starter_str in self.agent_nicks:
                                starter = self.agent_nicks[starter_str]
                            elif starter_str in self.agent_alias:
                                starter = self.agent_alias[starter_str]
                            else:
                                starter = starter_str

                            field_conditions[fc]["starter"] = starter
                            field_conditions[fc]["side"] = 'A'

                        break
                    fc_abil_re = re.search('{}'.format(ConditionCauses[fc]["ability"]), log_it)
                    if fc_abil_re is not None:
                        fc_line = log_it.split('\n')[0]
                        if fc_line[1:13] == "The opposing":
                            starter_text = fc_line[14:-1].replace(ConditionCauses[fc]["ability"], "").strip()
                            starter_str = starter_text[:-2]

                            if starter_str in self.opponent_nicks:
                                starter = self.opponent_nicks[starter_str]
                            elif starter_str in self.opponent_alias:
                                starter = self.opponent_alias[starter_str]
                            else:
                                starter = starter_str

                            field_conditions[fc]["starter"] = starter
                            field_conditions[fc]["side"] = 'O'
                        else:
                            starter_text = fc_line[1:-1].replace(ConditionCauses[fc]["ability"], "").strip()
                            starter_str = starter_text[:-2]

                            if starter_str in self.agent_nicks:
                                starter = self.agent_nicks[starter_str]
                            elif starter_str in self.agent_alias:
                                starter = self.agent_alias[starter_str]
                            else:
                                starter = starter_str

                            field_conditions[fc]["starter"] = starter
                            field_conditions[fc]["side"] = 'A'

                        break



        print("HERE")
        hazards = self.mask.field["hazards"]
        log = self.get_battle_log(wait)

        for html_line in log:
            lines = [x for x in html_line.get_attribute("innerText").split('\n') if x != '']
            for line in lines:
                if line in HazardsMap:
                    hazards = change_hazards(hazards, line)

        print(field_conditions)
        print(hazards)

        field["conditions"] = field_conditions
        field["hazards"] = hazards

        return field

    def stat_mult_to_add(self, stat, mult):
        convert_norm = {
            .67: -1,
            .5: -2,
            .4: -3,
            .33: -4,
            .29: -5,
            .25: -6,
            1.5: 1,
            2: 2,
            2.5: 3,
            3: 4,
            3.5: 5,
            4: 6
        }
        convert_ae = {
            0.75: -1,
            0.6: -2,
            0.5: -3,
            0.43: -4,
            0.38: -5,
            0.33: -6,
            1.33: 1,
            1.67: 2,
            2: 3,
            2.33: 4,
            2.67: 5,
            3: 6
        }
        if stat == 'Evasion' or stat == 'Accuracy':
            return convert_ae[mult]
        else:
            return convert_norm[mult]

    def stat_add_to_mult(self, stat, add):
        convert_norm = {
            -1: float(2/3),
            -2: 0.5,
            -3: .4,
            -4: float(1/3),
            -5: float(2/7),
            -6: .25,
            1: 1.5,
            2: 2,
            3: 2.5,
            4: 3,
            5: 3.5,
            6: 4
        }
        convert_ae = {
            -1: 0.75,
            -2: 0.6,
            -3: 0.5,
            -4: float(3/7),
            -5: float(3/8),
            -6: float(1/3),
            1: float(4/3),
            2: float(5/3),
            3: 2,
            4: float(7/3),
            5: float(8/3),
            6: 3
        }
        if stat == 'Envasion' or stat == 'Accuracy':
            return convert_ae[add]
        else:
            return convert_norm[add]

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
                except StaleElementReferenceException:
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='tooltip']"))).find_element_by_css_selector("img[alt='{}']".format(g))
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
                "moves": []
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
