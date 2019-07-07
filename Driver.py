

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException

import time
import re

from Battle import Battle
from Pokedex import Pokedex

class ShowdownDriver:

    def __init__(self):
        self.url = "https://play.pokemonshowdown.com/"
        self.user = "Contorted Bot"
        self.password = "12345"

        self.test_opp = "Contorted Lies"
        self.tier = "gen7ou"
        # self.team_file = "teams.txt"
        self.team_file = "sample_team.txt"

        self.team_name = "Untitled 11"

        self.pokedex = Pokedex()

    def run(self):
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        wait = WebDriverWait(self.driver, 30)

        self.login(wait)
        self.mute(wait)

        self.load_teams(wait)
        # self.find_ladder_game(wait)
        self.challenge_opponent(wait)

        self.quit()

    def login(self, wait):
        choose_name_button = wait.until(EC.visibility_of_element_located((By.NAME, "login")))
        choose_name_button.click()

        username_field = wait.until(EC.visibility_of_element_located((By.NAME,"username")))
        username_field.send_keys(self.user)

        submit_username_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
        submit_username_button.click()

        password_field = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
        password_field.send_keys(self.password)

        login_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
        login_button.click()

    def mute(self, wait):
        hide_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='closeHide']")))
        hide_button.click()

        sounds_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='openSounds']")))
        sounds_button.click()

        mute_checkbox = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='muted']")))
        mute_checkbox.click()

        sounds_button.click()

    def load_teams(self, wait):
        teambuilder_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[value='teambuilder']")))
        teambuilder_button.click()

        backup_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='backup']")))
        backup_button.click()

        f = open(self.team_file, 'r')
        teams = f.read()
        f.close()

        self.create_team(teams)

        teams_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea[class='textbox']")))
        teams_field.send_keys(teams)

        save_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='saveBackup']")))
        save_button.click()

        close_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='closeRoom']")))
        close_button.click()

    def change_gen(self, wait):
        format_button = wait.until(EC.visibility_of_element_located((By.NAME, "format")))
        format_button.click()

        tier_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[value='{}']".format(self.tier))))
        tier_button.click()

    def create_team(self, teams_str):
        teams_list = teams_str.splitlines()
        team_line = "=== [{}] {} ===".format(self.tier, self.team_name)
        index = teams_list.index(team_line)
        next_index = index + 1

        self.selected_team = []
        
        while "===" not in teams_list[next_index]:
            line = teams_list[next_index]
            
            if teams_list[next_index - 1] == '' and line != '':

                item = None
                gender = None
                nick = None

                misc, item = line.split('@')
                item = item.strip()
                misc = misc.strip()

                reg_gend = re.search('(\([MF]\))', misc)
                if reg_gend is not None:
                    gender = reg_gend.group(0)[1]
                    misc = misc[:-4]

                reg_species_w_nick = re.search('\(([^)]+)\)', misc)
                if reg_species_w_nick is not None:
                    species = reg_species_w_nick[1]
                    nick = misc.replace(reg_species_w_nick[0], "").strip()
                else:
                    species = misc.strip()

                next_index += 1
                line = teams_list[next_index]

                ability = line[9:]

                next_index += 1
                line = teams_list[next_index]

                level = 100
                shiny = False
                happiness = 255

                if line[0] == 'L':
                    level = int(line[7:].strip())
                    next_index += 1
                    line = teams_list[next_index]
                if line[0] == 'S':
                    shiny = True
                    next_index += 1
                    line = teams_list[next_index]
                if line[0] == 'H':
                    happiness = int(line[11:].strip())
                    next_index += 1
                    line = teams_list[next_index]
                
                ev_line = line[5:].split('/')
                ev_dict = {}
                for temp in ev_line:
                    stat = temp.strip()[-3:].strip()
                    ev = int(temp.strip().split()[0])
                    ev_dict[stat] = ev

                next_index += 1
                line = teams_list[next_index]
                
                if line.strip()[-6:] == "Nature":
                    nature = line.split()[0]
                    next_index += 1
                    line = teams_list[next_index]
                else:
                    nature = "Serious"
                

                iv_dict = {}
                if line[0] == 'I':
                    iv_line = line[5:].split('/')
                    for temp in iv_line:
                        stat = temp.strip()[-3:].strip()
                        iv = int(temp.strip().split()[0])
                        iv_dict[stat] = iv

                moves = []
                while line != '':
                    moves.append(line[2:])
                    next_index += 1
                    if next_index >= len(teams_list):
                        break
                    line = teams_list[next_index]
                
                set_dict = {
                    "species": species,
                    "nickname": nick,
                    "gender": gender,
                    "item": item,
                    "ability": ability,
                    "level": level,
                    "shiny": shiny,
                    "happiness": happiness,
                    "EVs": ev_dict,
                    "nature": nature,
                    "IVs": iv_dict,
                    "moves": moves
                }

                pokemon = self.pokedex.get_pokemon(species)
                pokemon.create_set(set_dict)
                self.selected_team.append(pokemon)

            next_index += 1
            if next_index >= len(teams_list):
                break

    def choose_team(self, wait):
        team_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='team']")))
        team_button.click()
        
        team_selection = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), '{}')]".format(self.team_name))))
        team_selection.click()

    def find_ladder_game(self, wait):
        self.change_gen(wait)
        self.choose_team(wait)

        search_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[class='button mainmenu1 big']")))
        search_button.click()

        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='battle']")))
            self.start_battle(wait)
        except TimeoutException:
            print("Could not find battle")
            return

    def challenge_opponent(self, wait):
        find_user_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='finduser']")))
        find_user_button.click()

        username_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='data']")))
        username_field.send_keys(self.test_opp)

        time.sleep(1)
        
        open_user_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
        open_user_button.click()
        
        try:
            challenge_button = wait.until(EC.visibility_of_element_located((By.NAME, "challenge")))
            challenge_button.click()
        except StaleElementReferenceException:
            challenge_button = wait.until(EC.visibility_of_element_located((By.NAME, "challenge")))
            challenge_button.click()
        
        self.change_gen(wait)
        self.choose_team(wait)

        challenge_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='makeChallenge']")))
        challenge_button.click()

        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='battle']")))
            self.start_battle(wait)
        except TimeoutException:
            cancel_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='cancelChallenge']")))
            cancel_button.click()
            return

    def accept_challenge(self, wait):
        self.choose_team(wait)

        accept_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[name='acceptChallenge']")))
        accept_button.click()

        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='battle']")))
            self.start_battle(wait)     
        except TimeoutException:
            return

    def start_battle(self, wait):
        battle = Battle(self.driver, self.pokedex, self.selected_team)
        battle.battle()

    def quit(self):
        while(True):
            s = input("Type 'q' to quit: ")

            if s == 'q':
                self.driver.quit()
                break
            

def main():
    
    sd = ShowdownDriver()
    sd.run()

if __name__ == "__main__":
    main()