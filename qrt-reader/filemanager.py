import os
from parameters import Parameters

class FileManager():

    def __init__(self):
        self.parameters = Parameters()

    def getSFCRPath(self, company, year):
        # later add logic for Azure / DB storage
        return "resources/SFCR Reports/" + self.parameters.FILENAME_MASKS[company] + " SFCR " + year + ".pdf"