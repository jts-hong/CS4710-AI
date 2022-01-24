##### Filename: util.py
##### Author: {Scott Hong}
##### Date: {8/25/21}
##### Email: {jh4ctf}

import copy

def helper(lst,start,number_from=0):
    if(len(lst)==1):
        base=[]
        base.append(lst[0]+number_from+start)
        return base
    else:
        output = []
        output.append(lst[0]+start+number_from)
        return output+helper(lst[1:],start,number_from+1)

class Util:

    ## Problem 1
    def matrix_multiply(self, x, y):

        a = len(x)
        b = 0
        for i in y[0]:
            b+=1
        result = [[0 for x in range(b)] for y in range(a)]  
        for i in range(len(x)):
            for j in range(len(y[0])):
               for k in range(len(y)):
                    result[i][j] += x[i][k] * y[k][j]
        #Citing from source https://www.programiz.com/python-programming/examples/multiply-matrix
        #print(result)
        return result
    ## Problem 2, 3
    class MyQueue:
        def __init__(self):
            self.item = []
        def push(self, val):
            self.item.insert(0,val)
        def pop(self):
                return self.item.pop()
        def __eq__(self, other):
            return self.item ==other

        def __ne__(self, other):
            return not(self.item ==other)
                        
        def __str__(self):
            re = "["
            for i in self.item:
                re+=str(i)
                re+=","
            re1 = re.rstrip(re[-1])
            re1+="]"
            print(re1)

    class MyStack:
        def __init__(self):
            self.s = []
        def push(self, val):
            self.s.append(val)
        def pop(self):
            if len(self.s) <= 0:
                return None
            else:   
                return self.s.pop()
        def __eq__(self, other):
            return self.s ==other

        def __ne__(self, other):
            return not(self.s == other)
        def __str__(self):
            re = "["
            for i in self.s:
                re+=str(i)
                re+=","
            re1 = re.rstrip(re[-1])
            re1+="]"
            print(re1)

    ## Problem 4
    def add_position_iter(self, lst, number_from=0):
        res = []
        for i in range(len(lst)):
            res.append(number_from)
            res[i]+= lst[i]
            res[i] +=i
        return res

    def add_position_recur(self, lst, number_from=0):
        return helper(lst,0,number_from)
        

    def add_position_map(self, lst, number_from=0):
        result = list(map(lambda x: x+lst.index(x)+number_from, lst))
        return result

    ## Problem 5
    def remove_course(self, roster, student, course):
        if course in roster[student]:
            roster[student].remove(course)

    ## Problem 6
    def copy_remove_course(self, roster, student, course):
        new_ro = copy.deepcopy(roster)
        self.remove_course(new_ro, student, course)
        #print(roster)
        #print(new_ro)
        return new_ro


#ret = Util().add_position_iter([7, 5, 1, 4]) 
#print(ret)
#assert(ret == [7, 6, 3, 7])
"""
ret = Util().add_position_map([7, 5, 1, 4]) 
assert(ret == [7, 6, 3, 7])


roster = {'kyu': set(['cs182']), 'david': set(['cs182'])} 
Util().remove_course(roster, 'kyu', 'cs182')
assert(roster == {'kyu': set([]), 'david': set(['cs182'])})


roster = {'kyu': set(['cs182']), 'david': set(['cs182'])} 
new_roster = Util().copy_remove_course(roster, 'kyu', 'cs182') 
assert(roster == {'kyu': set(['cs182']), 'david': set(['cs182'])}) 
assert(new_roster == {'kyu': set([]), 'david': set(['cs182'])})
"""
"""
rr= Util().MyQueue()
rr.push(1); 
rr.push(2) 
rr.push(3)
rr.push(4)
rr.__str__()
"""
# should evaluate to assert(q.pop() == 1)
#mm = ut.matrix_multiply([[1, 2, 3], [3, 4, 5],[6,7,8],[1,2,3]], [[5, 6], [7, 8],[8,9]])
#print(mm)
