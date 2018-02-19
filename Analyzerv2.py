import javalang
import ast
fp = open("key.txt","r")
text = fp.read()
text = text.split('\n')
fp.close()
file = raw_input("Java code Destination: ")
print '\n'
fp = open(file,'r')
Code = fp.read()
tree = javalang.parse.parse(Code)
tokens =  list(javalang.tokenizer.tokenize(Code))
Keys = {}
Vars = {}
Class = []
Meth = []
Loops = {}
Cond = {}
Search = {}
CodeList = Code.split('\n')
x = 0
count = 0
#for path,node in tree:
#    print node
#for x in tokens:
#    y = str(x)
#    y = y.split(',')
#    y = y[0].split(' ')
#    print y[1],y[3]
while (x < len(tokens)):
    if type(tokens[x]) is javalang.tokenizer.BasicType:
        count+=1
        typename = "(type)" + str(tokens[x].value) +" '"+ str(tokens[x+1].value)+"'"
        Vars[typename] = Vars.get(typename , 0) + 1
    x = x + 1
for x in tokens:
    if x.value in text:
        Keys[str(x.value)] = Keys.get(str(x.value),0) + 1
for path,node in tree.filter(javalang.tree.ClassDeclaration):
    Class.append(str(node.name))
for path,node in tree.filter(javalang.tree.MethodDeclaration):
    Meth.append(str(node.name))
for path,node in tree.filter(javalang.tree.ForStatement):
    Loops["For"] = Loops.get("For",0) + 1
for path,node in tree.filter(javalang.tree.DoStatement):
    Loops["DoWhile"] = Loops.get("DoWhile",0) + 1
for path,node in tree.filter(javalang.tree.WhileStatement):
    Loops["While"] = Loops.get("While",0) + 1
for path,node in tree.filter(javalang.tree.IfStatement):
    Cond["if"] = Cond.get("if",0) + 1
for path,node in tree.filter(javalang.tree.SwitchStatementCase):
    Cond["Switch"] = Cond.get("Switch",0) + 1
print "No. of Methods:",len(Meth)
print "Name of methods:",
for x in Meth:
    print x,
print "\n\nNo. of Classes:",len(Class)
print "Names of Classes:",
for x in Class:
    print x,
print "\n\nKeywords Found with count: "
for x in Keys:
    print x,":",Keys.get(x)  
print "\nVariables Initialized:",count
print "\nVariable Names with count: "
for x in Vars:
    print x,":",Vars.get(x)
fp.close()
print "\nNo.of Loops Used:",len(Loops)
for x in Loops:
    print x,":",Loops.get(x)
print "\nNo.of Conditional Statements used:",len(Cond)
for x in Cond:
    print x,":",Cond.get(x)
print '\n'
Char = raw_input("look for: ")
ctr = 1
chk = 0
chk2 = 0
for x in CodeList:
    y = x.split(' ')
    if Char in y:
        print x,ctr
        chk = 1
        chk2 = 1
    if chk2 == 0:
        if Char in x:
            print x,ctr
            chk = 1
            chk2 = 1
    ctr+=1    
if chk == 0:print "Not Found"
if chk2 == 1:print "Closest matches"