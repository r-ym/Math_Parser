from decimal import *
import unittest

class TestStringMethods(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(evaluate('7+8'),'15.00')
        self.assertEqual(evaluate('(9+3)+6'),'18.00')
        self.assertEqual(evaluate('(7.44    +5)+(6+4)'),'22.44')
    def test_subtraction(self):
        self.assertEqual(evaluate('7-8'),'-1.00')
        self.assertEqual(evaluate('(6-2)-3'),'1.00')
        self.assertEqual(evaluate('(67-   45.3)-(    2-1.5)'),'21.20')
    def test_multiplication(self):
        self.assertEqual(evaluate('7*8.24'),'57.68')
        self.assertEqual(evaluate('80*63*(54.2)'),'273168.00')
        self.assertEqual(evaluate('(8*4.6)*(5)'),'184.00')
    def test_division(self):
        self.assertEqual(evaluate('6/3'),'2.00')
        self.assertEqual(evaluate('(9/  2)/1.5'),'3.00')
        self.assertEqual(evaluate('(42/14)/  1.5/0.5'),'4.00')
    def test_all(self):
        self.assertEqual(evaluate('(42/14)+(1.5*  0.5)-3'),'0.75')
        self.assertEqual(evaluate('(((    7   )))*3+   90.66/3-18'),'33.22')
        self.assertEqual(evaluate('23-12+5*44/4'),'-44.00')
#returns a list of all operator indexes, while avoiding all negative sgins
def exp_list(string):
    exp=[]
    for i in range(0,len(string)):
        if string[i]=="+" or string[i]=="*" or string[i]=="/":
            exp.append(i)
        elif string[i]=="-" and not(string[i-1] in ['+','-','*','/']) and not(i==0):
            exp.append(i)
    return exp
#gets the first instance in a list or string (used to check for first plus/minus/division/multiplication sign), or the index of the first sign within the list of operator indices.
#the count variable is turned to 1 to account for any '-' sign at the start of the string due to negative numbers. only used in the _subtract function
def get_first (operator,iterable,count=0):
    for i in range(count,len(iterable)):
        if iterable[i]==operator:
            return i
#div function
def _div(string):
    while ('/' in string):
        #gets the operator index
        index = exp_list(string)
        #get first '/' instance
        div = get_first('/',string)
        #gets index for the first instance within the operator index
        operator=get_first(div,index)
        #flags to check for whether the operation will occur at the head or tail of the string, which will require different indices to stitch the string back
        head=False
        tail=False
        #error indicates the value left/right to the operator is at the strings head/tail, indices are changed accordingly and the flags are turned
        try:
            #print('1st')
            v1 = Decimal((string[(index[operator-1]+1):(index[operator])]))
            #print(v1)
        except (IndexError,DecimalException):
            v1 =Decimal((string[:(index[operator])]))
            head=True
            #print(v1)
        try:
            #print('2nd')
            v2 = Decimal(((string[index[operator]+1:index[operator+1]])))
            #print(v2)
        except (IndexError,DecimalException):
            v2 = Decimal((string[(index[operator]+1):]))
            tail = True
        #value calculated and rounded to two decimal places for the ~aesthetics~
        value = round(v1/v2,2)
        #check to see if this was the operation to be done, if so the value is returned as a string. if not the head/tail flags govern the stitching with specific indexing
        if len(index)==1:
                string = str(value)
        elif head:
            #print(head)
            string = str(value)+string[index[operator+1]:]
        elif tail:
            
            string = string[:index[operator-1]+1]+str(value)
        else: 
            string = string[:(index[operator-1]+1)] + str(value) + string[index[operator+1]:]     
    return string
#almost all operator functions work similar to each other, save for sub function
def _multi(string):
    
    while ('*' in string):
        index = exp_list(string)
        #print(index)
        multi = get_first('*',string)
        #print(multi)
        operator=get_first(multi,index)
        #print(operator)
        head=False
        tail=False
        try:
            #print('1st')
            v1 = Decimal((string[(index[operator-1]+1):(index[operator])]))
            #print(v1)
        except (IndexError,DecimalException):
            #print(string)
            v1 =Decimal((string[:(index[operator])]))
            head=True
            #print(v1)
        try:
            #print('2nd')
            v2 = Decimal(((string[index[operator]+1:index[operator+1]])))
            #print(v2)
        except (IndexError,DecimalException):
            v2 = Decimal((string[(index[operator]+1):]))
            tail = True
            #print(v2)
        value = round(v1*v2,2)
        if len(index)==1:
                string = str(value)
        elif head:
            #print(head)
            string = str(value)+string[index[operator+1]:]
        elif tail:
            
            string = string[:index[operator-1]+1]+str(value)
        else: 
            string = string[:(index[operator-1]+1)] + str(value) + string[index[operator+1]:]     
    return string

def _add(string):
        while ('+' in string):
            index = exp_list(string)
            #print(index)
            adder = get_first('+',string)
            #print(adder)
            operator=get_first(adder,index)
            #print(operator)
            head=False
            tail=False
            try:
                #print('1st')
                v1 = Decimal((string[(index[operator-1]+1):(index[operator])]))
                #print(v1)
            except (IndexError,DecimalException):
                v1 =Decimal((string[:(index[operator])]))
                head=True
                #print(v1)
            try:
                #print('2nd')
                v2 = Decimal(((string[index[operator]+1:index[operator+1]])))
                #print(v2)
            except (IndexError,DecimalException):
                v2 = Decimal((string[(index[operator]+1):]))
                tail = True
                #print(v2)
            value = round(v1+v2,2)
            if len(index)==1:
                string = str(value)
            elif head:
                #print(head)
                string = str(value)+string[index[operator+1]:]
            elif tail:
                
                string = string[:index[operator-1]+1]+str(value)
            else: 
                string = string[:(index[operator-1]+1)] + str(value) + string[index[operator+1]:]     
        return string

def _sub(string):
        while ('-' in string):
            index = exp_list(string)
            #clause to break as the while loop will keep running if a negative number remains with no operations to be done
            if index==[]:
                break
            #1 used for count to disregard all leading negative signs
            subt = get_first('-',string,1)
            #print(subt)
            operator=get_first(subt,index)
            #print(operator)
            head=False
            tail=False
            try:
                #print('1st')
                v1 = Decimal((string[(index[operator-1]+1):(index[operator])]))
                #print(v1)
            except (IndexError,DecimalException):
                v1 =Decimal((string[:(index[operator])]))
                head=True
                #print(v1)
            try:
                #print('2nd')
                v2 = Decimal(((string[index[operator]+1:index[operator+1]])))
                #print(v2)
            except (IndexError,DecimalException):
                v2 = Decimal((string[(index[operator]+1):]))
                tail = True
                #print(v2)
            value = round(v1-v2,2)
            #print(value)
            if len(index)==1:
                string = str(value)
            elif head:
                #print(head)
                string = str(value)+string[index[operator+1]:]
            elif tail:
                string = string[:index[operator-1]+1]+str(value)
            else: 
                string = string[:(index[operator-1]+1)] + str(value) + string[index[operator+1]:]
            
        return string

class Math_exp():
    def __init__(self,string):
#removes all whitespace
        self.string=string.replace(" ","")

    def parentheses_evaluator(self):
        #flag that checks True when both '(' index and ')' index are ascertained
        flag = False
        p1=0
        p2=len(self.string)
        i = 0
        i_i=0
        while i < len(self.string):
            if flag:
                break
            #loops thru till '('
            if self.string[i] == "(": 
                p1 = i
                i_i=i+1
                while i_i < len(self.string):
                    #then checks for ')' from there
                    if self.string[i_i] == ")":
                        #if found will return the second index and break
                        p2 = i_i
                        flag=True
                        break
                    elif self.string[i_i] == "(":
                        #if '(' found again break to continue looping rightward to find the most inward pair
                        break
                    else:
                        i_i+=1
            i+=1
        return [p1,p2]
def evaluate(TEST):
    #initialzes class with the input string
    expression=Math_exp(TEST)
    
    #checks to see if no operators or parentheses remain in the string
    while not(exp_list(expression.string)==[]) or ('(' in expression.string):       

        #print(expression.string)
        index=expression.parentheses_evaluator()
        
        #if first character is a parentheses function corrects for it with different indexing for each case
        if index==[0,len(expression.string)]:
            sliced = expression.string[index[0]:index[1]]
        else:
            sliced = expression.string[index[0]+1:index[1]]
        #runs the functions in nested order of DMAS
        sliced = _sub(_add(_multi(_div(sliced))))
        #stitches the value in, then loops till a single value is returned
        expression.string = expression.string[:index[0]] + sliced + expression.string[index[1]+1:]
       
    return expression.string

if __name__ == '__main__':
    unittest.main()


            
            

