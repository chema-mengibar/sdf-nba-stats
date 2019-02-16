import sys
import os
os.chdir( os.path.dirname(__file__) )

from os.path import isfile, join

class Router(object):

    def __init__( self ):

        #@todo: replace if necesary the project name
        localPath = '\\'
        self.rootFolder = 'sdf-nba-stats'
        
        #@todo: change the routes to the absolute project directory path
        self.root = localPath + self.rootFolder +  '\\'

        self.universe =  self.root + 'data\\universe\\'
        self.stage =  self.root + 'data\\stage\\'
        self.master =  self.root + 'data\\master\\'


    def getRoute( self, block ):
        if block == 'universe':
            return self.universe
        elif  block == 'stage':
            return self.stage
        elif  block == 'master':
            return self.master
        else:
            raise Exception("Router: Not a valid block")