from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

import math

# Import all match data
bans = pd.read_csv("data/bans.csv")
gold = pd.read_csv("data/gold.csv")
kills = pd.read_csv("data/kills.csv")
LOL = pd.read_csv("data/LeagueofLegends.csv")
matchinfo = pd.read_csv("data/matchinfo.csv")
monsters = pd.read_csv("data/matchinfo.csv")
structures = pd.read_csv("data/structures.csv")

# Some preprocessing
kills = kills.replace('TooEarly', 'NaN')

# Match class
class match:
    def __init__(self, address):
        self.address = address
    
    def info(self):
        return matchinfo.loc[matchinfo['Address'] == self.address]
    
    def bResult(self):
        return (self.info()['bResult'] == 1).bool()
    
    # ===== BANS =====
    def bans(self):
        return bans.loc[bans['Address'] == self.address]
    
    # ===== GOLD =====
    def gold(self):
        return gold.loc[gold['Address'] == self.address]
    
    def gold_type(self, gold_type):
        gold_df = gold.loc[(gold['Address'] == self.address) & (gold['Type'] == gold_type)]
        return gold_df.values[0, 2:]
    
    def gold_types(self):
        return list(self.gold()['Type'])
    
    # ===== KILLS =====
    def kills(self):
        return kills.loc[kills['Address'] == self.address]
    
    def blue_kills(self):
        self_kills = self.kills()
        return self_kills.loc[self_kills['Team'] == 'bKills']
    
    def red_kills(self):
        self_kills = self.kills()
        return self_kills.loc[self_kills['Team'] == 'rKills']
    
    def last_kill(self,minute):
        #Returns the time since last kill, the kill object, and its index.
        prev_kills = {}
        self_kills = self.kills()
        for index,kill in enumerate(self_kills.values):
            a = (minute - kill[2])
            if a > 0:
                prev_kills[str(a)] = index
        return min(prev_kills),self_kills.values[prev_kills[min(prev_kills)]],prev_kills[min(prev_kills)]
    
    def get_xy(self,index):
        #Returns the X,Y coordinates of a requested kill
        kill = self.kills().values[index]
        return kill[9],kill[10]

    def nexus_distance(self,xy):
        #returns the distance of a set of x,y coordinates from the blue team's nexus.
#         return math.dist(xy,(0,0))
         return math.sqrt(int(xy[0])**2+int(xy[1])**2)
    
    # ===== MONSTERS =====
    def monsters(self):
        return monsters.loc[monsters['Address'] == self.address]
    
    # ===== STRUCTURES =====
    def structures(self):
        return structures.loc[structures['Address'] == self.address]
    
    def blue_structures(self):
        self_structures = self.structures()
        return self_structures.loc[(self_structures['Team'] == 'bTowers') | (self_structures['Team'] == 'bInhibs')]
    
    def red_structures(self):
        self_structures = self.structures()
        return self_structures.loc[(self_structures['Team'] == 'rTowers') | (self_structures['Team'] == 'rInhibs')]
    
    def last_structure(self,minute):
        #Returns the time since last structure taken, the structure object, and its index.
        prev_structures = {}
        self_structures = self.structures()
        for index,structure in enumerate(self_structures.values):
            a = (minute - structure[2])
            if a > 0:
                prev_structures[str(a)] = index
        return min(prev_structures),self_structures.values[prev_structures[min(prev_structures)]],prev_structures[min(prev_structures)]
    
    # ===== GAME STATE TEST =====
    def game_state(self,minute):
        #Returns a test gamestate tuple for a given minute.
        minute = minute
        last_kill = self.last_kill(minute)
        last_structure = self.last_structure(minute)
        data = {"minute":minute,
                "Time since last kill":[last_kill[0]], 
                "Last kill blue":[last_kill[1][1] == "bKills"],
                "last kill distance":[self.nexus_distance(self.get_xy(last_kill[2]))],
                "Time since last structure":[last_structure[0]],
                "Last structure blue":[last_structure[1][1] == "bTowers"],
                "Gold diff":[self.gold_type("golddiff")[minute-1]]
               }
        return pd.DataFrame.from_dict(data)
    
# ==== HELPERS =====

def match_num_address(num):
    return matchinfo['Address'][num]

def num_matches():
    return len(matchinfo)

def get_all_matches():
    matches = []
    
    for i in range(0, num_matches()):
        matches.append(match(match_num_address(i)))
    
    return matches

def plot_map(ax):
    map_img = plt.imread("data/map.png")
    ax.imshow(map_img, extent=[0,14900,0,14900])