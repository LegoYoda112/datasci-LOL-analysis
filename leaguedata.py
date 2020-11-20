from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

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