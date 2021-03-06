import sys
import time
#import itertools
import os

class dots_and_boxes_game():
    '''Class to define the state of the game. This class remembers the players,
    the line segments, the scores. It also has to logic of the game to figure 
    out which line the user is playing, determine if a box is completed, 
    determine the scores, and whose turn it is.'''

    def __init__(self, grid_range, player1="A", player2="B"):
        '''Initial state of the game'''
        self.grid_range = list(grid_range)
        self.total_num_segments = len(self.grid_range)*(len(self.grid_range)-1)*2
        self.list_of_players = [player1, player2]
        self.score = {p:0 for p in self.list_of_players}
        #self.player_iter = itertools.cycle(list_of_players)
        self.player = self.list_of_players[0]
        print (self.list_of_players)
        self.list_of_lines = []
        self.mark_square = []
        self.square_player = ""

    def next_player (self):
        '''Return the next player'''
        # Cannot use itertools.cycle for getting next player
        # cycle object is not JSON serializable which is 
        # need to store flask session
        if self.player is self.list_of_players[0]:
            return self.list_of_players[1]
        if self.player is self.list_of_players[1]:
            return self.list_of_players[0]
    
    def get_scores(self):
        return self.score

    def get_current_player(self):
        '''returns the player whose turn it is'''
        return self.player
    
    def get_mark_square(self):
        '''Which squares are completed in this turn, if any'''
        return self.mark_square
    
    def get_square_player(self):
        '''Return the player name to which the self.mark_square
        belongs to'''
        return self.square_player
 
    def locate(self, pos, pair,ingrid = True):
        ''' Is the pair of points within the grid? If yes,
        Is the point pos roughly between the pair of points
        (within 10 pixels on either side)'''
        if  self.grid_range[0] <= pair[0][0] <= self.grid_range[-1] and \
            self.grid_range[0] <= pair[0][1] <= self.grid_range[-1] and \
            self.grid_range[0] <= pair[1][0] <= self.grid_range[-1] and \
            self.grid_range[0] <= pair[1][1] <= self.grid_range[-1]:
            pass
        elif not ingrid:
            pass
        else:
            return False
        if pair[0][0]-10 < pos[0] < pair[1][0]+10 and \
            pair[0][1]-10 < pos[1] < pair[1][1]+10:
            return True
        else:
            return False

    def click(self, pos):
        '''Do something with a click. If the click is where
        a valid line can be placed, return the x,y coordinates
        of both end points. Otherwise, return None'''
        self.mark_square = []
        self.square_player = ''
        pointlist = self.get_end_points(pos)
        #print("Got the points as :", pointlist)
        if pointlist:
            self.check_square(pointlist)
            self.list_of_lines.append(pointlist)
            return pointlist
        return None
    
    def find_winner(self):
        '''Figure out the winner and declare'''
        if len(self.list_of_lines) < self.total_num_segments:
            return None
        winner = "Both"
        player = list(self.score.keys())
        if self.score[player[0]] > self.score[player[1]]:
            winner = player[0]
        elif self.score[player[1]] > self.score[player[0]]:
            winner = player[1]
        return winner

    def get_end_points(self, pos):
        '''Figure out the nearest 2 points for the line'''
        size = self.grid_range[1] - self.grid_range[0]
        snap_x, snap_y = pos[0]//size*size, pos[1]//size*size
        points = [(snap_x, snap_y), (snap_x, snap_y+size), \
            (snap_x+size, snap_y), (snap_x+size, snap_y+size)]
        for pair in [(points[0],points[1]), (points[0], points[2]), \
            (points[1],points[3]),(points[2], points[3])]:
            #print ("checking if ", pos , " is in ", pair)
            if self.locate(pos, pair,self.grid_range):
                # Figured which pair of points make the line
                if pair in self.list_of_lines:
                    return None
                return pair
        return None


    def check_square(self, line, clear=False):
        '''Check if the new "line" completes a square, figure out what the squares 
        are (max 2) and which player the squares belong to'''
        x1, y1, x2, y2 = line[0][0],line[0][1],line[1][0], line[1][1] 
        v = y1-y2
        h = x1-x2
        if v:
            # verical line
            neighbors1= [(x1,y1),(x1-v,y1),(x2-v,y2),(x2,y2)]
            neighbors2 = [(x1,y1),(x1+v,y1),(x2+v,y2),(x2,y2)]
        else:
            #horizontal line
            neighbors1 = [(x1,y1),(x1,y1-h),(x2,y1-h),(x2,y2)]
            neighbors2 = [(x1,y1),(x1,y1+h),(x2,y1+h),(x2,y2)]
        # We know (x1,y1)(x2,y2) already has a line, so not checking
        # for it
        score = 0
        for n in [neighbors1,neighbors2]:
            for i in range(0,3):
                if (n[i],n[i+1]) in self.list_of_lines:
                    pass
                elif (n[i+1],n[i]) in self.list_of_lines:
                    pass
                else:
                    # one of the segments does not have a line, 
                    # so not a square
                    break
            else:
                score += 1
                '''Position for Label the square with the player who won it.
                5 adjustment to just make it a bit centered'''
                x = sum([i[0] for i in n])/4-5
                y = sum([i[1] for i in n])/4+5
                self.square_player = self.player
                try:
                    self.mark_square.append((x,y))
                except:
                    self.mark_square= [(x,y)]
        print("Got score", score, "for player", self.player)
        if score:
            self.score[self.player] += score
        else:
            self.player = self.next_player()
        return

