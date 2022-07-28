from xml.dom.expatbuilder import FragmentBuilderNS
import yaml

class Setting:
    development_mode = False

    def loadSetting(self):
        with open('setting.yml') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def getNetworkURL(self, network):
        return self.loadSetting()['networks'][network]['url']

    def getScanAPIURL(self, network):
        return self.loadSetting()['scanAPI'][network]['url']
            
    def getScanAPIKey(self, network):
        return self.loadSetting()['scanAPI'][network]['key']

    def getPathToPOCTemplate(self):
        return self.loadSetting()['path']['poc_template']
    
    def getPathToExploits(self):
        return self.loadSetting()['path']['exploits']
    
    def getPOCTemplateRepoURL(self):
        return self.loadSetting()['repo']['poc_template']
    
    def getTokenDatabaseRepoURL(self):
        return self.loadSetting()['repo']['tokens_database']
    
    def getPathToPOCDatabase(self):
        return self.loadSetting()['path']['poc_template']+"template_list.csv"


    def __init__(self):
        self.development_mode = True

global setting
setting = Setting()
