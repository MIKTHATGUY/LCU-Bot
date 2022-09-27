import json
from multiprocessing.resource_sharer import stop
import os.path
from re import search
from subprocess import check_output
from time import sleep
import time
import requests
from Definitions import Roles, Modes
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def GetAuthCreds():
  """
  Returns the login credentials and port
  """
  raw = check_output("wmic PROCESS WHERE name='LeagueClientUx.exe' GET commandline".split(" ")).decode("ASCII")
  lockfile = str(os.path.dirname(raw.split('"')[1])) + "/lockfile"
  with open(lockfile, "r") as f:
    f = f.read()
    port = f.split(":")[2]
    password = f.split(":")[3]
    return (port, "riot", password)

port, user, password = "", "", ""

try:
  port, user, password = GetAuthCreds()
except Exception:
  pass

def CreateParty(queueId: Modes):
  headers = {
      'accept': 'application/json',
      'Authorization': 'riot lWW9TykAGZxtRxScynziBw',
      # Already added when you pass json= but not when you pass data=
      # 'Content-Type': 'application/json',
  }

  json_data = {
      'queueId': queueId,
  }

  response = requests.post(f'https://127.0.0.1:{port}/lol-lobby/v2/lobby', auth=(user, password) ,headers=headers, json=json_data, verify=False)
  print(response.status_code)
  return response

def QuitParty():
  headers = {
    'accept': 'application/json',
    'Authorization': 'Basic cmlvdDpsV1c5VHlrQUdaeHRSeFNjeW56aUJ3',
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  response = requests.delete(f'https://127.0.0.1:{port}/lol-lobby/v2/lobby', auth=(user, password) ,headers=headers, verify=False)
  print(response.status_code)
  return response

def update_vars():
  try:
    global port,user,password
    print(port,user,password)
    port, user, password = GetAuthCreds()
    print(port,user,password)
  except:
    time.sleep(1)
    update_vars()

def SelectRoles(FirstPreference, SecondPreference):
  headers = {
      'accept': 'application/json',
      'Authorization': 'Basic cmlvdDpsV1c5VHlrQUdaeHRSeFNjeW56aUJ3',
      # Already added when you pass json= but not when you pass data=
      # 'Content-Type': 'application/json',
  }

  json_data = {
      'firstPreference': FirstPreference,
      'secondPreference': SecondPreference,
  }

  # Note: json_data will not be serialized by requests
  # exactly as it was in the original request.
  #data = '{\n  "firstPreference": "MIDDLE",\n  "secondPreference": "TOP"\n}'
  #response = requests.put(f'https://127.0.0.1:{port}/lol-lobby/v2/lobby/members/localMember/position-preferences', headers=headers, data=data, verify=False)
  response = requests.put(f'https://127.0.0.1:{port}/lol-lobby/v2/lobby/members/localMember/position-preferences', auth=(user, password) ,headers=headers, json=json_data, verify=False)
  print(response.status_code)
  return response

def StartMatchMaking():
  headers = {
    'accept': 'application/json',
    'Authorization': 'Basic cmlvdDpsV1c5VHlrQUdaeHRSeFNjeW56aUJ3',
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  response = requests.post(f'https://127.0.0.1:{port}/lol-lobby/v2/lobby/matchmaking/search', auth=(user, password) ,headers=headers, verify=False)
  print(response.status_code)
  return response

def StopMatchMaking():
  headers = {
    'accept': 'application/json',
    'Authorization': 'Basic cmlvdDpsV1c5VHlrQUdaeHRSeFNjeW56aUJ3',
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  response = requests.delete(f'https://127.0.0.1:{port}/lol-lobby/v2/lobby/matchmaking/search', auth=(user, password) ,headers=headers, verify=False)
  print(response.status_code)
  return response

def InfoMatchMaking():
  headers = {
      'accept': 'application/json',
      'Authorization': 'Basic cmlvdDpsV1c5VHlrQUdaeHRSeFNjeW56aUJ3',
  }

  response = requests.get(f'https://127.0.0.1:{port}/lol-matchmaking/v1/search', auth=(user, password) ,headers=headers, verify=False)
  print(response.status_code)
  json2 = json.loads(response.content.decode("UTF-8"))
  if not response.ok:
    return response.status_code
  time_elapsed = json2["timeInQueue"]
  time_estimated = json2["estimatedQueueTime"]
  queueId = json2["queueId"]
  search_state = json2["searchState"]
  return [json2, response]

