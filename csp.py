"""CSP (Constraint Satisfaction Problems) problems and solvers. (Chapter 6)."""
"""Adapted from https://github.com/aimacode/aima-python"""

from utils import argmin_random_tie, count, first
import search

from collections import defaultdict
from functools import reduce

import itertools
import re
import random
import sys, getopt


class CSP(search.Problem):
    """This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
        variables   A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b


    The following are just for debugging purposes:
        display(a)              Print a human-readable representation
    """

    def __init__(self, variables, domains, neighbors, constraints):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        variables = variables or list(domains.keys())

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0


    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""
        # Subclasses may implement this more efficiently
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment))
        return count(conflict(v) for v in self.neighbors[var])

    def display(self, assignment):
        """Show a human-readable representation of the CSP."""
        # Subclasses can print in a prettier way, or display with a GUI
        print('CSP with assignment:', assignment)

    def actions2(self, var, assignment):
        domain = []
        if var in assignment:
            #if assignment[var]
            domain.append(assignment[var])
            print(var, "sadas")
        else:
            domain = [val for val in self.domains[var] if (self.nconflicts(var, val, assignment) == 0)]

        return domain


    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    # These are for constraint propagation

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)


# ______________________________________________________________________________
# CSP Backtracking Search

# Variable ordering


def first_unassigned_variable(assignment, csp):
    """The default variable order."""
    return first([var for var in csp.variables if var not in assignment])

# Value ordering


def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var)


# Inference
def no_inference(csp, var, value, assignment, removals):
    return True

# The search, proper


def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    """[Figure 6.5]"""
    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)

        for value in order_domain_values(var, assignment, csp):
            print("Value = ", value)
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                #gui.circle_assigment(int(var),value)
                removals = csp.suppose(var, value)
                update_domain(csp,assignment)
                if inference(csp, var, value, assignment, removals):
                    #gui.wait()
                    inpt = input()
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        #gui.circle_unassigment(int(var))
        #gui.wait()
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result

def update_domain(csp, assignment):
    print('\n')

    csp.display(assignment)
    for Xi in csp.variables:
        #domain = csp.curr_domains[Xi]
        print("Asignados",assignment,Xi)
        domain = csp.actions2(Xi,assignment)
        print(Xi, '->', domain)







#
#-------------------- CSP problem formulation ----------------
#
# Constraint : neigboring nodes cannot have the same color
def different_values_constraint(A, a, B,assignment):
    """A constraint saying two neighboring variables must differ in value."""
    Restriccion = {'F': ['T','D'],
    			 'D': ['F','M'],
    			 'M': ['D','P'],
    			 'P': ['M','T'],
    			 'T': ['P','F']}
    print("Values",A,a,B,assignment[B])
    return (a != assignment[B]) #and not(a in Restriccion[b)
    '''for id,node in assignment.items():
        if a == node:
            return 0
    return'''

# Nine variables in the graph, ID of variables: numbers from 0 to 8
variables = list(range(1,6))
# Definition of neighbourhood for each variable
neighbors = {1: [3,4,5],
			 2: [1,3,5],
			 3: [1,2],
			 4: [1,3,5],
			 5: [2,4]}
# Initially, all variables have as domain {red, green, blue} colors
domains = dict.fromkeys(variables, 'FDMPT')
print(domains)
# Construction of the CSP problem
network = CSP(variables, domains, neighbors, different_values_constraint)
#
#----------------------------------------------------------

#
#- Main program --------
#
# Initiallize gui inteface
# gui.init_gui()
# # Solve CSP problem
# # backtracking_search(csp,
# #                     select_unassigned_variable=first_unassigned_variable,
# #                     order_domain_values=unordered_domain_values,
# #                     inference=no_inference)
# result = backtracking_search(network, inference=mac)
# gui.wait()


def main(argv):
	#gui.init_gui()

	result = backtracking_search(network)

	#gui.wait()


if __name__ == "__main__":
	main(sys.argv[1:])
