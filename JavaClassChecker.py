import fnmatch, os, re, urllib2, collections
from collections import defaultdict

sourceDirectory = "/home/didi/Projekte/legacyWahlzeit/MigrateWahlzeitIntoTheCloud/src/main/java"

packageName = "org.wahlzeit"

# empirical list, based on the migration experience of wahlzeit, 
# there are more for other projects
gaeSupportedPackages = ["com.google.common", "com.google.api", 
	"com.google.appengine", "com.googlecode.objectify", 
	"org.apache.commons.fileupload", "org.apache.http"]

blacklistPackages = ["java.sql"]

GAEWhitelistPath = "https://cloud.google.com/appengine/docs/java/jrewhitelist"

pathOffsetLen = len(sourceDirectory) + len(packageName) + 2

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


importPattern = re.compile("import .+;")
GAEJavaWhitelist = getGAEJavaWhitelist()
filesToAdjust = defaultdict(list)
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
						shortPath = path[pathOffsetLen:len(path)-len(".java")]
						filesToAdjust[shortPath].append(package)
						if package not in unsupportedPackages:
							unsupportedPackages.append(package)


print `len(unsupportedPackages)` + " diffent potentially unsupported imported classes:"
unsupportedPackages.sort()
for element in unsupportedPackages:
	print element

print "\n" + `len(filesToAdjust)` + " files to adjust:"
test = collections.OrderedDict(sorted(filesToAdjust.items(), key=lambda t: t[0]))
for k, v in test.items():
	print(k + ' includes ')
	for w in v:
		print("\t" + w)
