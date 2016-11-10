########################################################
# PROJECT              : SCANNER (README)
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

a. STEPS TO RUN 
	1. python scanner.py <input_file>
	2. <output_file> will be created in the same directory as the input file, appended by _gen. 
	   For ex : if <input_file>='/all_tests/foo.c' <output_file>='/all_tests/foo_gen.c'
	3. In case of any compilation failure, there will be an error message on terminal, as well as on <output_file>
	4. No messages in case of compilation success. The compiled code will be printed to <output_file>

b. DATA STRUCTURE AND LOGIC
	1. DATA STRUCTURE
		=============================================
		token_type : Class for acceptable token types 
		=============================================
		Main Variables
			-> type (Ex: identifier,digit,reserved_word,symbol,string,meta_character,blank_space,new_line)
			-> reg_exp (Regular expression for the token type)
		Main Functions
			-> check_token (to check if a string is a valid token)

		================================
		token : Class for possible token
		================================
		Main Variables
			-> name (The value of token string) 
			-> type (token_type object)
		Main Functions
			-> get and set functions for the variables 
			-> has functions to check if the token has a valid name/type

		======================================================
		scanner : Class for file operations and scanning logic
		======================================================
		Main Variables
			-> variables for handling input and output files
			-> token_type_list (List of acceptable token_type objects) 	
			-> rewind_steps, index (Variables to implement logic and read data from the input stream)
		Main Functions
			-> rewind, fast_forward (Go number of steps back, or go to end of file on the input file stream)
			-> has_more_tokens (Boolean function to check if there are more tokens in the input file)
			-> get_next_char (Get the next character from the input file. Takes a string as argument - Character is appended to the string)
			-> get_next_token (Function to get next valid token. Returns null for invalid character.)
			-> print_token (Function to print token to output file)
			-> print_invalid_character (Function to determine row and column of invalid character, and to print error messages for the invalid character.)

		Please find additional comments inline in code. 
	
	2. LOGIC
		The scanner works on a recursive technique (function - get_next_token()) to identify each token. 
		
		Ex : if line = "int abc=1;", the compiler starts with
		-> "i" is a valid token - identifier
		-> "in" is a valid token - identifier
		-> "int" is a valid token - reserved word 
		-> "int " is NOT a valid token. Return "int" as a valid token. Start next cycle from character " "
		-> " " is a valid token - blank space 
		-> " a" is NOT a valid token. Return " " as a valid token. Start next cycle from character "a"
		and so on . . .

		In case of an invalid character, the compiler will recursively check till the end of line. 
		Ex : if line = "a!=9\n",
		-> "a" is a valid token - identifier
		-> "a!" is NOT a valid token. Return "a"
		-> "!" is NOT a valid token. (Check till end of line in this case)
		-> "!=" is a valid token - symbol
		-> "!=9" is NOT a valid token. Return "!="
		-> "9" is a valid token 
		and so on . . . 

		Ex : if line = "a!!\n", 
		-> "a" is a valid token - identifier
		-> "a!" is NOT a valid token. Return "a"
		-> "!" is NOT a valid token. (Check till end of line in this case)
		-> "!!" is NOT a valid token. (End of line is the next character)
		-> Go back to character "!", and throw an INVALID CHARACTER error at the point 

		In case of invalid character, the scanner quits there. 
		All token and pattern recognition are done using Regular Expressions in Python. 

