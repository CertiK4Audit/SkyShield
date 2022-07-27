import fnmatch
import os
import re

def findFiles(keyword, path='.'):

    rule = re.compile(fnmatch.translate("*"+keyword+"*"), re.IGNORECASE)
    return [file for file in os.listdir(path) if rule.match(file)]

def findFilesRecusive(keyword, path='.'):
    matchedFiles = []
    rule = re.compile(fnmatch.translate("*"+keyword+"*"), re.IGNORECASE)
    for root, dir, files in os.walk(path):
        for file in files:
            if rule.match(file):
                matchedFiles.append(root+"/"+file)
    return matchedFiles