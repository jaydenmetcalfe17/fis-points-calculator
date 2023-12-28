## ONLY SUPPORT SL AND GS AS OF RIGHT NOW
from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import json
import sys

from flask import Flask, jsonify, request, render_template

## Due to version compatibility issues, ChromeDriver is manually installed since Selenium Manager is not currently working

##UPDATE CHROME_DRIVER_PATH SPECIFIC TO DEVICE 
chrome_driver_path = ""
chrome_service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=chrome_service)

F_FACTOR = 0
LIST_OF_RACERS = []
POINTS_LIST = []
TIMES_LIST = []
NAMES_LIST = []



class Racer:
    def __init__(self, name, points, r1, r2, total):
        self.name = name
        self.points = points
        self.r1 = r1
        self.r2 = r2
        self.total = total       


class PenaltyCalculation:
    def __init__(self, LIST_OF_RACERS, factor):
        self.LIST_OF_RACERS = LIST_OF_RACERS
        self.factor = factor
    
    def calculate_factor():
        discipline = driver.title
        if (" SL " in discipline):
            F_FACTOR = 730
        if (" GS " in discipline):
            F_FACTOR = 1010
        if ("SG" in discipline):
            F_FACTOR = 1190
        if ("DH" in discipline):
            F_FACTOR = 1250
        return F_FACTOR  
    
    def time_to_int(string_time):
        colon_index = string_time.find(":")
        decimal_index = string_time.find(".")

        minutes = float((string_time[0:colon_index])) * 60
        seconds = float(string_time[colon_index + 1:decimal_index])
        milliseconds = float(string_time[decimal_index+1:]) / 100

        time_in_sec = minutes + seconds + milliseconds
        return(time_in_sec)
    
    def calculate_points_per_second():
        ## BEST 2 TIMES ##
        F_FACTOR = PenaltyCalculation.calculate_factor()
        TIMES_LIST.sort()
        winner_time = PenaltyCalculation.time_to_int(TIMES_LIST[0])
        second_time = PenaltyCalculation.time_to_int(TIMES_LIST[1])

        time_difference = second_time - winner_time
        if (time_difference == 0):
            return 0
        else:
            ## POINTS PER SECOND ##
            ##((((F-Factor * 2nd place time) / winner time) - F-Factor) / difference of times)
            points_per_second = ((((F_FACTOR * second_time) / winner_time ) - F_FACTOR) / time_difference)
            return points_per_second
    
    def calculate_race_points(racer_time):
        ##race points = difference from first * points per second
        racer_time_int = PenaltyCalculation.time_to_int(racer_time)
        winner = PenaltyCalculation.time_to_int(TIMES_LIST[0])
        diff = racer_time_int - winner
        pps = PenaltyCalculation.calculate_points_per_second()
        race_points = diff * pps
        return round(race_points, 2)
    
    def best5_racers(racers_list):
        top5_racers = []

        temp_points_list = []
        for racer in racers_list:
            temp_points_list.append(racer.points)

        temp_points_list.sort()
        top5points = temp_points_list[0:5]
        for racer in racers_list:
            if racer.points in top5points:
                top5_racers.append(racer)

        return top5_racers

    def top5_in_top10():
        ## TOP 10 TIMES ##
        TIMES_LIST.sort()
        top10times = TIMES_LIST[0:10]
        i = 9
        while (TIMES_LIST[i] == TIMES_LIST[i+1]):
            top10times.append(TIMES_LIST[i])
            i+=1

        ## TOP 10 NAMES ##
        top10racers = []
        for racer in LIST_OF_RACERS:
            if racer.total in top10times:
                top10racers.append(racer)

        top5_in10_racers = PenaltyCalculation.best5_racers(top10racers)
        return(top5_in10_racers)
    
    ## POINTS OF BEST 5 IN TOP 10 ##
    def calculateA():
        best5 = PenaltyCalculation.top5_in_top10()
        
        ## POINTS TOTAL ##
        a_total = 0
        for racer in best5:
            a_total += racer.points
        return round(a_total, 2)
    
    ## BEST 5 RACERS AT START ##
    def calculateB():
        best5 = PenaltyCalculation.best5_racers(LIST_OF_RACERS)
        b_total = 0
        for racer in best5:
            b_total += racer.points
        return round(b_total, 2)


    ### BEST 5 IN 10 RACE POINTS ###
    def calculateC():
        best5 = PenaltyCalculation.top5_in_top10()
    
        c_total = 0
        for racer in best5:
            rp = PenaltyCalculation.calculate_race_points(racer.total)
            c_total += rp

        return round(c_total,2)

    ## PENALTY CALCULATION
    def calculate_penalty():
        a = PenaltyCalculation.calculateA()
        b = PenaltyCalculation.calculateB()
        c = PenaltyCalculation.calculateC()
 
        penalty = (a + b - c) / 10
        return round(penalty, 2)

    def calculate_score(racer):
        if (racer.total == "DNF" or racer.total == "DQ" or racer.total == "DNS"):
            return racer.total
        
        penalty = PenaltyCalculation.calculate_penalty()
        race_points = PenaltyCalculation.calculate_race_points(racer.total)
        score = penalty + race_points
        return (round(score, 2))
    
    def all_racers_scores():
        all_scores = {}
        for racer in LIST_OF_RACERS:
            all_scores[racer.name] = PenaltyCalculation.calculate_score(racer)
        return all_scores
    
    def print_scores():
        scores = PenaltyCalculation.all_racers_scores()
        for racer in scores:
            print(": ".join([racer, str(scores.get(racer))]))


    # def process_link(link):
    #     processed_result = f"Processed link: {link.upper()}"
    #     return processed_result

    
def main():

    WEBSITE_LINK = sys.argv[1]
    #WEBSITE_LINK = "https://live-timing.com/race2.php?r=253961"


    driver.get(WEBSITE_LINK)
    driver.implicitly_wait(0.5)
    driver.maximize_window()
    driver.implicitly_wait(0.5)

    rows = driver.find_elements(By.CLASS_NAME, "table")
    names_list_length = (len(rows))

    i = 2
    while (i < names_list_length + 2):
        if (i == 12):
            i+=1
            continue
        
        bib_element = driver.find_element(By.XPATH, str(i).join(["//*[@id='resultTable']/tbody/tr[","]/td[2]/div"]))
                
        actions = ActionChains(driver)
        points_mover = actions.move_to_element(bib_element).perform()
        points_element = driver.find_element(By.XPATH, "//*[@id='tooltip']/table/tbody/tr[5]/td[3]/font")
        name_element = driver.find_element(By.XPATH, "//*[@id='tooltip']/table/tbody/tr[1]/td[2]/font")


        points = float(points_element.text)

        name = name_element.text.strip()

        r1_element = driver.find_element(By.XPATH, str(i).join(["//*[@id='resultTable']/tbody/tr[","]/td[7]/div"]))
        r1 = r1_element.text.strip()

        r2_element = driver.find_element(By.XPATH, str(i).join(["//*[@id='resultTable']/tbody/tr[","]/td[8]/div"])) 
        r2 = r2_element.text.strip()

        total = ""

        if ("DQ" not in r1 and "DQ" not in r2):
            if(("DNF" in r1) or ("DNF" in r2) or ("DNS" in r2)):
                TIMES_LIST.append("DNF")
                total = "DNF"
            elif ("DNS" in r1):
                TIMES_LIST.append("DNS")
                total = "DNS"
            else:
                total_element = driver.find_element(By.XPATH, str(i).join(["//*[@id='resultTable']/tbody/tr[","]/td[9]/div"]))
                total = total_element.text.strip()
                TIMES_LIST.append(total)
        else:
            TIMES_LIST.append("DQ")
            total = "DQ"
                
        i+=1

        racer = Racer(name, points, r1, r2, total)
        LIST_OF_RACERS.append(racer)
        POINTS_LIST.append(points)

    print(json.dumps(PenaltyCalculation.all_racers_scores()))

if __name__ == '__main__':
     main()