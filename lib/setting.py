from xml.dom.expatbuilder import FragmentBuilderNS
import yaml
class Setting:
    development_mode = False

    def readNetworkURL(self, network):
        with open('setting.yml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data['networks'][network]['url']
    
    def __init__(self):
        self.development_mode = True
