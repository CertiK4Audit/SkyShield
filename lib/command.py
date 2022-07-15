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
POC_GITHUB = "git@github.com:CertiK-Yuannan/PoC_Template.git"
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
        os.system("git clone" + " " + POC_GITHUB)
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
        os.system("git clone -b" + " " + arg + " " + POC_GITHUB)

        ## if it has been downloaded
        try:
            os.rename("PoC_Template", arg)
        except Exception as e:
            print(e)
        os.chdir(prePwd) 

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
        exploit.show_parameters()
    except:
        print("No Exploit loaded")

def set(arg, exploit, pocName):
    key = arg.split(' ')[0]
    element = arg.split(' ')[1]
    value = arg.split(' ')[2]
    exploit.set_parameter(key, element, value)
    path = EXPLOITS_PATH + pocName + "/config.yml"
    print(path)

    storeParaToYaml(path, key, element, value)   
    return exploit

def storeParaToYaml(path, key, element, value):
    fr = open(path, "r")
    configuration = yaml.full_load(fr)
    fr.close()
    
    configuration[key.lower()][element] = value
    print(configuration)
    fw = open(path, "w")
    yaml.dump(configuration, fw)
    fw.close()
    

def update(pocName):
    return Exploit(pocName,EXPLOITS_PATH+ pocName)

def importConfig(arg, exploit):
    try:
        if (exploit is None):
            raise Exception('No Exploit loaded')
        path = arg.split(' ')[0]
        if os.path.exists(path):
            with open(path) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                for key, value in data['address'].items():
                    exploit.set_parameter('address', key, value)
                for key, value in data['parameters'].items():
                    exploit.set_parameter('parameters', key, value)
                for key, value in data['networks'].items():
                    exploit.set_parameter('networks', key, value)
        else:
            raise Exception('Config File Not Found')
    except Exception as e:
        print(e)
        print("Import Error")
    return exploit

def test(exploit, setting):
    # Check exploit
    if (exploit is None):
        print ('No Exploit loaded')
    elif not os.path.exists('configurations/node_modules') or not os.path.exists('configurations/package-lock.json'):
        print ('No initialized node_modules, please run command `init`')
    else:
    # Create folder in /tmp
        temp = '/tmp'
        if setting.development_mode:
            exploit_path = os.path.join('exploits/', exploit.name)
            path = os.path.join(temp, DEVMODE_TEMP_FOLDER_PREFIX+exploit.name)
        else:
            exploit_path = os.path.join(setting.path_to_database, exploit.name)
            path = os.path.join(temp, NORMAL_TEMP_FOLDER_PREFIX+exploit.name)
        oldpwd = os.getcwd()
        if not os.path.exists(path):
            os.mkdir(path)
        # elif not setting.development_mode: 
        #     shutil.rmtree(path)
        #     os.mkdir(path)
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
        with open(os.path.join(path, 'config.yml'), 'w') as f:
            yaml.dump(exploit.config, f)
    # Run exploit
        os.chdir(path)
        os.system("npx hardhat run scripts/attack.ts")
    # Return results

    # Delete this folder.
        # if not setting.development_mode:
            # shutil.rmtree(path) 
        # if not setting.development_mode:
        #     shutil.rmtree(os.path.join(oldpwd,"exploits",exploit.name))
        os.chdir(oldpwd)

def close(exploit, setting):
    if not setting.development_mode:
        oldpwd = os.getcwd()
        os.chdir('/tmp')
        for match in glob.iglob(NORMAL_TEMP_FOLDER_PREFIX+"*"):
            shutil.rmtree(match)
        os.chdir(oldpwd)