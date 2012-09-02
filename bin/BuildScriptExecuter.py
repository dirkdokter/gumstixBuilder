from xml.dom.minidom import parseString
from SourceFetcher import SourceFetcher
import utils
import os
import errno


class BuildingBlock:
	def __init__(self, name):
		self.name = name
		self.buildFolderName = None
	def build(self):
		print "[ERROR] \t Build method missing."
	
class BuildScriptExecuter:
	def __init__(self, buildScriptFile,buildFolder):
		self.buildFolder = buildFolder
		self.buildingBlocks = {}
		#open the buildscript xml file
		file = open(buildScriptFile,'r')
		data = file.read()

		file.close()

		dom = parseString(data)

		requirements = dom.getElementsByTagName('requirement')
		for requirement in requirements:
			r = Requirement(requirement.getAttribute('name'))
			srcs = requirement.getElementsByTagName('src')
			for src in srcs:
				type = src.getAttribute('type')
				s = fileTypeHandlers[type](r.name,src.getAttribute('version'),src.getAttribute('url'))
				r.sources[src.getAttribute('version')] = s
			self.requirementList[requirement.getAttribute('name')] = r

		print self.requirementList

	def fetch(self,requirementName,version):
		r = self.requirementList[requirementName]
		s = r.sources[version]
		#targetFolder = "%s/%s_v%s" % (self.rawSourcesFolder,requirementName, version)
		
		#s.fetchFile();
		s.fetch(self.rawSourcesFolder);
