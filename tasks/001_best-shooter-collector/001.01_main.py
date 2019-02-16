# -*- coding: utf-8 -*-
import os
import sys

TASK_NAME = os.path.basename(__file__)
DIR_TASK  = os.path.basename(os.getcwd())
DIR_LIB   = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
DIR_TASK  = os.path.dirname(os.path.abspath(__file__))

import json, csv, time, string, itertools, copy, yaml
import numpy as np
import pandas as pd
import datetime as dt

import requests

#com: get same prefix-file-name config file -> 100.00_config
CONFIG_FILE_NAME = TASK_NAME.split('_')[0] + '_config'
config = yaml.load( stream = file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'r'))

sys.path.append( DIR_LIB )

from lib.router import Router
router = Router( )

from lib.nba import Nba
nba = Nba( )

# --------------------------------------------------------------------------
today = dt.datetime.now().strftime("%Y-%m-%d--%H-%M") 


#STEP: output-dir

outputPath =  router.getRoute( config['target']['route'] ) + config['target']['dir'] 
#com: create output folder
if not os.path.exists( outputPath ):
  os.makedirs( outputPath )


#DEF:
def getSourceFile( _sourceKey, _fileIdx ):
  sourceName = config['source'][ _sourceKey ]
  sourcePathFile = router.getRoute( sourceName['route'] ) + sourceName['dir'] + sourceName['files'][ _fileIdx ]
  return open( sourcePathFile , 'r')

#com: keys and values in data are separated. 
HEADER_IDX__PLAYER_ID = 0
CONTEXT_MEASURE = 'FG3A' #FG3A, FGM, etc...

#STEP: load file json

#com: change the season idx manually: 0,1,2
seasonIdx = 2 

rawContent = getSourceFile( 'top10-shooters', seasonIdx )  
fileJsonContent = json.load( rawContent )

#com: loop for all 10 players in a season-file
for rowIdx, rowItem in enumerate(  fileJsonContent['rows'] ):

  playerIdx = rowIdx
  playerRow = fileJsonContent['rows'][playerIdx]

  LeagueID = fileJsonContent['endpoint']['params'][0][1]
  PerMode = fileJsonContent['endpoint']['params'][1][1]
  Scope = fileJsonContent['endpoint']['params'][2][1]
  Season = fileJsonContent['endpoint']['params'][3][1]
  SeasonType = fileJsonContent['endpoint']['params'][4][1]
  StatCategory = fileJsonContent['endpoint']['params'][5][1]


  #STEP: season data by player

  endPoint = {
  'name': 'shotchartdetail',
  'params' :  [ 
    ('AheadBehind',''),('CFID',''),('CFPARAMS',''),('ClutchTime',''),('Conference',''),('ContextFilter',''),
    ('DateFrom',''),('DateTo',''),('Division',''),('GROUP_ID',''),
    ('GameEventID',''),('GameID',''),('GameSegment',''),('GroupID',''),('GroupMode',''),
    ('Location',''),('Month','0'),('OnOff',''),('OpponentTeamID','0'),('Outcome',''),
    ('PORound','0'),('Period','0'),
    ('PlayerID1',''),('PlayerID2',''),('PlayerID3',''),('PlayerID4',''),('PlayerID5',''),('PlayerPosition',''),('PointDiff',''),
    ('Position',''), ('RangeType','0'),('RookieYear',''),('SeasonSegment',''),('ShotClockRange',''),('StartPeriod','1'),
    ('StartRange','0'),('StarterBench',''),('TeamID','0'),
    ('VsConference',''),('VsDivision',''),('VsPlayerID1',''),('VsPlayerID2',''),('VsPlayerID3',''),
    ('VsPlayerID4',''),('VsPlayerID5',''),('VsTeamID',''),
    ('EndPeriod','10'), ('EndRange','28800'), ('GroupQuantity','5'), ('LastNGames','0'),

    ('LeagueID', LeagueID),
    ('PlayerID', playerRow[ HEADER_IDX__PLAYER_ID ] ),
    ('Season', Season),
    ('SeasonType', SeasonType),
    ('ContextMeasure', CONTEXT_MEASURE ), 
    ]
  }

  result = requests.get( nba.apiUrl + endPoint['name'] , params=endPoint['params'], headers= nba.headers)
  resultObj =  result.json()

  customSuffix = 'details__' + 'season-' + Season + '__player-' + str(playerRow[ HEADER_IDX__PLAYER_ID ]) 
  outputFilePath = outputPath + config['target']['file'].replace("$CUSTOM$", customSuffix )


  #STEP: save 

  with open( outputFilePath , 'w') as outfile:
    json.dump( resultObj , outfile , indent=2, ensure_ascii=False)





# #STEP: update config file

# yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
