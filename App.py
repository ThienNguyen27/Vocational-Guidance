from flask import Flask, render_template, url_for, request, session, redirect,flash  # create virtualenv to install Flask
import numpy as np
from tensorflow import keras
from test import predictor
from flask_pymongo import PyMongo, MongoClient  # pip install Flask pymongo
import yaml  # pip install pyyaml, store MYSQL account at other file
import bcrypt

Personality_label = ['ENFJ', 'ENFP', 'ENTJ', 'ENTP', 'ESFJ', 'ESFP', 'ESTJ', 'ESTP', 'INFJ', 'INFP', 'INTJ', 'INTP', 'ISFJ','ISFP', 'ISTJ', 'ISTP'] 
Personality_label1 = ['ENFJ', 'ENFP', 'ENTJ', 'ENTP', 'ESFJ', 'ESFP', 'ESTJ', 'ESTP', 'INFJ', 'INFP', 'INTJ', 'INTP', 'ISFJ','ISFP', 'ISTJ', 'ISTP'] 

app = Flask(__name__)


model = keras.models.load_model(r'/Users/thien/Desktop/New Vocational Guidance/models/final.h5')  # Copy relative path

# Take the uri from yaml file
with open(r'db.yaml') as file: # Copy relative path
    dbpass=yaml.load(file, Loader=yaml.FullLoader)
    app.config['MONGO_URI'] = dbpass['uri']
    app.config['SECRET_KEY'] = dbpass['secret_key']
client = MongoClient(app.config['MONGO_URI'])

# Define the database name 
db = client.web_app

# Setup MongoDB
mongo = PyMongo(app)

@app.route('/home-eng', methods=['GET', 'POST']) 
def index_eng(): 
    if 'Email' not in session: 
        to_render = 'english-home-guest.html'
    else:
        flash(session['username'], category='Success')
        to_render = 'english-home-user.html'
    return render_template(to_render)

@app.route('/home-vn', methods=['GET', 'POST']) 
def index_vn():
    if 'Email' not in session: 
        to_render = 'vietnamese-home-guest.html'
    else:
        flash(session['username'], category='Success')
        to_render = 'vietnamese-home-user.html'
    return render_template(to_render)


@app.route('/', methods=['GET','POST']) # login page 
def login_eng():
    if request.method=='POST':
        # users = mongo.db.users
        login_user = db.users.find_one({'Email': request.form['email']}) #check if email has already stored in MongoDB
        if login_user: 
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) != login_user['password']:
                flash('Wrong password. Please try again.', category='Error')
            else:
                session['username'] = request.form['username']
                session['Email'] = request.form['email']
                return redirect(url_for('index_eng'))
        else:
            flash("Not exist. Please login again or sign up", category='Error')   
    return render_template('english-login.html')

@app.route('/vn', methods=['GET','POST']) 
def login_vn():
    if request.method=='POST':
        # users = mongo.db.users
        login_user = db.users.find_one({'Email': request.form['email']}) # check if email has already stored in MongoDB
        if login_user: 
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) != login_user['password']:
                flash('Sai mật khẩu. Vui lòng thử lại.', category='Error')        
            else:
                session['username'] = request.form['username']
                session['Email'] = request.form['email']
                return redirect(url_for('index_vn'))
        else:
            flash("Email không tồn tại. Vui lòng đăng nhập lại hoặc đăng ký bằng email khác", category='Error')
    return render_template('vietnamese-login.html')


@app.route('/signup-eng', methods=['POST', 'GET'])
def signup_eng():
    if request.method=='POST':
        # users = mongo.db.users
        existing_user = db.users.find_one({'Email': request.form['email']})
        if existing_user is None: # check if user is in MongoDB, if no store data, if yes ask user to login
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            db.users.insert_one({'Email': request.form['email'],'n ame': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            session['Email'] = request.form['email']
            return redirect(url_for('index_eng'))
        flash('That email already exists! Please log in or use other email to sign up!', category='Error')
    return render_template('english-signup.html')

@app.route('/signup-vn', methods=['POST', 'GET'])
def signup_vn():
    if request.method=='POST':
        # users = mongo.db.users
        existing_user = db.users.find_one({'Email': request.form['email']})
        if existing_user is None: #check if user is in MongoDB, if no store data, if yes ask user to login
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            db.users.insert_one({'Email': request.form['email'],'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            session['Email'] = request.form['email']
            return redirect(url_for('index_vn'))
        flash('Email đã được dùng! Vui lòng đăng nhập hoặc dùng email khác để đăng ký!', category='Error')
    return render_template('vietnamese-signup.html')

@app.route('/contact-eng')  # About us, about this project 
def contact_eng():
    return render_template('english-contact.html')
@app.route('/contact-vn')  
def contact_vn():
    return render_template('vietnamese-contact.html')

# @app.route('/intro-eng')  # About this project
# def intro_eng():
#     return render_template('english-intro.html')
# @app.route('/intro-vn')  
# def intro_vn():
#     return render_template('vietnamese-intro.html')


@app.route('/test-vn', methods=['POST', 'GET'])
def test_vn():
    return render_template('vietnamese-test.html')


@app.route('/result-vn', methods=['POST', 'GET']) #result page
def predict_vn(): 
    int_features = [int(x) for x in request.form.values()] # response value
    features = np.array(int_features)
    features = features.reshape(1, -1)
    probability_array = model.predict(features)  # array of 16 groups'probalities
    Personality_types_predict = Personality_label1[np.argmax(probability_array)] 
    Career_predict = predictor(Personality_types_predict)
    array=probability_array[0]
        # print('ISFP', round(100*array[13],2), "%")
    Label_list = []
    Percent_list = []
    for k in range(0,3): 
        max_num = max(array)   
        index = np.where(array==max_num)[0]
        Label=Personality_label[index[0]]
        Personality_label.pop(index[0])
        Percentage=round(100*max_num,2)
        print(Label, end=": ")
        print(Percentage, end="%")
        Label_list.append(Label)
        Percent_list.append(Percentage)
        print()
        array = array[array != max_num]  
    def insert_data_into_mongo():
        data = {}
        if request.method == 'POST':
            for i in range(1, 61):
                data[f'Question {i}'] = request.form[f'question{i}']
            data['Predicted personality types']=Personality_types_predict
            data['Predicted career']=Career_predict
            # db.users.insert_one(data)    
            rank_word=["nhất", "nhì", "ba"]
            for personality_rank in range(0,3):
                data[f'Nhóm ngành phù hợp thứ {rank_word[personality_rank]}']=Label_list[personality_rank]
                data[f'Tỉ lệ nhóm ngành phù hợp thứ {rank_word[personality_rank]}']=f'{Percent_list[personality_rank]}%'
            print(data)
            db.users.insert_one(data)    
    insert_data_into_mongo()
    return render_template('vietnamese-result.html', prediction_text='{}'.format(Personality_types_predict), jobs=Career_predict, Label_Group=Label_list, Percent_Group=Percent_list )
    
    # 1 câu/ 1 trang, add hiệu ứng