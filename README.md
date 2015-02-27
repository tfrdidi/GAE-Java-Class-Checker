# GAE-Java-Class-Checker
========================

A small script to help you migrating a Java application to Google App Engine (GAE). It scans your Java source files and searches for Java packages that are not supported by GAE.

--------------------

GAE does not support all classes of the Java SDK (see https://cloud.google.com/appengine/docs/java/jrewhitelist) hence it may be possible that your Java project uses Java classes that are not supported by Google App Engine.

This python skript downloads the whitelist of supported Java packages of GAE and searches for the packages your Java project uses. As a result you get all packages that are not supported by GAE and a list of files containing the imports of those packages. This may also include packages of third party libraries, that you can use in GAE. In this case ignore the corresponding packages in the result.


Usage
-----

* Download the JavaClassChecker.py
* edit the `sourceDirectory = "your source folder"`, e.g. `sourceDirectory = "/home/user/projects/GAE-Java-Class-Checker"` 
* save the script
* execute the script with `python JavaClassChecker.py`

It may take some seconds, because the whitelist is always loaded from the internet, hence you need an internet connection but are always up to date.