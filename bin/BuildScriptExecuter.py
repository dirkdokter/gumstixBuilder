from xml.dom.minidom import parseString
from SourceFetcher import SourceFetcher
import utils
import os
import errno


buildingBlockTypes = { 'generic'		: GenericBuildingBlock,
					   'linuxKernel'	: LinuxKernelBuildingBlock 
					 }


class BuildingBlock:
	def __init__(self, name, domContent, sourceFetcher):
		self.name = name
		self.domContent = domContent
		self.buildFolderName = None
		self.sourceFetcher = sourceFetcher
		
		dependencyDoms = domContent.getElementsByTagName('depends')
		for dependencyDom in dependencyDoms:
			sourceFetcher.fetch(dependencyDom.getAttribute('name'), dependencyDom.getAttribute('version'))
		
	def build(self):
		print "[ERROR] \t Build method missing."

class GenericBuildingBlock (BuildingBlock):
	def build(self):
		print "[ERROR] \t Build method missing."

class LinuxBuildingBlock (BuildingBlock):
	def build(self):
		linuxVersion = self.domContent.getElementsByTagName('version')[0];
				
		print "[ERROR] \t Build method missing."

	
class BuildScriptExecuter:
	def __init__(self, buildScriptFile,buildFolder,SRC_FOLDER):
		self.buildFolder = buildFolder
		self.buildingBlocks = {}
		#open the buildscript xml file
		file = open(buildScriptFile,'r')
		data = file.read()

		file.close()

		dom = parseString(data)

		sourceListDoms = dom.getElementsByTagName('sourceList')
		slPath = sourceListDoms[0].getAttribute('file')
		self.sourceFetcher = SourceFetcher(slPath,SRC_FOLDER);

		buildingBlockDoms = dom.getElementsByTagName('buildingBlock')
		for buildingBlockDom in buildingBlockDoms:
			bb = buildingBlockTypes[buildingBlockDom.getAttribute('name'),buildingBlockDom,self.sourceFetcher]
		self.buildingBlocks[bb.getAttribute('name')] = bb
			
	def startBuild(self,bbName):
		bb = self.buildingBlocks[bbName]
		bb.build()
