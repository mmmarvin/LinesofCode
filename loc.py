################
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#     
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
################
import os
import sys
from enum import Enum

class RunMode(Enum):
	RMNone = -1
	RMExclude = 0
	RMFileType = 1
	RMLocation = 2

def print_help():
	print("Usage: python3 {0} [--location [...] --extension [...] [additional options]] [--help]\n\t--help - Prints the help command\n\t--exclude [...] - Excludes the following folders\n\t--extension [...] - File extensions to count lines from\n\t--location [...] - Location where to run program from".format(sys.argv[0]))
	
def calculate_line(filename):
	print("Counting lines of {0}...".format(filename))
	with open(filename, "r") as f:
		lines = f.readlines()
		return len(lines)
		
	return 0
		
def calculate_lines(fexcluded_folders, ffiletypes, path):
	number_of_lines = 0
	for root, dirs, filenames in os.walk(path):		
		for f in filenames:
			af = os.path.abspath(os.path.join(path, f))
			if os.path.isfile(af):
				f_ext = os.path.splitext(af)[1]
				for i in range(0, len(ffiletypes)):
					if ffiletypes[i] == f_ext:
						number_of_lines += calculate_line(af)
						break	
		for d in dirs:
			ad = os.path.abspath(os.path.join(path, d))
			if os.path.isdir(ad):
				skip = False
				for i in range(0, len(fexcluded_folders)):
					if fexcluded_folders[i] == ad:
						skip = True
						break
				
				if not skip:
					number_of_lines += calculate_lines(fexcluded_folders, ffiletypes, ad)
					
	return number_of_lines
						
def run_program(excluded_folders, filetypes, location):
	fexcluded_folders = []
	ffiletypes = []
	for i in range(0, len(excluded_folders)):
		fexcluded_folders.append(os.path.abspath(os.path.join(location, excluded_folders[i])))
		
	for i in range(0, len(fexcluded_folders)):
		print("Excluding {0}...".format(fexcluded_folders[i]))
				
	number_of_lines = calculate_lines(fexcluded_folders, filetypes, os.path.abspath(location))
	print("Number of lines: ", number_of_lines)
	
def main():
	if len(sys.argv) == 2 and sys.argv[1] == "--help":
		print_help()
		return 0
		
	excluded_folders = []
	filetypes = []
	location = "."
	current_tag: RunMode = RunMode.RMNone
	for i in range(1, len(sys.argv)):
		param = sys.argv[i]
		if param == "--exclude":
			current_tag = RunMode.RMExclude
		elif param == "--extension":
			current_tag = RunMode.RMFileType
		elif param == "--location":
			current_tag = RunMode.RMLocation
		else:
			if len(param) > 2:
				if param[0] == '-' and param[1] == '-':
					if param == "--help":
						print("Invalid usage of '--help'")
						print_help()
						return -1
					else:
						print("Invalid parameter '{0}'".format(param))
						return -1
			
			if current_tag == RunMode.RMExclude:
				excluded_folders.append(param)
			elif current_tag == RunMode.RMFileType:
				filetypes.append(param)
			elif current_tag == RunMode.RMLocation:
				location = param
			else:
				print("Invalid parameter '{0}'".format(param))
				print_help()
				return -1
	
	if len(filetypes) == 0:
		print("Invalid usage")
		print_help()
		
	run_program(excluded_folders, filetypes, location)
	
	return 0

if __name__ == "__main__":
	main()
