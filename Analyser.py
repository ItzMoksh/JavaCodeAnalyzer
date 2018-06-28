import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import javalang
import ast
fp = open("key.txt","r")
text = fp.read()
text = text.split('\n')
fp.close()
UPLOAD_FOLDER = '\uploads'
ALLOWED_EXTENSIONS = set(['.java'])
app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/our_team')
def our_team():
	return render_template('our_team.html')

@app.route('/login')
def home():
	return render_template('login.html')

@app.route('/about')
def about():
	return render_template('about.html')
	
@app.route('/index', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if request.form['uname'] == 'admin':
			if request.form['pass'] == 'abcd':
				return render_template('index.html')
			else:
				error="Invalid Username or Password"
				return render_template('login.html', error=error)
		else:
			error="Invalid Username or Password"
			return render_template('login.html', error=error)

	else:
		return render_template('login.html')


@app.route('/file', methods = ['GET', 'POST'])
def action():
	if request.method == 'POST':
		f = request.files['file']
		fn = secure_filename(f.filename)
		#fn = fn.rsplit('.', 1)[1].lower()
		f.save(fn)
		fp = open(fn,"r")
		CodeStr = fp.read()
		return render_template('result.html', fn=fn)
		
	else:
		return render_template('index.html')

@app.route('/show', methods=['GET', 'POST'])
def show():
	result=request.form
	file=result.get("fname", "")
	fp = open(file,'r')
	CodeStr = fp.read()
	tree = javalang.parse.parse(CodeStr)
	tokens = list(javalang.tokenizer.tokenize(CodeStr))
	Keys = {}
	Vars = {}
	Class = []
	Meth = []
	Loops = {}
	Cond = {}
	Search = {}
	CodeList = CodeStr.split('\n')
	x = 0
	count = 0

	if request.method == 'POST':
		

		if request.form['submit'] == 'Keywords':
			for x in tokens:
				if x.value in text:
					Keys[str(x.value)] = Keys.get(str(x.value),0) + 1
			return render_template('result.html', Keys=Keys, fn=file)
		

		elif request.form['submit'] == 'Variables':
			while (x < len(tokens)):
			    if type(tokens[x]) is javalang.tokenizer.BasicType:
			        count+=1
			        typename = str(tokens[x].value) +" '"+ str(tokens[x+1].value)+"'"
			        Vars[typename] = Vars.get(typename , 0) + 1
			    x = x + 1
			return render_template('result.html', Vars=Vars, fn=file, count=count)
		

		elif request.form['submit'] == 'Classes':
			for path,node in tree.filter(javalang.tree.ClassDeclaration):
				Class.append(str(node.name))
			return render_template('result.html', Class=Class, fn=file)
		

		elif request.form['submit'] == 'Methods':
			for path,node in tree.filter(javalang.tree.MethodDeclaration):
				Meth.append(str(node.name))
			return render_template('result.html', Meth=Meth, fn=file)
		

		elif request.form['submit'] == 'Loops':
			for path,node in tree.filter(javalang.tree.ForStatement):
				Loops["For"] = Loops.get("For",0) + 1


			for path,node in tree.filter(javalang.tree.DoStatement):
				Loops["DoWhile"] = Loops.get("DoWhile",0) + 1


			for path,node in tree.filter(javalang.tree.WhileStatement):
				Loops["While"] = Loops.get("While",0) + 1
			
			return render_template('result.html', Loops=Loops, fn=file)
		

		elif request.form['submit'] == 'Conditions':
			for path,node in tree.filter(javalang.tree.IfStatement):
				Cond["if"] = Cond.get("if",0) + 1


			for path,node in tree.filter(javalang.tree.SwitchStatementCase):
				Cond["Switch"] = Cond.get("Switch",0) + 1
			
			return render_template('result.html', Cond=Cond, fn=file)
		

		elif request.form['submit'] == 'Back':
			return render_template('index.html')
	else:
		return render_template('result.html')	        


if __name__ == '__main__':
	app.run(debug = True)