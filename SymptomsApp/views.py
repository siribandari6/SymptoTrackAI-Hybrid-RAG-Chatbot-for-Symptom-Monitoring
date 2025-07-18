from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
import os
from .models import Register, Log
from transformers import AutoTokenizer, RagRetriever, RagSequenceForGeneration, RagTokenForGeneration
import torch
import faiss
import numpy as np
import pandas as pd
import pickle
import re
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

global username

# Global variables for lazy loading
tokenizer = None
retriever = None
model = None

def get_model():
    global tokenizer, retriever, model
    if tokenizer is None or model is None:
        tokenizer = AutoTokenizer.from_pretrained("facebook/rag-sequence-nq")
        retriever = RagRetriever.from_pretrained("facebook/rag-sequence-nq", index_name="exact", use_dummy_dataset=True)
        model = RagSequenceForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)
    return tokenizer, retriever, model


# Global variables for lazy loading
faiss_index = None
Y = None

def get_faiss_data():
    global faiss_index, Y
    if faiss_index is None or Y is None:
        tokenizer, retriever, model = get_model()
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
    return faiss_index, Y

def ViewLog(request):
    if request.method == 'GET':
        global username
        output = ''
        output+='<table border=1 align=center width=100%><tr><th><font size="3" color="black">Username</th><th><font size="3" color="black">Symptoms Text</th>'
        output+='<th><font size="3" color="black">Predicted Advice</th><th><font size="3" color="black">Logged & Monitored Time</th></tr>'
        scores = []
        labels = []
        logs = Log.objects.filter(username=username)
        for log in logs:
            output+='<tr><td><font size="3" color="black">'+log.username+'</td>'
            output += '<td><font size="3" color="black">'+str(log.symptoms_text)+'</td>'
            output += '<td><font size="3" color="black">'+str(log.predicted_advice)+'</td>'
            output += '<td><font size="3" color="black">'+log.checked_date+'</td></tr>'
        output+= "</table></br></br></br></br>" 
        context= {'data':output}
        return render(request, 'UserScreen.html', context)

def logData(username, question, advice):
    now = datetime.now()
    current_datetime = str(now.strftime("%Y-%m-%d %H:%M:%S"))
    Log.objects.create(
        username=username,
        symptoms_text=question,
        predicted_advice=advice,
        checked_date=current_datetime
    )
    

@csrf_exempt
def ChatData(request):
    if request.method == 'GET':
        global username
        tokenizer, retriever, model = get_model()
        faiss_index, Y = get_faiss_data()
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
        try:
            user = Register.objects.get(username=users, password=password)
            username = users
            status = "success"
        except Register.DoesNotExist:
            status = "failed"
        
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
        try:
            existing_user = Register.objects.get(username=username)
            output = username+" Username already exists"
        except Register.DoesNotExist:
            # Username doesn't exist, create new user
            Register.objects.create(
                username=username,
                password=password,
                contact_no=contact,
                email=email,
                address=address
            )
            output = "Signup process completed. Login to perform Symptoms Checker"
        
        context= {'data':output}
        return render(request, 'Register.html', context)

def RegisterView(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def UserLogin(request):
    if request.method == 'GET':
        return render(request, 'UserLogin.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

