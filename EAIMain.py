#!/usr/bin/python3

import random #random functions
import math #math functions
import time #time functions

#class to handle getting lists out of files
class fileListExtractor():

	#get a list from a file
	def getListFromFile(self,fileName):
		listFile = open(fileName,"r")
		listContent = listFile.readlines()
		listFile.close()
		return listContent

	def addStringListToDictionary(self,fileName,dictionaryObject):
		collectionList = self.getListFromFile(fileName)
		for listNumber in range(len(collectionList)):
			dictionaryObject[collectionList[listNumber].rstrip()] = collectionList[listNumber].rstrip()

	def addCharacterListToDictionary(self,fileName,dictionaryObject,universeObject):
		collectionList = self.getListFromFile(fileName)
		for listNumber in range(len(collectionList)):
			dictionaryObject[collectionList[listNumber].rstrip()] = universeObject.characterCollection[collectionList[listNumber].rstrip()]

#class for characters
class character():
	
	#set the owner universe and populate this character with stats from file
	def __init__(self,characterDetails,ownerUniverse,listExtractTool):
		self.fileListTool = listExtractTool
		self.ownerUniverse = ownerUniverse
		characterInitialDetails = characterDetails.split(',')
		self.characterName = characterInitialDetails[0]
		self.disposition = int(characterInitialDetails[1])
		self.inPreferences = {
			"Mechanical": { "Angry":int(characterInitialDetails[2]),
					"Sad":int(characterInitialDetails[3]),
					"Confused":int(characterInitialDetails[4]),
					"Neutral":int(characterInitialDetails[5]),
					"Inquisitive":int(characterInitialDetails[6]),
					"Happy":int(characterInitialDetails[7]),
					"Excited":int(characterInitialDetails[8])},
			"Verbal": { "Angry":int(characterInitialDetails[9]),
					"Sad":int(characterInitialDetails[10]),
					"Confused":int(characterInitialDetails[11]),
					"Neutral":int(characterInitialDetails[12]),
					"Inquisitive":int(characterInitialDetails[13]),
					"Happy":int(characterInitialDetails[14]),
					"Excited":int(characterInitialDetails[15]) },
		}
		self.targetName = "NONE"
		self.outputType = "Verbal"
		self.perceptions = {}

	#get the label for the current disposition number
	def getDispositionString(self):
		dispositionTypes = ["Angry","Sad","Confused","Neutral","Inquisitive","Happy","Excited"]
		dispositionLabel = "Neutral"
		for dispositionIteration in range(len(dispositionTypes)):
			if(self.disposition >= -10 + (3*dispositionIteration) and self.disposition <= -7 + (3*dispositionIteration)):
				dispositionLabel = dispositionTypes[dispositionIteration]
		return dispositionLabel

	#get the current disposition number
	def getDispositionNumber(self):
		return self.disposition

	#get the character that this character is currently focusing on, if any
	def getTargetName(self):
		return self.targetName

	#get the type of output this character is emitting
	def getOutputType(self):
		return self.outputType

	#generate an output based on self conditions
	def output(self):
		self.outputType = "Verbal"
		randomPickChance = random.randint(0,30)
		if(randomPickChance == 0): #visual and audio communication occur easier than mechanical actions
			self.outputType = "Mechanical"
		chosenCharacter = self.targetName
		taggingCharacters = ""
		allCharacters = self.ownerUniverse.getAllCharacters()
		for characterNumber in range(len(allCharacters)):#pick random character to message or find characters tagging this one
			randomPickChance = random.randint(0,100)	
			if(randomPickChance == 0):
				chosenCharacter = allCharacters[characterNumber][0]
			if(allCharacters[characterNumber][1].getTargetName() == self.characterName):
				if(taggingCharacters != ""):
					taggingCharacters = taggingCharacters + ","
				taggingCharacters = taggingCharacters + allCharacters[characterNumber][0]
		if(taggingCharacters != ""): # pick from tagging character overwrites random
			taggingCharacterList = taggingCharacters.split(',')
			chosenCharacter = random.choice(taggingCharacterList)
		randomPickChance = random.randint(0,3)
		if(chosenCharacter == self.characterName or randomPickChance == 0):#randomly give up on a long standing exchange or emit targetless if looking at self
			chosenCharacter = "NONE"
		self.targetName = chosenCharacter
		if(chosenCharacter == "NONE"):
			print(self.characterName + " >> " + self.getDispositionString() + " >> " + self.getOutputType())
		else:	
			targetObject = self.ownerUniverse.getCharacterByName(chosenCharacter)
			targetDisposition = targetObject.getDispositionString()
			targetOutputType = targetObject.getOutputType()
			print(self.characterName + " << " + targetOutputType + " << " + targetDisposition + " << " + chosenCharacter)
			targetPerception = 0 #start the perception of new characters from a neutral perception
			if(chosenCharacter in self.perceptions):
				targetPerception = self.perceptions[chosenCharacter]
			self.perceptions[chosenCharacter] = targetPerception + self.inPreferences[targetOutputType][targetDisposition] #add or change perception of character based on their input
			if(self.perceptions[chosenCharacter] > 100):
				self.perceptions[chosenCharacter] = 100
			elif(self.perceptions[chosenCharacter] < -100):
				self.perceptions[chosenCharacter] = -100
			if(self.perceptions[chosenCharacter] != targetPerception):
				print(self.characterName + " >> " + chosenCharacter + " >> perception: " + str(targetPerception) + " >> perception: " + str(self.perceptions[chosenCharacter]))
			self.inPreferences[targetOutputType][targetDisposition] = self.inPreferences[targetOutputType][targetDisposition] + self.perceptions[chosenCharacter]#update perception of action from this encounter
			if(self.inPreferences[targetOutputType][targetDisposition] > 100):
				self.inPreferences[targetOutputType][targetDisposition] = 100
			if(self.inPreferences[targetOutputType][targetDisposition] < -100):
				self.inPreferences[targetOutputType][targetDisposition] = -100
			oldDisposition = self.getDispositionString()			
			dispositionChange = self.perceptions[chosenCharacter]	
			if(dispositionChange > 2):
				dispositionChange = random.randint(1,2)
			elif(dispositionChange < -2):
				dispositionChange = -random.randint(1,2)
			newDisposition = self.disposition + dispositionChange
			if(newDisposition > 10):
				newDisposition = 10
			elif(newDisposition < -10):
				newDisposition = -10
			self.disposition = newDisposition #change how this character feels using a capped version of the perception of the interacting character
			if(self.getDispositionString() != oldDisposition):
				print(self.characterName + " >> " + oldDisposition + " >> " + self.getDispositionString())
			print(self.characterName + " >> " + self.getDispositionString() + " >> " + self.getOutputType() + " >> " + chosenCharacter)

#class for the universe containing characters	
class universe():

	#populate the universe with characters
	def __init__(self):
		self.characterCollection = {}
		self.currentCharacter = 0
		self.fileListTool = fileListExtractor()
		charactersList = self.fileListTool.getListFromFile("characterList.txt")
		for characterNumber in range(1,len(charactersList)):
			self.characterCollection[charactersList[characterNumber].rstrip().split(',')[0]] = character(charactersList[characterNumber].rstrip(),self,self.fileListTool)

	#return all characters as a list
	def getAllCharacters(self):
		return list(self.characterCollection.items())

	#get a character by their name
	def getCharacterByName(self,characterName):
		return self.characterCollection[characterName]

	#return the next character from the last
	def getNextCharacter(self):
		nextCharacter = list(self.characterCollection.items())[self.currentCharacter][1]
		self.currentCharacter += 1
		if(self.currentCharacter >= len(list(self.characterCollection.items()))):
			self.currentCharacter = 0
		return nextCharacter

	#return a random character
	def getRandomCharacter(self):
		return random.choice(list(self.characterCollection.items()))[1]

	#select a random character and make them interact
	def simulateCharacters(self):
		self.getNextCharacter().output()

#main function
def main():
	random.seed(time.time())
	mainUniverse = universe()
	while True:
		time.sleep(0.1)
		mainUniverse.simulateCharacters()

#checks for main so that this code can either be run solo or in addition to other code without interfering
if __name__ == "__main__":
    main()

