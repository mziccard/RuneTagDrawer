'''
Created on 29/lug/2011

@author: Marco
'''
class ConfigReader(object):
    '''
    Singleton configuration class
    '''
    
    def __init__(self):
        config_file = open("RuneTagNames","r")
        text = config_file.read()
        config_file.close()
        runeTagInfos = text.split("\n")
        self.RuneTagNames = []
        self.RuneTagSize = []

        for info in runeTagInfos:
            values = info.split("_")
            if values[0] != "":
                self.RuneTagNames.append(values[0])
                self.RuneTagSize.append(float(values[1]))
        