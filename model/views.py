from django.shortcuts import render
import pickle
import re
import os
import numpy  as np
# import openai
file_path = os.path.dirname(os.path.realpath(__file__))

# openai.api_key = "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"
# # os.getenv("OPENAI_API_KEY")
# openai.Model.list()




# Create your views here.
from django.shortcuts import render , redirect
from .models import ModelUsers
from django.utils import timezone
# Create your views here.


def index(request):
    request.session.set_test_cookie()
    context  = {
        'title': 'Cyber Incident Prediction System'
    }

    try:
        
        if request.POST:
            username = request.POST.get('username')
            userauth = request.POST.get('userauth')
            user_table = ModelUsers.objects.get(user_name=username)
            if userauth == user_table.user_auth:
                context['res_mes'] = 'Login Successfull'
                context['class'] = 'alert-success' 
                context['display'] = 'block'
                request.session['user'] = user_table.user_name
                return redirect(to='dashboard/')
            else:
                context['res_mes'] = 'Invalid Credentials'
                context['class'] = 'alert-danger' 
                context['display'] = 'block'

    except ModelUsers.DoesNotExist:
        context['res_mes'] = 'Invalid Credentials'
        context['class'] = 'alert-danger' 
        context['display'] = 'block'
    return  render(request , 'app/index.html', context)

def signup(request):
    context = {
        'title': 'Sign Up Page',
        'display': 'none'
        
    }

    try:
        
        if request.POST:
            _fullname = request.POST.get('fullname')
            username = request.POST.get('username')
            userauth = request.POST.get('userauth')
            user_table = ModelUsers(user_name=username , user_auth=userauth , fullname=_fullname)
            user_table.save()
            context['res_mes'] = 'User Account Created Successfully'
            context['class'] = 'alert-success' 
            context['display'] = 'block'
            request.session['user'] = user_table.user_name
            # print("User Account Created Successfully")

        
    except:
        context['res_mes'] = 'Error Occur, can not create user account successfully!, please contact admin'
        context['class'] = 'alert-danger' 
        context['display'] = 'block'

    return render(request , 'app/signup.html', context)


def dashboard(request):
    context = {
        'title': 'Cyber Incident Prediction System'
    }

    if request.session['user']:
        # try:
            user_table = ModelUsers.objects.get(user_name=request.session['user'])
            context['fullname'] = user_table.fullname
            context['username'] = user_table.user_name
            if request.POST: 
                dst_port = str( request.POST.get('dst-port') )
                protocol =  str(request.POST.get('protocol')) 
                flow_duration = str(request.POST.get('flow-duration') )
                f_pkts =  str(request.POST.get('f-pkts')) 
                b_pkts =   str(request.POST.get('b-pkts')) 

                if dst_port and protocol and flow_duration and f_pkts and b_pkts:
                    dst_port = int( re.sub('[a-z]|[A-Z]' , repl= " " ,  string= dst_port) )
                    protocol = int( re.sub('[a-z]|[A-Z]' , repl= " " ,  string= protocol) )
                    flow_duration = int( re.sub('[a-z]|[A-Z]' , repl= " " ,  string= flow_duration) )
                    f_pkts = int( re.sub('[a-z]|[A-Z]' , repl= " " ,  string= f_pkts) )
                    b_pkts = int( re.sub('[a-z]|[A-Z]' , repl= " " ,  string= b_pkts) )

                    X_test  = np.array([dst_port , protocol , flow_duration , f_pkts , b_pkts] ).reshape(1 , 5)
                    with open(file_path+'/classifier.modelsystem' , 'rb') as file:
                        model = pickle.load(file)
                        y_pred = model.predict(X_test)
                        y_pred   = np.array(y_pred).reshape(1)                        
                        # # create a chat completion
                        # chat_completion = openai.ChatCompletion.create(model="text-curie-001", messages=[{"role": "user", "content": "Hello world"}])
                        # # print the chat completion
                        # print(chat_completion.choices[0].message.content)

                       
                        
                        if  dst_port == 21:
                            with open(file_path + '/21_remark.txt' , 'r') as remark:
                                context['remark'] = remark.read(2024*5)
                        elif dst_port == 22 :
                             with open(file_path + '/21_remark.txt' , 'r') as remark:
                                context['remark'] = remark.read(2024*5)
                        else:
                            with open(file_path + '/general_report.txt' , 'r') as remark:
                                context['remark'] = remark.read(2024*5)

                        if y_pred[0] >= 0.7 :
                            context['high'] = '90'
                            context['medium'] = '20'
                            context['low'] = '10'
                            context['safe'] = '10'
                            context['status'] = "System is Highly Vulnerable!"
                        elif y_pred  >= 0.5 and y_pred <= 0.4 :
                            context['medium'] = '70'
                            context['high'] = '20'
                            context['low'] = '5'
                            context['safe'] = '30'
                            context['status'] = "System vulnerable and need a technical department attention!"

                        else:
                            context['low'] = '100'
                            context['medium'] = '5'
                            context['high'] = '5'
                            context['safe'] = '100'
                            context['status'] = "System is safe, but please take my security recommendation to tighten security!"

        # except:
        #     return redirect("/model")
    else:
        return redirect("/model")

    return render(request , 'app/dashboard.html' , context)