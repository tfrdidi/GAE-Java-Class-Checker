import fnmatch, os, re
import urllib2

sourceDirectory = "wahlzeit"

def getGAEJavaWhitelist():
	packageLinePattern = re.compile("<li>[a-z|A-Z|\.]+</li>")
	response = urllib2.urlopen("https://cloud.google.com/appengine/docs/java/jrewhitelist")
	GAEJavaWhitelistPageSource = response.read()
	packageLines = re.findall(packageLinePattern, GAEJavaWhitelistPageSource)
	GAEJavaWhitelist = []
	for packageLine in packageLines:
		GAEJavaWhitelist.append(packageLine[4:-5])
	return GAEJavaWhitelist

def printArrayLinewise(array):
	for element in array:
		print element


importPattern = re.compile("import .+;")
GAEJavaWhitelist = getGAEJavaWhitelist()
filesToAdjust = []
unsupportedPackages = []

for root, dirnames, filenames in os.walk(sourceDirectory):
	for filename in fnmatch.filter(filenames, '*.java'):
		path = os.path.join(root, filename)
		for line in open(path).readlines():
			for match in re.finditer(importPattern, line):
				if not sourceDirectory in line: 
					package = line.split( )[1][:-1]
					if package not in GAEJavaWhitelist:
						if path not in filesToAdjust:
							filesToAdjust.append(path)
						if package not in unsupportedPackages:
							unsupportedPackages.append(package)


# print result
print "potentially unsupported imports:"
unsupportedPackages.sort()
printArrayLinewise(unsupportedPackages)

print "\nfiles to adjust:"
filesToAdjust.sort()
printArrayLinewise(filesToAdjust)
