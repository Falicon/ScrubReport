"""
DESCRIPTION:
===============================
  A command line interface to the scrub_report class/tool.

PROGRAM USE:
===============================
  scrub_report.py directory_to_analyze \
    comma_seperated_list_of_file_types_to_analyze

EXAMPLES:
===============================
  scrub_report.py pubgears py
    -- would look through all .py files within the pubgears directory 
       (and sub directories)

  scrub_report.py pubgears 'py,js'
    -- would look through all .py and .js files within the pubgears directory
      (and sub directories)

  scrub_report.py pubgears '' html,less
    -- would look through all files within the pubgears directory (and sub 
       directories) that were not .html or .less
"""

import sys
import scrub_report

filepath = ''
if (len(sys.argv) > 1 and sys.argv[1] != ""):
  # use the provided path
  filepath = sys.argv[1]

keep = []
if (len(sys.argv) > 2 and sys.argv[2] != ""):
  # use the provided keep list
  keep = [x.strip() for x in sys.argv[2].split(',')]

ignore = []
if (len(sys.argv) > 3 and sys.argv[3] != ""):
  # use the provided keep list
  ignore = [x.strip() for x in sys.argv[3].split(',')]

sr = scrub_report.ScrubReport(filepath, keep, ignore)
files = sr.get_files()
methods = sr.get_methods(files)
called_by = sr.get_files_using_methods(files, methods)
not_called = sr.get_methods_not_called(called_by, methods)

print "The following methods are not directly called by code in the project:"
print "====================================================================="
for nc in not_called:
  print " - %s" % nc