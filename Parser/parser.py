########################################################
# PROJECT              : PARSER
# DESCRIPTION          : Phase 2 of Compiler Construction
# COURSE               : CSC 512 - COMPILER CONSTRUCTION
# AUTHOR               : ZUBIN THAMPI 
# UNITY ID             : zsthampi 
# E-Mail               : zsthampi@ncsu.edu
# REVISION NUMBER      : 2
# UPDATES              : 1. Added '_' as a valid character in Scanner
# LAST UPDATED         : September 23, 2016
# TESTED ON            : Python 2.7.6, Python 2.7.10
# PENDING ENHANCEMENTS : None 
# FUTURE PHASES        : 1.INTRO-FUNCTION CODE GENERATOR
#                        2.INTER-FUNCTION CODE GENERATOR
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

	def __init__(self,name=None,type=None):
		self.name = name
		self.type = type

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

	# Function to check if a token is equal to another. Used in parser module
	def equals(self,token):
		if not self.has_token_type():
			return False
		elif self.has_token_name():
			if self.get_token_name()==token.get_token_name() and self.get_token_type()==token.get_token_type():
				return True
		else:
			if self.get_token_type()==token.get_token_type():
				return True
		return False

	def is_empty(self):
		if not self.has_token_name and not self.has_token_type():
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

		print "ERROR in Scanner - Invalid character at Row:"+str(row_number)+" Column:"+str(column_number)
		print row
		print ' '*(column_number-1)+'^'

		self.output_file_stream.write('\n\n')
		self.output_file_stream.write("ERROR in Scanner - Invalid character at Row:"+str(row_number)+" Column:"+str(column_number)+'\n')
		self.output_file_stream.write(row+'\n')
		self.output_file_stream.write(' '*(column_number-1)+'^')

		self.fast_forward()

# Class non_terminal stores all attributes and functions related to Non Terminals in the language
class non_terminal():
	# Name for Non-Terminal
	name = ""
	# Multi-dimensional list to store the productions for a non_terminal. 
	production = []
	# Stores the count of each rule (row) of the non-terminal production.
	count = {}

	def __init__(self,name,production=[]):
		self.name = name
		self.production = []
		self.count = {}

	def get_name(self):
		return self.name

	def get_production(self):
		return self.production

	def set_production(self,production):
		self.production = production
		# For each production, set the count as 0
		for i in range(0,len(production)):
			self.count[i] = 0

	# Increment the count for the production rule by 1
	def increment(self,row):
		if not row:
			row = 0
		self.count[row]+=1

	def get_count(self):
		return self.count

	def get_count_for_row(self,row):
		return self.count[row]

	# Function to get a list of possible tokens immediately following a non-terminal.
	def first(self,memory=None):
		global non_terminal_list

		first_dict = {}
		for row,rule in enumerate(self.get_production()):
			if rule:
				element = rule[0]
				# If the first element in a non-terminal is a token, then add that to the list
				if element.__class__.__name__=="token":
					if memory:
						first_dict[element] = memory
					else:
						first_dict[element] = [self,row]
				# If the first element in a non-terminal is another non-terminal.
				elif element.__class__.__name__=="non_terminal":
					# Find first element for non_terminal recursively, and combine
					if memory:
						first_dict.update(element.first(memory))
					else:
						first_dict.update(element.first([self,row]))
		return first_dict

	# # Function to get a list of possible tokens immediately following an empty non-terminal.
	# # Used only to validate if the grammar is LL(1).
	# # NOT IN USE in this parser. 
	# def follow(self,non_terminal_list,memory=[]):
	# 	first_dict = {}
	# 	for non_terminal in non_terminal_list:
	# 		for row,rule in enumerate(non_terminal.get_production()):
	# 			for index,element in enumerate(rule):
	# 				if element.__class__.__name__=="non_terminal" and element.get_name()==self.get_name():
	# 					if index < len(rule) -1:
	# 						next_element = rule[index+1]
	# 						if next_element.__class__.__name__=="token":
	# 							first_dict[next_element] = [non_terminal,row]
	# 						elif next_element.__class__.__name__=="non_terminal":
	# 							first_dict.update(next_element.first([next_element,row]))
	# 	return first_dict

# Class parser stores all the details and functions for Parser module
class parser():
	scanner = None
	token = None

	def __init__(self,scanner):
		self.scanner = scanner

	def get_first_token(self):
		if not self.get_next_token():
			return False
		return True

	# Function to get the next token.
	# Ignores tokens which are blank_space, new_line or meta_characters.
	# The scanner module also prints tokens, invalid character errors to output file.
	def get_next_token(self):
		if self.scanner.has_more_tokens():
			self.token = self.scanner.get_next_token()
			if self.token:
				if self.token.get_token_type()=='blank_space' or self.token.get_token_type()=='new_line' or self.token.get_token_type()=='meta_character':
					self.scanner.print_token(self.token)
					return self.get_next_token()
				elif self.token.get_token_type()=='identifier' and self.token.get_token_name()!='main':
					self.token.set_token_name('cs512'+self.token.get_token_name())
				self.scanner.print_token(self.token)
				return True
			else:
				self.scanner.print_invalid_character()
				return False
		else:
			# Set token = None and return True (GET NEXT TOKEN function did not fail. It just reached end of input program)
			self.token = None
			return True

	# Function to check if a token is in the first elements list of a non-terminal.
	def token_in(self,first):
		for key in first.keys():
			if key.equals(self.token):
				return [first[key][0],first[key][1]]
		return None

	# Function to recursively check if the input program is valid. 
	def check_language(self,non_terminal,row=None):
		# Exits when token is None
		# Pass when an empty production rule exists. 
		if not self.token:
			if [] in non_terminal.get_production():
				non_terminal.increment(row)
				return True
			else:
				return False

		# Block for first iteration of the function. 
		# Find the row to follow using First element list
		if row is None:
			first = non_terminal.first()
			row_in_first = self.token_in(first)
			if row_in_first:
				# Recursively call for next production rule.
				if not self.check_language(row_in_first[0],row_in_first[1]):
					return False
			else:
				return False
		# When the production rule (row) is known		
		else:
			rule = non_terminal.get_production()[row]
			for index,element in enumerate(rule):
				if element.__class__.__name__=='token':
					# If tokens are exhausted from the input program, return False.
					if not self.token:
						return False

					# Check if the token is valid in case of terminal elements in the production rule.
					if element.equals(self.token):
						if not self.get_next_token():
							return False
					else:	
						return False
						
				# In case of non-terminals, find the row to follow using First element list
				elif element.__class__.__name__=='non_terminal':
					# If tokens are exhausted from the input program, check exit condition.
					if not self.token:
						if [] in element.get_production():
							return True
						else:
							return False

					first = element.first()
					row_in_first = self.token_in(first)
					if row_in_first:
						if not self.check_language(row_in_first[0],row_in_first[1]):
							return False
					
		# Initial function call can terminate ONLY on error, or if the tokens from the input program are deplete.
		if row is None:
			if not self.token:
				if [] in non_terminal.get_production():
					non_terminal.increment(row)
					return True
				else:
					return False
		# Pass all other non-terminals, since they reached end of line
		else:
			non_terminal.increment(row)
			return True


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

# Define Non-Terminals and their corresponding production rules
Program = non_terminal("Program")
Program1 = non_terminal("Program1")
Program2 = non_terminal("Program2")
FunctionList = non_terminal("FunctionList")
Function = non_terminal("Function")
FunctionDeclaration = non_terminal("FunctionDeclaration")
FunctionDeclaration1 = non_terminal("FunctionDeclaration1")
TypeName = non_terminal("TypeName")
ParameterList = non_terminal("ParameterList")
NonEmptyList = non_terminal("NonEmptyList")
NonEmptyList1 = non_terminal("NonEmptyList1")
NonEmptyList2 = non_terminal("NonEmptyList2")
DataDeclaration = non_terminal("DataDeclaration")
IdList = non_terminal("IdList")
IdList1 = non_terminal("IdList1")
Id = non_terminal("Id")
Id1 = non_terminal("Id1")
BlockStatements = non_terminal("BlockStatements")
Statements = non_terminal("Statements")
Statement = non_terminal("Statement")
Statement1 = non_terminal("Statement1")
ExpressionList = non_terminal("ExpressionList")
ExpressionList1 = non_terminal("ExpressionList1")
IfStatement = non_terminal("IfStatement")
ConditionExpression = non_terminal("ConditionExpression")
Condition = non_terminal("Condition")
ComparisonOperator = non_terminal("ComparisonOperator")
Condition1 = non_terminal("Condition1")
ConditionOperator = non_terminal("ConditionOperator")
WhileStatement = non_terminal("WhileStatement")
ReturnStatement = non_terminal("ReturnStatement")
ReturnStatement1 = non_terminal("ReturnStatement1")
BreakStatement = non_terminal("BreakStatement")
ContinueStatement = non_terminal("ContinueStatement")
Expression = non_terminal("Expression")
Expression1 = non_terminal("Expression1")
Term = non_terminal("Term")
Term1 = non_terminal("Term1")
AddOperator = non_terminal("AddOperator")
Factor = non_terminal("Factor")
Factor1 = non_terminal("Factor1")
MultiplyOperator = non_terminal("MultiplyOperator")

Program.set_production([[],[TypeName,Id,Program1]])
Program1.set_production([[token(";",symbol),Program2],[token(",",symbol),IdList1,token(";",symbol),Program2],[token("(",symbol),ParameterList,FunctionDeclaration1,FunctionList]])
Program2.set_production([[],[TypeName,Id,Program1]])
FunctionList.set_production([[],[Function,FunctionList]])
Function.set_production([[FunctionDeclaration,FunctionDeclaration1]])
FunctionDeclaration.set_production([[TypeName,token(None,identifier),token("(",symbol),ParameterList]])
FunctionDeclaration1.set_production([[token(";",symbol)],[token("{",symbol),DataDeclaration,Statements]])
TypeName.set_production([[token("int",reserved_word)],[token("void",reserved_word)],[token("binary",reserved_word)],[token("decimal",reserved_word)]])
ParameterList.set_production([[token(")",symbol)],[token("void",reserved_word),NonEmptyList2,token(")",symbol)],[token("int",reserved_word),NonEmptyList,token(")",symbol)],[token("binary",reserved_word),NonEmptyList,token(")",symbol)],[token("decimal",reserved_word),NonEmptyList,token(")",symbol)]])
NonEmptyList.set_production([[token(None,identifier),NonEmptyList1]])
NonEmptyList1.set_production([[],[token(",",symbol),TypeName,token(None,identifier),NonEmptyList1]])
NonEmptyList2.set_production([[],[token(None,identifier),NonEmptyList1]])
DataDeclaration.set_production([[],[TypeName,IdList,token(";",symbol),DataDeclaration]])
IdList.set_production([[Id,IdList1]])
IdList1.set_production([[token(",",symbol),Id,IdList1],[]])
Id.set_production([[token(None,identifier),Id1]])
Id1.set_production([[],[token("[",symbol),Expression,token("]",symbol)]])
BlockStatements.set_production([[token("{",symbol),Statements]])
Statements.set_production([[token("}",symbol)],[Statement,Statements]])
Statement.set_production([[Id,Statement1],[IfStatement],[WhileStatement],[ReturnStatement],[BreakStatement],[ContinueStatement],[token("read",reserved_word),token("(",symbol),token(None,identifier),token(")",symbol),token(";",symbol)],[token("write",reserved_word),token("(",symbol),Expression,token(")",symbol),token(";",symbol)],[token("print",reserved_word),token("(",symbol),token(None,string),token(")",symbol),token(";",symbol)]])
Statement1.set_production([[token("=",symbol),Expression,token(";",symbol)],[token("(",symbol),ExpressionList,token(")",symbol),token(";",symbol)]])
IfStatement.set_production([[token("if",reserved_word),token("(",symbol),ConditionExpression,token(")",symbol),BlockStatements]])
ConditionExpression.set_production([[Condition,Condition1]])
Condition.set_production([[Expression,ComparisonOperator,Expression]])
ComparisonOperator.set_production([[token("==",symbol)],[token("!=",symbol)],[token(">",symbol)],[token(">=",symbol)],[token("<",symbol)],[token("<=",symbol)],])
Condition1.set_production([[],[ConditionOperator,Condition]])
ConditionOperator.set_production([[token("&&",symbol)],[token("||",symbol)]])
WhileStatement.set_production([[token("while",reserved_word),token("(",symbol),ConditionExpression,token(")",symbol),BlockStatements]])
ReturnStatement.set_production([[token("return",reserved_word),ReturnStatement1]])
ReturnStatement1.set_production([[Expression,token(";",symbol)],[token(";",symbol)]])
BreakStatement.set_production([[token("break",reserved_word),token(";",symbol)]])
ContinueStatement.set_production([[token("continue",reserved_word),token(";",symbol)]])
ExpressionList.set_production([[],[Expression,ExpressionList1]])
ExpressionList1.set_production([[],[token(",",symbol),Expression,ExpressionList1]])
Expression.set_production([[Term,Expression1]])
Expression1.set_production([[],[AddOperator,Expression]])
Term.set_production([[Factor,Term1]])
Term1.set_production([[],[MultiplyOperator,Term]])
AddOperator.set_production([[token("+",symbol)],[token("-",symbol)]])
MultiplyOperator.set_production([[token("*",symbol)],[token("/",symbol)]])
Factor.set_production([[token(None,identifier),Factor1],[token(None,digit)],[token("-",symbol),token(None,digit)],[token("(",symbol),Expression,token(")",symbol)]])
Factor1.set_production([[],[token("[",symbol),Expression,token("]",symbol)],[token("(",symbol),ExpressionList,token(")",symbol)]])

# Below list stores the list of Non-Terminals accepted by the parser.
# Used only for Follow() function, to validate that the grammar is LL(1)
non_terminal_list = [Program,Program1,Program2,FunctionList,Function,FunctionDeclaration,FunctionDeclaration1,TypeName,ParameterList,NonEmptyList,NonEmptyList1,DataDeclaration,IdList,IdList1,Id,Id1,BlockStatements,Statements,Statement,ExpressionList,ExpressionList1,IfStatement,ConditionExpression,Condition,ComparisonOperator,Condition1,ConditionOperator,WhileStatement,ReturnStatement,ReturnStatement1,BreakStatement,ContinueStatement,Expression,Expression1,Term,Term1,AddOperator,Factor,Factor1,MultiplyOperator]

# Read the input file name - Display error to use in case of failure. 
try:
	input_file_location = sys.argv[1]
except:
	input_file_location = None
	print "ERROR - Please provide the Compiler Input File."

if input_file_location:
	# Create a scanner object
	s = scanner(input_file_location,token_type_list)
	
	# Create a parser object
	p = parser(s)

	# Load the first token from the scanner. 
	if p.get_first_token():
		# Check if the file is a valid program
		if p.check_language(Program):
			print "PASS - Variable : "+str(Program1.get_count_for_row(0)+DataDeclaration.get_count_for_row(1)+IdList1.get_count_for_row(0))+" Function : "+str(FunctionDeclaration1.get_count_for_row(1))+" Statement : "+str(Statements.get_count_for_row(1))
		else:
			print "ERROR in Parser"
	else:
		print "ERROR in Parser"

	s.close()

##############
# Main - END #
##############