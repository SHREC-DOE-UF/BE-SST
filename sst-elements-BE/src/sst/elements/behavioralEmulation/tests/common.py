"""
  Assorted shared definitions, as part of scalable simulator.

    Copyright (C) 2015 {NSF CHREC, UF CCMT, Dylan Rudolph}

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import operator
import sys
import re

from collections import OrderedDict
from string import letters
from random import sample


# ---------------------- 'Enum'-Like String Definitions --------------------- #

INSTRUCTIONS = """
  CALL COMM PROG SIMUL INDEP BEGIN ASSIGN ACCESS OBTAIN OBTARY JUMPLT JUMPGT
  JUMPNL JUMPNG JUMPEQ JUMPNQ ADD SUB MUL DIV MOD INC DEC TARGET PRINT """

TOKENS = """
  NUMBER COMMENT IGNORE FOR IF STRING NAME REGION_LEFT REGION_RIGHT
  SCOPE_LEFT SCOPE_RIGHT LIST_LEFT LIST_RIGHT SEPARATOR PLUS MINUS TIMES
  DIVIDES MODULO POWER NOT_EQUALS NOT_GREATER NOT_LESS EQUALS GREATER LESS
  COLON SWITCH LOOP ACCESS ASSIGN INC"""

COMPILER_ASSORTED = """
  MATH OPERATOR OPERANDS TERMS TERM_A TERM_B INSTRUCTION REFERENCE UPDATE
  DO END_OF_FILE ROOT ITERABLE ITERATOR ROUTINE VALUE END LIMIT NAME"""

SIMULATOR_ASSORTED = """
  SEND MESH TORUS TREE CUBE NEAREST LINEAR LAGRANGE POLYNOMIAL KRIGING RBF POLYNOMIAL
  NEIGHBORS VARIOGRAM FUNCTION SELF AUNT PARENT SIBLING CHILD COUSIN"""

KEYWORDS = ' '.join( [ INSTRUCTIONS, TOKENS, COMPILER_ASSORTED,
                       SIMULATOR_ASSORTED ] )

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --- #
#  Generate a list of attributes for this module which are named after the    #
#  whitespace-separated items in KEYWORDS. These attributes exist only to     #
#  prevent the use of "magic strings" in the source code.                     #
#                                                                             #
for construct in re.findall(r"[\w']+", KEYWORDS):                             #
    lowercase = construct.replace("_", " ").lower()                           #
    setattr(sys.modules[__name__], construct, lowercase)                      #
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --- #


# ----------------------- Assorted Compiler Definitions --------------------- #

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --- #
#  Define a set of regular expressions which match all of the language        #
#  constructs that can be found in the source code text.                      #
#                                                                             #
SEARCH_PATTERNS = OrderedDict([                                               #
    (NUMBER, r'(\d+\.\d*|(\(-\d+\)|\(\+\d+\)|\d+))'),                         #
    (COMMENT, r'#+.*'),                                                       #
    (IGNORE, r'[ \t]+'),                                                      #
    (SWITCH, r'SWITCH'),                                                            #
    (FOR, r'FOR'),                                                            #
    (IF, r'IF'),                                                              #
    (INC, r'INC'),                                                              #
    (LOOP, r'LOOP'),                                                              #
    (ACCESS, r'ACCESS'),                                                              #
    (ASSIGN, r'ASSIGN'),                                                              #
    (STRING, r'"[-a-zA-Z0-9_.,:;|(){}<>~`!@#$%^&*\\/ ]+"'),                   #
    (NAME, r'[a-zA-Z]*[a-zA-Z0-9_\.]*[a-zA-Z0-9]'),                           #
    (REGION_LEFT, r'\('),                                                     #
    (REGION_RIGHT, r'\)'),                                                    #
    (SCOPE_LEFT, r'\{'),                                                      #
    (SCOPE_RIGHT, r'\}'),                                                     #
    (LIST_LEFT, r'\['),                                                       #
    (LIST_RIGHT, r'\]'),                                                      #
    (SEPARATOR, r','),                                                        #
    (COLON, r':'),                                                        #
    (PLUS, r'\+'),                                                            #
    (MINUS, r'-'),                                                            #
    (TIMES, r'\*'),                                                           #
    (DIVIDES, r'\/'),                                                         #
    (MODULO, r'\%'),                                                          #
    (POWER, r'\^'),                                                           #
    (NOT_EQUALS, r'!='),                                                      #
    (NOT_GREATER, r'<='),                                                     #
    (NOT_LESS, r'>='),                                                        #
    (EQUALS, r'=='),                                                          #
    (GREATER, r'>'),                                                          #
    (LESS, r'<')                                                              #
])                                                                            #
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --- #

SOURCE_MACRO_PATTERN_WHOLE = r'DEFINE ::.*?>>'
SOURCE_MACRO_PATTERN_SPLIT = ( r'DEFINE ::[ \t]*([a-zA-Z]+)[ \t]*' +
                               r'(?:<< |<<)(.*?)(?: >>|>>)' )


# ----------------- Symbol and Operation Classes and Mappings --------------- #

IRRELEVANT_TOKENS = [ COMMENT, IGNORE ]

JUMP_INSTRUCTIONS = [ JUMPLT, JUMPNL, JUMPGT, JUMPNG, JUMPEQ, JUMPNQ ]
USER_ACCESSABLE_INSTRUCTIONS = [ CALL, COMM, PROG, INDEP,
                                 SIMUL, BEGIN, PRINT, OBTAIN, OBTARY ]
#                                 ASSIGN, ACCESS ]

COMPARISON_OPERATORS = [ EQUALS, GREATER, LESS,
                         NOT_EQUALS, NOT_GREATER, NOT_LESS ]

ARITHMETIC_OPERATORS = [ PLUS, MINUS, TIMES, DIVIDES, MODULO, POWER ]

OPERATOR_PRECEDENCE = { PLUS: 0, MINUS: 0, TIMES: 1, DIVIDES: 1,
                        MODULO: 2, POWER: 2 }

OPERATORS = { PLUS: operator.add, MINUS: operator.sub,
              TIMES: operator.mul, DIVIDES: operator.div,
              MODULO: operator.mod, POWER: operator.pow }

STRING_OPERATORS = { "==": operator.eq, "!=": operator.ne,
                     "<=": operator.le, ">=": operator.ge,
                     "<": operator.lt, ">": operator.gt }

UNCACHEABLE_INSTRUCTIONS = [ CALL, COMM, PROG, OBTAIN, OBTARY, INDEP, SIMUL, BEGIN ]

# ------------------------ Name Generator Definitions ----------------------- #

# Compiler:

SUID_SIZE = 3; SUID_PREFIX = '~'; SUID_SUFFIX = '~'; SUIDS = set()
RUID_SIZE = 2; RUID_PREFIX = 'r`'; RUID_SUFFIX = ''; RUIDS = set()

def SUID():
    """Generate a random String Unique Identification (SUID)."""

    gen = lambda: ''.join(sample(letters * SUID_SIZE, SUID_SIZE))
    new = gen()
    while new in SUIDS: new = gen()
    SUIDS.add(new)

#    print SUIDS

    return SUID_PREFIX + new + SUID_SUFFIX

def RUID():
    """Generate a sequential Register Unique Identification (RUID)."""

    new = ("{:0>" + repr(RUID_SIZE) + "}").format(len(RUIDS))
    RUIDS.add(new)

    return RUID_PREFIX + new + RUID_SUFFIX

# Simulator:

PID_SIZE = 4; PIDS = set(); PID_SUFFIX = ")"
PID_ROUTINE_PREFIX, PID_MESSAGE_PREFIX, PID_EXECUTOR_PREFIX = 'R-(','M-(','E-('

def PID(prefix):
    """Generate a random Process (Pseudo-Unique) Identification (PID)."""
    return prefix + ''.join(sample(letters * PID_SIZE, PID_SIZE)) + PID_SUFFIX


# ------------------------------ File Related ------------------------------- #

# Compiler:

FILE_EXTENSION_COMPILED = ".smc.txt"
FILE_EXTENSION_AST = ".ast.txt"
FILE_EXTENSION_IR = ".ir.txt"
FILE_EXTENSION_MC = ".txt"
FILENAME_DEFAULT = "out"

# Simulator:

INPUT_LOOKUP_HEADER = "Input"
OUTPUT_LOOKUP_HEADER = "Output"

# --------------------------------- Errors ---------------------------------- #

# Compiler:

ERR_SYNTAX = "Cannot Parse (needed: '{}', found: '{}') on line {}:\n\n{}\n{}^"
ERR_DICTION = "Unknown pattern on line {}:\n\n{}\n{}^"
ERR_UNINSTANTIATED = "Variable '{}' referenced before instantiation."
ERR_TRANSLATE_INSTRUCTION = "Bad instruction identifier: '{}'"

# Simulator:

ERR_RELATIONSHIP = "No matching relationship: '{}' is not '{}' of '{}'."
ERR_CONCURRENCY = "Invalid 'begin' ('indep' xor 'simul' needed)."
ERR_UNROUTABLE = "Router: cannot make a path from {} to {}."
ERR_INTERPOLATION_SCHEME = "Invalid interpolation scheme: '{}'"

# --------------------------- Printing and Logging -------------------------- #

# Compiler:

NOTE_TIME = "{: <61} {:8.4f}s elapsed"
NOTE_TIME_IND = "{: <59} {:8.4f}s elapsed"
NOTE_COMPILER  = "Compiling Source Code"

NOTE_PREPROCESS = "Macro definitions substituted: {:.>46}"
NOTE_TOKENIZE =   "Meaningful tokens in token stream: {:.>42}"
NOTE_PARSE =      "Nodes in abstact syntax tree: {:.>47}"

NOTE_SIMPLIFY =   "Expressions simplified: {:.>53}"
NOTE_GENERATE =   "Lines in intermediate representation: {:.>39}"

NOTE_TRANSLATE =  "Lines in output machine code: {:.>47}"
NOTE_ALLOCATE =   "Number of registers required: {:.>47}"

# Simulator:

KIND_WIDTH, COUNT_WIDTH, GID_WIDTH = 22, 6, 35

NOTE_COMPONENT_HEADER = ( ":: " + "Count".center(COUNT_WIDTH) + " :: " +
                          "Kind".center(KIND_WIDTH) + " :: " +
                          "First Few GIDs".center(GID_WIDTH) + " ::" )

NOTE_COMPONENT_RULE = ( ":: " + "-" * COUNT_WIDTH + " :: " +
                        "-" * KIND_WIDTH + " :: " +
                        "-" * GID_WIDTH + " ::" )

NOTE_COMPONENT = "::{:> 7} :: {} ::{}  ::"
NOTE_RUN = "Executing Run {}:"
NOTE_SIM_TIME = "Simulated Time: {:.>61}"
NOTE_SIM_EVENTS = "Number of Events: {:.>59}"
NOTE_SIM_SPEED = "Simulation Speed: {:.>54} kE/s"

IDT = "> ID: {}, T: {:9.7f} :: {} :: {} :: "

LOG_MESSAGE_STARTED = IDT + " << started >>  :: {} to {}, size: {}, tag: {}"
LOG_MESSAGE_CREATED = IDT + "< new message > :: pid: {}"
LOG_MESSAGE_UPDATE =  IDT + "  (location)    :: ID: {}, new routine: {}"
LOG_MESSAGE_ENDED =   IDT + "  << ended >>   ::"

LOG_EXECUTOR_STARTED = IDT + " << started >>  ::"
LOG_EXECUTOR_CREATED = IDT + "< new executor >:: pid: {}"
LOG_EXECUTOR_UPDATE =  IDT + " (instruction)  :: {}"
LOG_EXECUTOR_ENDED =   IDT + "  << ended >>   ::"

LOG_ROUTINE_STARTED =   IDT + " << started >>  :: input: {}, outputs: {}"
LOG_ROUTINE_CREATED =   IDT + "< new routine > :: pid: {}, gid: {}"
LOG_ROUTINE_CHANGE =    IDT + "   -change-     :: {} is now {}"
LOG_ROUTINE_TIMEOUT =   IDT + "   -timeout-    :: pause for {}"
LOG_ROUTINE_CONDITION = IDT + "  -condition-   :: pause until {} {} {}"
LOG_ROUTINE_CONTINUE  = IDT + "  (unpausing)   ::"
LOG_ROUTINE_PROVISION = IDT + "event ignored due to provision"
LOG_ROUTINE_ENDED =     IDT + "  << ended >>   ::"

LOG_ROUTINE_STATE_META = IDT + "{}"


# ----------------------------- Default Options ----------------------------- #

DEFAULT_INTERPOLATION_SCHEME = POLYNOMIAL

DEFAULT_INTERPOLATION_OPTIONS = { KRIGING: { POLYNOMIAL: 0,
                                             NEIGHBORS : 6,
                                             VARIOGRAM : { "range": 30.0} },
                                  RBF: { FUNCTION: LINEAR } }

DEFAULT_ROUTING_POLICIES = { MESH:  "first-to-last",
                             TORUS: "first-to-last",
                             TREE:  "default",
                             CUBE:  "first-to-last" }
