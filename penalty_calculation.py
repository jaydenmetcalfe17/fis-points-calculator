## ONLY SUPPORT SL AND GS AS OF RIGHT NOW
import json
import sys


class Racer:
    def __init__(self, name, points, r1, r2, total, totalAsInt):
        self.name = name
        self.points = points
        self.r1 = r1
        self.r2 = r2
        self.total = total  
        self.totalAsInt = totalAsInt     


class PenaltyCalculation:
    DISCIPLINES = {
        "Slalom": 730,
        "Giant Slalom": 1010,
        "Super G": 1190,
        "Super-G": 1190,
        "Downhill": 1250,
    }

    def __init__(self, racers_list, discipline, times_list):
        self.racers_list = racers_list
        self.discipline = discipline
        self.times_list = times_list
    
    def calculate_factor(self):
        return self.DISCIPLINES.get(self.discipline, 0)

    
    def calculate_points_per_second(self):
        ## BEST 2 TIMES ##
        self.times_list.sort()
        winner_time = (self.times_list[0] / 1000)
        second_time = (self.times_list[1] / 1000)
        f_factor = self.calculate_factor()

        time_difference = second_time - winner_time
        if (time_difference == 0):
            return 0
        else:
            ## POINTS PER SECOND ##
            ##((((F-Factor * 2nd place time) / winner time) - F-Factor) / difference of times)
            points_per_second = ((((f_factor * second_time) / winner_time ) - f_factor) / time_difference)
            return points_per_second
    
    def calculate_race_points(self, racer_time):
        ##race points = difference from first * points per second
        racer_time_int = racer_time / 1000
        winner = self.times_list[0] / 1000
        diff = racer_time_int - winner
        pps = self.calculate_points_per_second()
        race_points = diff * pps
        return round(race_points, 2)
    
    def best5_racers(self, racers = None):
        if racers == None:
            racers = self.racers_list
        

        ## THIS COULD BE CLEANER
        top5_racers_all = sorted(racers, key=lambda r: r.points)
        top5_racers = []
        for r in top5_racers_all:
            if (self.discipline in ["Super G", "Super-G", "Downhill"]):
                if (r.r1 != "DNS"):
                    top5_racers.append(r)
            elif (r.r1 != "DNS" and r.r2 != "DNS"):
                top5_racers.append(r)

        return top5_racers[:5]

    def top5_in_top10(self):
        self.times_list.sort()
        top10_times = self.times_list[:10]
        top10_racers = [racer for racer in self.racers_list if racer.totalAsInt in top10_times]
        return self.best5_racers(top10_racers)
    
    ## POINTS OF BEST 5 IN TOP 10 ##
    def calculateA(self):
        best5 = self.top5_in_top10()
        ## POINTS TOTAL ##
        
        return round(sum(racer.points for racer in best5), 2)
    
    ## BEST 5 RACERS AT START ##
    def calculateB(self):
       best5 = self.best5_racers()
       return round(sum(racer.points for racer in best5), 2)


    ### BEST 5 IN 10 RACE POINTS ###
    def calculateC(self):
        best5 = self.top5_in_top10()
        c_total = sum(self.calculate_race_points(racer.totalAsInt) for racer in best5)
        return round(c_total,2)

    ## PENALTY CALCULATION
    def calculate_penalty(self):
        a = self.calculateA()
        b = self.calculateB()
        c = self.calculateC()
 
        penalty = (a + b - c) / 10
        return round(penalty, 2)

    def calculate_score(self, racer):
        if (self.discipline in ["Super G", "Super-G", "Downhill"]):
            if (racer.r1 in ["DNF", "DQ", "DNS"]):
                return racer.r1
            
        elif (racer.r2 in ["DNF", "DQ", "DNS"]) and (self.discipline not in ["Super G", "Super-G", "Downhill"]):
            return racer.r2
        
        penalty = self.calculate_penalty()
        race_points = self.calculate_race_points(racer.totalAsInt)
        score = penalty + race_points
        return (round(score, 2))
    

    def all_racers_scores(self):
        all_scores = {racer.name: self.calculate_score(racer) for racer in self.racers_list}

        finishers = {k: v for k, v in all_scores.items() if isinstance(v, (int, float))}
        non_finishers = {k: v for k, v in all_scores.items() if not isinstance(v, (int, float))}

        sorted_scores = {**dict(sorted(finishers.items(), key=lambda item: item[1])), **non_finishers}

        return sorted_scores
    
    def print_scores(self):
        scores = self.all_racers_scores()
        for racer in scores:
            print(": ".join([racer, str(scores.get(racer))]))
    
def main():

    ## WHEN RUNNING WITH SERVER 
    COMPS = json.loads(sys.argv[1])
    DISCIPLINE = sys.argv[2]

    ## FOR MANUAL TESTING PURPOSES (1 Super-G, 1 Slalom): 

    # DISCIPLINE = "Super-G"
    # COMPS = [{"rank":"","bib":"25","name":"BEXTON, Gemma","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"DNF","totalAsInt":2147483500,"fnumber":"108124","fpoints":"14124"},{"rank":"","bib":"27","name":"ROSENBLUTH, Joanna","r1":"1:12.87","r1AsInt":"72870","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:12.87","totalAsInt":2147483500,"fnumber":"6536717","fpoints":"14113"},{"rank":"","bib":"34","name":"LAMBERT, Mathilde","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"DNF","totalAsInt":2147483500,"fnumber":"108335","fpoints":"99999"},{"rank":"","bib":"8","name":"GAGNON, Marie-Michele","r1":"DNS","r1AsInt":"2147483607","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"105269","fpoints":"549"},{"rank":"","bib":"32","name":"HOLLISTER, Alexis","r1":"1:19.59","r1AsInt":"79590","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:19.59","totalAsInt":2147483500,"fnumber":"6536735","fpoints":"22004"},{"rank":"","bib":"23","name":"BERTRAND-DUBE, Marie","r1":"1:16.53","r1AsInt":"76530","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:16.53","totalAsInt":2147483500,"fnumber":"108115","fpoints":"14660"},{"rank":"","bib":"29","name":"HARVEY, Keirsten","r1":"1:15.72","r1AsInt":"75720","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:15.72","totalAsInt":2147483500,"fnumber":"108136","fpoints":"14709"},{"rank":"","bib":"21","name":"GRAY, Jacquelyn","r1":"1:15.52","r1AsInt":"75520","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:15.52","totalAsInt":2147483500,"fnumber":"108262","fpoints":"13118"},{"rank":"","bib":"26","name":"BOUTIN, Megane","r1":"1:15.01","r1AsInt":"75010","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:15.01","totalAsInt":2147483500,"fnumber":"108256","fpoints":"14011"},{"rank":"","bib":"31","name":"GOULET, Sarah-Maude","r1":"1:13.88","r1AsInt":"73880","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:13.88","totalAsInt":2147483500,"fnumber":"108103","fpoints":"21182"},{"rank":"","bib":"24","name":"ANDERSON, Grace","r1":"1:13.87","r1AsInt":"73870","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:13.87","totalAsInt":2147483500,"fnumber":"108254","fpoints":"11147"},{"rank":"","bib":"22","name":"FAFARD, Charlotte","r1":"1:13.40","r1AsInt":"73400","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:13.40","totalAsInt":2147483500,"fnumber":"108301","fpoints":"13436"},{"rank":"","bib":"17","name":"ALEXANDER, Ashleigh","r1":"1:13.39","r1AsInt":"73390","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:13.39","totalAsInt":2147483500,"fnumber":"107991","fpoints":"7591"},{"rank":"","bib":"13","name":"LEBSACK, Avery","r1":"1:13.22","r1AsInt":"73220","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:13.22","totalAsInt":2147483500,"fnumber":"108086","fpoints":"8045"},{"rank":"","bib":"30","name":"HOSHIZAKI, Tora","r1":"1:12.94","r1AsInt":"72940","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:12.94","totalAsInt":2147483500,"fnumber":"108085","fpoints":"9841"},{"rank":"","bib":"3","name":"SMITH, Chelsea","r1":"1:12.35","r1AsInt":"72350","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:12.35","totalAsInt":2147483500,"fnumber":"6536594","fpoints":"14810"},{"rank":"","bib":"19","name":"KRANJC, Kristen Gigi","r1":"1:12.08","r1AsInt":"72080","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:12.08","totalAsInt":2147483500,"fnumber":"108111","fpoints":"8205"},{"rank":"","bib":"16","name":"HUME, Helen","r1":"1:11.70","r1AsInt":"71700","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:11.70","totalAsInt":2147483500,"fnumber":"107879","fpoints":"7539"},{"rank":"","bib":"4","name":"ROSS, Julia","r1":"1:11.39","r1AsInt":"71390","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:11.39","totalAsInt":2147483500,"fnumber":"108125","fpoints":"9915"},{"rank":"","bib":"5","name":"CUNNINGHAM, Haley","r1":"1:11.37","r1AsInt":"71370","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:11.37","totalAsInt":2147483500,"fnumber":"108080","fpoints":"9526"},{"rank":"","bib":"12","name":"BONNEVILLE, Jade","r1":"1:11.13","r1AsInt":"71130","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:11.13","totalAsInt":2147483500,"fnumber":"108255","fpoints":"7069"},{"rank":"","bib":"28","name":"BEAUVAIS, Lara","r1":"1:11.11","r1AsInt":"71110","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:11.11","totalAsInt":2147483500,"fnumber":"108114","fpoints":"9770"},{"rank":"","bib":"33","name":"LAMONTAGNE, Justine","r1":"1:10.96","r1AsInt":"70960","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:10.96","totalAsInt":2147483500,"fnumber":"108336","fpoints":"99999"},{"rank":"","bib":"14","name":"ALEXANDER, Kiara","r1":"1:10.05","r1AsInt":"70050","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:10.05","totalAsInt":2147483500,"fnumber":"108095","fpoints":"5324"},{"rank":"","bib":"20","name":"MAH, Nicole","r1":"1:09.96","r1AsInt":"69960","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:09.96","totalAsInt":2147483500,"fnumber":"107869","fpoints":"7542"},{"rank":"","bib":"9","name":"BENNETT, Sarah","r1":"1:09.45","r1AsInt":"69450","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:09.45","totalAsInt":2147483500,"fnumber":"108075","fpoints":"5213"},{"rank":"","bib":"10","name":"BEAUCHAMP, Caroline","r1":"1:09.15","r1AsInt":"69150","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:09.15","totalAsInt":2147483500,"fnumber":"107983","fpoints":"7261"},{"rank":"","bib":"1","name":"METCALFE, Jayden","r1":"1:08.94","r1AsInt":"68940","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:08.94","totalAsInt":2147483500,"fnumber":"108143","fpoints":"12879"},{"rank":"","bib":"7","name":"CARDINAL, Frederique","r1":"1:08.90","r1AsInt":"68900","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:08.90","totalAsInt":2147483500,"fnumber":"107984","fpoints":"7528"},{"rank":"","bib":"15","name":"VAN SOEST, Katrina","r1":"1:08.82","r1AsInt":"68820","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:08.82","totalAsInt":2147483500,"fnumber":"107951","fpoints":"5962"},{"rank":"","bib":"18","name":"RENZONI, Ella","r1":"1:08.48","r1AsInt":"68480","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:08.48","totalAsInt":2147483500,"fnumber":"107993","fpoints":"5231"},{"rank":"","bib":"2","name":"CARRIER, Olivia","r1":"1:08.45","r1AsInt":"68450","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:08.45","totalAsInt":2147483500,"fnumber":"108116","fpoints":"11120"},{"rank":"","bib":"6","name":"LEVER, Beatrix","r1":"1:07.51","r1AsInt":"67510","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:07.51","totalAsInt":2147483500,"fnumber":"107762","fpoints":"2794"},{"rank":"","bib":"11","name":"TIMMERMANN, Claire","r1":"1:08.35","r1AsInt":"68350","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"1:08.35","totalAsInt":2147483500,"fnumber":"108018","fpoints":"5546"}] 
    
    
    # DISCIPLINE = "Slalom"
    # COMPS = [{"rank":"","bib":"80","name":"PARENT, Maxim","r1":"DNS","r1AsInt":"2147483607","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108590","fpoints":"25909"},{"rank":"","bib":"79","name":"JOANISSE, Lyana","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108709","fpoints":"23365"},{"rank":"","bib":"78","name":"CLOUTIER, Leanne","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108479","fpoints":"20963"},{"rank":"","bib":"77","name":"BOISVERT, Rose","r1":"59.23","r1AsInt":"59230","r1Rank":"","r2":"1:00.86","r2AsInt":"60860","r2Rank":"","total":"2:00.09","totalAsInt":120090,"fnumber":"108319","fpoints":"17516"},{"rank":"","bib":"76","name":"TETREAULT, Mariane","r1":"DNS","r1AsInt":"2147483607","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108475","fpoints":"17138"},{"rank":"","bib":"75","name":"YARDLEY, Keira","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"6537602","fpoints":"16945"},{"rank":"","bib":"74","name":"ALAIN, Alice","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108713","fpoints":"16614"},{"rank":"","bib":"73","name":"ALEXANDER, Josie","r1":"DQg7","r1AsInt":"2147483627","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"6537315","fpoints":"15873"},{"rank":"","bib":"72","name":"LEGAULT, Arielle","r1":"DQg7","r1AsInt":"2147483627","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108700","fpoints":"15771"},{"rank":"","bib":"71","name":"PARENTEAU, Laurence","r1":"DQg7","r1AsInt":"2147483627","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108603","fpoints":"15589"},{"rank":"","bib":"70","name":"DAWOOD, Nora","r1":"DQg7","r1AsInt":"2147483627","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108693","fpoints":"15565"},{"rank":"","bib":"69","name":"SARGENT, Sophie","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"6536900","fpoints":"15273"},{"rank":"","bib":"68","name":"BOILY, L.aurence","r1":"59.20","r1AsInt":"59200","r1Rank":"","r2":"58.85","r2AsInt":"58850","r2Rank":"","total":"1:58.05","totalAsInt":118050,"fnumber":"108697","fpoints":"14409"},{"rank":"","bib":"67","name":"DAJANI, Lanielle","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108686","fpoints":"14221"},{"rank":"","bib":"66","name":"BEAUCHEMIN, Anne-Sophie","r1":"59.22","r1AsInt":"59220","r1Rank":"","r2":"57.99","r2AsInt":"57990","r2Rank":"","total":"1:57.21","totalAsInt":117210,"fnumber":"107881","fpoints":"13823"},{"rank":"","bib":"65","name":"DONAHUE, Beatrice","r1":"58.91","r1AsInt":"58910","r1Rank":"","r2":"59.12","r2AsInt":"59120","r2Rank":"","total":"1:58.03","totalAsInt":118030,"fnumber":"108706","fpoints":"13693"},{"rank":"","bib":"64","name":"CARTER, Sara","r1":"59.44","r1AsInt":"59440","r1Rank":"","r2":"1:06.16","r2AsInt":"66160","r2Rank":"","total":"2:05.60","totalAsInt":125600,"fnumber":"108671","fpoints":"13670"},{"rank":"","bib":"63","name":"REAIN, Riley","r1":"1:04.48","r1AsInt":"64480","r1Rank":"","r2":"1:02.60","r2AsInt":"62600","r2Rank":"","total":"2:07.08","totalAsInt":127080,"fnumber":"108651","fpoints":"13079"},{"rank":"","bib":"62","name":"GILMOUR, Nicola","r1":"59.75","r1AsInt":"59750","r1Rank":"","r2":"1:00.61","r2AsInt":"60610","r2Rank":"","total":"2:00.36","totalAsInt":120360,"fnumber":"108586","fpoints":"12746"},{"rank":"","bib":"61","name":"DIMKINA, Kalina","r1":"DQg7","r1AsInt":"2147483627","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108726","fpoints":"12250"},{"rank":"","bib":"60","name":"HOUDE, Kelly-Ann","r1":"DQg62","r1AsInt":"2147483627","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108424","fpoints":"12159"},{"rank":"","bib":"59","name":"BOUCHARD, Kymie","r1":"DQg7","r1AsInt":"2147483627","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108754","fpoints":"11910"},{"rank":"","bib":"58","name":"TELLIER, Valerie","r1":"DNS","r1AsInt":"2147483607","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108474","fpoints":"11543"},{"rank":"","bib":"57","name":"LAPERRIERE, Coralie","r1":"58.99","r1AsInt":"58990","r1Rank":"","r2":"57.66","r2AsInt":"57660","r2Rank":"","total":"1:56.65","totalAsInt":116650,"fnumber":"108506","fpoints":"11389"},{"rank":"","bib":"56","name":"LEMIRE, Sarah-Maude","r1":"57.68","r1AsInt":"57680","r1Rank":"","r2":"57.34","r2AsInt":"57340","r2Rank":"","total":"1:55.02","totalAsInt":115020,"fnumber":"108428","fpoints":"11271"},{"rank":"","bib":"55","name":"CORMIER, Cassandra","r1":"54.96","r1AsInt":"54960","r1Rank":"","r2":"54.52","r2AsInt":"54520","r2Rank":"","total":"1:49.48","totalAsInt":109480,"fnumber":"108468","fpoints":"11086"},{"rank":"","bib":"54","name":"ROBERT, Maika","r1":"56.76","r1AsInt":"56760","r1Rank":"","r2":"57.92","r2AsInt":"57920","r2Rank":"","total":"1:54.68","totalAsInt":114680,"fnumber":"108736","fpoints":"10692"},{"rank":"","bib":"53","name":"BOIES, Charlotte","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108691","fpoints":"10544"},{"rank":"","bib":"52","name":"BOUCHARD, Laurence","r1":"55.00","r1AsInt":"55000","r1Rank":"","r2":"53.90","r2AsInt":"53900","r2Rank":"","total":"1:48.90","totalAsInt":108900,"fnumber":"108715","fpoints":"10309"},{"rank":"","bib":"51","name":"HOWARD, Hazel","r1":"56.65","r1AsInt":"56650","r1Rank":"","r2":"56.26","r2AsInt":"56260","r2Rank":"","total":"1:52.91","totalAsInt":112910,"fnumber":"6537333","fpoints":"10075"},{"rank":"","bib":"50","name":"NOEL, Florence","r1":"59.60","r1AsInt":"59600","r1Rank":"","r2":"59.29","r2AsInt":"59290","r2Rank":"","total":"1:58.89","totalAsInt":118890,"fnumber":"108704","fpoints":"9976"},{"rank":"","bib":"49","name":"PICHE, Camille","r1":"55.27","r1AsInt":"55270","r1Rank":"","r2":"54.31","r2AsInt":"54310","r2Rank":"","total":"1:49.58","totalAsInt":109580,"fnumber":"108724","fpoints":"9556"},{"rank":"","bib":"48","name":"BUZDUGAN, Sara","r1":"54.38","r1AsInt":"54380","r1Rank":"","r2":"54.80","r2AsInt":"54800","r2Rank":"","total":"1:49.18","totalAsInt":109180,"fnumber":"108606","fpoints":"9347"},{"rank":"","bib":"47","name":"CARDIN, Aube","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108725","fpoints":"9298"},{"rank":"","bib":"46","name":"GEBHARDT, Kelly","r1":"57.33","r1AsInt":"57330","r1Rank":"","r2":"57.44","r2AsInt":"57440","r2Rank":"","total":"1:54.77","totalAsInt":114770,"fnumber":"6537036","fpoints":"9281"},{"rank":"","bib":"45","name":"LEGAULT, Cassandre","r1":"53.83","r1AsInt":"53830","r1Rank":"","r2":"55.02","r2AsInt":"55020","r2Rank":"","total":"1:48.85","totalAsInt":108850,"fnumber":"107987","fpoints":"9167"},{"rank":"","bib":"44","name":"BOUTIN, Megane","r1":"55.03","r1AsInt":"55030","r1Rank":"","r2":"DNF","r2AsInt":"2147483617","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108256","fpoints":"9124"},{"rank":"","bib":"43","name":"DESROSIERS, Laurence","r1":"55.70","r1AsInt":"55700","r1Rank":"","r2":"56.17","r2AsInt":"56170","r2Rank":"","total":"1:51.87","totalAsInt":111870,"fnumber":"108584","fpoints":"9106"},{"rank":"","bib":"42","name":"MUSCARELLA, Simona","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"6537326","fpoints":"8890"},{"rank":"","bib":"41","name":"VAN STRIEN, Maxine","r1":"56.26","r1AsInt":"56260","r1Rank":"","r2":"56.70","r2AsInt":"56700","r2Rank":"","total":"1:52.96","totalAsInt":112960,"fnumber":"108580","fpoints":"8824"},{"rank":"","bib":"40","name":"CORNISH, Molly","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108721","fpoints":"8684"},{"rank":"","bib":"39","name":"NOYES, Althea","r1":"54.31","r1AsInt":"54310","r1Rank":"","r2":"DNF","r2AsInt":"2147483617","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"6537549","fpoints":"8661"},{"rank":"","bib":"38","name":"QUEALLY, Molly","r1":"54.02","r1AsInt":"54020","r1Rank":"","r2":"55.08","r2AsInt":"55080","r2Rank":"","total":"1:49.10","totalAsInt":109100,"fnumber":"6537284","fpoints":"8556"},{"rank":"","bib":"37","name":"GOULET, Corinne","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"107882","fpoints":"8325"},{"rank":"","bib":"36","name":"ARBEC, Sarah Jane","r1":"54.72","r1AsInt":"54720","r1Rank":"","r2":"53.99","r2AsInt":"53990","r2Rank":"","total":"1:48.71","totalAsInt":108710,"fnumber":"108315","fpoints":"8134"},{"rank":"","bib":"35","name":"HUME, Helen","r1":"54.84","r1AsInt":"54840","r1Rank":"","r2":"53.17","r2AsInt":"53170","r2Rank":"","total":"1:48.01","totalAsInt":108010,"fnumber":"107879","fpoints":"8086"},{"rank":"","bib":"34","name":"FAFARD, Charlotte","r1":"57.26","r1AsInt":"57260","r1Rank":"","r2":"56.72","r2AsInt":"56720","r2Rank":"","total":"1:53.98","totalAsInt":113980,"fnumber":"108301","fpoints":"8073"},{"rank":"","bib":"33","name":"BEAUSEJOUR, Agathe","r1":"54.75","r1AsInt":"54750","r1Rank":"","r2":"53.99","r2AsInt":"53990","r2Rank":"","total":"1:48.74","totalAsInt":108740,"fnumber":"108720","fpoints":"7990"},{"rank":"","bib":"32","name":"BYERS, Abbygail","r1":"54.08","r1AsInt":"54080","r1Rank":"","r2":"54.51","r2AsInt":"54510","r2Rank":"","total":"1:48.59","totalAsInt":108590,"fnumber":"108547","fpoints":"7807"},{"rank":"","bib":"31","name":"BERGERON-SAUCIER, Alyssa","r1":"56.53","r1AsInt":"56530","r1Rank":"","r2":"56.27","r2AsInt":"56270","r2Rank":"","total":"1:52.80","totalAsInt":112800,"fnumber":"108415","fpoints":"7686"},{"rank":"","bib":"30","name":"JONES, Ada","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"6537539","fpoints":"7567"},{"rank":"","bib":"29","name":"PETER, Clea","r1":"53.16","r1AsInt":"53160","r1Rank":"","r2":"53.67","r2AsInt":"53670","r2Rank":"","total":"1:46.83","totalAsInt":106830,"fnumber":"516797","fpoints":"7294"},{"rank":"","bib":"28","name":"BOURRET, Ashley","r1":"53.35","r1AsInt":"53350","r1Rank":"","r2":"54.25","r2AsInt":"54250","r2Rank":"","total":"1:47.60","totalAsInt":107600,"fnumber":"108321","fpoints":"7232"},{"rank":"","bib":"27","name":"ALAIN, Laurence","r1":"53.67","r1AsInt":"53670","r1Rank":"","r2":"54.97","r2AsInt":"54970","r2Rank":"","total":"1:48.64","totalAsInt":108640,"fnumber":"108192","fpoints":"7101"},{"rank":"","bib":"26","name":"HAMILTON, Gillian","r1":"53.96","r1AsInt":"53960","r1Rank":"","r2":"54.15","r2AsInt":"54150","r2Rank":"","total":"1:48.11","totalAsInt":108110,"fnumber":"108466","fpoints":"7035"},{"rank":"","bib":"25","name":"ST-PIERRE, Simone","r1":"52.55","r1AsInt":"52550","r1Rank":"","r2":"53.59","r2AsInt":"53590","r2Rank":"","total":"1:46.14","totalAsInt":106140,"fnumber":"108718","fpoints":"6975"},{"rank":"","bib":"24","name":"METCALFE, Jayden","r1":"55.27","r1AsInt":"55270","r1Rank":"","r2":"55.07","r2AsInt":"55070","r2Rank":"","total":"1:50.34","totalAsInt":110340,"fnumber":"108143","fpoints":"6816"},{"rank":"","bib":"23","name":"CARON, Anne-Frederique","r1":"DNS","r1AsInt":"2147483607","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108583","fpoints":"6809"},{"rank":"","bib":"22","name":"FAFARD, Gabrielle","r1":"55.77","r1AsInt":"55770","r1Rank":"","r2":"57.14","r2AsInt":"57140","r2Rank":"","total":"1:52.91","totalAsInt":112910,"fnumber":"108117","fpoints":"6707"},{"rank":"","bib":"21","name":"BARAER, Marion","r1":"54.70","r1AsInt":"54700","r1Rank":"","r2":"55.02","r2AsInt":"55020","r2Rank":"","total":"1:49.72","totalAsInt":109720,"fnumber":"108414","fpoints":"6687"},{"rank":"","bib":"20","name":"MARTIN, Estelle","r1":"52.23","r1AsInt":"52230","r1Rank":"","r2":"DNF","r2AsInt":"2147483617","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108679","fpoints":"6211"},{"rank":"","bib":"19","name":"BOURGEOIS, Amelie","r1":"52.64","r1AsInt":"52640","r1Rank":"","r2":"53.05","r2AsInt":"53050","r2Rank":"","total":"1:45.69","totalAsInt":105690,"fnumber":"108668","fpoints":"6165"},{"rank":"","bib":"18","name":"BEAUVAIS, Laura","r1":"DQ","r1AsInt":"2147483627","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108439","fpoints":"6107"},{"rank":"","bib":"17","name":"BRUNET, Marie-Pier","r1":"DQ","r1AsInt":"2147483627","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108437","fpoints":"5952"},{"rank":"","bib":"16","name":"CALORO, Benedetta","r1":"DQ","r1AsInt":"2147483627","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"6296108","fpoints":"5796"},{"rank":"","bib":"15","name":"BONNEVILLE, Jade","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108255","fpoints":"4510"},{"rank":"","bib":"14","name":"BROWN, Sarah","r1":"52.57","r1AsInt":"52570","r1Rank":"","r2":"DNF","r2AsInt":"2147483617","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108257","fpoints":"4352"},{"rank":"","bib":"13","name":"ROBINSON, Sophie-Anne","r1":"53.66","r1AsInt":"53660","r1Rank":"","r2":"53.34","r2AsInt":"53340","r2Rank":"","total":"1:47.00","totalAsInt":107000,"fnumber":"108140","fpoints":"4217"},{"rank":"","bib":"12","name":"HECKEY, Megan","r1":"54.70","r1AsInt":"54700","r1Rank":"","r2":"52.32","r2AsInt":"52320","r2Rank":"","total":"1:47.02","totalAsInt":107020,"fnumber":"108423","fpoints":"4972"},{"rank":"","bib":"11","name":"REHA, Mika Anne","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108113","fpoints":"3912"},{"rank":"","bib":"10","name":"CARLE, Eloise","r1":"1:12.57","r1AsInt":"72570","r1Rank":"","r2":"57.66","r2AsInt":"57660","r2Rank":"","total":"2:10.23","totalAsInt":130230,"fnumber":"107985","fpoints":"5190"},{"rank":"","bib":"9","name":"CARDINAL, Frederique","r1":"DNF","r1AsInt":"2147483602","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"107984","fpoints":"5073"},{"rank":"","bib":"8","name":"GAMBERT, Aurelie","r1":"DQg15","r1AsInt":"2147483627","r1Rank":"","r2":"DNS","r2AsInt":"2147483607","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"197545","fpoints":"5609"},{"rank":"","bib":"7","name":"THEBERGE, Anne-Catherine","r1":"53.49","r1AsInt":"53490","r1Rank":"","r2":"54.03","r2AsInt":"54030","r2Rank":"","total":"1:47.52","totalAsInt":107520,"fnumber":"108593","fpoints":"5346"},{"rank":"","bib":"6","name":"BEAUCHAMP, Caroline","r1":"52.82","r1AsInt":"52820","r1Rank":"","r2":"52.96","r2AsInt":"52960","r2Rank":"","total":"1:45.78","totalAsInt":105780,"fnumber":"107983","fpoints":"4019"},{"rank":"","bib":"5","name":"ROBINSON, Marie-Penelope","r1":"53.81","r1AsInt":"53810","r1Rank":"","r2":"54.01","r2AsInt":"54010","r2Rank":"","total":"1:47.82","totalAsInt":107820,"fnumber":"108442","fpoints":"5705"},{"rank":"","bib":"4","name":"LAMONTAGNE, Justine","r1":"51.78","r1AsInt":"51780","r1Rank":"","r2":"51.85","r2AsInt":"51850","r2Rank":"","total":"1:43.63","totalAsInt":103630,"fnumber":"108336","fpoints":"3686"},{"rank":"","bib":"3","name":"CARRIER, Olivia","r1":"52.02","r1AsInt":"52020","r1Rank":"","r2":"DNF","r2AsInt":"2147483617","r2Rank":"","total":"","totalAsInt":2147483500,"fnumber":"108116","fpoints":"5011"},{"rank":"","bib":"2","name":"NICOLICI, Andreea","r1":"52.24","r1AsInt":"52240","r1Rank":"","r2":"53.06","r2AsInt":"53060","r2Rank":"","total":"1:45.30","totalAsInt":105300,"fnumber":"108576","fpoints":"3972"},{"rank":"","bib":"1","name":"AMICO, Isabella","r1":"53.07","r1AsInt":"53070","r1Rank":"","r2":"53.66","r2AsInt":"53660","r2Rank":"","total":"1:46.73","totalAsInt":106730,"fnumber":"6536632","fpoints":"5789"}]
    

    racers_list = []
    times_list = []
    for comp in COMPS:
        racer = Racer(comp.get("name"), int(comp.get("fpoints")) / 100, comp.get("r1"), comp.get("r2"), comp.get("total"), comp.get("totalAsInt"))

        if (DISCIPLINE in ["Super G", "Super-G", "Downhill"]) and (racer.total not in ["DNF", "DNS", "DQ"]):
            racer.totalAsInt = int(comp.get("r1AsInt"))
            times_list.append(racer.totalAsInt)
        
        else:
            if (racer.totalAsInt < 2147483500):
                times_list.append(racer.totalAsInt)
             
        racers_list.append(racer)

    penalty_calculation = PenaltyCalculation(racers_list, DISCIPLINE, times_list)
    print(json.dumps(penalty_calculation.all_racers_scores()))

if __name__ == '__main__':
     main()