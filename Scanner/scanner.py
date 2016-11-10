########################################################
# PROJECT              : SCANNER
# COURSE               : CSC 512 - COMPILER CONSTRUCTION
# AUTHOR               : ZUBIN THAMPI 
# STUDENT ID           : 200131461
# UNITY ID             : zsthampi 
# E-Mail               : zsthampi@ncsu.edu
# REVISION NUMBER      : 1
# LAST UPDATED         : September 4, 2016
# TESTED ON            : Python 2.7.6, Python 2.7.10
# PENDING ENHANCEMENTS : None 
# FUTURE PHASES        : 1.PARSER
#                        2.INTRO-FUNCTION CODE GENERATOR
#                        3.INTER-FUNCTION CODE GENERATOR
########################################################

import sys
import os
import re

###################
# Classes - START #
###################

# Class token_type stores details and functions for each type of token. 
class token_type():
	type = None
	reg_exp = r''

	# Constructor.
	def __init__(self,type,reg_exp):
		self.type = type
		self.reg_exp = reg_exp

	def get_token_type(self):
		return self.type

	# Function to check if a string matches the RE of token. Returns boolean. 
	def check_token(self,string):
		if re.match(self.reg_exp,string):
			return True
		else:
			return False

# Class token stores details and functions for a possible token. 
class token():
	name = None
	type = None

	def __init__(self,name=None):
		self.name = name

	def get_token_name(self):
		return self.name

	def set_token_name(self,token_name):
		self.name = token_name

	def has_token_name(self):
		if self.name:
			return True
		return False

	def get_token_type(self):
		return self.type.get_token_type()

	def set_token_type(self,token_type):
		self.type = token_type

	def has_token_type(self):
		if self.type:
			return True
		return False

# Class scanner stores all details and functions for the scanner module.
class scanner():
	input_file_location = None
	output_file_location = None
	input_file_stream = None
	output_file_stream = None

	# Token types to be considered by the scanner. Initialized in the constructor. 
	token_type_list = []
	# Index of present character being read from the input file.
	index = None
	# Number of steps to rewind in input file. 
	rewind_steps = 0

	# Constructor
	def __init__(self,input_file_location,token_type_list=[]):
		self.input_file_location = input_file_location
		self.input_file_stream = open(self.input_file_location)

		# Get output file location - Default to foo.c in case of failure. 
		try:
			self.output_file_location = input_file_location.split('.')[0]+'_gen.c'
		except:
			self.output_file_location = 'foo.c'

		self.output_file_stream = open(self.output_file_location,'w+')
		self.token_type_list = token_type_list

	# Close all file streams.
	def close(self):
		self.input_file_stream.close()
		self.output_file_stream.close()

	# Function to rewind on the input file stream.
	# Called from get_next_token() function, when the token becomes invalid. 
	# Go back 1 step by default, unless specified.
	def rewind(self,rewind_steps=1):
		self.input_file_stream.seek(-1*rewind_steps,1)
		self.index = self.input_file_stream.tell()

	# Function to go to end of file. 
	# Called from get_next_token() function, when an invalid character is found.
	def fast_forward(self):
		# Move to End of File.
		self.input_file_stream.seek(0,2)

	# Function to check if there are more tokens. 
	def has_more_tokens(self):
		if self.input_file_stream.read(1):
			self.rewind()
			return True
		else:
			return False

	# Function to get next character from the input file. 
	# The character is appended to an existing string - passed as argument.
	# If no argument is passed, string is initialized to empty string.
	def get_next_char(self,string=''):
		char = self.input_file_stream.read(1)
		# Set index of character. 
		self.index = self.input_file_stream.tell()
		return (string+char)

	# Function to get the next token. 
	# It runs recursively till the token becomes invalid, or end of file is reached. 
	# In case of invalid token, return the previous valid token and continue. 
	# Variable - prev_token - stores the previous valid token. (If not passed as argument, it is initialized to blank token object)
	## In case there is no previous valid token, scanner continues till end of line to check for valid tokens.
	## Detailed example provided in readme.txt file. 
	### Ex : Line - 'abc=1;'
	### a - is a valid token - identifier
	### ab is a valid token - identifier
	### abc is a valid token - identifier
	### abc= is NOT a valid token. 
	### Return token 'abc'. Start next time from character '='.
	def get_next_token(self,prev_token=token()):
		if prev_token.has_token_name():
			if self.has_more_tokens():
				current_token = token(self.get_next_char(prev_token.get_token_name()))
			elif prev_token.has_token_type():
				self.rewind_steps = 0
				return prev_token
			else:
				self.rewind_steps = 0
				return None
		else:
			if self.has_more_tokens():
				current_token = token(self.get_next_char())
			else:
				self.rewind_steps = 0
				return None

		# Check if the token matches any of the token types. 
		for token_type in self.token_type_list:
			if token_type.check_token(current_token.get_token_name()):
				current_token.set_token_type(token_type)
		
		# Check if it is a valid token.
		if current_token.has_token_type():
			return self.get_next_token(current_token)
		else:
			# If it was a valid token in the previous iteration, return that. 
			if prev_token.has_token_type():
				self.rewind()
				self.rewind_steps = 0
				return prev_token
			# Else, continue till end of line 
			else:
				# If at end of line, return null and stop further scanning
				if current_token.get_token_name()[-1:]=='\n' or not self.has_more_tokens():
					self.rewind(self.rewind_steps)
					self.fast_forward()
					self.rewind_steps = 0
					return None
				# Continue till end of line
				else:
					self.rewind_steps = self.rewind_steps + 1
					return self.get_next_token(current_token)

	# Function to print token to output file. 
	def print_token(self,token):
		self.output_file_stream.write(token.get_token_name())
	
	# Function to find the row and column of invalid character, and print error messages on terminal and output file. 
	def print_invalid_character(self):
		self.input_file_stream.seek(0,0)
		content = self.input_file_stream.read(self.index)

		row_number = content.count('\n')+1
		if '\n' in content:
			index_of_last_new_line = content.rindex('\n')+1
		else:
			index_of_last_new_line = 0
		column_number = self.index - index_of_last_new_line

		self.input_file_stream.seek(index_of_last_new_line,0)
		row = self.input_file_stream.readline().replace('\n','')

		print "ERROR - Invalid character at Row:"+str(row_number)+" Column:"+str(column_number)
		print row
		print ' '*(column_number-1)+'^'

		self.output_file_stream.write('\n\n')
		self.output_file_stream.write("ERROR - Invalid character at Row:"+str(row_number)+" Column:"+str(column_number)+'\n')
		self.output_file_stream.write(row+'\n')
		self.output_file_stream.write(' '*(column_number-1)+'^')

		self.fast_forward()

#################
# Classes - END #
################# 


################
# Main - START #
################

# Convert reserved word list into a string, which can be used in regular expression.
reserved_word_list = ['int','void','if','while','return','read','write','print','continue','break','binary','decimal']
reserved_word_string = '|'.join(each for each in reserved_word_list)

# Create token_type objects for each of the token types considered in the scanner. 
# For future token types - create new object and add it in the token_type_list variable. 

# Identifier should not be a reserved word either.
identifier = token_type('identifier',r'(?=[a-zA-Z_][a-zA-Z0-9_]*$)(?!('+reserved_word_string+')$)(?!.*\n)')
digit = token_type('digit',r'(?=[0-9]+$)(?!.*\n)')
reserved_word = token_type('reserved_word',r'(?=('+reserved_word_string+'){1}$)(?!.*\n)')
symbol = token_type('symbol',r'(?=(\(|\)|\{|\}|\[|\]|\,|\;|\+|\-|\*|\/|==|!=|>|>=|<|<=|=|&&|\|\|){1}$)(?!.*\n)')
string = token_type('string',r'(?=("{1}.*"{1}$)|(\'{1}.*\'{1}$))(?!.*\n)')
meta_character = token_type('meta_character',r'(#|//){1}.*$')

# Adding extra tokens for blank space and new line
blank_space = token_type('blank_space',r'(?=\s+$)(?!.*\n)')
new_line = token_type('new_line',r'\n{1}$')

# List of token_type objects to be considered by the compiler.
# For future token types - create new object and add it in the token_type_list variable. 
token_type_list = [identifier,digit,reserved_word,symbol,string,meta_character,blank_space,new_line]

# Read the input file name - Display error to use in case of failure. 
try:
	input_file_location = sys.argv[1]
except:
	input_file_location = None
	print "ERROR - Please provide the Compiler Input File."

if input_file_location:
	# Create a scanner object
	s = scanner(input_file_location,token_type_list)
	while (s.has_more_tokens()):
		t = s.get_next_token()
		if t:
			if t.get_token_type()=='identifier' and t.get_token_name()!='main':
				t.set_token_name('cs512'+t.get_token_name())
			s.print_token(t)
		else:
			s.print_invalid_character()

	s.close()

##############
# Main - END #
##############