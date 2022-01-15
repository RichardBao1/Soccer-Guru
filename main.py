import requests
from bs4 import BeautifulSoup
import pickle
import threading

class SoccerGuru():
    def __init__(self):
        self.URL_BASE = "https://www.futwiz.com/en/fifa22/players?page="

        # {overall_stats: [[name, rating]]}
        self.allplayers = {}
        self.lock1 = threading.Lock()
        self.lock2 = threading.Lock()
        self.player_count = 0

    def create_pickle(self):
        player_dict = self.allplayers
        self.begin_thread()
        self.pickle_object(player_dict)

    def get_player_dict(self):
        return self.allplayers

    def unload_pickle(self):
        player_dict = self.unpickle_object()
        return player_dict

    def get_players(self, start, end):
        for i in range(start, end):
            print(i)
            URL = self.URL_BASE + str(i)
            page = requests.get(URL)

            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(class_ = "playersearchresults")
            players = results.find_all("tr", class_="table-row")

            for player_row in players:
                self.lock2.acquire()
                self.player_count += 1
                self.lock2.release()
                league = player_row.find("p", class_ = "team").find_all("a")[1].text
                position = list(player_row.children)[7].text.strip()
                country = player_row.find("img", class_ = "nation").attrs['src'].split(".")[0].split("/")[-1]
                name = player_row.find("b").text
                stats = player_row.find_all(class_="stat")
                rating = player_row.find(class_="otherversion22-txt").text
                overall_stats = 0
                for stat in stats:
                    overall_stats += int(stat.text)

                if overall_stats in self.allplayers:
                    self.lock1.acquire()
                    self.allplayers[overall_stats].append([name, rating, league, country, position])
                    self.lock1.release()
                else:
                    self.lock1.acquire()
                    self.allplayers[overall_stats] = [[name, rating, league, country, position]]
                    self.lock1.release()


    def pickle_object(self, player_dict):
        dbfile = open('playerpickle1', 'ab')
        pickle.dump(player_dict, dbfile)
        dbfile.close()

    def unpickle_object(self):
        dbfile = open('playerpickle1', 'rb')
        player_dict = pickle.load(dbfile)
        dbfile.close()
        return player_dict

    def begin_thread(self):
        for i in range(0,6):
            t = threading.Thread(target = self.get_players, args=(i*50, i*50+50))
            t.start()

        for thread in threading.enumerate()[1:]:
            thread.join()

    def filter(self, player_dict, rating_cap=100, league="", country=""):
        new_player_dict = dict()
        for key, value in player_dict.items():
            for i in value:
                if int(i[1]) <= rating_cap and (league == i[2] or league == "") and (country == i[3] or country== ""):
                    if i[1] in new_player_dict:
                        new_player_dict[key].append(i)
                    else:
                        new_player_dict[key] = [i]

        return new_player_dict

    """
      Chemistry
      +1 for same league, +1 for same club, +1 for same nation
    
      +5 for green link
      automatic decrease from green->yellow->red if different position
    
    
    """

def print_top():
    a = SoccerGuru()
    player_dict = a.unload_pickle()
    player_dict = a.filter(player_dict, 100, "FRA 1")
    overall_list = list(player_dict.keys())
    overall_list.sort()
    overall_list = reversed(overall_list)

    for i in range(30):
        overall = next(overall_list)
        print(player_dict[overall], overall)

def create():
    a = SoccerGuru()
    a.create_pickle()

print_top()