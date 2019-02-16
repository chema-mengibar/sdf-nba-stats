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


#STEP: leagueLeaders

seasonsList = ['2016-17','2017-18','2018-19']

#com: change the season idx manually
SEASON = seasonsList[ 2 ]

endPoint = {
 'name': 'leagueLeaders',
 'params' :  [ 
    ('LeagueID', '00'),
    ('PerMode', 'Totals'),
    ('Scope', 'S'),
    ('Season', SEASON),
    ('SeasonType', 'Regular Season'),
    ('StatCategory', 'PTS')
  ]
}
result = requests.get( nba.apiUrl + endPoint['name'], params=endPoint['params'], headers= nba.headers)
resultObj =  result.json()

dataHeader = resultObj['resultSet']['headers']
dataRows = resultObj['resultSet']['rowSet'][0:10]
outputObj = {
  'header': dataHeader,
  'rows': dataRows,
  'request': result.request.url,
  'endpoint': endPoint,
}

customSuffix = 'top10-shooters__season-' + endPoint['params'][3][1]
outputFilePath = outputPath + config['target']['file'].replace("$CUSTOM$", customSuffix )


#STEP: save 

with open( outputFilePath , 'w') as outfile:
  json.dump( outputObj , outfile , indent=2, ensure_ascii=False)


#STEP: update config file

yaml.dump( config, file( DIR_TASK + '\\' + CONFIG_FILE_NAME + '.yml', 'w'), indent=2, default_flow_style=False )
