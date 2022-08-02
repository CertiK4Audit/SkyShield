import subprocess
import requests
import json
import yaml

YAML_FILE_PATH="config.yml"

def init():
    subprocess.run(['npm', 'install'])

def useNetwork(arg):
    try:
        if(len(arg.split(' '))==1):
            setNetwork(arg)
        elif(len(arg.split(' '))==2):
            setNetwork(arg.split(' ')[0])
            setBlockNumber(arg.split(' ')[1])
        else:
            raise Exception("Incorrect Parameters Passing")
    except:
        print("No Exploit loaded")

def query(arg):
    try:
        #TODO: add verifications for address and input patter so that user know what is wrong.
        contractAddr = arg.split('.')[0]
        functionCall = arg.split('.')[1]
        
        #Add support for parameters
        #param = arg.split(' ')[1]
        #print(param)
        
        #get abi from address
        abiPath = getAbi(contractAddr)
        
        with open(YAML_FILE_PATH, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            config['contractAddress'] = contractAddr
            config['function'] = functionCall
            #config['param'] = param
            config['abi'] = abiPath
        with open(YAML_FILE_PATH, 'w') as f:
            yaml.dump(config,f)
        runQuery()
        
    except Exception as e:
        print(e)
        print("Query Failed")



def setNetwork(network):
    try:
        with open(YAML_FILE_PATH, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            config['url'] = config['networks'][network]['url']
            config['apiURL'] = config['scanAPI'][network]['url']
            config['apiKey'] = config['scanAPI'][network]['key']
        with open(YAML_FILE_PATH, 'w') as f:
            yaml.dump(config,f)
    except:
        print("Setting network failed")

def setBlockNumber(blockNumber):
    try:
        with open(YAML_FILE_PATH, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            #print(config['url'])
            config['blockNumber'] = blockNumber
        with open(YAML_FILE_PATH, 'w') as f:
            yaml.dump(config,f)
    except Exception as e:
        print(e)
        print("Setting block number failed")

def runQuery():
    subprocess.run(['npx', 'hardhat', 'run', 'scripts/query.ts'])

def getAbi(addr):
    try:
        print("Getting abi from ethereum....")
        with open(YAML_FILE_PATH, 'r') as f:
                config = yaml.load(f, Loader=yaml.FullLoader) 
                url = config['apiURL']
                key = config['apiKey']
        params = {
            "module": "contract",
            "action": "getabi",
            "address": addr,
            "apikey": key
        }
        url = url + "/api"
        response = requests.get(url = url, params = params)
        contractABIJson = response.json()['result']
        with open("./abis/"+addr+".json", 'w') as f:
            f.write(contractABIJson)
        return "./abis/"+addr+".json"
    except Exception as e:
        print(e)
        print("Get abi failed!")
    

