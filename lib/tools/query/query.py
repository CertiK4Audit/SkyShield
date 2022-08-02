from shutil import copyfile
from lib.api.endpoints import getContractABI
from lib.setting import setting
from lib.util import copyAllTypeScriptFiles, dumpYamlFileTo, executeScripts, prepareHardHatEnv, removeTemporaryFolder

def makeConfigYamlFile():
    config = {
        'networks':
            {
                'blockNumber': '',
                'url': ''
    },
    'path_to_abi': '',
    'address': '',
    'function': ''
    }
    return config

def queryFunctionWithAddressAndBlockNumber(network, blockNumber, address, function):
    # Prepare environment for hardhat
    tmpPath = prepareHardHatEnv("query")

    # Prepare config.yml
    config = makeConfigYamlFile()
    config['networks']['blockNumber'] = blockNumber
    config['networks']['url'] = setting.getNetworkURL(network)
    config['address'] = address
    config['function'] = function
    

    # Get and save ABI json file via api
    config['path_to_abi'] = address + '.json' 
    contractABIJson = getContractABI(network, address)
    
    if contractABIJson is None:
        removeTemporaryFolder("query")
        return
    
    with open(tmpPath+"/"+address + '.json', "w") as f:
        f.write(contractABIJson)
    
    # Copy query.ts to temporary file
    copyAllTypeScriptFiles("./lib/tools/query/", tmpPath+"/scripts")

    # Dump config.yml
    dumpYamlFileTo(config, tmpPath+'/config.yml')
    
    # Execute script
    executeScripts(tmpPath, 'query.ts')

    # Remove temporary folder
    removeTemporaryFolder("query")

    return