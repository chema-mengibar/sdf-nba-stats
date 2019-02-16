import sys
import os
os.chdir( os.path.dirname(__file__) )

from os.path import isfile, join

class Nba(object):

  def __init__( self ):
    self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    self.apiUrl = 'https://stats.nba.com/stats/'

    self.apiEvents = 'https://stats.nba.com/events/'
    self.apiStats = 'https://stats.nba.com/stats/'


  def urlDebug( self, endPointUrlConstruct, endPointParams ):
    paramsStr = "&".join( [  str(p[0]) + '=' + str(p[1]) for p in endPointParams ] )
    return  endPointUrlConstruct + '?' + paramsStr
