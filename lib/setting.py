import yaml
class Setting:
    path_to_database = None
    development_mode = False
    
    def __init__(self):
        with open('setting.yml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            #print(data)
            self.path_to_database = data['path']['database']
