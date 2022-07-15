import cmd, os, shutil

from lib.exploit import Exploit
from lib.setting import Setting
import lib.command


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

class FrameworkShell(cmd.Cmd):
    intro = 'Welcome to the Exploit Framework.   Type help or ? to list commands.\n'
    prompt = "({}) > ".format(Str("framework").red())
    file = None
    exploit = None
    setting = Setting()
    pocName = ""

    # basic commands
    def do_clear(self,arg):
        'Clear shell'
        clear()
    def do_exit(self,arg):
        'Exit framework'
        lib.command.close(self.exploit, self.setting)
        return True
    
    # init the environmemt, install basic packages
    def do_init(self,arg):
        'Install required node_modules'
        lib.command.init(arg)
    
    # list all exploits
    def do_list(self, arg):
        'List all exploits'
        lib.command.list(self.setting)
    
    # choose exploit
    def do_load(self, arg):
        'Choose an exploit with fullname'
        self.exploit = lib.command.load(arg, self.setting)
    
    def do_use(self, arg):
        'Use a specific nework for testing'
        lib.command.useNetworks(arg, self.exploit, self.setting)
    # set parameters
    def do_set(self, arg):
        'Set a parameter required by specific exploit'
        lib.command.set(arg, self.exploit)
    
    def do_update(self, arg):
        lib.command.update(self.exploit)

    # show current value of parameters
    def do_show_parameters(self, arg):
        'Set a parameter required by specific exploit'
        lib.command.showParameters(self.exploit, self.setting)
    # run exploits
    def do_test(self,arg):
        'Testing selected exploit'
        #@audit update it before test
        lib.command.update(self.exploit)
        lib.command.test(self.exploit, self.setting)
if __name__ == '__main__':
    FrameworkShell().cmdloop()