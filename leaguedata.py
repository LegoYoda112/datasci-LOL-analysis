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
    
    def length(self):
        return int(self.info()['gamelength'].values)
    
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
    
    
    def prev_kills(self,minute,team_type = "all"):
        '''Returns a dictionary object with all kills before a specified minute, containing the time of kill, and its index.
        Also takes a team type argument for specifying, blue, red, or all.'''
        
        prev_kills = pd.DataFrame({'Time' : [],'Index':[],'Blue':[],'XY':[]})
        
        if team_type == "red":
            kill_list = self.red_kills()
        elif team_type == "blue":
            kill_list = self.blue_kills()
        else:
            kill_list = self.kills()
        
        for index,kill in enumerate(kill_list.values):
            a = (minute - kill[2])
            if a > 0:
                this_kill = pd.DataFrame({'Time' : [kill[2]],
                                          'Index':[index],
                                          'Blue':[kill[1] == "bKills"],
                                          'XY':[self.get_xy(index)]})
                
                prev_kills = pd.concat([prev_kills,this_kill], ignore_index=True)
                
        return prev_kills.sort_values('Time').reset_index(drop=True)
    
    def kill_freq(self,minute,time_range = 5,team_type = "all"):
        '''Gets the kill frequency from a given minute, over a given range (default = 5 mins),
        for either blue, red, or all teams. (default = all)'''
        prev_kills = self.prev_kills(minute,team_type)
        return len(prev_kills.loc[prev_kills['Time'] > (minute-time_range)].index)/time_range

    
#-----------------------------------REDUNDANT FUNCTION-----------------------------------#    
    def last_kill(self,minute,team_type = "all"):
        '''Returns the time since last kill, the kill object, and its index.'''
        
        prev_kills = self.prev_kills(minute,team_type)
        
        if team_type == "red":
            kill_list = self.red_kills()
        elif team_type == "blue":
            kill_list = self.blue_kills()
        else:
            kill_list = self.kills()
        
        if prev_kills != {}:
            last_kill_time = max(prev_kills)
            delta_time = minute - last_kill_time
            index = prev_kills[last_kill_time]
            return delta_time,kill_list.values[index],index
        else:
            return None
#----------------------------------------------------------------------------------------#   



    def get_xy(self,index):
        '''Returns the X,Y coordinates of a requested kill'''
        
        kill = self.kills().values[index]
        return kill[9],kill[10]

    def nexus_distance(self,xy):
        '''returns the distance of a set of x,y coordinates from the blue team's nexus.'''
        
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
    
    def prev_structures(self,minute,team_type = "all"):
        '''Returns a dictionary object with all structures taken before a specified minute, containing the time of event, and its index.
        Also takes a team type argument for specifying, blue, red, or all.'''

        prev_structures = pd.DataFrame({'Time' : [],'Index':[],'Blue':[]})
        
        if team_type == "red":
            self_structures = self.red_structures()
        elif team_type == "blue":
            self_structures = self.blue_structures()
        else:
            self_structures = self.structures()
        
        for index,structure in enumerate(self_structures.values):
            a = (minute - structure[2])
            if a > 0:
                this_structure = pd.DataFrame({'Time' : [structure[2]],
                                               'Index':[index],
                                               'Blue':[(structure[1] == 'bTowers')|(structure[1] == 'bInhibs')]})
                
                prev_structures = pd.concat([prev_structures,this_structure],ignore_index=True)
                
        return prev_structures.sort_values('Time').reset_index(drop=True)
    
    def structure_freq(self,minute,time_range = 5,team_type = "all"):
        '''Gets the kill frequency from a given minute, over a given range (default = 5 mins),
        for either blue, red, or all teams. (default = all)'''
        prev_structures = self.prev_structures(minute,team_type)
        return len(prev_structures.loc[prev_structures['Time'] > (minute-time_range)].index)/time_range

    
#-----------------------------------REDUNDANT FUNCTION-----------------------------------#
    def last_structure(self,minute,team_type = "all"):
        '''Returns the time since last structure taken, the structure object, and its index.'''
        prev_structures = self.prev_structures(minute,team_type)
        
        if team_type == "red":
            structure_list = self.red_structures()
        elif team_type == "blue":
            structure_list = self.blue_structures()
        else:
            structure_list = self.structures()
            
        if prev_structures != {}:
            last_structure_time = max(prev_structures)
            delta_time = minute - last_structure_time
            index = prev_structures[last_structure_time]
            return delta_time,structure_list.values[index],index
        else:
            return None
#----------------------------------------------------------------------------------------#       



    # ===== GAME STATE TEST =====
    def game_state(self,minute):
        '''Returns a test gamestate tuple for a given minute.'''
        nd = None
        minute = minute
        prev_kills = self.prev_kills
        prev_structures = self.prev_structures
#         last_kill = self.last_kill(minute)
#         if last_kill != nd:
#             last_kill_distance = [self.nexus_distance(self.get_xy(last_kill[2]))]
#             last_kill_blue = [last_kill[1][1] == "bKills"]
#             last_kill_time = [last_kill[0]]
#         else:
#             last_kill_blue = [nd]
#             last_kill_distance = [nd]
#             last_kill_time = [nd]
            
#         last_structure = self.last_structure(minute)
#         if last_structure != nd:
#             last_structure_blue = [last_structure[1][1] == "bTowers"]
#             last_structure_time = [last_structure[0]]
#             prev_red_structures = [len(self.prev_structures(minute,"red").index)]
#             prev_blue_structures = [len(self.prev_structures(minute,"blue").index)]
#         else:
#             last_structure_blue = [nd]
#             last_structure_time = [nd]
#             prev_red_structures = [nd]
#             prev_blue_structures = [nd]
        bluegold = self.gold_type("goldblue")[minute-1]
        golddiff = self.gold_type("golddiff")[minute-1]
        oldgolddiff = self.gold_type("golddiff")[minute-4] if minute>3 else 0
        data = {"Address":self.info()['Address'].values,
                "minute":[minute],
                "Blue kills":[len(prev_kills(minute,"blue").index)],
                "Blue Deaths":[len(prev_kills(minute,"red").index)],
                "Kill freq":[self.kill_freq(minute)],
                "Blue kill freq":[self.kill_freq(minute,team_type = "blue")],
                "Blue death freq":[self.kill_freq(minute,team_type = "red")],
                "Red structures taken":[len(prev_structures(minute,"blue").index)],
                "Blue structures lost":[len(prev_structures(minute,"red").index)],
                "Structure freq":[self.structure_freq(minute)],
                "Blue structure freq":[self.structure_freq(minute,team_type = "blue")],
                "Red structure freq":[self.structure_freq(minute,team_type = "red")],
                "Bluegold":[bluegold],
                "Gold diff":[golddiff],
                "Delta Gold diff":[golddiff - oldgolddiff],
                "Blue Win": [self.bResult()]
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