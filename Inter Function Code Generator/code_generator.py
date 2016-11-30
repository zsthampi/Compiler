#############################################################
# PROJECT              : INTER FUNCTION CODE GENERATOR README
# DESCRIPTION          : Phase 4 of Compiler Construction
# COURSE               : CSC 512 - COMPILER CONSTRUCTION
# AUTHOR               : ZUBIN THAMPI 
# UNITY ID             : zsthampi 
# E-Mail               : zsthampi@ncsu.edu
# REVISION NUMBER      : 4
# UPDATES              : 
# LAST UPDATED         : November 30, 2016
# TESTED ON            : Python 2.7.6, Python 2.7.10
# PENDING ENHANCEMENTS : None 
# FUTURE PHASES        : None
#############################################################

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

	# Function to print a string to output file
	def print_string(self,string):
		self.output_file_stream.write(string)
	
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
				if self.token.get_token_type()=='blank_space' or self.token.get_token_type()=='new_line':
					# self.scanner.print_token(self.token)
					return self.get_next_token()
				elif self.token.get_token_type()=='meta_character':
					self.scanner.print_token(self.token)
					return self.get_next_token()
				# elif self.token.get_token_type()=='identifier' and self.token.get_token_name()!='main':
				# 	self.token.set_token_name('cs512'+self.token.get_token_name())
				# self.scanner.print_token(self.token)
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
	def check_language(self,non_terminal,row,node):
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
				# Use the same node as it is still in Program non terminal
				if not self.check_language(row_in_first[0],row_in_first[1],node):
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
						# Create new child node for non-terminal
						child_node = Node(self.token.__class__.__name__,self.token.get_token_type(),self.token.get_token_name(),node)
						# node.add_child(child_node)
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
						# Create new child node for non-terminal
						child_node = Node(element.__class__.__name__,element.get_name(),None,node)
						# node.add_child(child_node)
						if not self.check_language(row_in_first[0],row_in_first[1],child_node):
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

# Class node to create parse tree
class Node():
	parent = None
	# Variable to store array of child nodes. Stored in the order of creation
	child = []
	# Type - non_terminal or token
	type = None
	name = None
	value = None
	modified_value = None
	code = None
	# Boolean value to check if the scope is local or global
	is_global = None
	# Boolean value to check whether to print code
	generate = True
	# Boolean value to check whether to reduce the nodes
	reduce = False
	# Variables to store label values for goto
	start_label = None
	end_label = None
	# Class level variable to store the count for labels generated so far. 
	label_count = 0

	# Static dictionary of global identifiers
	global_dict = {}
	# Dictionary of local identifiers
	local_dict = None

	# Static variable to store the most recently added global identifier
	# We need to remove this, in case it turns out to be a function in the production rule
	most_recent_global_identifier = None

	def __init__(self,type,name,value=None,parent=None):
		self.type = type
		self.name = name
		self.value = value
		self.code = None
		self.generate = True
		self.child = []

		self.start_label = None
		self.end_label = None

		self.parent = parent
		if parent is not None:
			parent.add_child(self)

		if self.type=='non_terminal' and self.name=='Program':
			self.is_global = True
		elif self.type=='non_terminal' and (self.name=='ParameterList' or self.name=='FunctionDeclaration1' or self.name=='FunctionList'):
			self.is_global = False
		else:
			self.is_global = parent.is_global

		if self.type=='non_terminal' and self.name=='FunctionDeclaration1' and self.parent is not None and self.parent.name!='Program1':
			self.local_dict = {}
		elif self.type=='non_terminal' and self.name=='Program1':
			self.local_dict = {}
		else:
			if self.parent is not None and self.parent.local_dict is not None:
				self.local_dict = self.parent.local_dict
			else:
				self.local_dict = None

		# if self.type=='non_terminal' and (self.name=='Expression' or self.name=='ConditionExpression'):
		if self.type=='non_terminal' and self.name=='Expression':
			self.reduce = True
		elif self.parent is not None and self.parent.reduce:
			self.reduce = True

	def get_next_label(self):
		label = 'Label'+str(Node.label_count)
		Node.label_count += 1
		return label

	def add_child(self,child):
		self.child.append(child)

	def add_to_dict(self,identifier=None):
		if self.is_global:
			if identifier is None:
				element = len(self.global_dict)
				self.global_dict[element] = element
				return 'mem['+str(element)+']'
			else:
				if identifier not in self.global_dict.keys():
					self.global_dict[identifier] = len(self.global_dict)
					Node.most_recent_global_identifier = identifier
		else:
			if identifier is None:
				element = len(self.local_dict)
				self.local_dict[element] = element
				return 'mem[base + '+str(element)+']'
			else:
				if identifier not in self.local_dict.keys():
					self.local_dict[identifier] = len(self.local_dict)

	def get_modified_identifier(self,identifier,return_type=None):
		if self.local_dict is not None:
			if identifier in self.local_dict:
				if return_type is None:
					return 'mem[base + '+str(self.local_dict[identifier])+']'
				else:
					return ['local',str(self.local_dict[identifier])]
		if self.global_dict is not None:
			if identifier in self.global_dict:
				if return_type is None:
					return 'mem['+str(self.global_dict[identifier])+']'
				else:
					return ['global',str(self.global_dict[identifier])]
		return identifier

	def remove_most_recent_global_identifier(self):
		if Node.most_recent_global_identifier is not None:
			self.global_dict.pop(Node.most_recent_global_identifier)


#################
# Classes - END #
################# 

# Global variables required in Inter Function Code Generator
label_dict = {}

# DEBUG FUNCTION - Function to print intented results for the parse tree
def iterate_tree(node,level=0):
	print ('    '*level)+node.name+":"+str(node.value)+":"+str(node.modified_value)+":"+str(node.code)+":"+str(node.global_dict)+":"+str(node.local_dict)
	for child in node.child:
		iterate_tree(child,level+1)

# Initial iteration to find array declarations and remove ( ) from Expressions
def zeroeth_iteration(node):
	if node.type=='token' and node.name=='digit' and node.parent is not None and node.parent.name=='Factor' and node.parent.parent is not None and node.parent.parent.name=='Term' and node.parent.parent.parent is not None and node.parent.parent.parent.name=='Expression' and node.parent.parent.parent.parent is not None and node.parent.parent.parent.parent.name=='Id1':
		node.parent.parent.parent.parent.value = node.value
	if node.type=='non_terminal' and node.name=='Factor' and len(node.child)==3:
		node.child = node.child[1:-1]
	for child in node.child:
		zeroeth_iteration(child)

# First iteration to store local and global variables
def first_iteration(node):
	if node.type=='token' and node.name=='identifier' and node.parent is not None and node.parent.name=='Id' and node.parent.parent is not None and node.parent.parent.name!='Statement':
		node.add_to_dict(node.value)
		if len(node.parent.child)==2:
			if node.parent.child[1].value is not None:
				for i in range(1,int(node.parent.child[1].value)):
					node.add_to_dict()

	if node.type=='token' and node.name=='identifier' and node.parent is not None and node.parent.name in ['NonEmptyList','NonEmptyList1','NonEmptyList2']:
		# Set parent to the corresponding DataDeclaration/Statements non terminal
		parent = node.parent
		while (parent.name not in ['Function','Program1'] and parent.parent is not None):
			parent = parent.parent
		if parent.name=='Function':
			parent = parent.child[1]
		else:
			parent = parent.child[2]
		if len(parent.child)>1:
			parent = parent.child[1]
			parent.add_to_dict(node.value)
			# if parent.code is None:
			# 	parent.code = parent.get_modified_identifier(node.value)+' = '+node.value+';\n'
			# else:
			# 	parent.code = parent.get_modified_identifier(node.value)+' = '+node.value+';\n' + parent.code

	if node.type=='token' and node.name=='symbol' and node.value=='(' and node.parent is not None and node.parent.name=='Program1':
		node.remove_most_recent_global_identifier()

	for child in node.child:
		first_iteration(child)

# Second iteration to modify identifier values and store it in code (except array assignments)
def second_iteration(node):
	if node.type=='token':
		if node.name=='identifier' and node.parent is not None:
			if node.parent.type=='non_terminal' and node.parent.name=='Id' and len(node.parent.child)>1:
				node.modified_value = None
			elif node.parent.type=='non_terminal' and node.parent.name in ['NonEmptyList','NonEmptyList1','NonEmptyList2']:
				node.modified_value = node.value
			else:
				node.modified_value = node.get_modified_identifier(node.value)
		elif node.name=='symbol' and node.value==';':
			node.modified_value = node.value+'\n'
		else:
			node.modified_value = node.value
	for child in node.child:
		second_iteration(child)

# Third iteration to evaluate expressions, condition expressions and generate code
def third_iteration(node):
	for child in node.child:
		third_iteration(child)
	if node.type=='non_terminal' and node.reduce and node.modified_value is None and node.parent is not None:
		if len(node.child)==1:
			if node.child[0].modified_value is not None:
				node.modified_value = node.child[0].modified_value
			elif node.child[0].code is not None:
				identifier = node.add_to_dict()
				node.modified_value = identifier
				node.code = identifier+' = '+node.child[0].code+';\n'
		elif node.name=='Factor1' and len(node.child)==3 and node.child[0].type=='token' and node.child[0].value=='[':
			scope,index = node.get_modified_identifier(node.parent.child[0].value,'return list')
			# element = node.add_to_dict()
			# if node.parent.code is None:
			# 	node.parent.code = (element+' = '+index+' + '+node.child[1].modified_value+';\n')
			# else:
			# 	node.parent.code += (element+' = '+index+' + '+node.child[1].modified_value+';\n')
			# # Set modified value for Id
			# node.parent.modified_value = scope+'['+element+']'
			if scope == 'local':
				node.parent.modified_value = 'mem[base + '+str(index)+' + '+str(node.child[1].modified_value)+']'
			else:
				node.parent.modified_value = 'mem['+str(index)+' + '+str(node.child[1].modified_value)+']'

		elif len(node.child)>1 and node.child[0].type=='non_terminal' and (node.child[0].name=='Factor' or node.child[0].name=='Term'):
			identifier = node.add_to_dict()
			node.modified_value = identifier
			code = []
			for child in node.child:
				if child.modified_value is not None:
					code.append(child.modified_value)
				elif child.code is not None:
					code.append(child.code)
			node.code = identifier+' = '+(' '.join(value for value in code))+';\n'
		else:
			code = []
			for child in node.child:
				if child.modified_value is not None:
					code.append(child.modified_value)
				elif child.code is not None:
					code.append(child.code)
			node.code = (' '.join(value for value in code))

		if node.name=='Factor1' and node.child[0].type=='token' and node.child[0].value=='(':
			identifier = node.add_to_dict()
			parent = node.parent
			parent.modified_value = identifier
			label = parent.child[0]
			print_expression_list(node.child[1],parent)
			new_label = add_label()
			if parent.code is None:
				parent.code = 'mem[top + 0] = base;\n'
			else:
				parent.code = parent.code + 'mem[top + 0] = base;\n'
			parent.code = parent.code + 'mem[top + 1] = top;\n'
			parent.code = parent.code + 'mem[top + 3] = '+new_label+';\n'
			parent.code = parent.code + 'base = top + 4;\n'
			parent.code = parent.code + "goto "+label.value+';\n'
			parent.code = parent.code + label_dict[new_label]+':;\n'
			parent.code = parent.code + identifier + ' = mem[top + 2];\n'

# Fourth Iteration to reduce expressions
def fourth_iteration(node):
	if node.reduce and node.parent is not None:
		if node.modified_value is not None and node.code is not None:
			
			# Find the parent to store the code
			parent = node.parent
			while(parent.name!='Statement'):
				parent = parent.parent

			if parent.code is None:
				parent.code = node.code
			else:
				parent.code = node.code + parent.code

			node.code = None

	for child in node.child:
		fourth_iteration(child)

	if node.reduce and node.parent is not None and not node.parent.reduce:
		node.child = []

# Fifth Iteration to assign arrays
def fifth_iteration(node):
	for child in node.child:
		fifth_iteration(child)
	if node.type=='token' and node.name=='identifier' and node.parent is not None and node.parent.name=='Id' and len(node.parent.child)==2 and node.parent.parent is not None and node.parent.parent.name=='Statement':
		scope,index = node.get_modified_identifier(node.value,'return list')

		parent = node.parent
		while(parent.name not in ['Program','Program1','Program2','DataDeclaration','Statement'] and parent.parent is not None):
			parent = parent.parent

		# Copy Expression code to parent
		if node.parent.child[1].child[1].code is not None:
			if parent.code is None:
				parent.code = node.parent.child[1].child[1].code
			else:
				parent.code += node.parent.child[1].child[1].code

		# element = node.add_to_dict()
		# if parent.code is None:
		# 	parent.code = (element+' = '+index+' + '+node.parent.child[1].child[1].modified_value+';\n')
		# else:
		# 	parent.code += (element+' = '+index+' + '+node.parent.child[1].child[1].modified_value+';\n')
		# # Set modified value for Id
		# node.parent.modified_value = scope+'['+element+']'
		if scope == 'local':
			node.parent.modified_value = 'mem[base + '+str(index)+' + '+str(node.parent.child[1].child[1].modified_value)+']'
		else:
			node.parent.modified_value = 'mem['+str(index)+' + '+str(node.parent.child[1].child[1].modified_value)+']'
		# Clear children for Id
		node.parent.child = []

# Global boolean variable to check whether to remove global data declarations
remove_global_declaration_flag = True
# Sixth iteration to remove data declaration and add common - global and local declaration
def sixth_iteration(node):
	global remove_global_declaration_flag

	for child in node.child:
		sixth_iteration(child)
	# Find the last node for Program 2 and link it to Program node directly
	if remove_global_declaration_flag and node.type=='non_terminal' and node.name=='Program2' and node.parent is not None:
		parent = node.parent
		while(parent.name!='Program' and parent.parent is not None):
			parent = parent.parent
		parent.child = [node]
		remove_global_declaration_flag = False

	# if node.type=='non_terminal' and node.name=='Program':
	# 	if node.global_dict is not None and len(node.global_dict)>0:
	# 		if node.code is None:
	# 			node.code = 'int global['+str(len(node.global_dict))+'];'
	# 		else:
	# 			node.code = 'int global['+str(len(node.global_dict))+'];' + node.code

	if node.type=='non_terminal' and (node.name=='DataDeclaration' or node.name=='Statements') and node.parent is not None and node.parent.name=='FunctionDeclaration1' and node.parent.child[1].name==node.name:
		# if node.local_dict is not None and len(node.local_dict)>0:
		# 	if node.code is None:
		# 		node.code = 'int local['+str(len(node.local_dict))+'];'
		# 	else:
		# 		node.code = 'int local['+str(len(node.local_dict))+'];' + node.code
		if node.name=='DataDeclaration':
			node.child = []

# Seventh iteration to update code for if, while, break and continue statements
# Also remove curly braces 
def seventh_iteration(node):
	if node.type=='non_terminal' and node.name=='IfStatement':
		node.start_label = node.get_next_label()
		node.end_label = node.get_next_label()

		# Set the child as Block Statement node in If statement
		child = node.child[-1]
		# Remove the left curly brace 
		child.child = child.child[1:]
		if child.code is None:
			child.code = 'goto '+node.start_label+';\n'+'goto '+node.end_label+';\n'+node.start_label+':;'
		else:
			child.code = 'goto '+node.start_label+';\n'+'goto '+node.end_label+';\n'+node.start_label+':;' + child.code

		# Set child as the Statements block terminating the block
		child = node.child[-1]
		while (len(child.child)!=1 or child.name!='Statements'):
			child = child.child[-1]
		# Remove right curly brace from Statements
		child.child = []
		if child.code is None:
			child.code = node.end_label+':;'
		else:
			child.code = node.end_label+':;' + child.code

	if node.type=='non_terminal' and node.name=='WhileStatement':
		node.start_label = node.get_next_label()
		node.end_label = node.get_next_label()

		# Update while to if 
		node.child[0].modified_value = 'if'

		# code = [child.modified_value for child in node.child if child.modified_value is not None]
		code = 'if ( '+(' '.join(each for each in get_node_value(node.child[2])))+' )'

		# Set the child as Block Statement node in If statement
		child = node.child[-1]
		# Remove the left curly brace 
		child.child = child.child[1:]
		if child.code is None:
			child.code = 'goto '+node.start_label+';\n'+'goto '+node.end_label+';\n'+node.start_label+':;'
		else:
			child.code = 'goto '+node.start_label+';\n'+'goto '+node.end_label+';\n'+node.start_label+':;' + child.code

		# Set child as the Statements block terminating the block
		child = node.child[-1]
		while (len(child.child)!=1 or child.name!='Statements'):
			child = child.child[-1]
		# Remove right curly brace from Statements
		child.child = []
		if child.code is None:
			child.code = code+' goto '+node.start_label+';\n'+node.end_label+':;'
		else:
			child.code = code+' goto '+node.start_label+';\n'+node.end_label+':;' + child.code

	if node.type=='non_terminal' and (node.name=='BreakStatement' or node.name=='ContinueStatement') and node.parent is not None:
		parent = node.parent
		while (parent.name!='WhileStatement' and parent.parent is not None):
			parent = parent.parent

		if node.name=='BreakStatement':
			node.child[0].modified_value = 'goto '+parent.end_label
		else:
			node.child[0].modified_value = 'goto '+parent.start_label

	for child in node.child:
		seventh_iteration(child)

# Eighth iteration for adding include and macro statements at Program node
def eighth_iteration(node):
	x = len(node.global_dict.keys())
	code = '#include <assert.h> \n'+'#include <stdlib.h> \n'+'int mem[2000]; \n'+'#define top mem['+str(x)+']\n'+'#define base mem['+str(x+1)+']\n'+'#define jumpReg mem['+str(x+2)+']\n'+'#define membase '+str(x+3)+'\n\n'+'int main() {\ntop = membase;\nmem[top] = 0;\nbase = top + 1;\ngoto main;\n\n'
	if node.code is None:
		node.code = code
	else:
		node.code = code + node.code 

# Ninth iteration to write function code
def ninth_iteration(node):
	for child in node.child:
		ninth_iteration(child)

	if node.type=='non_terminal' and node.name=='FunctionDeclaration1' and node.child[0].type=='token' and node.child[0].name=='symbol' and node.child[0].value=='{' and node.parent is not None:
		parent = node.parent
		if parent.type=='non_terminal' and parent.name=='Function':
			label = parent.child[0].child[1]
			parent.child[0].generate = False
			node.child[0].generate = False
		else:
			label = parent.parent.child[1].child[0]
			parent.parent.child[0].generate = False
			parent.parent.child[1].generate = False
			parent.child[0].generate = False
			parent.child[1].generate = False
			node.child[0].generate = False

		# Add epilogue code
		statements_node = node.child[-1]
		while(statements_node.child[-1].type=='non_terminal' and statements_node.child[-1].name=='Statements'):
			statements_node = statements_node.child[-1]
		statements_node.child[0].modified_value = 'top = mem[base - 3];\n'+'jumpReg = mem[base - 1];\n'+'base = mem[base - 4];\n'+'goto jumpTable;\n'

		if parent.code is None:
			parent.code = label.value+':;\n'+'top = base + '+str(len(node.local_dict.keys()))+';\n'
		else:
			parent.code = parent.code + label.value+':;\n'+'top = base + '+str(len(node.local_dict.keys()))+';\n'
		
	# elif node.type=='non_terminal' and node.name=='Statements' and node.child==[]:
	# 	node.modified_value = 'jumpReg = mem[base - 1];\n'+'goto JumpReg;\n'
	# Check if the previous statement is return!!!
	# elif node.type=='non_terminal' and node.name=='Statements' and node.child[0].type=='token' and node.child[0].name=='symbol' and node.child[0].value=='}':
	# 	node.modified_value = 'jumpReg = mem[base - 1];\n'+'goto JumpReg;\n'
	elif node.name=='Statement1' and node.child[0].type=='token' and node.child[0].value=='(':
		parent = node.parent
		parent.child[0].generate = False
		parent.child[1].generate = False
		while (parent.type!='non_terminal' or parent.name!='Statement'):
			parent = parent.parent
		label = node.parent.child[0].child[0]
		print_expression_list(node.child[1],parent)
		new_label = add_label()
		if parent.code is None:
			parent.code = 'mem[top + 0] = base;\n'
		else:
			parent.code = parent.code + 'mem[top + 0] = base;\n'
		parent.code = parent.code + 'mem[top + 1] = top;\n'
		parent.code = parent.code + 'mem[top + 3] = '+new_label+';\n'
		parent.code = parent.code + 'base = top + 4;\n'
		parent.code = parent.code + "goto "+label.value+';\n'
		parent.code = parent.code + label_dict[new_label]+':;\n'

	elif node.name=='ReturnStatement1' and len(node.child)==2:
		parent = node.parent

		parent.child[0].generate = False
		parent.child[1].generate = False

		if parent.code is None:
			parent.code = 'mem[base - 2] = '+node.child[0].modified_value+';\n'+'top = mem[base - 3];\n'+'jumpReg = mem[base - 1];\n'+'base = mem[base - 4];\n'+'goto jumpTable;\n'
		else:
			parent.code = parent.code + 'mem[base - 2] = '+node.child[0].modified_value+';\n'+'top = mem[base - 3];\n'+'jumpReg = mem[base - 1];\n'+'base = mem[base - 4];\n'+'goto jumpTable;\n'

	elif node.name=='ReturnStatement1' and len(node.child)==1:
		parent = node.parent

		parent.child[0].generate = False
		parent.child[1].generate = False

		if parent.code is None:
			parent.code = 'top = mem[base - 3];\n'+'jumpReg = mem[base - 1];\n'+'base = mem[base - 4];\n'+'goto jumpTable;\n'
		else:
			parent.code = parent.code + 'top = mem[base - 3];\n'+'jumpReg = mem[base - 1];\n'+'base = mem[base - 4];\n'+'goto jumpTable;\n'

	elif node.name=='FunctionDeclaration1' and len(node.child)==1:
		parent = node.parent
		if parent.name=='Function':
			parent.child[0].generate = False
			parent.child[1].generate = False
		else:
			parent.parent.child[0].generate = False
			parent.parent.child[1].generate = False
			parent.child[0].generate = False
			parent.child[1].generate = False
			parent.child[2].generate = False

def print_expression_list(node,parent,count=0):
	for child in node.child:
		if child.type=='non_terminal' and child.name=='Expression':
			if parent.code is None:
				parent.code = 'mem[top + 4 + '+str(count)+'] = '+child.modified_value+';\n'
			else:
				parent.code = parent.code + 'mem[top + 4 + '+str(count)+'] = '+child.modified_value+';\n'
		elif child.type=='non_terminal' and child.name=='ExpressionList1':
			print_expression_list(child,parent,count+1)

def add_label():
	element = str(len(label_dict.keys())+1)
	label_dict[element] = 'Jump'+element
	return element

# Global variable to store final code 
code = []
def print_code(node):
	global code
	if node.generate:
		if node.code is not None:
			code.append(node.code)
		if node.modified_value is not None:
			code.append(node.modified_value)
		for child in node.child:
			print_code(child)

# Function to recursively get the modified value of a node
def get_node_value(node):
	result = []
	if node.modified_value is not None:
		result.append(node.modified_value)
	for child in node.child:
		result = result+get_node_value(child)
	return result

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

# Create the parent node on parse tree 
program_node = Node(Program.__class__.__name__,Program.get_name())
		
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
		if p.check_language(Program,None,program_node):
			print "PASS - Variable : "+str(Program1.get_count_for_row(0)+DataDeclaration.get_count_for_row(1)+IdList1.get_count_for_row(0))+" Function : "+str(FunctionDeclaration1.get_count_for_row(1))+" Statement : "+str(Statements.get_count_for_row(1))
			zeroeth_iteration(program_node)
			first_iteration(program_node)
			second_iteration(program_node)
			third_iteration(program_node)
			fourth_iteration(program_node)
			fifth_iteration(program_node)
			sixth_iteration(program_node)
			seventh_iteration(program_node)
			eighth_iteration(program_node)
			ninth_iteration(program_node)
			print_code(program_node)
			# iterate_tree(program_node)

			# Add switch statement and right curly brace for main 
			code.append('\njumpTable:;\nswitch(jumpReg) {\ncase 0: exit(0);\n'+('\n'.join('case '+key+': goto '+label_dict[key]+';' for key in label_dict.keys()))+'\ndefault: assert(0);\n}\n}\n')
			code = ' '.join(each for each in code)
			# code = code.replace(";",";\n").replace('{','\n{').replace('}','}\n')

			# print code
			s.print_string(code)
		else:
			print "ERROR in Parser"
	else:
		print "ERROR in Parser"

	s.close()

##############
# Main - END #
##############