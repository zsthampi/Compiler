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

---------------
a. STEPS TO RUN 
---------------
	1. python code_generator.py <input_file>
	2. <output_file> will be created in the same directory as the input file, appended by _gen. 
	   For ex : if <input_file>='/all_tests/foo.c' <output_file>='/all_tests/foo_gen.c'
	3. The parser outputs "PASS" or "ERROR" after processing the input program file. 
	4. If the parsing is successful, the parser output the number of variables (global and local), functions and statements in the input program.
		Ex : PASS Variable : 6 Function : 6 Statement : 35
	5. ALL MESSAGES ARE SAME AS THE PARSER PROJECT. THERE ARE NO ADDITIONAL MESSAGES ON THE TERMINAL

---------------------------
b. DATA STRUCTURE AND LOGIC
---------------------------
	The data structures and logic are similar to the intra function code generator. Modifications are made in the functions to iterate and modify the parse tree. 

	1. LOGIC 

		The intra function code generator works in 2 stages 
		i. Create a Parse Tree from the output of the Parser. (Please refer to class Node)
		ii. Make multiple iterations over the Parse Tree to modify the code. 

		Finally, it prints the modified code in the parse tree to the output file. 

		Specifically, the code-generator does 10 iterations, each performed by the functions detailed in DATA STRUCTURE section. 
			
	2. DATA STRUCTURE

		=================================================
		node : Class to store each node of the parse tree
		=================================================

		Main Variables
			-> parent (Parent node of the node)
			-> child (List of child nodes of the node)
			-> type (non_terminal/token)
			-> name (name of the non-terminal/token)
			-> value/modified_value (value of the node)
			-> code (code to be added before the node)
			-> is_global (To check the scope of the node)
			-> global_dict/local_dict (Variables to store the global/local identifiers available at the node)

		Main Functions
			-> zeroeth_iteration : Initial iteration to find array declarations and remove ( ) from Expressions
			-> first_iteration : First iteration to store local and global variables
			-> second_iteration : Second iteration to modify identifier values and store it in code (except array assignments)
			-> third_iteration : Third iteration to evaluate expressions, condition expressions and generate code
			-> fourth_iteration : Fourth Iteration to reduce expressions
			-> fifth_iteration : Fifth Iteration to assign arrays
			-> sixth_iteration : Sixth iteration to remove data declaration and add common - global and local declaration
			-> seventh_iteration : Seventh iteration to update code for if, while, break and continue statements
			-> eighth_iteration : Eighth iteration for adding include and macro statements at Program node
			-> ninth_iteration : Ninth iteration to write function code


