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
        lib.command.close(self.exploit, self.setting)
        return True
    # enter development mode
    def do_enter_dev_mode(self,arg):
        'Enter the development mode'
        self.setting.development_mode = True
        self.prompt = "({})(dev) > ".format(Str("framework").red())
    # exit development mode
    def do_exit_dev_mode(self,arg):
        'Exit the development mode'
        self.setting.development_mode = False
        self.prompt = "({}) > ".format(Str("framework").red())
    # list all exploits
    def do_list(self, arg):
        'List all exploits'
        lib.command.list(self.setting)
    # search exploit
    def do_search(self, arg):
        'Search exploits via keyword'
        lib.command.search(arg,self.setting)
    # choose exploit
    def do_load(self, arg):
        'Choose an exploit with fullname'
        self.exploit = lib.command.load(arg, self.setting)
    # show helper of exploit 
    def do_info(self, arg):
        'Choose an exploit with fullname'
        lib.command.info(self.exploit)
    # set parameters
    def do_set(self, arg):
        'Set a parameter required by specific exploit'
        self.exploit = lib.command.set(arg, self.exploit)
    # set parameters from customized config.yml file
    def do_import(self, arg):
        'Set parameters from customized config.yml file'
        self.exploit = lib.command.importConfig(arg, self.exploit)
    # show current value of parameters
    def do_show_parameters(self, arg):
        'Set a parameter required by specific exploit'
        lib.command.showParameters(self.exploit, self.setting)
    # run exploits
    def do_run(self,arg):
        'Run selected exploit'
        lib.command.run(self.exploit, self.setting)
if __name__ == '__main__':
    FrameworkShell().cmdloop()