'''
Created on 19/ago/2011

@author: Marco
'''

class DigitalModel(object):
    '''
    Digital representation of a model, a set of rune tags
    and their position
    '''

    def __init__(self, name, tagNames, tagPositions, tagSizes, tagDefaultSizes):
        '''
        Constructor
        '''
        self.name = name
        self.tagPositions = tagPositions
        self.tagNames = tagNames
        self.tagSizes = tagSizes
        self.tagDefaultSizes = tagDefaultSizes