import json
import os
import subprocess
from pysondb import db
from lib.api.endpoints import getContractABI
from lib.api.etherscan import handleEtherScanAPIResponseForGetContractABI,prepareEtherScanAPIParametersForGetContractABI
from lib.api.bscscan import handleBscScanAPIResponseForGetContractABI, prepareBscScanAPIParametersForGetContractABI
from lib.util import bcolors, findFiles, findFilesRecusive
from lib.setting import setting
from lib.exploit import exploit

def searchTokens(network, tokenName):
    # Format json file to satisfy the requirement of pysondb 
    path = setting.getPathToPOCTemplate()+'tokens/'+network+'/tokens-'+network+'.json'
    
    if not os.path.exists(path):
        print("Unsupported network")
        return
    
    with open (path, 'r') as f:
        jsonFile = json.load(f)
    jsonFileWithData = {'data': jsonFile}
    tmpPath = '/tmp'+'/tokens-'+network+'.json'
    with open(tmpPath, 'w') as f:
        json.dump(jsonFileWithData, f)
    
    # Load json file
    tokenDB=db.getDb(tmpPath)
    
    # Search token with keyword
    results = tokenDB.reSearch("symbol", r'(?i)(\w|^)'+tokenName+r'(\w|$)')
    print('Results:')
    print('-----------------')
    for result in results:
        print('Symbol: '+ bcolors.OKGREEN + result['symbol'] + bcolors.ENDC)
        print('Name: '+ bcolors.OKGREEN + result['name'] + bcolors.ENDC)
        print('Address: '+ bcolors.OKGREEN + result['address'] + bcolors.ENDC)
        print('Website: '+ bcolors.OKGREEN +result['website'] + bcolors.ENDC)
        print('Network: '+ bcolors.OKGREEN +network + bcolors.ENDC)
        print('-----------------')
    
    # Delete temp file
    os.remove(tmpPath)
    return

def searchInterfacesWithProjectAndKeyword(project, interface):
    print(bcolors.HEADER + "Please check the detail of interfaces under the folder " + setting.getPathToPOCTemplate()+"interfaces/" + bcolors.ENDC)
    
    directories = findFiles(project,setting.getPathToPOCTemplate()+"interfaces")
    
    for directory in directories:
        files = findFilesRecusive(interface, setting.getPathToPOCTemplate()+"interfaces/"+directory)
        for file in files:
            print ("Add [" + bcolors.OKGREEN + file.replace(setting.getPathToPOCTemplate()+"interfaces/","",1) + bcolors.ENDC + "] to config.yml")
            print ("    Usage: " + bcolors.OKGREEN + "import \"./"+file.replace(setting.getPathToPOCTemplate()+"interfaces/","",1)+"\";" + bcolors.ENDC)
    return

def searchInterfacesWithKeyword(interface):
    print(bcolors.HEADER + "Please check the detail of interfaces under the folder " + setting.getPathToPOCTemplate()+"interfaces/" + bcolors.ENDC)
    files = findFilesRecusive(interface, setting.getPathToPOCTemplate()+"interfaces/")
    for file in files:
        print ("Add [" + bcolors.OKGREEN + file.replace(setting.getPathToPOCTemplate()+"interfaces/","",1) + bcolors.ENDC + "] to config.yml")
        print ("    Usage: " + bcolors.OKGREEN + "import \"./"+file.replace(setting.getPathToPOCTemplate()+"interfaces/","",1)+"\";" + bcolors.ENDC)
    return

def searchInterfacesWithAddress(network, address, name=None):

    # Get contract ABI via Scan API
    contractABIJson = getContractABI(network, address)
    if contractABIJson is None:

        return
    
    # Convert ABI to interfaces
    name = "Interface_"+address if name == None else name
    echoResult = subprocess.run(["echo", contractABIJson], check=True, capture_output=True)
    convertedInterface = subprocess.run(["npx", "abi-to-sol", name], input=echoResult.stdout, capture_output=True)
    
    # Save the interfaces to current POC folder or directly show in terminal
    if (exploit.name == None):
        print("--------------------------------------------------------------")
        print(bcolors.WARNING + "EXPLOIT NOT LOADED, ONLY SHOW CONVERTED INTERFACE IN TERMINAL" + bcolors.ENDC)
        print("--------------------------------------------------------------")
        print(convertedInterface.stdout.decode())
    else:
        path = os.path.join(setting.getPathToExploits(), exploit.name)
        print(path)
        with open(os.path.join(path,name+".sol"), 'w') as f:
            f.write(convertedInterface.stdout.decode())
            print("--------------------------------------------------------------")
            print(bcolors.OKGREEN + "CONVERTED INTERFACE SAVED IN THE FOLDER OF LOADED EXPLOIT" + bcolors.ENDC)
            print("--------------------------------------------------------------")
        # Show the path for importing converted interfaces
        print ('Usage: ' + bcolors.OKGREEN + "import \"./"+name+".sol"+"\";" + bcolors.ENDC)
    
    return
