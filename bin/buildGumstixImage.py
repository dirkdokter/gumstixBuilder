from SourceFetcher import SourceFetcher 

SRC_FOLDER = "/home/dirk/nonSynced/gumstixBuilder/sources/"
BUILD_FOLDER = "/home/dirk/nonSynced/gumstixBuilder/build/"

sourceFetcher = SourceFetcher('config/sources.xml',SRC_FOLDER);

sourceFetcher.fetch("linuxKernel", "3.5")
