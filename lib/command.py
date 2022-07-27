import subprocess
import yaml

YAML_FILE_PATH="config.yml"

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
        
        #get abi from address
        abiPath = getAbi(contractAddr)
        
        with open(YAML_FILE_PATH, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            config['contractAddress'] = contractAddr
            config['function'] = functionCall
            config['abi'] = abiPath
        with open(YAML_FILE_PATH, 'w') as f:
            yaml.dump(config,f)
        runQuery()
        
    except Exception as e:
        print(e)
        print("Query ")



def setNetwork(network):
    try:
        with open(YAML_FILE_PATH, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            print(config['url'])
            config['url'] = config['networks'][network]['url']
        with open(YAML_FILE_PATH, 'w') as f:
            yaml.dump(config,f)
    except:
        print("Setting network failed")

def setBlockNumber(blockNumber):
    try:
        with open(YAML_FILE_PATH, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            print(config['url'])
            config['blockNumber'] = blockNumber
        with open(YAML_FILE_PATH, 'w') as f:
            yaml.dump(config,f)
    except Exception as e:
        print(e)
        print("Setting block number failed")

def runQuery():
    subprocess.run(['npx', 'hardhat', 'run', 'scripts/query.ts'])

def getAbi(addr):
    return './abis/wbnb.json'

