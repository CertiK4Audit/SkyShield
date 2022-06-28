import cmd, sys
import glob, os
import yaml
import shutil


clear = lambda: os.system('clear')

class Str(str):
    def red(self):
        return "\033[31m{}\033[0m".format(self)

    def green(self):
        return "\033[32m{}\033[0m".format(self)

    def yellow(self):
        return "\033[33m{}\033[0m".format(self)

    def blue(self):
        return "\033[34m{}\033[0m".format(self)

class Exploit:

    def load_config(self, name):
        try:
            with open('exploits/'+ name +'/config.yml') as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                #print(data)
                self.config = data
        except:
            print("Config File Not Found")
        
    
    def set_parameter(self, key, element, value):
        try:
            self.config[key][element] = value
        except:
            print("Key, Element, or Value is not correct")
    
    def show_parameters(self):
        print('--------')
        print('Address:')
        for key, value in self.config['address'].items():
            print(key, "-->", value)
        print('--------')
        print('Parameters:')
        for key, value in self.config['parameters'].items():
            print(key, "-->", value)
        print('--------')
        print('Networks:')
        for key, value in self.config['networks'].items():
            print(key, "-->", value)
        print('--------')

    def __init__(self, name):
        self.name = name
        self.load_config(name)

class FrameworkShell(cmd.Cmd):
    intro = 'Welcome to the Exploit Framework.   Type help or ? to list commands.\n'
    prompt = "({}) > ".format(Str("framework").red())
    file = None

    exploit = None

    # basic commands
    def do_test(self, arg):
        'Test command'
        print(arg)
        print('test')
    def do_test2(self, arg):
        'Test second command'
        print('test2')
    def do_clear(self,arg):
        'Clear shell'
        clear()
    def do_exit(self,arg):
        'Exit framework'
        self.close()
        return True
    def close(self):
        if self.exploit:
            if os.path.exists('/tmp'+self.exploit.name):
                shutil.rmtree('/tmp'+self.exploit.name)
    # search exploit
    def do_search(self, arg):
        'Search exploits via keyword'
        try:
            os.chdir("exploits")
            for file in glob.glob('*'+arg+'*'):
                print(file)
            os.chdir("..")
        except:
            print("Exploit Not Found")
    # choose exploit
    def do_use(self, arg):
        'Choose an exploit with fullname'
        try:
            self.exploit = Exploit(arg)
            print(self.exploit.config['description'])
        except:
            self.exploit = None
            print('Exception occurred when loading config file')
    # show helper of exploit 
    def do_info(self, arg):
        'Choose an exploit with fullname'
        try:
            print(self.exploit.config['description'])
        except:
            print("No Exploit loaded")
    # set parameters
    def do_set(self, arg):
        'Set a parameter required by specific exploit'
        key = arg.split(' ')[0]
        element = arg.split(' ')[1]
        value = arg.split(' ')[2]
        self.exploit.set_parameter(key, element, value)
    # set parameters from customized config.yml file
    def do_import(self, arg):
        'Set parameters from customized config.yml file'
        try:
            if (self.exploit is None):
                raise Exception('No Exploit loaded')
            path = arg.split(' ')[0]
            if os.path.exists(path):
                with open(path) as f:
                    data = yaml.load(f, Loader=yaml.FullLoader)
                    for key, value in data['address'].items():
                        self.exploit.set_parameter('address', key, value)
                    for key, value in data['parameters'].items():
                        self.exploit.set_parameter('parameters', key, value)
                    for key, value in data['networks'].items():
                        self.exploit.set_parameter('networks', key, value)
            else:
                raise Exception('Config File Not Found')
        except Exception as e:
            print(e)
            print("Import Error")
    # show current value of parameters
    def do_show_parameters(self, arg):
        'Set a parameter required by specific exploit'
        try:
            self.exploit.show_parameters()
        except:
            print("No Exploit loaded")
    # run exploits
    def do_run(self,arg):
        'Run selected exploit'
        # Check
        if (self.exploit is None):
            print ('No Exploit loaded')
        else:
            # Create folder in /tmp
            temp = '/tmp'
            directory = self.exploit.name
            path = os.path.join(temp, directory)
            oldpwd = os.getcwd()
            if os.path.exists(path):
                shutil.rmtree(path)
            os.mkdir(path)
            # Create three sub directories
            subdirectories = ["contracts", "scripts", "contracts/interfaces"]
            for subdirectory in subdirectories:
                os.mkdir(os.path.join(path,subdirectory))
            # Copy hardhat.config.ts, package.json and tsconfig.json to this folder
            configFiles = ['hardhat.config.ts', 'package.json', 'tsconfig.json']
            for configFile in configFiles:
                shutil.copyfile("configurations/"+configFile, os.path.join(path,configFile))
            # Copy required interfaces to contracts/interfaces
            interfaces = self.exploit.config['interfaces']
            for interface in interfaces:
                shutil.copyfile('contracts/interfaces/' + interface, os.path.join(path,'contracts/interfaces/', interface))
            # Copy attack.ts to scripts and exploit.sol to contracts.
            shutil.copyfile('exploits/' + self.exploit.name + '/Attack.ts', os.path.join(path,'scripts', 'Attack.ts'))
            shutil.copyfile('exploits/' + self.exploit.name + '/Exploit.sol', os.path.join(path,'contracts', 'Exploit.sol'))
            # Create a config.yml based on users' inputs in this folder
            with open(os.path.join(path, 'config.yml'), 'w') as f:
                yaml.dump(self.exploit.config, f)
            # Run exploit
            os.chdir(path)
            os.system("npm install")
            os.system("npx hardhat run scripts/attack.ts")
            # Return results

            # Delete this folder.
            shutil.rmtree(path)
            os.chdir(oldpwd)
if __name__ == '__main__':
    FrameworkShell().cmdloop()