import os
import subprocess
from lib.setting import setting
from lib.util import bcolors, copyAllSolidityFiles, copyConfigYamlFile, dumpYamlFileTo, prepareHardHatEnv, removeTemporaryFolder

def makeConfigYamlFile():
    config = {
        'networks':
            {
                'blockNumber': 'empty',
                'url': 'empty'
    }
    }
    return config


def flattenSolidityFile(sourcePath, outputPath):
    flattenedContracts = subprocess.run(['npx', 'hardhat', 'flatten', sourcePath], capture_output=True)
    with open(outputPath, 'w') as f:
    # TODO Fix the error of multiple SPDX license
    # https://github.com/NomicFoundation/truffle-flattener/issues/55
        f.write(flattenedContracts.stdout.decode())
        print(bcolors.FAIL + flattenedContracts.stderr.decode() + bcolors.ENDC)
    
    return

def flattenSolidityFolder(sourcePath, interfacesPath, outputDirectory):

    tmpPath = prepareHardHatEnv("flatten_contracts")

    #copyConfigYamlFile("./lib/tools/flatten/", tmpPath)
    dumpYamlFileTo(makeConfigYamlFile(), tmpPath+'/config.yml')
    
    copyAllSolidityFiles(sourcePath, tmpPath+"/contracts")

    os.makedirs(outputDirectory, exist_ok=True)

    prePWD = os.getcwd()
    os.chdir(tmpPath)

    if not os.path.isdir(tmpPath+"/contracts"+interfacesPath):
        file = tmpPath+"/contracts"+interfacesPath
        flattenSolidityFile(file, outputDirectory+"/"+os.path.basename(file))
        print("Output: " + bcolors.OKGREEN + os.path.normpath(outputDirectory+"/"+os.path.basename(file)) + bcolors.ENDC)
        os.chdir(prePWD)
        removeTemporaryFolder("flatten_contracts")
        return 
    
    for root, dir, files in os.walk(tmpPath+"/contracts"+interfacesPath):
        for file in files:
            relativePath = os.path.relpath(root, tmpPath+"/contracts"+interfacesPath)
            relativePath = relativePath if relativePath != "." else ""
            outputPath = os.path.join(outputDirectory, relativePath) + "/"
            os.makedirs(outputPath, exist_ok=True)
            flattenSolidityFile(root+"/"+file, outputPath+file)
            print("Output: " + bcolors.OKGREEN + os.path.normpath(outputPath+file) + bcolors.ENDC)
    os.chdir(prePWD)
    removeTemporaryFolder("flatten_contracts")
    return 

