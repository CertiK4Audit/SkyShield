import json
import os
import requests
import subprocess
from pysondb import db
from lib.api import handleBscScanAPIResponseForGetContractABI, handleEtherScanAPIResponseForGetContractABI, prepareBscScanAPIParametersForGetContractABI, prepareEtherScanAPIParametersForGetContractABI
from lib.util import findFiles, findFilesRecusive

def searchTokens(setting, network, tokenName):
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
        print('Symbol: '+result['symbol'])
        print('Name: '+result['name'])
        print('Address: '+result['address'])
        print('Website: '+result['website'])
        print('Network: '+network)
        print('-----------------')
    
    # Delete temp file
    os.remove(tmpPath)
    return

def searchInterfacesWithProjectAndKeyword(setting, project, interface):
    print("Please check the detail of interfaces under the folder " + setting.getPathToPOCTemplate()+"interfaces/")
    
    directories = findFiles(project,setting.getPathToPOCTemplate()+"interfaces")
    
    for directory in directories:
        files = findFilesRecusive(interface, setting.getPathToPOCTemplate()+"interfaces/"+directory)
        for file in files:
            print ("Add ["+file.replace(setting.getPathToPOCTemplate()+"interfaces/","",1)+"] to the `interfaces` field under config.yml")
            print ("    Usage: import \"./"+file.replace(setting.getPathToPOCTemplate()+"interfaces/","",1)+"\";")
    return

def searchInterfacesWithKeyword(setting, interface):
    print("Please check the detail of interfaces under the folder " + setting.getPathToPOCTemplate()+"interfaces/")
    files = findFilesRecusive(interface, setting.getPathToPOCTemplate()+"interfaces/")
    for file in files:
        print ("Add ["+file.replace(setting.getPathToPOCTemplate()+"interfaces/","",1)+"] to the `interfaces` field under config.yml")
        print ("    Usage: import \"./"+file.replace(setting.getPathToPOCTemplate()+"interfaces/","",1)+"\";")
    return

def searchInterfacesWithAddress(setting, network, address, name=None, exploit=None):
    url = setting.getScanAPIURL(network)
    key = setting.getScanAPIKey(network)

    # Get contract ABI via Scan API
    contractABIJson = None
    if network == "eth":
        url = url+"/api"
        params = prepareEtherScanAPIParametersForGetContractABI(key, address)
        response = requests.get(url = url, params = params)
        contractABIJson = handleEtherScanAPIResponseForGetContractABI(response)
    elif network == "bsc":
        url = url+"/api"
        params = prepareBscScanAPIParametersForGetContractABI(key, address)
        response = requests.get(url = url, params = params)
        contractABIJson = handleBscScanAPIResponseForGetContractABI(response)
    else:
        print("Unsupport Network")
        return
    
    # Convert ABI to interfaces
    name = "Interface_"+address if name == None else name
    echoResult = subprocess.run(["echo", contractABIJson], check=True, capture_output=True)
    convertedInterface = subprocess.run(["npx", "abi-to-sol", name], input=echoResult.stdout, capture_output=True)
    
    # Save the interfaces to current POC folder or directly show in terminal
    if (exploit == None):
        print("--------------------------------------------------------------")
        print("EXPLOIT NOT LOADED, ONLY SHOW CONVERTED INTERFACE IN TERMINAL")
        print("--------------------------------------------------------------")
        print(convertedInterface.stdout.decode())
    else:
        path = os.path.join(setting.getPathToExploits(), exploit.name)
        with open(os.path.join(path,name+".sol"), 'w') as f:
            f.write(convertedInterface.stdout.decode())
            print("--------------------------------------------------------------")
            print("CONVERTED INTERFACE SAVED IN THE FOLDER OF LOADED EXPLOIT")
            print("--------------------------------------------------------------")
        # Show the path for importing converted interfaces
        print ("import \"./"+name+".sol"+"\";")
    
    return
