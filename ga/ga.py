"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    File: GUI_Application.py
    
    Purpose:  Contains required code for GUI.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""


from ga.pystsup.utilities import (parseFile, getPath, createExperimentsFromRealData,createExperiments,
readFile,parseConfigFile,strToOp,saveExpResults,updateConfigFile, calcFitnessCache, getData, writeFrontier)
from ga.pystsup.data import Solution, Student, Supervisor, BipartiteGraph
from ga.pystsup.evolutionary import GeneticAlgorithm

import os
    
        
def startRUN(students,supervisors):

    #Creating Fitness Cache and RankWeights
    print("Creating the fitness cache..")
    
    rankWeights = Solution.calcRankWeights()
    fitnessCache = calcFitnessCache(students,supervisors,rankWeights)
    

    #Setting up the parameters

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = os.path.join(BASE_DIR, 'ga/configGA.json')

    print("Parsing the GA Config file..")

    gen,size,crOp,muOp,selOp,muProb,swProb,trProb = parseConfigFile(config)
        
    geneticAlgorithm = GeneticAlgorithm(students,supervisors,fitnessCache,rankWeights,muOp,crOp,selOp)

    #Running the GA

    print("Starting GA Run..")
    
    metricData,front = geneticAlgorithm.start(size,gen,muProb,swProb,trProb)
    

    return front,metricData

    
def saveAs(self):

    filename = "Result"
    self.outputName = filename
    self.label_3['text']= filename + ".xlsx"
    
    
def runGA(stuFile, supFile, keywordsFile):
  

    #Getting the Data
    if stuFile != None or supFile!=None  or keywordsFile!=None:
                
        print("Getting the input data from excel files..")
        students,supervisors = getData(stuFile, supFile, keywordsFile=keywordsFile)     

        
        non_dominated_solutions,metricData = startRUN(students,supervisors)

        print("Saving the results..")
        writeFrontier("Result",non_dominated_solutions,metricData,supervisors,students)

        filename = "Result.xlsx"

        print("Success","Genetic Algoritm Evolution completed. The results have been saved in "+filename+".")
            
    else:
        print("Error", "Input files not provided. Please select appropriate student and supervisor data files.")
        

def updateConfig(self):
    updateConfigFile("configGA.json",int(self.entry1.get()),int(self.entry2.get()),float(self.entry3.get()),float(self.entry4.get()),float(self.entry5.get()))
    print("Success","Genetic Algorithm Parameters have been sucessfully updated.")
    self.top1.destroy()

    
