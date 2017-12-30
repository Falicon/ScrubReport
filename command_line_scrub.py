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

  scrub_report.py pubgears 'py,js' true
    -- would look through all .py and .js files within the pubgears directory
      (and sub directories)

  scrub_report.py pubgears '' true html,less
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

check_methods = False
if (len(sys.argv) > 3 and sys.argv[3] != ""):
  if sys.argv[3] != 'false':
    check_methods = True

ignore = []
if (len(sys.argv) > 4 and sys.argv[4] != ""):
  # use the provided keep list
  ignore = [x.strip() for x in sys.argv[4].split(',')]

sr = scrub_report.ScrubReport(filepath, keep, ignore)
files = sr.get_files()

code_details = sr.count_lines_of_code(files)

if check_methods:
  methods = sr.get_methods(files)
  called_by = sr.get_files_using_methods(files, methods)
  not_called = sr.get_methods_not_called(called_by, methods)

print "Basic code breakdown"
print "====================================================================="
print "%s files" % len(files)
print "%s lines of code" % code_details['code']
print "%s comments" % code_details['comments']
print
print "====================================================================="
print
print "The following methods are not directly called by code in the project:"
print "====================================================================="
# for nc in not_called:
#   print " - %s" % nc
