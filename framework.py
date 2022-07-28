from asyncio import subprocess
import cmd, os, shutil


from lib.setting import setting
from lib.exploit import exploit
import lib.command


clear = lambda: os.system('clear')
#clear = lambda: subprocess.run(['clear'])

class Str(str):
    def red(self):
        return "\033[31m{}\033[0m".format(self)

    def green(self):
        return "\033[32m{}\033[0m".format(self)

    def yellow(self):
        return "\033[33m{}\033[0m".format(self)

    def blue(self):
        return "\033[34m{}\033[0m".format(self)

class FrameworkShell(cmd.Cmd):
    intro = 'Welcome to the Exploit Framework.   Type help or ? to list commands.\n'
    prompt = "({}) > ".format(Str("framework").red())

    # basic commands
    def do_clear(self,arg):
        'Clear shell'
        clear()
    def do_exit(self,arg):
        'Exit framework'
        lib.command.close()
        return True
    
    # init the environmemt, install basic packages
    def do_init(self,arg):
        'Install required node_modules'
        lib.command.init(arg)
    
    # list all exploits
    def do_list(self, arg):
        'List all exploits'
        lib.command.list()
    
    def do_search(self,arg):
        "Search tools (Work in progress)"
        lib.command.search(arg)
    
    # choose exploit
    def do_load(self, arg):
        'Choose an exploit with fullname'
        lib.command.load(arg)
    
    def do_use(self, arg):
        'Use a specific nework for testing'
        lib.command.useNetworks(arg)
    # set parameters
    def do_set(self, arg):
        'Set a parameter required by specific exploit'
        lib.command.set(arg)
    # Update config.yml
    def do_update(self, arg):
        lib.command.update()

    # show current value of parameters
    def do_show_parameters(self, arg):
        'Set a parameter required by specific exploit'
        lib.command.showParameters()

    # flatten contracts to specific path
    def do_flatten(self, arg):
        'Flatten contracts to specific path'
        lib.command.flatten(arg)
    # run exploits
    def do_test(self,arg):
        'Testing selected exploit'
        #@audit update it before test
        lib.command.update()
        lib.command.test()
if __name__ == '__main__':
    FrameworkShell().cmdloop()