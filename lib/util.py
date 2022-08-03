import fnmatch
import os
import re
import shutil
import subprocess
import yaml

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def findFiles(keyword, path='.'):

    rule = re.compile(fnmatch.translate("*"+keyword+"*"), re.IGNORECASE)
    return [file for file in os.listdir(path) if rule.match(file)]

def findFilesRecusive(keyword, path='.'):
    matchedFiles = []
    rule = re.compile(fnmatch.translate("*"+keyword+"*"), re.IGNORECASE)
    for root, dir, files in os.walk(path):
        for file in files:
            if rule.match(file):
                matchedFiles.append(root+"/"+file)
    return matchedFiles

def createTemporaryFolder(name):
    # TODO Need to support windows
    temporaryFolderPrefix = '/tmp/'
    temporaryFolderPath = temporaryFolderPrefix + name
    if os.path.exists(temporaryFolderPath):
        shutil.rmtree(temporaryFolderPath)    
    os.mkdir(temporaryFolderPath)
    return temporaryFolderPath

def removeTemporaryFolder(name):
    temporaryFolderPrefix = '/tmp/'
    temporaryFolderPath = temporaryFolderPrefix + name
    if os.path.exists(temporaryFolderPath):
        shutil.rmtree(temporaryFolderPath)

def prepareHardHatEnv(name):
    # Create folder
    path = createTemporaryFolder(name)

    # Create three sub directories
    subdirectories = ["contracts", "scripts", "contracts/interfaces"]
    for subdirectory in subdirectories:
        os.makedirs(os.path.join(path,subdirectory), exist_ok = True)
    
    # Copy hardhat.config.ts, package.json and tsconfig.json to this folder
    configFiles = ['hardhat.config.ts', 'package.json', 'tsconfig.json']
    for configFile in configFiles:
        shutil.copyfile("configurations/"+configFile, os.path.join(path,configFile))
    
    # Create a softlink to node_modules
    prePWD = os.getcwd()
    os.chdir(path)
    subprocess.run(['ln', '-s', prePWD + '/configurations/node_modules', 'node_modules'])
    os.chdir(prePWD)

    return path

def copyRequiredInterfaces(interfaces, src, dst):
    # src: setting.getPathToPOCTemplate()+'interfaces/'
    if interfaces is not None:
            for interface in interfaces:
                os.makedirs(os.path.join(dst, os.path.dirname(interface)), exist_ok=True)
                shutil.copyfile(src + interface, os.path.join(dst, interface))

def copyConfigYamlFile(src, dst):
    shutil.copyfile(os.path.join(src, 'config.yml'), os.path.join(dst, 'config.yml'))

def dumpYamlFileTo(content,pathToFile):
    with open (pathToFile, "w") as f:
        yaml.dump(content,f)

def copyAttackScripts(src, dst):
    shutil.copyfile(os.path.join(src, 'Attack.ts'), os.path.join(dst,'scripts', 'Attack.ts'))

def copyAllTypeScriptFiles(src,dst):
    typeScriptFiles = findFilesRecusive(".ts", src)
    for typeScriptFile in typeScriptFiles:
        os.makedirs(os.path.join(dst, os.path.dirname(os.path.relpath(typeScriptFile, src))), exist_ok=True)
        shutil.copy(typeScriptFile, os.path.join(dst, os.path.relpath(typeScriptFile, src)))
    return

def copyAllSolidityFiles(src, dst):
    solidityFiles = findFilesRecusive(".sol", src)
    for solidityFile in solidityFiles:
        os.makedirs(os.path.join(dst, os.path.dirname(os.path.relpath(solidityFile, src))), exist_ok=True)
        shutil.copy(solidityFile, os.path.join(dst, os.path.relpath(solidityFile, src)))
    return

def executeScripts(path, scriptName):
    prePWD =  os.getcwd()
    os.chdir(path)
    subprocess.run(['npx', 'hardhat', 'run', 'scripts/'+scriptName])
    os.chdir(prePWD)
    