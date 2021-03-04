"""
  Interpolation-related defitions, as part of scalable simulator.

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

# Attempt to use the faster cPickle library.
try: import cPickle as pickle
except: import pickle

import csv
import datetime
import random
import math
import numpy as np
from copy import deepcopy
from random import *

# Avoiding unwieldy import; but everything from common is in UPPERCASE.
from common import *


class Librarian(object):

    def __init__(self, scheme=DEFAULT_INTERPOLATION_SCHEME,
                 options=DEFAULT_INTERPOLATION_OPTIONS):
        """The Librarian manages interpolators and samples."""

        # 'cache' has keys: ("filename", (inputs,)) and values: [outputs].
        self.cache = {}

        # 'interpolators' has keys: "filename" and values [interpolator]
        self.interpolators = {}

        self.scheme = scheme
        self.options = options

    def newInterpolator(self, samples, filename, degree):
        """Create a new interpolator from some samples based on our scheme."""

        if self.scheme == "linear":
            return Linear(samples, filename)

        elif self.scheme == "polynomial":
            return PolynomialTemp(samples, filename, degree)

        elif self.scheme == "lagrange":
            return Lagrange(samples, filename)

        else:
            raise NameError(ERR_INTERPOLATION_SCHEME.format(self.scheme))

        # See note at bottom of non-commented portion of file.

        """
        elif self.scheme == RBF:
            return Rbf(samples, self.options[RBF][FUNCTION])

        #elif self.scheme == KRIGING:l=
            return Kriging(samples, self.options[KRIGING][POLYNOMIAL],
                           self.options[KRIGING][NEIGHBORS],
                           self.options[KRIGING][VARIOGRAM])
        """

    def lookup(self, filename, inputs, degree):
        """Determine the outputs for a given filename and inputs."""

        # If we've already cached this input:
        if (filename, tuple(inputs)) in self.cache:

            # Just return the cached entry.
            return self.cache[ (filename, tuple(inputs)) ]

        # Otherwise, if we have already opened this file:
        elif filename in self.interpolators:

            # Perform the interpolation.
            #interp = random.choice(self.interpolators[filename])
            #outputs = [interp.interpolate(inputs)[0]]

            outputs = [ interp.interpolate(inputs)[0] for interp in
                        self.interpolators[filename] ]

            # Add the new entry to the cache.
            self.cache[ (filename, tuple(inputs)) ] = outputs

            # Return the new entry.
            return outputs

        # Otherwise, if we haven't seen this filename before:
        else:

            # Load the file.
            self.interpolators[filename] = self.load(filename, degree)

            # Re-call lookup with the same parameters.
            return self.lookup(filename, inputs, degree)

    def load(self, filename, degree):
        """Load a .csv file and return all of its data as an interpolator."""

        # Create a reader-generator for the file name.
        reader = csv.reader(open(filename, 'rb'))
        # Grab the metadata, but (as of this writing) don't use it.
        metadata = dict(zip(reader.next(), reader.next()))

        # Skip rows until we get to the real data.
        line = reader.next()
        while (INPUT_LOOKUP_HEADER not in line
               and INPUT_LOOKUP_HEADER.lower() not in line):
            line = reader.next()

        # Determine which columns are inputs and which are outputs.
        icols = [c for c in range(len(line)) if line[c]==INPUT_LOOKUP_HEADER]
        ocols = [c for c in range(len(line)) if line[c]==OUTPUT_LOOKUP_HEADER]

        # Skip a line, this should contain the names of the parameters.
        reader.next()

        # Intitialize the point and value lists.
        points, values, = [], []

        # For each remaining row:
        for row in reader:
            # Add a point with the entry from each input/output column.
            points.append( [eval( row[col] ) for col in icols] )
            values.append( [eval( row[col] ) for col in ocols] )

        # Create sets of samples, one for each output, with the same inputs.
        sampleSets = [Samples(points, [[i] for i in v]) for v in zip(*values)]

        #def unpair(inputset):
            #level = len(inputset[0]) 

        # Create an interpolator for each set of samples:
        return [ self.newInterpolator(samples, filename, degree) for samples in sampleSets ]


class Samples(object):

    def __init__(self, points, values):
        """Samples contain independent and dependent parameters."""
        self.points = deepcopy(points)
        self.values = deepcopy(values)
        self.dimension = len(self.points[0])


class Lagrange(object):

    def __init__(self, samples, filename):
        """Lagrange polynomial interpolation method."""

        self.samples = samples
        self.filename = filename
        self.interpolate = lambda p: [float(self.interpolatedOP(p))]

    def polyip(self, x1, y1, x2, y2, k):

        slope = (y2-y1)/(x2-x1)
        return (y2 - (slope*(x2-k)))

    def lagrangeip(self, ip, ipset, opset):

        op = 0.0
        i = 0

        for entryO in ipset:
            s = 1.0
            t = 1.0
            j = 0

            for entryI in ipset:
                if j != i:
                    s = s*(ip-entryI)
                    t = t*(entryO-entryI)
                j = j+1

            op = op + ((s/t)*opset[i])
            i = i+1

        if (op < 0) or (op > opset[len(opset)-1] or op < opset[0]):
            print "Warning---Lagrange interpolation failed for one set in "+self.filename+". Trying linear interpolation!"
            k = 0
            for x in ipset:
                if x == ip: return opset[k]
                if x > ip : return self.polyip(ipset[k-1], opset[k-1], x, opset[k], ip)
                k = k+1
            return opset[k-1]

        else:
            return op

    def interpolatedOP(self, inputset):

        if len(inputset) != len(self.samples.points[0]): 
            raise Exception("Invalid Input set "+str(inputset));
            return 0

        j = 0
        for ip_sample in self.samples.points:
            if tuple(inputset) == tuple(ip_sample): return self.samples.values[j][0]
            j = j+1

        level = len(inputset)-1
        curr_level_op = [float(v[0]) for v in self.samples.values]
        first_level_ip = []

        if level == 0: 
            for inputval in self.samples.points:
                first_level_ip.append(float(inputval[0]))

        while level > 0:
            
            i = 0
            next_level_op = []
            parent = self.samples.points[0][level-1]
            if level == 1: first_level_ip.append(float(parent))
            iplist = []
            oplist = []

            for sampleip in self.samples.points:
                if sampleip[level-1] == parent:
                    iplist.append(float(sampleip[level]))
                    oplist.append(float(curr_level_op[i]))
                else:
                    next_level_op.append(self.lagrangeip(float(inputset[level]), iplist, oplist))
                    parent = sampleip[level-1]
                    iplist = [float(sampleip[level])]
                    oplist = [float(curr_level_op[i])]
                    if level == 1: first_level_ip.append(float(parent))
     
                i = i+1

            next_level_op.append(self.lagrangeip(float(inputset[level]), iplist, oplist))
            curr_level_op = next_level_op
            level = level-1

        return self.lagrangeip(float(inputset[level]), first_level_ip, curr_level_op)


class Polynomial(object):  #Must verify multidimensional interpolation!! Buggy!

    def __init__(self, samples, filename, degree):
        """Polynomial is the polynomial interpolation method."""

        self.samples  = samples
        self.filename = filename
        self.degree   = degree
        """        
        # If this is multi-dimensional interpolation:
        if len(samples.points[0]) > 1:
            self.interp = spi.LinearNDInterpolator( np.array(samples.points),
                                                    np.array(samples.values),
                                                    fill_value=0.0 )

        else: # If there is just one input dimension:
            self.interp = spi.interp1d( zip(*samples.points)[0],
                                        zip(*samples.values)[0],
                                        fill_value=0.0, kind=LINEAR)

        self.interpolate = lambda p: [float(v) for v in self.interp(p)]
        """
        self.interpolate = lambda p: [float(self.interpolatedOP(p))]

    def polyip(self, degree, x1, y1, x2, y2, k):
        d = degree
        slope = (y2-y1)/((x2**d)-(x1**d))
        return (y2 - (slope*((x2**d)-(k**d))))

    def fetchValue(self, level, parent, inputset, samples, index, value_pos):

        if len(inputset) == 0: return self.samples.values[value_pos][0]

        offset = 0

        for sampleip in samples:

            if parent == sampleip[level-1] and sampleip[level] == inputset[0]:
                return self.fetchValue(level+1, sampleip[level], inputset[1:], samples[offset:], index+offset, index+offset)

            elif parent == sampleip[level-1] and sampleip[level] > inputset[0]:
                opl = self.fetchValue(level+1, samples[offset-1][level], inputset[1:], samples[0:offset], 0, index+offset-1)
                opn = self.fetchValue(level+1, sampleip[level], inputset[1:], samples[offset:], index+offset, index+offset)
                return self.polyip(self.degree, samples[offset-1][level], opl, sampleip[level], opn, inputset[0])

            elif parent >= sampleip[level-1]:
                offset = offset+1

        return self.samples.values[value_pos+offset-1][0]    

    def interpolatedOP(self, inputset):

        if len(inputset) != len(self.samples.points[0]): 
            raise Exception("Invalid Input set "+str(inputset));
            return 0

        index = 0
        
        for sampleip in self.samples.points:

            if tuple(sampleip) == tuple(inputset): return self.samples.values[index][0]

            if sampleip[0] == inputset[0]:
                return self.fetchValue(1, sampleip[0], inputset[1:], self.samples.points[index:], index, index)

            elif sampleip[0] > inputset[0]:
                opl = self.fetchValue(1, self.samples.points[index-1][0], inputset[1:], self.samples.points[0:index], 0, index-1)
                opn = self.fetchValue(1, sampleip[0], inputset[1:], self.samples.points[index:], index, index) 
 
                interp_op = self.polyip(self.degree, self.samples.points[0][0], self.samples.values[0][0], self.samples.points[1][0], self.samples.values[1][0], inputset[0])

                if (interp_op > opn or interp_op < opl): 
                    #interp_op = self.polyip(self.degree, self.samples.points[0][0], self.samples.values[0][0], self.samples.points[len(self.samples.points)-1][0], self.samples.values[len(self.samples.values)-1][0], inputset[0])
                    interp_op = self.polyip(1, self.samples.points[index-1][0], opl, sampleip[0], opn, inputset[0])

                return interp_op

            index = index+1

        return self.samples.values[index-1][0] 


class PolynomialTemp(object):

    def __init__(self, samples, filename, degree):
        """Polynomial is the polynomial interpolation method."""

        self.samples  = samples
        self.dataset = zip(self.samples.points, self.samples.values)
        self.filename = filename
        self.degree   = degree
        self.interpolate = lambda p: [float(self.interpolatedOP(p))]

    def linearip(self, x1, y1, x2, y2, k):

        slope = (y2-y1)/(x2-x1)
        return (y2 - (slope*(x2-k)))

    def polyip(self, x1, y1, x2, y2, k):

        deg = self.degree
        return (k**deg)*self.linearip(x1, y1/(x1**deg), x2, y2/(x2**deg), k)   

    def interpolatedOP(self, inputset):

        if len(inputset) != len(self.samples.points[0]): 
            raise Exception("Invalid Input set "+str(inputset));
            return 0

        prev_input=0
        prev_output=0
        next_input=0
        next_output=0

	for dset in self.dataset:

            if tuple(inputset) == tuple(dset[0]): return dset[1][0]

            elif dset[0][-1] == inputset[-1] and dset[0][0] < inputset[0]:
                prev_input = dset[0][0] 
                prev_output = dset[1][0]/dset[0][-1]

            elif dset[0][-1] == inputset[-1] and dset[0][0] > inputset[0]:
                next_input = dset[0][0]
                next_output = dset[1][0]/dset[0][-1]
                break

	return inputset[-1]*self.polyip( prev_input, prev_output, next_input, next_output, inputset[0] )  


class Linear(object):

    def __init__(self, samples, filename):
        """Linear is the polynomial interpolation method."""

        self.samples  = samples
        self.filename = filename
        """        
        # If this is multi-dimensional interpolation:
        if len(samples.points[0]) > 1:
            self.interp = spi.LinearNDInterpolator( np.array(samples.points),
                                                    np.array(samples.values),
                                                    fill_value=0.0 )

        else: # If there is just one input dimension:
            self.interp = spi.interp1d( zip(*samples.points)[0],
                                        zip(*samples.values)[0],
                                        fill_value=0.0, kind=LINEAR)

        self.interpolate = lambda p: [float(v) for v in self.interp(p)]
        """
        self.interpolate = lambda p: [float(self.interpolatedOP(p))]

    def linearip(self, x1, y1, x2, y2, k):

        slope = (y2-y1)/(x2-x1)
        return (y2 - (slope*(x2-k)))

    def fetchValue(self, level, parent, inputset, samples, index, value_pos):

        if len(inputset) == 0: return self.samples.values[value_pos][0]

        offset = 0

        for sampleip in samples:

            if parent == sampleip[level-1] and sampleip[level] == inputset[0]:
                return self.fetchValue(level+1, sampleip[level], inputset[1:], samples[offset:], index+offset, index+offset)

            elif parent == sampleip[level-1] and sampleip[level] > inputset[0]:
                opl = self.fetchValue(level+1, samples[offset-1][level], inputset[1:], samples[0:offset], 0, index+offset-1)
                opn = self.fetchValue(level+1, sampleip[level], inputset[1:], samples[offset:], index+offset, index+offset)
                return self.linearip(samples[offset-1][level], opl, sampleip[level], opn, inputset[0])

            elif parent >= sampleip[level-1]:
                offset = offset+1

        return self.samples.values[value_pos+offset-1][0]    

    def interpolatedOP(self, inputset):

        if len(inputset) != len(self.samples.points[0]): 
            raise Exception("Invalid Input set "+str(inputset));
            return 0

        index = 0

        for sampleip in self.samples.points:

            if tuple(sampleip) == tuple(inputset): return self.samples.values[index][0]

            if sampleip[0] == inputset[0]:
                return self.fetchValue(1, sampleip[0], inputset[1:], self.samples.points[index:], index, index)

            elif sampleip[0] > inputset[0]:
                opl = self.fetchValue(1, self.samples.points[index-1][0], inputset[1:], self.samples.points[0:index], 0, index-1)
                opn = self.fetchValue(1, sampleip[0], inputset[1:], self.samples.points[index:], index, index) 
                return self.linearip(self.samples.points[index-1][0], opl, sampleip[0], opn, inputset[0])

            index = index+1

        return self.samples.values[index-1][0]  


def lookupValue(filename, inputs, i_scheme):

    degree = 1
    if str(i_scheme).find("polynomial") != -1:
        if str(i_scheme).find("-") != -1: degree = float(str(i_scheme)[(str(i_scheme).find("-"))+1:])
        else: degree = 1
        i_scheme = "polynomial"

    librarian = Librarian(scheme=i_scheme)

    if filename == "titan-transfer-inter-bw.csv": return [ (inputs[0]/(1024*1024*(librarian.lookup("Lookup/"+filename, inputs, degree))[0])) + ((librarian.lookup("Lookup/titan-transfer-inter-lat.csv", inputs, degree))[0]) ]

    elif filename == "titan-transfer-intra-bw.csv": return [ (inputs[0]/(1024*1024*(librarian.lookup("Lookup/"+filename, inputs, degree))[0])) + ((librarian.lookup("Lookup/titan-transfer-intra-lat.csv", inputs, degree))[0]) ]

    outputs = librarian.lookup("Lookup/"+filename, inputs, degree)

    return outputs

def lookupEquation(equation, input1):
#def lookupEquation(equation, input1, i_scheme):
    #print ("[lookupEquation] ---  ", equation)
    #print ("inputs")
    #print (input1)              
    #print (i_scheme)
    def add(a,b):
        return (a+b)
    def sub(a,b):
        return (a-b)
    def mul(a,b):
        return (a*b)
    def div(a,b):
        return (a/b)
    def square (a):
        return (a*a)
    def cube (a):
        return (a*a*a)
    def ln(a):
        return (np.log(a))
    def exp(a):
        return (math.exp(a))
    def logtwo(a):
	print (a, math.log2(a))
	return (math.log2(a))
    
    equation_new = "Equations/"+equation
    fp = open(equation_new,'r')
    # equation_expression = str(fp.read())
    length = len(input1)

    lines = fp.read().splitlines()

    for l in lines:
        if len(l) != 0:
            if l[0] != '#':
                variable=l.split("=")
                if variable[0] == "Parameters" or variable[0] == "parameters" or variable[0] == "PARAMETERS":
                    params = variable[1].split(",")
                elif variable[0] == "Equation" or variable[0] == "equation" or variable[0] == "EQUATION":
                    equation_expression = variable[1]
        
    # print(params)
    # print(equation_expression)

    if len(params) != len(input1):
        print ("Number of app parameters in " +equation+ " file does not match AppBEO")
        exit()

    for x in range(length):
        equation_expression = equation_expression.replace(params[x],str(input1[x]))

    #print(equation_expression)

    '''arguments = {'lelt':0,'lx1':0,'alpha':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0}
    list_arguments = ['lelt','lx1','alpha','d','e','f','g','h','i','j']
    size = len(arguments) - len(input1)
    while(size > 0):
        input1.append(0)
        size = size - 1
    for name_argument, value in enumerate(input1):
        arguments[list_arguments[name_argument]] = value'''
    
    output_value = []
    output_value.append(eval(eval(equation_expression)))
    #print ("output value")
    fp.close()
    #print (eval(eval(equation_expression)))
    return (output_value)


if __name__ == "__main__":

    # Perform tests on a few files to make sure things roughly work:

    print lookupValue("vulcan-compute-conv.csv", [17, 256], "polynomial-4")[0]
    print lookupValue("fft-dummy.csv", [128, 128], "polynomial-2")[0]
    print lookupValue("fft-dummy.csv", [99, 10], "linear")[0]
#    print lookupValue("transfer-dummy-A.csv", [999], "lagrange")[0]
#    print lookupValue("transfer-dummy-A.csv", [10], "polynomial-3")[0]

    print lookupValue("transfer-dummy-B.csv", [79], "linear")[0]
#    print lookupValue("transfer-dummy-B.csv", [10], "polynomial")[0]
    print lookupEquation("testPart1.txt", [10])[0]
    print lookupEquation("testPart3.txt", [64,9,10])[0]

#polynomial interpolation needs to be checked


