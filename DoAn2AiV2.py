# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 11:21:28 2021

@author: DELL
"""

import os
import itertools

INPUT_DIR = 'D:/inputAI2/'
OUTPUT_DIR = 'D:/outputAI2/'

class NormHelper:
    def __init__(self):
        return
        
    def checkComplementary(self,clauseList):
        clauseListChecked=[]
        for clause in clauseList:
            check=True
            negativeAtoms = self.convertAtomsToNegative(clause)
            for atom in negativeAtoms:
                if atom in clause:
                    check=False
                    break
            if(check==True):
                clauseListChecked.append(clause)
        return clauseListChecked
    
 
    
    def convertAtomsToNegative(self,clause):
        negativeAtoms=[]
        for atom in clause:
            if(atom[0]=='-'):
                negativeAtoms.append(atom[1:]) 
            else: 
                negativeAtoms.append('-'+atom)
        return negativeAtoms
    
    def convertAtomToNegative(self, atom):
        if(atom[0]=='-'):
            return atom[1:] 
        else: 
            return '-'+atom
    
    def convertClauseToNegative(self,clause):
        negativeClause=[]
        negativeAtoms = self.convertAtomsToNegative(clause)
        for atom in negativeAtoms:
            negativeClause.append([atom])
        return  negativeClause
    
    def combinationOfClauses(self, clauses):
        return list(itertools.combinations(clauses, 2))
    
    def removeDuplicate(self, clause):
        return list(dict.fromkeys(clause))
        

    
    def checkComplementaryTwoAtom(self,atom1, atom2):
        if atom1==self.convertAtomToNegative(atom2) or atom2==self.convertAtomToNegative(atom1):
            return False
        return True
    def checkComplementaryClause(self, clause):
        check=True
        negativeAtoms = self.convertAtomsToNegative(clause)
        for atom in negativeAtoms:
            if atom in clause:
                check=False
                break
        return check
                
    def reverseAtom(self,atom):
        return atom[::-1]
    
    def sort(self,clause):
        return sorted(clause,key=self.reverseAtom)
        
        
    

class Input:
    def __init__(self,alpha,num,KB):
        self.normHelper = NormHelper()
        self.alpha=self.preFixAlpha(alpha)
        self.num=num
        self.KB= self.preFixKB(KB)
    
    def KBConverter(self, kb):
        kbConverted =[]
        for clause in kb:
            clause=clause.split()
            clauseConverted = filter(lambda x: x!="OR", clause)
            kbConverted.append(list(clauseConverted))
        return kbConverted
    
    def preFixKB(self, kb):
        #Remove OR
        kb = self.KBConverter(kb)
        #Remove duplicate
        kb = [ list(x) for x in set(tuple(x) for x in kb) ]
        #remove not complementary clause
        kb = self.normHelper.checkComplementary(kb)
        return kb
    
    def preFixAlpha(self,alpha):
        alpha=alpha.split()
        #Remove OR
        alphaFixed = filter(lambda x: x!="OR", alpha)
        return list(alphaFixed)

class Output:
    def __init__(self,):
        self.answer=None 
        self.numberClause=[]
        self.clausesList=[]
    def setLoop(self, numberClause, clausesList):
        self.numberClause.append(numberClause)
        self.clausesList.append(clausesList)
    def setAnswer(self,answer):
        self.answer=answer
    def writeOutput(self,fileName):
        fileOutput = open(fileName,'w+')
        for i in range(len(self.numberClause)):
            fileOutput.write(str(self.numberClause[i])+'\n')
            for clause in self.clausesList[i]:
                for i in range(len(clause)-1):
                    fileOutput.write(str(clause[i])+' OR ')
                fileOutput.write(str(clause[-1])+'\n')
        if self.answer==True:
            fileOutput.write('YES')
        else:
            fileOutput.write('NO')
        
        
    
class PL_Resolution:
    def __init__(self, alpha, kb):
        self.normHelper= NormHelper()
        self.outputHelper = Output()
        self.alpha=alpha
        self.kb=kb

    def createKBandNotAlpha(self,alpha,kb):
        negativeAlpha = self.normHelper.convertClauseToNegative(alpha)
        clausesSorted=[]
        for clause in kb + negativeAlpha:
            clausesSorted.append(self.normHelper.sort(clause))
        return clausesSorted
    
    def resolve(self, Ci, Cj, clausesBase):
        resolvents=[]
        for i in range(len(Ci)):
            for j in range(len(Cj)):
                if(self.normHelper.checkComplementaryTwoAtom(Ci[i], Cj[j])==False):
                    clause=Ci[:i]+Ci[i+1:]+Cj[:j]+Cj[j+1:]
                    if not clause:
                        resolvents.append(['{}'])
                    else:
                        clause=self.normHelper.sort(clause)
                        clause=self.normHelper.removeDuplicate(clause)
                        if self.normHelper.checkComplementaryClause(clause)==True and clause not in clausesBase:
                            resolvents.append(clause)
        return resolvents
    
    def checkStop(self,new, clauses):
        check=True
        for item in new:
            if item not in clauses and item != ['{}']:
                check =False
                break
        return check        
        
    def solve(self):
        clauses= self.createKBandNotAlpha(self.alpha,self.kb)
        
        new=[]
        while True:
            resolvents = []
            clausePairs = self.normHelper.combinationOfClauses(clauses)
            for pair in clausePairs:
                resolvent = self.resolve(pair[0],pair[1],clauses)
                if resolvent and resolvent[0] not in resolvents:
                    resolvents.extend(resolvent)
            self.outputHelper.setLoop(len(resolvents), resolvents)
            print("--------------------------------------------")
            new=new+[iteral for iteral in resolvents if iteral not in new]
            if ['{}'] in resolvents:
                self.outputHelper.setAnswer(True)
                return self.outputHelper
            if self.checkStop(new, clauses):
                self.outputHelper.setAnswer(False)
                return self.outputHelper
            clauses=clauses+[iteral for iteral in new if iteral not in clauses]
            

                    

    
    
    
def readFile(fileName):
    fileInput=open(fileName,'r')
    lines=fileInput.readlines()
    numKB=int(lines[1])
    KB=[]
    for i in range(0,numKB):
        KB.append(lines[2+i])
    input = Input(lines[0],lines[1],KB)
    return input


    
    

inputFiles = [file for file in os.listdir(INPUT_DIR) if os.path.isfile(os.path.join(INPUT_DIR, file))]
ouputFilea = []
index=0
for fileName in inputFiles:
    index+=1
    inputFile = readFile(os.path.join(INPUT_DIR, fileName))
    m=PL_Resolution(inputFile.alpha, inputFile.KB).solve()
    m.writeOutput(os.path.join(OUTPUT_DIR,'output'+str(index)+'.txt'))





    

   