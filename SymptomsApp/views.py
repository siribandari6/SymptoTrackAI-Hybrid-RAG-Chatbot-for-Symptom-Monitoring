from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
import pymysql
from transformers import AutoTokenizer, RagRetriever, RagSequenceForGeneration, RagTokenForGeneration
import torch
import faiss
import numpy as np
import pandas as pd
import pickle
import re
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# MySQL Database Configuration
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '11189121')
DB_NAME = os.getenv('DB_NAME', 'symptoms')

global username

tokenizer = AutoTokenizer.from_pretrained("facebook/rag-sequence-nq")
try:
    retriever = RagRetriever.from_pretrained("facebook/rag-sequence-nq")
    model = RagSequenceForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)
except Exception as e:
    print(f"Warning: RAG retriever initialization failed ({str(e)}). Using model without retriever.")
    # Initialize model without retriever for question encoding only
    model = RagSequenceForGeneration.from_pretrained("facebook/rag-token-nq")


if os.path.exists("model/faiss.pckl"):
    f = open('model/faiss.pckl', 'rb')
    faiss_index = pickle.load(f)
    f.close()
    Y = np.load("model/Y.npy")
else:
    X = []
    Y = []
    dataset = pd.read_csv("Dataset/Symptom2Disease.csv", usecols=['label','text'])
    dataset = dataset.values
    for i in range(len(dataset)):
        try:
            disease = dataset[i,0]
            data = dataset[i,1].strip('\n').strip().lower()
            data = re.sub('[^a-z]+', ' ', data)
            inputs = tokenizer(data, return_tensors="pt")
            input_ids = inputs["input_ids"]
            symptoms_hidden_states = model.question_encoder(input_ids)[0]
            symptoms_hidden_states = symptoms_hidden_states.detach().numpy().ravel()
            X.append(symptoms_hidden_states)
            Y.append(disease)
            print(str(i)+" "+str(len(data)))
        except:
            print(data+"===============================================================")
            pass
    X = np.asarray(X)
    print(X.shape)
    dimension = X.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(X)
    print(faiss_index)
    f = open('model/faiss.pckl', 'wb')
    pickle.dump(faiss_index, f)
    f.close()
    Y = np.asarray(Y)
    np.save("model/Y", Y)

def ViewLog(request):
    if request.method == 'GET':
        global username
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="3" color="black">Username</th><th><font size="3" color="black">Symptoms Text</th>'
        output+='<th><font size="3" color="black">Predicted Advice</th><th><font size="3" color="black">Logged & Monitored Time</th></tr>'
        scores = []
        labels = []
        con = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from log where username='"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                output+='<tr><td><font size="3" color="black">'+row[0]+'</td>'
                output += '<td><font size="3" color="black">'+str(row[1])+'</td>'
                output += '<td><font size="3" color="black">'+str(row[2])+'</td>'
                output += '<td><font size="3" color="black">'+row[3]+'</td></tr>' 
        output+= "</table></br></br></br></br>" 
        context= {'data':output}
        return render(request, 'UserScreen.html', context)        

def logData(username, question, advice):
    now = datetime.now()
    current_datetime = str(now.strftime("%Y-%m-%d %H:%M:%S"))
    db_connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset='utf8')
    db_cursor = db_connection.cursor()
    # Use parameterized query to prevent SQL injection
    student_sql_query = "INSERT INTO log VALUES(%s, %s, %s, %s)"
    db_cursor.execute(student_sql_query, (username, question, advice, current_datetime))
    db_connection.commit()    
    

@csrf_exempt
def ChatData(request):
    if request.method == 'GET':
        global tokenizer, faiss_index, Y, username
        question = request.GET.get('mytext', False)
        inputs = tokenizer(question, return_tensors="pt")
        input_ids = inputs["input_ids"]
        query = model.question_encoder(input_ids)[0]
        query = query.detach().numpy()
        print(query.shape)
        distances, indices = faiss_index.search(query, k=1)
        output = ""
        for i, idx in enumerate(indices[0]):
            logData(username, question, Y[idx])
            output += "Predicted Advice Based on Symptoms = "+Y[idx]
            output+= "Requested to take "+Y[idx]+" medicines to cure disease"
            break
        if len(output) == 0:
            output = "Sorry! Chatbot model unaware of this symptoms"
        return HttpResponse("Chatbot: "+output, content_type="text/plain")       

def Chatbot(request):
    if request.method == 'GET':
        return render(request, 'Chatbot.html', {})       

def UserScreen(request):
    if request.method == 'GET':
        return render(request, 'UserScreen.html', {})  

def UserLoginAction(request):
    global username
    if request.method == 'POST':
        global username
        status = "none"
        users = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        con = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == users and row[1] == password:
                    username = users
                    status = "success"
                    break
        if status == 'success':
            context= {'data':'Welcome '+username}
            return render(request, "UserScreen.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'UserLogin.html', context)

def RegisterAction(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
               
        output = "none"
        con = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break                
        if output == "none":
            db_connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register VALUES(%s, %s, %s, %s, %s)"
            db_cursor.execute(student_sql_query, (username, password, contact, email, address))
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = "Signup process completed. Login to perform Symptoms Checker"
        context= {'data':output}
        return render(request, 'Register.html', context)        

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})         

def UserLogin(request):
    if request.method == 'GET':
        return render(request, 'UserLogin.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

