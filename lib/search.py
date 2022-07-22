import json
import os
from pysondb import db
POC_Template_DIR = './PoC_Template/'
def searchTokens(network, tokenName):
    # Format json file to satisfy the requirement of pysondb 
    path = POC_Template_DIR+'tokens/'+network+'/tokens-'+network+'.json'
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