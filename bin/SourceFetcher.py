from xml.dom.minidom import parseString
import downloader
import tarfile
import utils
import os
import errno


class Requirement:
	def __init__(self, name):
		self.name = name
		self.sources = {}

class Source:
	def __init__(self, name, version, url):
		self.name = name
		self.version = version
		self.url = url
		self.targetFileName   = None
		self.targetFolderName = None
		self.redownloadedSource = False
	def fetch(self):
		print "[ERROR] \t Fetch method of this source is undefined."
		
class TarballSource (Source):
	def fetch(self,SRC_FOLDER):
		self.targetFileName   = "%s/%s_%s.tar" % (SRC_FOLDER,self.name,self.version)
		self.targetFolderName = "%s/%s_%s/"    % (SRC_FOLDER,self.name,self.version)
		self.fetchFile()
		self.extract()
	def fetchFile(self):
		try:
			localFileSize = os.path.getsize(self.targetFileName)
			remoteFileSize = downloader.httpGetFileSize(self.url)
			if localFileSize == remoteFileSize:
				print "[INFO] \t File [%s] is same size as file on server. Skipping download. Remove the file if you want to re-download it." % self.targetFileName
			else:
				print "[INFO] \t File [%s] already exists locally, but has a different size than on the server. I will remove the file and re-download it." % self.targetFileName
				os.remove(self.targetFileName)
				self.redownloadedSource = True
				downloader.httpFetch(self.targetFileName,self.url)
		except os.error:
			print "[INFO] \t File [%s] does not exist locally yet. Proceeding with download." % self.targetFileName
			self.redownloadedSource = True
			downloader.httpFetch(self.targetFileName,self.url)

	def extract(self):
		try:
			os.makedirs(self.targetFolderName)
			print "[INFO] \t Extracting to [%s]" % self.targetFolderName
			tf = tarfile.open(self.targetFileName)
			tarMembers = tf.getmembers()
			for tm in tarMembers:
				tm._extract_memeber(tm,)
			tf.extractall(self.targetFolderName,[tf.getmembers()[0]])
			tf.close()
		except OSError, e:
			if e.errno == errno.EEXIST:
				print "[INFO] \t Folder [%s] already exists. Skipping extraction." % self.targetFolderName
			else:
				raise

class TarballGzSource (TarballSource):
	def fetch(self,SRC_FOLDER):
		self.targetFileName   = "%s/%s_%s.tar.gz" % (SRC_FOLDER,self.name,self.version)
		self.targetFolderName = "%s/%s_%s/"       % (SRC_FOLDER,self.name,self.version)
		self.fetchFile()
		self.extract()
	
class TarballBzSource (TarballSource):
	def fetch(self,SRC_FOLDER):
		self.targetFileName   = "%s/%s_%s.tar.bz2" % (SRC_FOLDER,self.name,self.version)
		self.targetFolderName = "%s/%s_%s/"        % (SRC_FOLDER,self.name,self.version)
		self.fetchFile()
		self.extract()


fileTypeHandlers = { 'tarball'		: TarballSource,
					 'tarballGz' 	: TarballGzSource,
					 'tarballBz2' 	: TarballBzSource}
	
class SourceFetcher:
	def __init__(self, sourceListFile,rawSourcesFolder):
		self.rawSourcesFolder = rawSourcesFolder
		self.requirementList = {}
		#open the sourceList xml file
		file = open(sourceListFile,'r')
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
