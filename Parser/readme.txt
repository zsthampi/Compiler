########################################################
# PROJECT              : PARSER README
# DESCRIPTION          : Phase 2 of Compiler Construction
# COURSE               : CSC 512 - COMPILER CONSTRUCTION
# AUTHOR               : ZUBIN THAMPI 
# UNITY ID             : zsthampi 
# E-Mail               : zsthampi@ncsu.edu
# REVISION NUMBER      : 1
# LAST UPDATED         : September 23, 2016
# TESTED ON            : Python 2.7.6, Python 2.7.10
# PENDING ENHANCEMENTS : None 
# FUTURE PHASES        : 1.INTRO-FUNCTION CODE GENERATOR
#                        2.INTER-FUNCTION CODE GENERATOR
########################################################

---------------
b. STEPS TO RUN 
---------------
	1. python parser.py <input_file>
	2. <output_file> will be created in the same directory as the input file, appended by _gen. 
	   For ex : if <input_file>='/all_tests/foo.c' <output_file>='/all_tests/foo_gen.c'
	3. The parser outputs "PASS" or "ERROR" after processing the input program file. 
	4. If the parsing is successful, the parser output the number of variables (global and local), functions and statements in the input program. 
		Ex : PASS Variable : 6 Function : 6 Statement : 35

---------------------------
c. DATA STRUCTURE AND LOGIC
---------------------------

	1. LOGIC 

		The parser uses a RECURSIVE-DESCENT approach to verify if the input program is valid. 
		The parser uses the LL(1) grammar mentioned above in the code. 

		It starts with Non-Terminal "PROGRAM" and traverses down to further Non-Terminals, based on a look-ahead character.  
		The look-ahead is implemented by function "first()" in the non-terminal class. 

		For Ex : If current Non-Terminal is "PROGRAM", and next token is "int"
			Step 1 : Parser executes rule 2 of Non-Terminal "PROGRAM" (TypeName Id Program1)
			Step 2 : Parser executes rule 1 of Non-Terminal "TypeName" (int)
			Step 3 : After end-of-line on Production rule on step 2, the parser goes back to step 1 and checks the next element in the rule (Non-Terminal "Id")

		The parser reports PASS if the input program completes Non-Terminal "PROGRAM" successfully. 
		ERROR otherwise (No details of the error are provided on standard output)

	2. DATA STRUCTURE

		========================================================================
		non_terminal : Class to store the details and functions of non-terminals
		========================================================================

		Main Variables
			-> name (Ex: Program,Statement)
			-> production (Multi-dimensional array to store the production rules of a non-terminal. Each row in the array denotes a separate production rule. Each element in a rule may be a terminal (token object) or another non-terminal (non-terminal object) )
			Ex : ExpressionList production = [[],[Expression,ExpressionList1]]
			-> count (Dictionary to store the count of each rule in the production)
			-> scanner (scanner module from Phase 1 of project. Passed as an object)
		Main Functions
			-> first (to get a list of terminals that could immediately follow the non-terminal. Returns a dictionary of all possible terminal values.)
			Ex value : first[identifier] = [Statement,1]   ie. Rule 1 of Non-Terminal Statement

		==================================================================
		parser : Class to store the details and functions of parser module
		==================================================================

		Main Variables
			-> token (The current token being parsed. Also used as a look-ahead character)
			-> scanner (scanner module from Phase 1 of project. Passed as an object)
		Main Functions
			-> check_token (to check if a string is a valid token)
			-> get_next_token (to get the next valid token from the scanner. Ignores meta characters)
			-> token_in (to check if a terminal is in the first dictionary of a non-terminal)
			-> check_language (main function of the parser to recursively check if the input program is valid. Additional details provided as comments in the function. )


