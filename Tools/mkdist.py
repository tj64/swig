#!/usr/local/bin/python

# This script builds a swig-1.3 distribution.
# Usage : mkdist.py version, where version should be 1.3.x

import sys
import string
import os

def failed():
  print "Failed to complete"
  sys.exit(1)


try:
   version = sys.argv[1]
   dirname = "swig-" + version
except:
   print "Usage: mkdist.py version, where version should be 1.3.x"
   sys.exit(0)

# Check name matches normal unix conventions
if string.lower(dirname) != dirname:
  print "directory name ("+dirname+") should be in lowercase"
  sys.exit(2)

# If directory and tarball exist, remove it
print "Removing ", dirname
os.system("rm -rf "+dirname)

print "Removing "+dirname+".tar if exists"
os.system("rm -f "+dirname+".tar.gz")

print "Removing "+dirname+".tar.gz if exists"
os.system("rm -f "+dirname+".tar")

# Do a SVN export into the directory name

print "Grabbing latest SWIG from svn"
os.system("svn export -r HEAD https://swig.svn.sourceforge.net/svnroot/swig/trunk "+dirname) == 0 or failed()

# Remove the debian directory -- it's not official

os.system("rm -Rf "+dirname+"/debian") == 0 or failed()

# Blow away all .cvsignore files

print "Blowing away .cvsignore files"
os.system("find "+dirname+" -name .cvsignore -exec rm {} \\;") == 0 or failed()

# Go build the system

print "Building system"
os.system("cd "+dirname+"; ./autogen.sh") == 0 or failed()
os.system("cd "+dirname+"/Tools/WAD; autoconf") == 0 or failed()
os.system("cd "+dirname+"/Source/CParse; bison -y -d parser.y; mv y.tab.c parser.c; mv y.tab.h parser.h") == 0 or failed()
os.system("cd "+dirname+"; make -f Makefile.in libfiles srcdir=./") == 0 or failed()

# Remove autoconf files
os.system("find "+dirname+" -name autom4te.cache -exec rm -rf {} \\;")

# Build documentation
print "Building documentation"
os.system("cd "+dirname+"/Doc/Manual && make && rm *.bak") == 0 or failed()

# Build the tar-ball
os.system("tar -cf "+dirname+".tar "+dirname) == 0 or failed()
os.system("gzip "+dirname+".tar") == 0 or failed()
