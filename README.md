#DESCRIPTION:
A simple tool to parse all code within a directory and report back on what
methods appear to not be called from within that code.

Initially intended to be used with .py files for finding Python methods that
not being called from within a project.

##NOTE:
This program makes no code changes or alterations and essentially operates in
read-only mode. It simply dumps a report to help you decide what to do in code.

###EXAMPLE PROGRAM:

import scrub_report
sr = scrub_report.ScrubReport('my_code_dir', ['py'], [])
files = sr.get_files()
methods = sr.get_methods(files)
called_by = sr.get_files_using_methods(files, methods)
not_called = sr.get_methods_not_called(called_by, methods)
print not_called

