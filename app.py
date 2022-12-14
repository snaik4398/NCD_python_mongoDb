### Integrate HTML With Flask
### HTTP verb GET And POST
import collections
import email
from gc import collect
from lib2to3.pgen2 import pgen
from math import pi
from pdb import post_mortem
from tkinter import Variable
from typing import Collection
from unicodedata import name
from flask import Flask,redirect,url_for,render_template,request
import pymongo
import random



app=Flask(__name__)
# welcome page
@app.route('/')
def welcome():
    return render_template('signup.html')
# when we tap to the back button it will go to the index.html page 
@app.route('/back',methods=['POST','GET'])
def back():
    if request.method=='POST':
        return render_template('signup.html')
def bio():
    return  ' Name: '+pname+'   Email: '+pemail+'   Gender: ' +pgender+' D.O.B: '+pdob+'  PIN: '+ppin+' '
    

@app.context_processor
def context_processor():
     # if we directly return the value then its showing not definedName=pname,Email=pemail,Gender=pgender,Dob=pdob,PIN=ppin 
    return dict(bio=bio)

def home():
    #when we are trying to re render it its showing method not allowed 
    return redirect(url_for('welcome'))
    
    # return redirect('/')

# def emailsave(mail):
#     global email
#     email=mail


def making_global_info(name,mail,pin,gender,dob,id):

    global pemail,pdob,pgender,ppin,pname,gpid
    pname=name
    pemail=mail
    pdob=dob
    pgender=gender
    ppin=pin
    gpid=id

def randomPat_id(digits):
    lower = 10**(digits-1)
    upper = 10**digits - 1
    return random.randint(lower, upper)


@app.route('/success/<int:score>')
def success(score):
    res=""
    print(score)
   
    if score>=4:
        res="NEED TO CHECHK UP"
    else:
        res="NO NEED TO CHECHK UP"
    # here email is a global variable that we are trying to access
    prev={"pat_id":gpid}
    nextt={"$set":{"result":res,
                    "score":score             
                }}
    collections.update_one(prev,nextt)


    return render_template('result.html',result=res,sc=score,id=gpid)


@app.route('/fail/<string:s>')
def fail(s):
    return s+"     please enter the valid input as written in the webpage"

### Result checker submit html page
@app.route('/signup/',methods=['POST','GET'])
def signup():
    # creating the local variable inside the function to fetch the values from the form 
    name1 =" "
    email1=" "
    gen1=" "
    pin=" "
    dob= " "
    pat_id=0

    # in the form we mention method=POST so the request object need to go by the post methods 
    if request.method=='POST':
        name1=request.form['fname']
        name1+=" "
        name1+= request.form['lname']

        gen1=request.form['gender']
        dob=request.form['birthday']
        email1=request.form['email']
        pin=request.form['pincode']
        pat_id=randomPat_id(14)#will return random patient id of 14 digit every time
        
# calling a normal pyhton function to store the  fetching email value (from the form that is created in the signup page) and in that funcion we assign to a global variable email
    making_global_info(name1,email1,pin,gen1,dob,pat_id)
    
    # creating a dictionary in pyhton to store it in mongo db as it is similar to jason format so it wll wasy to store in this way 
    # also dictionary is mutable so we can change the stored value
    patient_info_dictionary={
        'pat_id':pat_id,
        'name':name1,
        'gender':gen1,
        'date_of_birth':dob,
        'email_id':email1,
        'pincode':pin
        
    }
    # checking the global email variable is initiated or not by by printing it in console
    # print(email)

    collections.insert_one(patient_info_dictionary)  
    return render_template('index.html',nm=name1,gen=gen1,pin=pin,dob=dob,email=email1,id=pat_id)





# after pressing the submit button in the index.html page  app.route(/submit ) is going to executed  
@app.route('/submit',methods=['POST','GET'])
def submit():
    # declaring global Variable to use within the submit function
    total_score=0
    # mail=email
    c=0

    if request.method=='POST':
        a1=int(request.form['age'])
        if (a1>3 or a1<0):
            return redirect(url_for('fail',s="invalid input"))
        p2=int(request.form['2pp'])
        if (p2>2 or p2<0):
            return redirect(url_for('fail',s="invalid input"))     
        p3=int(request.form['3pp'])
        if (p3>1 or p3<0):
            return redirect(url_for('fail',s="invalid input"))
        p4=int(request.form['4pp'])
        if (p4>3 or p4<0):
            return redirect(url_for('fail',s="invalid input"))
        p5=int(request.form['5pp'])
        if (p5>2 or p5<0):
            return redirect(url_for('fail',s="invalid input"))
        p6=int(request.form['6pp'])
        if (p6>2 or p6<0):
            return redirect(url_for('fail',s="invalid input"))
    
        total_score=(a1+p2+p3+p4+p5+p6)
      
   
    # sendind the total score to success function 
    return redirect(url_for('success',score=total_score))

    



if __name__=='__main__':
    client = pymongo.MongoClient("mongodb://localhost:27017")
    print(client)
    # print(email)
    db = client['pat_info']
    collections = db['information']
    print(email)
   
 
    app.run(debug=True,port=4398)