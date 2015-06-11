import fnmatch, os, re
import urllib2

sourceDirectory = "/home/didi/Projekte/wahlzeit/src"

# empirical list, based on the migration experience of wahlzeit
gaeSupportedPackages = ["com.google.appengine", "com.googlecode.objectify", "javax.servlet", 
	"org.apache.commons.fileupload", "org.apache.http", "com.google.common", "com.google.api", "javax.mail",]
packageName = "org.wahlzeit"

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

def isImportSupported(importLine):
	result = False
	for supportedPackage in gaeSupportedPackages:
		if supportedPackage in importLine:
			result = True
	if result == False and packageName in importLine:
		result = True
	return result


importPattern = re.compile("import .+;")
GAEJavaWhitelist = getGAEJavaWhitelist()
filesToAdjust = []
unsupportedPackages = []

for root, dirnames, filenames in os.walk(sourceDirectory):
	for filename in fnmatch.filter(filenames, '*.java'):
		path = os.path.join(root, filename)
		for line in open(path).readlines():
			for match in re.finditer(importPattern, line):
				if not isImportSupported(line): 
					lineSplit = line.split( )
					package = lineSplit[len(lineSplit)-1][:-1]
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
