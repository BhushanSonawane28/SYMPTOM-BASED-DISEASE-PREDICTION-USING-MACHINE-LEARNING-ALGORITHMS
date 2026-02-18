from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import secrets
import sys
import DecisionTree
import Randomforest
import NaiveBayes
import csv
import os
print(NaiveBayes.NaiveBayes("constipation","constipation","constipation","constipation","constipation"))
app = Flask(__name__)

app.secret_key = 'thisissingh98250'
secret_key = secrets.token_hex(16)
# example output, secret_key = 000d88cd9d90036ebdd237eb6b0db000
app.config['SECRET_KEY'] = secret_key

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem" 
 

 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'geeklogin'
 
mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg1=''
    global  username
    global  account

    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['username'] = account['username']
            msg1 = 'Logged in successfully !'
            return redirect("list", code=302)
            #return render_template('list.html', msg1 = msg1)
            #return "asdsdad"
            #return list()
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg1 = msg1)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)
    if session['username'] == account['username']:
        msg1='success'
        return print('succes')
@app.route('/list')
def list():
    
    symtoms = ['back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
    'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
    'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
    'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
    'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
    'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
    'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
    'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
    'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
    'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
    'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
    'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
    'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
    'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
    'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
    'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
    'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
    'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
    'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
    'yellow_crust_ooze']

    try:
        if session['username']:
            return render_template('list.html', len=len(symtoms), symtoms = symtoms)
    except:
        return redirect("login", code=302)
    return render_template('list.html', len=len(symtoms), symtoms = symtoms)
    
@app.route('/process')
def process():
    msg = ''
    symtoms1 = request.args.get('symtoms1')
    symtoms2 = request.args.get('symtoms2')
    symtoms3 = request.args.get('symtoms3')
    symtoms4 = request.args.get('symtoms4')
    symtoms5 = request.args.get('symtoms5')
    
    
    submit = request.args.get('submit')
    
    
   
    if (submit == 'decisiontree'):
     return DecisionTree.DecisionTree(symtoms1,symtoms2,symtoms3,symtoms4,symtoms5)
    elif (submit == 'randomforest'):
     #return 'randomforest'
     return Randomforest.RandomForest(symtoms1,symtoms2,symtoms3,symtoms4,symtoms5)
     #return render_template('process.html')
    elif (submit == 'naivebayes'):
     #return 'NaiveBayes'
     return NaiveBayes.NaiveBayes(symtoms1,symtoms2,symtoms3,symtoms4,symtoms5)
     #return render_template('process.html')
    elif (submit == 'all'):
      DT = DecisionTree.DecisionTree(symtoms1,symtoms2,symtoms3,symtoms4,symtoms5)
      RF = Randomforest.RandomForest(symtoms1,symtoms2,symtoms3,symtoms4,symtoms5)
      NB = NaiveBayes.NaiveBayes(symtoms1,symtoms2,symtoms3,symtoms4,symtoms5)
      FR = ""
      if(DT == RF):
        FR = RF
      elif(DT == NB):
        FR = NB
      elif(RF == NB):
        FR = NB
      else:
        FR = DT
      with open('symtoms.csv', 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        #header= ["UserName","symtoms","symtoms2","symtoms3","symtoms4","symtoms5", "Prediction"]
        #writer.writerow(header)        
        data =[username, symtoms1, symtoms2, symtoms3, symtoms4, symtoms5, FR]
        writer.writerow(data)
        f.close()
        
      return render_template('process.html', msg=FR)
      #return "All____" + DT + "_____"+ RF + "_____" + NB + "<br>" + FR
    
    #return symtoms1 + "  " + symtoms2 + " " + symtoms3 + "  " + symtoms4 + " " + symtoms5 + result
    #return render_template('process.html')
    
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        
        return f'{name}, your username is {username}'
    return render_template('list.html', msg=msg)


if __name__ == '__main__':  
    app.run(debug = True,port=3736)  
