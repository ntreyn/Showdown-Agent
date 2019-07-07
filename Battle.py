

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

class Battle:

    def __init__(self, driver, pokedex, agent_team):
        self.driver = driver
        self.pokedex = pokedex

        self.done = False
        self.turn = 1

        self.agent_team = agent_team
        self.opponent_team = []
    
    def battle(self):

        wait = WebDriverWait(self.driver, 10)
        self.set_teams(wait)

        self.mask = Mask()
        self.agent = Agent(self.mask)


        while not self.done:
            self.execute_turn()

    def execute_turn(self):

        # Speed and damage calcs
        # Assess switches (both sides)

        # Assess following turns

        # Choose action
        # Attack or switch

        # Update info

        action = self.agent.get_action()
        self.execute_action(action)



        self.turn += 1
        self.done = True


    def execute_action(self, action):




        
        self.update_mask()    

    def update_mask(self):
        pass

    def set_teams(self, wait):
        for i, a in enumerate(self.agent_team):
            if a.set.gender is None:
                gender = self.get_agent_team_gender(wait, i)
                a.set.update_set({ "gender": gender })
        
        self.get_opposing_team(wait)

    def set_opposing_team(self, team_list):
        
        for d in team_list:
            pokemon = self.pokedex.get_pokemon(d.pop("species"))
            pokemon.create_set(d)
            self.opponent_team.append(pokemon)

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
                item = True
            else:
                item = False

            team_list.append({ "species": name, "level": level, "gender": gender, "item": item })
            
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
