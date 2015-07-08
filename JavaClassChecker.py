import fnmatch, os, re, urllib2

sourceDirectory = "/home/didi/Projekte/legacyWahlzeit/MigrateWahlzeitIntoTheCloud/src/main/java"

packageName = "org.wahlzeit"

# empirical list, based on the migration experience of wahlzeit, 
# there are more for other projects
gaeSupportedPackages = ["com.google.common", "com.google.api", 
	"com.google.appengine", "com.googlecode.objectify", 
	"org.apache.commons.fileupload", "org.apache.http"]

blacklistPackages = ["java.sql"]

GAEWhitelistPath = 
	"https://cloud.google.com/appengine/docs/java/jrewhitelist"

pathOffsetLen = len(sourceDirectory)+len(packageName)+2

def getGAEJavaWhitelist():
	packageLinePattern = re.compile("<li>[a-z|A-Z|\.]+</li>")
	response = urllib2.urlopen(GAEWhitelistPath)
	pageSource = response.read()
	packageLines = re.findall(packageLinePattern, pageSource)
	GAEJavaWhitelist = []
	for packageLine in packageLines:
		newClass = packageLine[4:-5]
		appendNewClass = True
		for blacklistPackage in blacklistPackages:
			if blacklistPackage in newClass:
				appendNewClass = False
		if appendNewClass:
			GAEJavaWhitelist.append(newClass)
	return GAEJavaWhitelist

def isImportSupported(importLine):
	result = False
	for supportedPackage in gaeSupportedPackages:
		if supportedPackage in importLine:
			result = True
	if result == False and packageName in importLine:
		result = True
	return result

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
				if not isImportSupported(line): 
					lineSplit = line.split( )
					package = lineSplit[len(lineSplit)-1][:-1]
					if package not in GAEJavaWhitelist:
						shortPath = path[pathOffsetLen:]
						if shortPath not in filesToAdjust:
							filesToAdjust.append(shortPath)
						if package not in unsupportedPackages:
							unsupportedPackages.append(package)


# print result
print "potentially unsupported imports:"
unsupportedPackages.sort()
printArrayLinewise(unsupportedPackages)

print "\nfiles to adjust:"
filesToAdjust.sort()
printArrayLinewise(filesToAdjust)
