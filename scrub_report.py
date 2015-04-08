"""
DESCRIPTION:
===============================
  A simple tool to parse all code within a directory and report back on what
  methods appear to not be called from within that code.

  Initially intended to be used for finding Python methods that not being
  called from within a project.

EXAMPLE PROGRAM:
===============================

import scrub_report
sr = scrub_report.ScrubReport('my_code_dir', ['py'], [])
files = sr.get_files()
methods = sr.get_methods(files)
called_by = sr.get_files_using_methods(files, methods)
not_called = sr.get_methods_not_called(called_by, methods)
print not_called

"""
import re

from os import walk

class ScrubReport(object):
  def __init__(self, filepath, keep, ignore):
    self.filepath = filepath
    self.keep = keep
    self.ignore = ignore
    return

  # build the initial list of files that match what we are looking for
  def get_files(self):
    all_files = []
    for (dirpath, dirnames, filenames) in walk(self.filepath):
      for file in filenames:
        file = '%s/%s' % (dirpath, file)
        all_files.append(file)

    files_found = []
    if len(self.ignore) != 0:
      # specifically listed what to ignore
      for file in all_files:
        keep_file = True
        for i in self.ignore:
          m = re.search(r'%s$' % i, file)
          if m:
            keep_file = False
        if keep_file:
          files_found.append(file)
    else:
      # specifically listed what to keep
      for file in all_files:
        keep_file = False
        for k in self.keep:
          m = re.search(r'%s$' % k, file)
          if m:
            keep_file = True
        if keep_file:
          files_found.append(file)

    return files_found

  # go through our list of files and look for method definitions
  def get_methods(self, files):
    methods = []
    for file in files:
      f = open(file, 'r')
      raw_data = f.read()
      for line in raw_data.split('\n'):
        m = re.search(r'def ([^(]+)', line)
        if m:
          method_name = m.group(1).strip()
          if method_name not in methods:
            methods.append(method_name)
    return methods

  # go through our files and look for calls of these methods
  def get_files_using_methods(self, files, methods):
    called_by = {}
    for file in files:
      f = open(file, 'r')
      raw_data = f.read()
      for line in raw_data.split('\n'):
        for method in methods:
          try:
            # check if the method is called
            m = re.search(r'%s' % method, line)
            # make sure it's not just the def of the method itself
            n = re.search(r'def %s' % method, line)
            if m and not n:
              # this file appears to call this method
              if method not in called_by.keys():
                called_by[method] = [file]
              else:
                if file not in called_by[method]:
                  called_by[method].append(file)
          except:
            pass
    return called_by

  def get_methods_not_called(self, called_by, methods):
    not_called = []
    for method in methods:
      if method not in called_by.keys():
        not_called.append(method)
    return not_called
