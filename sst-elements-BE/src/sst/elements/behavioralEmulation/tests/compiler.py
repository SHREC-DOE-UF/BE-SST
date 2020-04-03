#! /usr/bin/env python

"""
  Application-descriptor-language compiler, as part of scalable simulator.
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

import os
import re
import sys
import ast
import copy
import time
import argparse
from collections import namedtuple

#import pdb

# Attempt to use the faster cPickle module.
try: import cPickle as pickle
except: import pickle

# Avoiding unwieldy import; but everything from common is in UPPERCASE.
#from source.common import *
from common import *

from shell import Shell
#from source.shell import Shell

# Suppress the trace when an error is raised (better-looking syntax errors).
# sys.tracebacklimit = 0

# --------------------------------------------------------------------------- #
# ----------------------- Data Structure Definitions ------------------------ #
# --------------------------------------------------------------------------- #

class Token(object):

    def __init__(self, line, column, kind, text):
        """A Token contains information about a string."""
        self.line = line
        self.column = column
        self.kind = kind
        self.text = text

    def __repr__(self):
        """Create a string representation of the Token for printing."""
        return "Index: ({:>3},{:>3}) :: Type: {:>14} :: >{}<".format(
            self.line, self.column, self.kind, self.text)

class Node(object):

    def __init__(self, initializer):
        """A Node is an element in a Syntax Tree."""

        # The initializer can be either a Token or a string.
        if isinstance(initializer, Token):
            self.kind = initializer.kind
            self.token = initializer

            # Fill the Node's payload, if possible.
            self.payload = (
                ( ast.literal_eval(self.token.text[1:-1])
                  if self.token.text.startswith(REGION_LEFT)
                  else ast.literal_eval(self.token.text) )
                if self.token.kind == NUMBER
                else ( self.token.text
                       if self.token.kind in [STRING, NAME]
                       else None ) )

        else:
            self.kind = initializer
            self.token = None
            self.payload = None

        self.parent = None
        self.children = []

#        print self.kind, self.token, self.payload, self.parent, self.children


    def __str__(self, indent=0):
        """Create a long-form recursive string representation of the Node."""

        # The prefix is an indent-lengthed arrow at the front of each line.
        prefix = "- " * max(indent - 1, 0) + ("> " if indent else "") + "("
        contents = " :: " + repr(self.payload) if self.payload != None else ""
        string = prefix + self.kind + contents + ")\n"

        # Recursively add the strings of child nodes too.
        for child in self.children:
            string += child.__str__(indent + 1)

        return string

    def __repr__(self):
        """Create a simple string representation of the Node for printing."""
        contents = " :: " + repr(self.payload) if self.payload != None else ""
        return "(" + self.kind + contents + ")"

    @property
    def descendants(self):
        """A list of every child, direct and indirect, of this Node."""
        descendants = copy.copy(self.children)
        for child in self.children:
            descendants.extend(child.descendants)
        return descendants

    def append(self, other):
        """Add a child Node to this Node."""
        self.children.append(other)
        other.parent = self

    def insert(self, index, other):
        """Add a child Node to a specific index in this Node."""
        self.children.insert(index, other)
        other.parent = self

    def replace(self, other):
        """Replace this Node with the non-parent attributes of another."""
        self.kind = other.kind
        self.token = other.token
        self.children = other.children
        self.payload = other.payload


class Directive(object):

    def __init__(self, kind, payload={}):
        """A Directive is an element in the Intermediate Representation."""
        self.kind = kind
        self.payload = payload

    def __repr__(self):
        """Create a string representation of this Directive for printing."""
        payload = ", ".join([ item[0] + ": " + repr(item[1]) for item in
                              sorted(self.payload.items()) ])
        return "{: <4} :: {}".format(self.kind, payload)


class Instruction(object):

    def __init__(self, kind, operands, line=None):
        """An Instruction is an element in the output machine code."""
        self.kind = kind
        self.line = line
        self.operands = operands

    def __repr__(self):
        """Create a string representation of this Instruction for printing."""
        operands = " ".join( [ "({:0>3})".format(op.line)
                               if isinstance(op, Instruction) else str(op)
                               for op in self.operands ] )
        return "({:0>3}) {: >6} :: {}".format(self.line, self.kind, operands)


# --------------------------------------------------------------------------- #
# --------------------------- Primary Definitions --------------------------- #
# --------------------------------------------------------------------------- #

class Parser(object):

    def __init__(self, code):
        """The parser builds an AST by reading the source code."""

        self.code = code
        self.tokens = []
        self.tokenIndex = 0

    # -------------------------- Utility Definitions ------------------------ #

    @property
    def current(self):
        """Return the Token presently being read."""
        return self.tokens[self.tokenIndex]

    def gobble(self, kind):
        """Return the current Token and advance to the next one."""
        if self.current.kind == kind:
            self.tokenIndex += 1
            return self.tokens[self.tokenIndex - 1]
        else:
            self.syntaxError(kind)

    def syntaxError(self, expected):
        """Raise an error with generic information on the problem."""

        code = self.code.split("\n")[self.current.line]
        space = " " * (self.current.column)

        raise SyntaxError(ERR_SYNTAX.format(expected, self.current.kind,
                                            self.current.line+1, code, space))

    def dictionError(self, line, column):
        """Raise an error and point out the location of the problem."""

        raise SyntaxError(ERR_DICTION.format( line + 1,
                                              self.code.split("\n")[line],
                                              " " * (column) ) )


    # ---------------------------- Main Functions --------------------------- #

    def preprocess(self):
        """Find macro substitutions and perform them."""

        self.toReplace = re.findall(SOURCE_MACRO_PATTERN_SPLIT, self.code)
        self.toRemove = re.findall(SOURCE_MACRO_PATTERN_WHOLE, self.code)

        for item in self.toRemove:
            self.code = self.code.replace(item, "")
        for old, new in self.toReplace:
            self.code = self.code.replace(old, new)

    def tokenize(self):
        """Perform lexical analysis on the input string to generate Tokens."""

        # Walk through the source code line-wise.
        for line, lineString in enumerate(self.code.split('\n')):
            column = 0
            while column < len(lineString):

                # Gobble the next string if a match is found.
                	#Search_Patterns is a dict
                for kind, pattern in SEARCH_PATTERNS.items():
                    match = re.match(pattern, lineString[column:])
                    if match:
                        newString, newKind = match.group(), kind
                        break
                else:
                    # Raise an error if no match is found.
                    self.dictionError(line, column)

                self.tokens.append( Token(line, column, newKind, newString) )
                column += len(newString)

        # Strip away the irrelevant tokens.
        for item in IRRELEVANT_TOKENS:
            self.tokens = filter(lambda x: x.kind != item, self.tokens)

        self.tokens.append( Token(line, column, END_OF_FILE, "") )

    def parse(self):
        """Perform syntatic analysis on the token stream to create the AST."""

        self.preprocess()
        self.tokenize()

        # Create a new root node and call the root function of the grammar.
        root = Node(ROOT)
        self._program_(root)

        return root


    # -------------------------- Grammar Definitions ------------------------ #

    def _program_(self, rootNode):
        """ EBNF :: statement {statement} endoffile ;
                 ::           root-node
            AST  ::          /    |    \
                 ::  statement   ...   ...
        """
        self._statement_(rootNode)

        while not self.current.kind == END_OF_FILE:
            self._statement_(rootNode)

        self.gobble(END_OF_FILE)

    def _statement_(self, node):
        """ EBNF :: do | for | if ; """

        branches = { NAME: self._do_,
                     SWITCH: self._switch_,
                     LOOP: self._loop_,
                     ACCESS: self._access_,
                     ASSIGN: self._assign_,
                     INC: self._inc_,
                     FOR: self._for_,
                     IF: self._if_ }

        if self.current.kind in branches:
            branches[self.current.kind](node)
        else:
            self.syntaxError("statement")

    def _do_(self, node):
        """ EBNF :: name "(" argument {"," argument} ")" ;
                 ::        do-node
            AST  ::      /    |    \
                 ::  name argument argument ...
        """

        doNode = Node(DO)
        doNode.append( Node(self.gobble(NAME) ) )

        self.gobble(REGION_LEFT)
        node.append(doNode)

        while self.current.kind != REGION_RIGHT:
            self._argument_(doNode)
            if self.current.kind == SEPARATOR:
                self.gobble(SEPARATOR)

        self.gobble(REGION_RIGHT)

    def _for_(self, node):
        """ EBNF :: for "(" name "," iterable ")" "{" {statement} "}" ;
                 ::       for-node
            AST  ::      /   |    \
                 ::  name iterable statement ...
        """

        forNode = Node(self.gobble(FOR))
        node.append(forNode)

        # Accept the name and iterable portions of the statement.
        self.gobble(REGION_LEFT)
        self._name_(forNode)
        self.gobble(SEPARATOR)

        self._iterable_(forNode)
        self.gobble(REGION_RIGHT)

        # Accept all substatements.
        self.gobble(SCOPE_LEFT)
        while self.current.kind != SCOPE_RIGHT:
            self._statement_(forNode)
        self.gobble(SCOPE_RIGHT)

    def _loop_(self, node):
        """ EBNF :: loop "(" iterator "," limit ")" "{" {statement} "}" ;
                 ::          loop-node
            AST  ::         /    |    \
                 :: iterator   limit   statement
        """

        loopNode = Node(self.gobble(LOOP))
        node.append(loopNode)

        # Accept the name and iterable portions of the statement.
        self.gobble(REGION_LEFT)
        self._name_(loopNode)
        self.gobble(SEPARATOR)
        self._argument_(loopNode)
        self.gobble(REGION_RIGHT)

        # Accept all substatements.
        self.gobble(SCOPE_LEFT)
        while self.current.kind != SCOPE_RIGHT:
            self._statement_(loopNode)
        self.gobble(SCOPE_RIGHT)

    def _access_(self, node):
        """ EBNF :: access "(" return "," array "," index ")"
                 ::          access-node
            AST  ::         /    |    \
                 ::   return   array   index
        """

        accessNode = Node(self.gobble(ACCESS))
        node.append(accessNode)

        # Accept the name and iterable portions of the statement.
        self.gobble(REGION_LEFT)
        self._name_(accessNode)
        self.gobble(SEPARATOR)
        self._name_(accessNode)
        self.gobble(SEPARATOR)
        self._argument_(accessNode)
#        self._name_(accessNode)
        self.gobble(REGION_RIGHT)

    def _assign_(self, node):
        """ EBNF :: assign "(" name "," number ")"
                 ::          assign-node
            AST  ::         /           \
                 ::     name             number
        """
        assignNode = Node(self.gobble(ASSIGN))
        node.append(assignNode)
        self.gobble(REGION_LEFT)
        self._name_(assignNode)
        self.gobble(SEPARATOR)
        self._argument_(assignNode)
        self.gobble(REGION_RIGHT)

    def _inc_(self, node):
        """ EBNF :: inc "(" name  ")"
                 ::   inc-node
            AST  ::      |
                 ::    name
        """
        incNode = Node(self.gobble(INC))
        node.append(incNode)
        self.gobble(REGION_LEFT)
        self._name_(incNode)
        self.gobble(REGION_RIGHT)

    def _switch_(self, node):
        """ EBNF :: switch "(" name ")" "{" {statement0} "," ... "," {statementN-1} "}" ;
                 ::         switch-node
            AST  ::      /       |        \
                 ::  name  statement0 ... statementN-1
        """
#        switchNode = Node(self.gobble(SWITCH))
#        node.append(switchNode)

#        self.gobble(REGION_LEFT)
#        self._name_(switchNode)
#        self.gobble(REGION_RIGHT)

#        self.gobble(SCOPE_LEFT)
#        while self.current.kind != SCOPE_RIGHT:
#            self.gobble(SCOPE_LEFT)
#            while self.current.kind != SCOPE_RIGHT:
#                self._statement_(switchNode)
#            self.gobble(SCOPE_RIGHT)
#            if self.current.kind == SEPARATOR:
#                self.gobble(SEPARATOR)
#        self.gobble(SCOPE_RIGHT)

        self.gobble(SWITCH)
        self.gobble(REGION_LEFT)
        switchName = self.gobble(NAME)
        self.gobble(REGION_RIGHT)

        switchIndex = 0
        self.gobble(SCOPE_LEFT)
        while self.current.kind != SCOPE_RIGHT:
            switchNode = Node(Token(switchName.line,switchName.column,"if","IF"))
            testNode = Node(Token(switchName.line,switchName.column,"equals","=="))
            testNode.append(Node(switchName))
            testNode.append(Node(Token(switchName.line,switchName.column,NUMBER,str(switchIndex))))
            switchNode.append(testNode)
            node.append(switchNode)
            switchIndex = switchIndex + 1
            self.gobble(SCOPE_LEFT)
            while self.current.kind != SCOPE_RIGHT:
                self._statement_(switchNode)
            self.gobble(SCOPE_RIGHT)
            if self.current.kind == SEPARATOR:
                self.gobble(SEPARATOR)
        self.gobble(SCOPE_RIGHT)


    def _if_(self, node):
        """ EBNF :: "if" "(" conditional ")" "{" {statement} "}" ;
                 ::            if-node
            AST  ::           /       \
                 ::  conditional     statement ...
        """

        ifNode = Node(self.gobble(IF))
        node.append(ifNode)

        # Accept the conditional portion of the statement.
        self.gobble(REGION_LEFT)
        self._conditional_(ifNode)
        self.gobble(REGION_RIGHT)

        # Accept all substatements.
        self.gobble(SCOPE_LEFT)
        while self.current.kind != SCOPE_RIGHT:
            self._statement_(ifNode)
        self.gobble(SCOPE_RIGHT)

    def _argument_(self, node):
        """ EBNF :: string | iterable | expression ; """

        branches = { STRING: self._string_,
                     LIST_LEFT: self._iterable_,
                     REGION_LEFT: self._expression_,
                     NUMBER: self._expression_,
                     NAME: self._expression_ }

        if self.current.kind in branches:
            branches[self.current.kind](node)
        else:
            self.syntaxError("argument")

    def _conditional_(self, node):
        """ EBNF :: expression comparison expression ;
                 ::        comparison-node
            AST  ::         /          \
                 ::  expression       expression
        """

        # Because we aren't looking ahead, we must make a temporary node
        # here for the expressions. (We will later determine its type).
        comparisonNode = Node("")

        # Parse the expression on the left side of the comparison.
        self._expression_(comparisonNode)

        # Now determine the type of the comparison node.
        for comparison in COMPARISON_OPERATORS:
            if self.current.kind == comparison:
                comparisonNode.kind = comparison
                comparisonNode.token = self.gobble(comparison)
                break
        else:
            self.syntaxError("comparison")

        # Parse the expression on the right side of the comparison.
        self._expression_(comparisonNode)

        node.append(comparisonNode)

    def _iterable_(self, node):
        """ EBNF :: iterable = "[" expression {"," expression} "]" ;
                 ::           iterable-node
            AST  ::          /      |      \
                 ::  expression expression expression ...
        """
        iterableNode = Node( self.gobble(LIST_LEFT) )
        iterableNode.kind = ITERABLE

	#Add iterable node to tree
        node.append(iterableNode)

        while self.current.kind != LIST_RIGHT:
            if self.current.kind == NUMBER:
                startIndex = int(self.current.text)+1
#                print "start", startIndex
                self._expression_(iterableNode)
            if self.current.kind == SEPARATOR:
                self.gobble(SEPARATOR)
            if self.current.kind == COLON:
                self.gobble(COLON)
                stopIndex = int(self.current.text)+1
#                print "stop", stopIndex
                self.gobble(NUMBER)
                for i in range(startIndex, stopIndex):
                    loopToken = Token(0,0, NUMBER, str(i))
	            loopTokenIndex = self.tokenIndex
                    self.tokens.insert( loopTokenIndex, loopToken )
                    self._expression_(iterableNode)

        self.gobble(LIST_RIGHT)

    def _expression_(self, node):
        """ Precedence-climbing expression parser.
          Translation of function on wikipedia, found January 2015 at:
            http://en.wikipedia.org/wiki/Operator-precedence_parser
        """

        def atom():
            """An atom is a number, name, or parenthisized subexpression."""
            if self.current.kind == NUMBER:
                newNode = Node(self.gobble(NUMBER))
            elif self.current.kind == NAME:
                newNode = Node(self.gobble(NAME))
            elif self.current.kind == REFERENCE:
                newNode = Node(self.gobble(REFERENCE))
            elif self.current.kind == REGION_LEFT:
                self.gobble(REGION_LEFT)
                newNode = self._expression_(Node(""))
                self.gobble(REGION_RIGHT)
            else:
                self.syntaxError("atom")
            return newNode

        def expression(left, minPrecedence):
            """Recursive function used for precedence climbing."""

            # While current token is an operator with sufficient precedence:
            peek = self.current.kind
            while (peek in ARITHMETIC_OPERATORS
                   and OPERATOR_PRECEDENCE[peek] >= minPrecedence):

                # Keep track of the operator token for later use.
                op = self.gobble(peek)
                right = atom()

                # While the current token is a binary operator with precedence
                # in excess of the above operator.
                peek = self.current.kind
                while ( peek in ARITHMETIC_OPERATORS and
                        ( OPERATOR_PRECEDENCE[peek] >
                          OPERATOR_PRECEDENCE[op.kind] ) ):
                    right = expression(right, OPERATOR_PRECEDENCE[peek])
                    peek = self.current.kind

                # Create the operator node, insert it into the tree, return it.
                new = Node(op)
                new.append(left)
                new.append(right)
                left = new

            return left

        childNode = expression(atom(), 0)
        node.append(childNode)

        return childNode

    def _name_(self, node):
        """ EBNF :: None """
        node.append( Node(self.gobble(NAME)) )

    def _number_(self, node):
        """ EBNF :: None """
        node.append( Node(self.gobble(NUMBER)) )

    def _string_(self, node):
        """ EBNF :: None """
        node.append( Node(self.gobble(STRING)) )


class Generator(object):

    def __init__(self, ast):
        """The generator builds an IR by walking through the AST."""
        self.ast = ast
        self.ir = []



#        for x in ast.children:
#            print x.kind
#            if x.token:
#                print x.token.line, x.token.column, x.token.kind, x.token.text
#            print x.payload
#            print x.children
#            if x.children[0]:
#                print x.children[0].kind, x.children[0].token, x.children[0].payload, x.children[0].children
#            print ""

    # ---------------------------- Main Functions --------------------------- #

    def simplify(self):
        """Reduce all expressions in the AST to their simplest form."""

        simplifiable = lambda x: ( x.kind in ARITHMETIC_OPERATORS
                                   and x.children[0].kind == NUMBER
                                   and x.children[1].kind == NUMBER )

        # Continue to simplify for as long as possible.
        self.nodesReduced = 0
        while len( filter(simplifiable, self.ast.descendants) ) > 0:
            for node in filter(simplifiable, self.ast.descendants):

                # Compute the resulting simplification and insert it.
                new = Node(NUMBER)
                new.payload = OPERATORS[node.kind](
                    node.children[0].payload,
                    node.children[1].payload )
                node.replace(new)
                self.nodesReduced += 1

    def generate(self):
        """Walk through the AST to generate the IR."""

        self.simplify()

        # The root node just contains a series of statements.
        for child in self.ast.children:
            self._statement_(child)

        return self.ir


    # -------------------------- Grammar Definitions ------------------------ #

    def _statement_(self, node):
        """A statement can be any of "switch", "loop", "for", "if", or "do"."""

        # Select among the possible branches.
        { SWITCH: self._switch_,
          LOOP: self._loop_,
          ACCESS: self._access_,
          ASSIGN: self._assign_,
          INC: self._inc_,
          IF: self._if_,
          FOR: self._for_,
          DO: self._do_ }[node.kind]( node )

    def _if_(self, node):
        """An if statement contains a conditional to be evaluated."""

        # Add the starting Directive.
        self.ir.append( Directive(IF, payload={
            OPERATOR: node.children[0].kind,
            TERM_A:   self._argument_(node.children[0].children[0]),
            TERM_B:   self._argument_(node.children[0].children[1])} )
        )

        # Accept all sub-statements.
        for child in node.children[1:]:
            self._statement_(child)

        # Add the concluding Directive.
        self.ir.append( Directive(END) )

    def _switch_(self, node):
        """A switch statement contains a select variable and statements."""
        pass

    def _loop_(self, node):
        """A loop statement contains a limit. child statements are performed limit times."""

        # Add the starting Directive.
        self.ir.append( Directive(LOOP, payload={
            ITERATOR: node.children[0].payload,
            LIMIT:    node.children[1].payload } )
        )

        # Accept all sub-statements.
        for child in node.children[2:]:
            self._statement_(child)

        # Add the concluding Directive.
        self.ir.append( Directive(END) )

    def _for_(self, node):
        """A for statement contains an iteration variable and iterable."""

        # Add the starting Directive.
        self.ir.append( Directive(FOR, payload={
            ITERATOR: node.children[0].payload,
            ITERABLE: [x.payload for x in node.children[1].children]} )
        )

        # Accept all sub-statements.
        for child in node.children[2:]:
            self._statement_(child)

        # Add the concluding Directive.
        self.ir.append( Directive(END) )

    def _access_(self, node):
        """access obtained array."""

        # Add the do Directive to the IR directly.
        self.ir.append(
            Directive(ACCESS, payload={
                VALUE: node.children[0].payload,
                TERM_A: node.children[1].payload,
                TERM_B: node.children[2].payload
            }))

    def _assign_(self, node):
        """access obtained array."""

        # Add the do Directive to the IR directly.
        self.ir.append(
            Directive(ASSIGN, payload={
                NAME: node.children[0].payload,
                VALUE: node.children[1].payload
            }))

    def _inc_(self, node):
        """access obtained array."""

        # Add the do Directive to the IR directly.
        self.ir.append(
            Directive(INC, payload={ NAME: node.children[0].payload }))

    def _do_(self, node):
        """A do statement contains a function and its arguments."""

        # Add the do Directive to the IR directly.
        self.ir.append(
            Directive(DO, payload={
                ROUTINE: node.children[0].payload,
                TERMS: [self._argument_(x) for x in node.children[1:]]
            }))

    def _argument_(self, node):
        """An argument is either a math node, name, or number."""

        # If the type of the node is an operator, it is a math node.
        return ( self._math_(node) if node.kind in ARITHMETIC_OPERATORS
                 else node.payload )

    def _math_(self, node):
        """Recursively create new lines and add new names to flatten a node."""

        # Get a new name for the result node.
        new = SUID()

        # Add the new Directive, and possibly recurse for each term.
        self.ir.append( Directive(MATH, payload={
            OPERATOR: node.kind, VALUE: new,
            TERM_A: ( node.children[0].payload
                      if node.children[0].kind in [NAME, NUMBER]
                      else self._math_(node.children[0]) ),
            TERM_B: ( node.children[1].payload
                      if node.children[1].kind in [NAME, NUMBER]
                      else self._math_(node.children[1]) )} )
        )

        # Pass the new name back up a level.
        return new


class Translator(object):

    def __init__(self, ir):
        """The Translator builds the output machine code using the IR."""
        self.ir = ir

        # Keep a stack of instructions which are popped when _end_ is called.
        self.pending = []

    # ---------------------------- Main Functions --------------------------- #

    def translate(self):
        """Generate the output machine code using the IR."""
        self.code = []

        for line in self.ir:
            translator = getattr(self, "_" + line.kind + "_")
            self.code.extend( translator(line.payload) )

        # Set the line numbers.
        for index, instruction in enumerate(self.code):
            instruction.line = index

        return self.allocate()

    def allocate(self):
        """Perform register allocation for the named variables.
        The graph of mutually-alive variables is 'colored' by the greedy
        heuristic (also known as the Welsh-Powell algorithm). Lower-numbered
        registers are given (with small priority) to long-lived variables.
        """

        # Build a record of the lines in which each variable is referenced.
        references = {}

        for instr in self.code:

            # Because several instructions have non-variable strings,
            # we need to limit the operand scope to exclude those strings.

            # Calls start with two string arguments.
            if instr.kind == CALL:                  bot = 2

            # comms, progs and prints start with 1 string argument.
            elif instr.kind in [COMM, PROG, PRINT]: bot = 1

            # No other instructions start with string arguments.
            else:                                   bot = 0

            # Obtains and Obtarys end with a string argument, and no other instructions do.
            top = 1 if instr.kind in [OBTAIN,OBTARY] else len(instr.operands)

            # Find the lines in which a given variable is referenced.
            for var in filter(lambda x: type(x)==str, instr.operands[bot:top]):
                if var in references and var[0] != '"' and var[-1] != '"':
                    references[var].append(instr.line)
                elif var[0] != '"' and var[-1] != '"':
                    references[var] = [instr.line]

            # Something of a hack: registers in 'obtain' and 'obtary' instructions are
            # completely dedicated after the obtain. This prevents issues
            # with registers being overwritten after backwards jumps.
            if instr.kind in [OBTAIN,OBTARY]:
                references[instr.operands[0]].append(len(self.code))

#            if instr.kind == ACCESS:
#                references[instr.operands[0]].append(len(self.code))

        # Build a set of tuples which contain the (first, last) reference.
        # Note: because of the design of the language, issues with looping
        #   constructs can be effectively ignored. However, future changes
        #   may require traversal of the instructions across different loop
        #   branches to see when the "real" lifetimes are.
        lifetimes = { item: (min(references[item]), max(references[item]))
                      for item in references.keys() }

        # Return whether or not two variables share an edge in the graph.
        edge = lambda x, y: (
            lifetimes[y][0] <= lifetimes[x][0] <= lifetimes[y][1] or
            lifetimes[x][0] <= lifetimes[y][0] <= lifetimes[x][1] or
            ( lifetimes[x] == lifetimes[y] and x != y ) )

        # Build the graph of variables which are mutually alive.
        graph = { item: filter(lambda x: edge(x, item), lifetimes.keys())
                  for item in lifetimes.keys() }

        # Sort the vertics by edge count and (tie breaker) earliest reference.
        sort = lambda x: float( len(x[1]) ) + 1.0 / (lifetimes[ x[0] ][0] + 1)
        graph = sorted(graph.items(), key=sort, reverse=True)
        coloring, colors = {}, {}

        # While we haven't completely colored the graph.
        while len(coloring) < len(graph):

            # Make a new 'color'.
            new = RUID()
            colors[new] = []

            # Color each possible vertex with this new color.
            for vertex, edges in graph:
                needs = vertex not in coloring
                valid = set(edges).isdisjoint( set(colors[new]) )
                if needs and valid:
                    coloring[vertex] = new
                    colors[new].append(vertex)

        # Replace all variable names with register names (a.k.a. 'colors').
        for old, new in coloring.items():
            for instr in self.code:
                instr.operands = [new if a==old else a for a in instr.operands]

        # Return both the machine code and the necessary register count.
        return self.code, len(colors)

    def rename(self, thing, assign=False, variables={}):
        """Map a variable name to a generic name if possible.
        Note: Utilizes the mutability of default keyword arguments to store
        the list of already-assigned variables.
        """

        # If given a list, recurse on each item in the list.
        if type(thing) == list: return [self.rename(item) for item in thing]

        # If given anything other than a string, just give it back.
        elif not type(thing) == str: return thing

        # Otherwise, potentially replace the string as necessary.
        else:

            if thing[0] == '"' and thing[-1] == '"':
                return str(thing)

            # If we've already made a name:
            if thing in variables:
                return variables[thing]

            # If we should create a new name:
            elif assign:
                variables[thing] = SUID()
                return variables[thing]

            # If it already had an acceptable name:
            elif thing.startswith(SUID_PREFIX):
                return thing

            # Otherwise, raise an error.
            else:
                raise SyntaxError(ERR_UNINSTANTIATED.format(thing))


    # -------------------------- Grammar Definitions ------------------------ #

    def _do_(self, details):
        """ Input Details         :: { routine: A,
                                  ::   terms: [B, C, ...] }
            Output Instruction(s) :: Dependent on Routine.
        """

        routine, terms = details[ROUTINE], details[TERMS]

        if routine in USER_ACCESSABLE_INSTRUCTIONS:

            # If the function is an obtain, make an intermediate name.
            if routine in [OBTAIN]:
                terms = [self.rename(terms[0], assign=True)] + terms
	
	    # If the function is an obtary, make an intermediate name.
	    elif routine in [OBTARY]:
                terms = [self.rename(terms[0], assign=True)] + terms

            # For prints: rename all of arguments after the first.
            elif routine in [PRINT]:
                terms = [" "] + terms
                terms = terms[:1] + self.rename(terms[1:])

            # For comms: rename all of arguments after the first.
            elif routine in [COMM]: terms = terms[:1] + self.rename(terms[1:])

            # For calls: rename all of arguments after the second.
            elif routine in [CALL]: terms = terms[:2] + self.rename(terms[2:])

            return [ Instruction( routine, terms ) ]

        # If the function is not a defined instruction, error out.
        else: raise SyntaxError(ERR_TRANSLATE_INSTRUCTION.format(routine))

    def _math_(self, details):
        """ Input Details         :: { term a: A,
                                  ::   term b: B,
                                  ::   operator: C,
                                  ::   value: D }
            Output Instruction(s) :: C D A B;
        """
        operation = { PLUS: ADD, MINUS: SUB, TIMES: MUL, DIVIDES: DIV,
                      MODULO: MOD } [ details[OPERATOR] ]

        return [ Instruction(operation, self.rename([ details[VALUE],
                                                      details[TERM_A],
                                                      details[TERM_B] ])) ]

    def _access_(self, details):
        """ Input Details         :: { value: V,
                                  ::   term a: A,
                                  ::   term b: B }
            Output Instruction(s) ::  access V A B;
        """
        value = self.rename(details[VALUE], assign=True)
        array = self.rename(details[TERM_A])
        index = self.rename(details[TERM_B], assign=True)
        return [ Instruction(ACCESS, [value, array, index]) ]

    def _assign_(self, details):
        """ Input Details         :: { name: N,
                                  ::   value: V }
            Output Instruction(s) ::   assign N V;
        """
        name = self.rename(details[NAME], assign=True)
        value = self.rename(details[VALUE], assign=True)
        return [ Instruction(ASSIGN, [name, value]) ]

    def _inc_(self, details):
        """ Input Details         :: { name: N }
            Output Instruction(s) ::  inc N;
        """
        return [ Instruction(INC, [self.rename(details[NAME])]) ]

    def _loop_(self, details):
        """ Input Details         :: { iterator: A,
                                  ::   limit : B }

            Output Instruction(s) :: assign A 0;
                                  :: target; <----------------------------+
                                  :: ...                                  |
                                  :: inc A;                               |
                                  :: jumplt A B <target>; >---------------+
            Note: the target and jump instructions are mutually referenced.
        """
        iterator = self.rename(details[ITERATOR], assign=True)
        limit = self.rename(details[LIMIT], assign=True)

        # Set up the mutually-referencing instructions.
        target = Instruction(TARGET, [])
        jumplt = Instruction(JUMPLT, [iterator, limit, target])
        target.operands.append(jumplt)

        self.pending.append([ Instruction(INC, [iterator]), jumplt ])

        return [ Instruction(ASSIGN, [iterator, 0]), target ]

    def _for_(self, details):
        """ Input Details         :: { iterator: A,
                                  ::   iterable: B }
            Output Instruction(s) :: assign <UID1> 0;
                                  :: target; <----------------------------+
                                  :: assign <UID0> B;                     |
                                  :: access A <UID0> <UID1>;              |
                                  :: ...                                  |
                                  :: inc    <UID1>;                       |
                                  :: jumplt <UID1> <len(B)> <target>; >---+
            Note: the target and jump instructions are mutually referenced.
        """
        iterable = details[ITERABLE]
        iterator = self.rename(details[ITERATOR], assign=True)
        iterableID, counterID = SUID(), SUID()
        counterMax = len(iterable)

        # Set up the mutually-referencing instructions.
        target = Instruction(TARGET, [])
        jumplt = Instruction(JUMPLT, [counterID, counterMax, target])
        target.operands.append(jumplt)

        self.pending.append([ Instruction(INC, [counterID]), jumplt ])

        return [ Instruction(ASSIGN, [counterID, 0]), target,
                 Instruction(ASSIGN, [iterableID, iterable]),
                 Instruction(ACCESS, [iterator, iterableID, counterID]) ]

    def _if_(self, details):
        """ Input Details         :: { term a: A,
                                  ::   term b: B,
                                  ::   operator: C }
            Output Instruction(s) :: <jump!C> A B <target>; >------+
                                  :: ...                           |
                                  :: target; <---------------------+
            Note: the target and jump instructions are mutually referenced.
        """

        operation = { NOT_EQUALS: JUMPEQ,  EQUALS: JUMPNQ,
                      NOT_GREATER: JUMPGT, GREATER: JUMPNG,
                      NOT_LESS: JUMPLT,    LESS: JUMPNL } [ details[OPERATOR] ]

        # Set up the mutually-referencing instructions.
        target = Instruction(TARGET, [])
        jump = Instruction(operation, [ self.rename(details[TERM_A]),
                                        self.rename(details[TERM_B]),
                                        target ])
        target.operands.append(jump)

        self.pending.append([target])
        return [jump]

    def _end_(self, details):
        """Pop and return the last instructions from the pending stack."""
        return self.pending.pop()


class Compiler(object):

    def __init__(self, shell=None, logDirectory=None):
        """The Compiler is a wrapper for the three compiler components."""

        self.shell = shell if shell else Shell()
        self.logDirectory = logDirectory

        # Make a cache for loading files.
        self.cache = {}

    def parse(self, source):
        """Parse the source code to make an AST."""

        start = time.time()
        parser = Parser(source)
        ast = parser.parse()
        dt = time.time() - start

        macros, tokens, nodes = ( len(parser.toRemove),
                                  len(parser.tokens),
                                  len(ast.descendants) )

        self.shell.say(NOTE_TIME.format("Parsing complete:", dt))

        self.shell.increase_indent()
        self.shell.say(NOTE_PREPROCESS.format(macros),verbose=True)
        self.shell.say(NOTE_TOKENIZE.format(tokens), verbose=True)
        self.shell.say(NOTE_PARSE.format(nodes), verbose=True)
        self.shell.decrease_indent()
        self.shell.newline(verbose=True)

        return ast

    def generate(self, ast):
        """Walk through the AST to make an IR."""

        start = time.time()
        generator = Generator(ast)
        ir = generator.generate()
        dt = time.time() - start

        simplified = generator.nodesReduced

        self.shell.say(NOTE_TIME.format("Generation complete:", dt))

        self.shell.increase_indent()
        self.shell.say(NOTE_SIMPLIFY.format(simplified), verbose=True)
        self.shell.say(NOTE_GENERATE.format(len(ir)), verbose=True)
        self.shell.decrease_indent()
        self.shell.newline(verbose=True)

        return ir

    def translate(self, ir):
        """Walk through the IR to make the output machine code."""

        start = time.time()
        translator = Translator(ir)
        code, regs = translator.translate()
        dt = time.time() - start

        self.shell.say(NOTE_TIME.format("Translation complete:", dt))

        self.shell.increase_indent()
        self.shell.say(NOTE_TRANSLATE.format(len(code)), verbose=True)
        self.shell.say(NOTE_ALLOCATE.format(regs), verbose=True)
        self.shell.decrease_indent()
        self.shell.newline()

        return code, regs

    def compile(self, source):
        """Compile the source code to make the output machine code."""

        self.shell.subheading(NOTE_COMPILER)

        self.ast = self.parse(source)
        self.ir = self.generate(self.ast)
        self.code, self.regs = self.translate(self.ir)

        return self.code

    def load(self, filename):
        """Return a sequence of Instructions from a machine code file."""

        if filename in self.cache:
            return self.cache[filename]

        else:
            with open(filename, 'r') as binary:
                self.cache[filename] = pickle.load(binary)
            return self.load(filename)


if __name__ == "__main__":
    """Allow this script to be run as a standalone program."""


    # ------------------------ Argument Parser Setup ------------------------ #

    defaultOutput = FILENAME_DEFAULT + FILE_EXTENSION_COMPILED

    ap = argparse.ArgumentParser()

    ap.add_argument('input')

    ap.add_argument('-o', '--out', default=defaultOutput,
                    help="output file name (default: %(default)s)")

    ap.add_argument('-v', '--verbose', action='store_true',
                    help="verbose command line output")

    ap.add_argument('-s', '--silent', action='store_true',
                    help="suppress command line output")

    ap.add_argument('-d', '--debug', action='store_true',
                    help="log intermediate data structures to files")

    ap.add_argument('-p', '--printout', action='store_true',
                    help="print the output file to console")

    ap.add_argument('-r', '--readable', action='store_true',
                    help="output a human-readable machine code")

    args = ap.parse_args()


    # --------------------------- General Setup ----------------------------- #

    S = Shell(suppress=args.silent, verbose=args.verbose)
    C = Compiler(shell=S)

    with open (args.input, 'r') as sourcefile: code = sourcefile.read()
    outputFiles = []

    # ----------------------------- Compilation ----------------------------- #

    machinecode = C.compile(code)

    # Write out the 'binary' file.
	
    if args.out:

        outMCfile = os.path.splitext(args.out)[0] + FILE_EXTENSION_MC
        with open(outMCfile, 'wb') as binaryMC:
            binaryMC.write("\n".join([repr(item) for item in machinecode]))

        outputFiles.append(outMCfile)
        S.say("Compilation successful: output written to '{}'".format(args.out))


    # -------------------------- Various Switches --------------------------- #

    # If requested, also write out a human-readble machine code file.
    if args.readable:

        readableMCfile = os.path.splitext(args.out)[0] + FILE_EXTENSION_MC
        with open(readableMCfile, 'wb') as readableMC:
            readableMC.write("\n".join([repr(item) for item in machinecode]))

        outputFiles.append(readableMCfile)

    # If requested, also write out the debug files.
    if args.debug:

        ASTfile = os.path.splitext(args.out)[0] + FILE_EXTENSION_AST
        with open(ASTfile, 'wb') as ast:
            ast.write(str(C.ast))

        IRfile = os.path.splitext(args.out)[0] + FILE_EXTENSION_IR
        with open(IRfile, 'wb') as ir:
            ir.write("\n".join([repr(item) for item in C.ir]))

        outputFiles.append(ASTfile)
        outputFiles.append(IRfile)

    if outputFiles[1:]:
        S.say("Other outputs: {}".format(("\n"+" "*17).join(outputFiles[1:])))

    # If requested, output a human-readable version of the machine code.
    if args.printout:
        S.newline()
        S.say("Output Machine Code:")
        S.increase_indent()
        for line in machinecode:
            S.say(repr(line))
