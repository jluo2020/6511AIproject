#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import copy, random
import numpy as np

class csp_back_tracking: #csp
    def __init__(self, k, input): # k is the amount of colors, and input is the constraints.
        self.assignment={} # Store result in this dict
        self.connection={} # Store the connecion relationship
        self.domain=[] # Store the color domain
        self.constraint=[] # Store the binary constraints
        self.load_data(input) # Load input data
        self.get_domain(k) # Set the orignal domain space
        self.set_parameter() # Set the orignal domain space
        self.k=k 
        self.variable_index={} # Store the number of connected cities for each city.
        for key, value in self.connection.items():
                self.variable_index.setdefault(key, len(value))
        self.forward_checking_processing()

    def set_parameter(self): #
        def transfer(*args): # A tuple has been introduced to allocate the int variable, due to the list object is unhashable while updating dict. Besides, the *args can easily forge multiple int variables in a single tuple.
            return args
        self.variable=[]
        self.allocated_variable=[]
        for key, value in self.connection.items(): # Set the constraints
            self.assignment.setdefault(key)
            self.variable.append(key)
            for j in range(0, len(value)):
                if key< value[j]:
                    constraint=transfer(key, value[j])
                else:
                    constraint=transfer(value[j], key)
                if constraint not in self.constraint:
                    self.constraint.append(constraint)
    
    def load_data(self, input):  # Set the connecions.
        def transfer(*args):
            return args
        for connect in input:
            if connect[0] not in self.connection.keys():
                self.connection.setdefault(connect[0],transfer(connect[1]))
            else:
                if connect[1] not in self.connection[connect[0]]:
                    self.connection[connect[0]]+=transfer(connect[1])
            if connect[1] not in self.connection.keys():
                self.connection.setdefault(connect[1],transfer(connect[0]))
            else:
                if connect[0] not in self.connection[connect[1]]:
                    self.connection[connect[1]]+=transfer(connect[0])
                
    def forward_checking_processing(self): 
        self.all_domain={}
        for key in iter(self.connection.keys()):
            colors=copy.deepcopy(self.domain)
            random.shuffle(colors)
            self.all_domain.setdefault(key, colors)
        
    def forward_checking(self, variable, value): #forward checking with AC-3
        def transfer(*args):
            return args
        bash=[]
        self.removed_by_checking={}
        bash.append(value)
        for neighbor in self.connection[variable]:
            if neighbor in self.allocated_variable:
                continue
            elif self.all_domain[neighbor]==bash:
                self.removed_by_checking={}
                return 0
            elif len(self.all_domain[neighbor])==0: 
                self.removed_by_checking={}
                return 0
            elif value in self.all_domain[neighbor]:
                self.removed_by_checking.setdefault(neighbor, value)
        for k1,v1 in self.removed_by_checking.items():
            self.all_domain[k1].remove(v1)
        return 1
    
    def get_domain(self, k=4):
        self.color_store={'Gold':(220,20,220), 'Green':(0, 255, 0), 'Blue':(255, 0, 0), 'White':(255, 255, 255)}
        if k > len(self.color_store):
            raise KeyError('No enough colors to allocate.')
        sup=0
        for color in iter(self.color_store):
            if sup==k:
                break
            self.domain.append(color)
            sup+=1
    
    def back_tracking_search(self):
        return self.back_track()
           
    def back_track(self):
        def test_assignment():
            counter=0
            for k, v in self.assignment.items():
                if v!=None:
                    counter+=1
            if counter==len(self.assignment):
                return 1
            else:
                return 0

        def test_constraint():
            for variable in self.allocated_variable:
                for neighbor in self.connection[variable]:
                    if self.assignment[variable]==None:
                        return 1
                    if self.assignment[variable]==self.assignment[neighbor]:
                        return 0
            return 1

        def select_unassigned_variable(var): # Minimum remaining values (List-constraint value)
            for j in range(len(self.variable)-1, 0, -1):
                for i in range(0, j ):
                    if self.variable_index[self.variable[i]]>self.variable_index[self.variable[i+1]]:
                        self.variable[i], self.variable[i+1] = self.variable[i+1], self.variable[i]   
          
        def order_domain_values(var): # min conflicts
            def list_move_left(A,a):
                for i in range(a):
                    A.insert(len(A),A[0])
                    A.remove(A[0])
                return A
            f=0
            for k, v in self.all_domain.items():
                if k==var:
                    f=1
            if f==1:
                list_move_left(self.all_domain[var],1)
            else:
                return
        if test_assignment() and test_constraint():
            return 1            
        var=self.variable.pop(-1)
        select_unassigned_variable(var)
        self.allocated_variable.append(var) 
        order_domain_values(var)
        for color in self.all_domain[var]:
            self.all_domain[var].remove(color)
            if test_constraint():
                self.assignment[var]=color
                if self.forward_checking(var, color):
                    del self.all_domain[var]
                    return self.back_track()
                else:    
                    if len(self.removed_by_checking)>0:  
                        for k1,v1 in self.removed_by_checking.items():
                            cache=copy.deepcopy(self.all_domain[k1])
                            cache.append(v1)
                            del self.all_domain[k1]
                            self.all_domain.setdefault(k1,cache)
                            del cache
        buffer=self.allocated_variable.pop(-1)
        self.variable.append(buffer)
        self.assignment[var]=None
        return 0
        

flag=0
constraint=[(1,2),(1,3),(1,4),(1,5),(2,3),(2,4),(2,6),(2,7),(3,5),(3,6),(3,7),(4,5),(4,6),(4,7),(5,6),(5,7),(6,7)]
for i in range(0, 99999):
    flag+=1
    B=csp_back_tracking(4, constraint)
    a=B.back_track()
    if a==1:
        print(B.assignment)
        print('Okay!!!!')
        break
    else:
        print('again')
        del B
