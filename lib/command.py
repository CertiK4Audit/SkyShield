from genericpath import exists
from importlib.resources import path
from inspect import Parameter
import sys, os, glob, yaml, shutil, time
from .exploit import Exploit
from .setting import Setting

# The prefix name of temp folder
NORMAL_TEMP_FOLDER_PREFIX = 'exploit-framework-normal-tmp-'
DEVMODE_TEMP_FOLDER_PREFIX = 'exploit-framework-dev-tmp-'

# Variables
POC_GITHUB = "https://github.com/CertiK-Yuannan/PoC_Template.git"
POC_LIST_DIR = "./PoC_Template/template_list.csv"
EXPLOITS_PATH = "./exploits/"


def init(arg):
    init_installPackage()
    init_loadPoC()

# install packages specified in the configuration packages
def init_installPackage():
    prePwd = os.getcwd()
    os.chdir('./configurations')
    os.system('npm install')
    os.chdir(prePwd) 

# load PoCs github to the current folder
def init_loadPoC():
    try:
        print("Downloading PoCs ....")
        os.system("git clone -b main" + " " + POC_GITHUB)
    except:
        print("Unable to download PoCs")

def list(setting):
    try:
        f = open(POC_LIST_DIR, "r")
        exploits = f.readlines()
        f.close()
        for exploit in exploits:
            print (exploit)
    except:
        print("Incorrect database path")

def load(arg, setting):
    try:
        #remove old PoC's if have 
        try:
            os.system("rm -rf " + EXPLOITS_PATH + arg)
        except Exception as e:
            print(e)

        prePwd = os.getcwd()
        # checkout to given branch
        os.chdir(EXPLOITS_PATH)
        os.system("git clone -b" + " " + arg + " " + POC_GITHUB + " "+arg)

        os.chdir(prePwd) 
        if not os.path.exists(os.path.join(EXPLOITS_PATH, arg)):
            raise Exception("Network problem or PoC not found")

        #set parameters
        exploit = Exploit(arg, EXPLOITS_PATH + arg)
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
        if(len(arg.split(' '))==1):
            networkURL = setting.readNetworkURL(arg)
            exploit.setNetwork(networkURL)
        elif(len(arg.split(' '))==2):
            network = arg.split(' ')[0]
            blockNumber = arg.split(' ')[1]
            networkURL = setting.readNetworkURL(network)
            exploit.setNetwork(networkURL,blockNumber)
    except:
        print("No Exploit loaded")

def set(arg, exploit):
    key = arg.split(' ')[0]
    element = arg.split(' ')[1]
    value = arg.split(' ')[2]
    exploit.setParameter(key, element, value)

# def storeParaToYaml(path, key, element, value):
#     fr = open(path, "r")
#     configuration = yaml.full_load(fr)
#     fr.close()
    
#     configuration[key.lower()][element] = value
#     print(configuration)
#     fw = open(path, "w")
#     yaml.dump(configuration, fw)
#     fw.close()
    

def update(exploit):
    exploit.loadConfig()


def test(exploit, setting):
    # Check exploit
    if (exploit is None):
        print ('No Exploit loaded')
    elif not os.path.exists('configurations/node_modules') or not os.path.exists('configurations/package-lock.json'):
        print ('No initialized node_modules, please run command `init`')
    else:
    # Create folder in /tmp
        temp = '/tmp'
        exploit_path = os.path.join('exploits/', exploit.name)
        path = os.path.join(temp, DEVMODE_TEMP_FOLDER_PREFIX+exploit.name)
        oldpwd = os.getcwd()
        if not os.path.exists(path):
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
        #os.symlink(oldpwd+'/configurations/node_modules', 'node_modules')
        os.system('ln -s '+oldpwd+'/configurations/node_modules'+ ' node_modules')
        os.chdir(oldpwd)
    # Copy required interfaces to contracts/interfaces
        interfaces = exploit.config['interfaces']
        if interfaces is not None:
            for interface in interfaces:
                shutil.copyfile('contracts/interfaces/' + interface, os.path.join(path,'contracts/interfaces/', interface))
    # Copy attack.ts to scripts and exploit.sol to contracts.
        shutil.copyfile(os.path.join(exploit_path, 'Attack.ts'), os.path.join(path,'scripts', 'Attack.ts'))
        for file_path in glob.glob(os.path.join(exploit_path, '**', '*.sol'), recursive=True):
            dst_path = os.path.join(path, "contracts/" + os.path.basename(file_path))
            shutil.copy(file_path, dst_path)
    # Create a config.yml based on users' inputs in this folder
        # with open(os.path.join(path, 'config.yml'), 'w') as f:
        #     yaml.dump(exploit.config, f)
        shutil.copyfile(os.path.join(exploit_path, 'config.yml'), os.path.join(path, 'config.yml'))
    # Run exploit
        os.chdir(path)
        os.system("npx hardhat run scripts/attack.ts")
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