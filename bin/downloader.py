import urllib2

def httpGetFileSize(url):
	u = urllib2.urlopen(url)
	meta = u.info()
	fileSize = int(meta.getheaders("Content-Length")[0])
	return fileSize


def httpFetch(targetFileName,url):
	u = urllib2.urlopen(url)
	if type(targetFileName) == type(None):
		raise Exception('TagetFileName for this download is not specified.')
	f = open(targetFileName, 'wb')
	meta = u.info()
	fileSize = int(meta.getheaders("Content-Length")[0])
	print "Downloading %s Size: %s kB" % (targetFileName, fileSize/1000)

	numBytesFetched = 0
	blockSize = 8192
	while True:
		downloadBuffer = u.read(blockSize)
		if not downloadBuffer:
			break
		
		numBytesFetched += len(downloadBuffer)
		f.write(downloadBuffer)
		status = r"%10d kB  [%3.2f%%]" % (numBytesFetched/1000, numBytesFetched * 100. / fileSize)
		status = status + chr(8)*(len(status)+1)
		print status,

	f.close()
