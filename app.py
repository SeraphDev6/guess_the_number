from flask import Flask, render_template, redirect, request, session
from random import randint
app = Flask(__name__)
app.secret_key = 'asdihbvlkjsdadbvnai'
@app.route('/')
def index():
    if not 'box' in session:
        session['guesses'] = 5
        session['number']=randint(1,100)
        print(session['number'])
        session['box']=""
        session['form']='<form action="/check_num" method="POST"><input type="number" name="num" id="num" step="1" min="1" max="100" value="1"><input type="submit" value="Guess!"></form>'
    return render_template('index.html',box=session['box'], form_val=session['form'])
@app.route('/check_num', methods=['POST'])
def check_num():
    session['guesses'] -=1
    win = False
    if int(request.form['num']) == session['number']:
        win = True
        session['box'] = "<div id='results' class='right'><h2>"+str(session['number'])+" was the number!</h2><h3>You had "+str(session['guesses'])+" guesses remaining!</h3><form action='/submission' method='POST'><input type='text' name='name' id='name' placeholder='Whats your name?' required></input><input type='submit' value='See How You Scored!'></form></div>"
    elif int(request.form['num']) < session['number']:
        session['box'] = "<div id='results' class='wrong'><h2>Too Low</h2><h3>You have "+str(session['guesses'])+" guesses remaining!</h3></div>"
    elif int(request.form['num']) > session['number']:
        session['box'] = "<div id='results' class='wrong'><h2>Too High</h2><h3>You have "+str(session['guesses'])+" guesses remaining!</h3></div>"
    if win:
        session['form']="<a href='/reset'><button>Play again!</button></a>"
    elif session['guesses'] == 0:
        session['form']="<a href='/reset'><button>Play again!</button></a>"
        session['box'] = "<div id='results' class='wrong'><h2>You Lose</h2><h3>:(</h3></div>"
    return redirect('/')
@app.route('/reset')
def reset():
    session.pop('box')
    return redirect('/')
@app.route('/submission', methods=['POST'])
def add_score():
    if 'scores' in session:
        session['scores'].append({'name':request.form['name'],'guesses':5-session['guesses']})
        session['scores']= sorted(session['scores'], key= lambda i: i['guesses'])
        print(session["scores"])
    else:
        session['scores']=[{'name':request.form['name'],'guesses':5-session['guesses']}]
    return redirect('/leaderboard')
@app.route('/leaderboard')
def see_scores():
    return render_template('leaderboard.html',scores=session['scores'])
if __name__ == '__main__':
    app.run(debug=True)