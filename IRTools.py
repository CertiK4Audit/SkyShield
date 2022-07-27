from asyncio import subprocess
import cmd, os
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

    # basic commands
    def do_clear(self,arg):
        'Clear shell'
        clear()
    def do_exit(self,arg):
        'Exit framework'
        lib.command.close(self.exploit, self.setting)
        return True
    def do_use(self,arg):
        lib.command.useNetwork(arg)

    # Use specific network
    def do_query(self,arg):
        'Install required node_modules'
        lib.command.query(arg)
    

if __name__ == '__main__':
    FrameworkShell().cmdloop()