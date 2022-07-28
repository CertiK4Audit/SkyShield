from genericpath import exists
from importlib.resources import path
from inspect import Parameter
from posixpath import dirname
import sys, os, glob, yaml, shutil, time
from lib.flattener import flattenSolidityFolder

from lib.search import searchInterfacesWithAddress, searchInterfacesWithKeyword, searchInterfacesWithProjectAndKeyword, searchTokens
from .exploit import Exploit
from .setting import Setting
import subprocess

# The prefix name of temp folder
NORMAL_TEMP_FOLDER_PREFIX = 'exploit-framework-normal-tmp-'
DEVMODE_TEMP_FOLDER_PREFIX = 'exploit-framework-dev-tmp-'



def init(arg,setting):
    init_installPackage(setting)
    init_loadPoC(setting)

# install packages specified in the configuration packages
def init_installPackage(setting):
    prePWD = os.getcwd()
    os.chdir('./configurations')
    subprocess.run(['npm', 'install'])
    os.chdir(prePWD) 

# load PoCs github to the current folder
def init_loadPoC(setting):
    try:
        if os.path.exists("PoC_Template"):
            shutil.rmtree("PoC_Template")
        print("Downloading PoCs ....")
        subprocess.run(['git', 'clone', '-b', 'main', setting.getPOCTemplateRepoURL()])
    except:
        print("Unable to download PoCs")

def list(setting):
    try:
        f = open(setting.getPathToPOCDatabase(), "r")
        exploits = f.readlines()
        f.close()
        for exploit in exploits:
            print (exploit)
    except:
        print("Incorrect database path")

def search (arg, setting, exploit):
    try:
        tool = arg.split()[0]
        if tool=='address':
            type = arg.split()[1]
            if type == 'token':
                searchTokens(setting, arg.split()[2],arg.split()[3])
            else:
                print('Function not found or work in progress')
        elif tool=='interfaces':
            type = arg.split()[1]
            if type == 'address':
                name = arg.split()[4] if len(arg.split())>4 else None 
                searchInterfacesWithAddress(setting, arg.split()[2], arg.split()[3], name, exploit)
            elif type == 'project':
                searchInterfacesWithProjectAndKeyword(setting, arg.split()[2], arg.split()[3])
            elif type == 'global':
                searchInterfacesWithKeyword(setting, arg.split()[2])
            else:
                print('Function not found or work in progress')
        else:
            print('Tool not found or work in progress')
    except Exception as exception:
        print(exception)
        print('Incorrect command')

def load(arg, setting):
    try:
        #Create the folder
        if not os.path.exists(setting.getPathToExploits()):
            subprocess.run(["mkdir", setting.getPathToExploits()])
            
        prePWD = os.getcwd()
        # checkout to given branch
        if not os.path.exists(setting.getPathToExploits()+arg):
            os.chdir(setting.getPathToExploits())
            subprocess.run(['git', 'clone', '-b', arg, setting.getPOCTemplateRepoURL(), arg])
        os.chdir(prePWD) 
        if not os.path.exists(os.path.join(setting.getPathToExploits(), arg)):
            raise Exception("Network problem or PoC not found")

        #set parameters
        exploit = Exploit(arg, setting.getPathToExploits() + arg)
        print("##############################  "+arg+ " PoC" + "  ################################")
        print(exploit.config['description'])
    except Exception as e:
        print(e)
        exploit = None
        print('Exception occurred when loading config file')
    return exploit

def showParameters(exploit, setting):
    try:
        exploit.showParameters()
    except:
        print("No Exploit loaded")

def useNetworks(arg, exploit, setting):
    try:
        if(len(arg.split())==1):
            networkURL = setting.getNetworkURL(arg)
            exploit.setNetwork(networkURL)
        elif(len(arg.split())==2):
            network = arg.split()[0]
            blockNumber = arg.split()[1]
            networkURL = setting.getNetworkURL(network)
            exploit.setNetwork(networkURL,blockNumber)
    except:
        print("No Exploit loaded")

def set(arg, exploit):
    key = arg.split()[0]
    element = arg.split()[1]
    value = arg.split()[2]
    exploit.setParameter(key, element, value)
    
def update(exploit):
    exploit.loadConfig()

def flatten(arg, setting):
    try:
        #TODO Need better method to split 
        sourcePath = arg.split(" /")[0]
        interfacesPath = arg.split(" /")[1]
        outputPath = arg.split(" /")[2]
        outputPath = "/"+outputPath
        interfacesPath = "/" +interfacesPath
        print("Source: ")
        print(sourcePath)
        print("Relative path to interfaces: ")
        print(interfacesPath)
        print("Output directory: ")
        print(outputPath)
        flattenSolidityFolder(sourcePath, interfacesPath, outputPath)
    except Exception as e:
        print(e)
        print("Something wrong")


def test(exploit, setting):
    # Check exploit
    if (exploit is None):
        print ('No Exploit loaded')
    elif not os.path.exists('configurations/node_modules') or not os.path.exists('configurations/package-lock.json') or not os.path.exists('PoC_Template/interfaces'):
        print ('No initialized node_modules, please run command `init`')
    else:

    # Create folder in /tmp
        temp = '/tmp'
        exploit_path = os.path.join(setting.getPathToExploits(), exploit.name)
        path = os.path.join(temp, DEVMODE_TEMP_FOLDER_PREFIX+exploit.name)
        oldpwd = os.getcwd()
        if os.path.exists(path):
            shutil.rmtree(path)    
        os.mkdir(path)

    # Create three sub directories
        subdirectories = ["contracts", "scripts", "contracts/interfaces"]
        for subdirectory in subdirectories:
            os.makedirs(os.path.join(path,subdirectory), exist_ok = True)
    
    # Copy hardhat.config.ts, package.json and tsconfig.json to this folder
        configFiles = ['hardhat.config.ts', 'package.json', 'tsconfig.json']
        for configFile in configFiles:
            shutil.copyfile("configurations/"+configFile, os.path.join(path,configFile))
    
    # Create a softlink to node_modules
        os.chdir(path)
        subprocess.run(['ln', '-s', oldpwd + '/configurations/node_modules', 'node_modules'])
        os.chdir(oldpwd)
    
    # Copy required interfaces to contracts/interfaces
        interfaces = exploit.config['interfaces']
        if interfaces is not None:
            for interface in interfaces:
                os.makedirs(os.path.join(path,'contracts/'+os.path.dirname(interface)), exist_ok=True)
                shutil.copyfile(setting.getPathToPOCTemplate()+'interfaces/' + interface, os.path.join(path,'contracts/', interface))
    
    # Copy attack.ts to scripts and exploit.sol to contracts.
        shutil.copyfile(os.path.join(exploit_path, 'Attack.ts'), os.path.join(path,'scripts', 'Attack.ts'))
        for file_path in glob.glob(os.path.join(exploit_path, '**', '*.sol'), recursive=True):
            dst_path = os.path.join(path, "contracts/" + os.path.basename(file_path))
            shutil.copy(file_path, dst_path)
    
    # Create a config.yml based on users' inputs in this folder
        shutil.copyfile(os.path.join(exploit_path, 'config.yml'), os.path.join(path, 'config.yml'))
    
    # Run exploit
        os.chdir(path)
        subprocess.run(['npx', 'hardhat', 'run', 'scripts/attack.ts'])
    
    # Return results

    # Delete this folder.
        shutil.rmtree(path)    
        os.chdir(oldpwd)

def close(exploit, setting):
    oldpwd = os.getcwd()
    os.chdir('/tmp')
    for match in glob.iglob(DEVMODE_TEMP_FOLDER_PREFIX+"*"):
        shutil.rmtree(match)
    os.chdir(oldpwd)