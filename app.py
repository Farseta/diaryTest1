from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)



connection_string =os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")
client = MongoClient(connection_string)
db = client[DB_NAME]
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    posts = list(db.diary.find({},{'_id':False}))
    return jsonify({"post" : posts})

# @app.route('/diary',methods = ['POST']) 
# def saving():
#     sample_post = request.form['sample_give']
#     print(sample_post)
#     return jsonify({"msg" : 'Post request received'})

@app.route('/diary', methods=['POST'])
def save_diary():
    # sample_receive = request.form.get('sample_give')
    # print(sample_receive)
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('description_give')
    file = request.files['file_give']
    extention =file.filename.split('.')[-1]
    today = datetime.now()
    mytime = today.strftime("%Y-%m-%d-%H-%M-%S")
    fileName =f'static/post-{mytime}.{extention}'
    
    fileProfile = request.files['fileProfile_give']
    extention2 = fileProfile.filename.split('.')[-1]
    fileNameProfile = f'static/imgProfile/post-profile-{mytime}.{extention2}'
    print(fileProfile)
    timeSave = today.strftime("%Y.%m.%d")
    if title_receive and content_receive:
        file.save(fileName)
        fileProfile.save(fileNameProfile)
        
        doc = {
            'file' : fileName,
            'fileProfile': fileNameProfile,
            'title' : title_receive,
            'content': content_receive,
            'createdAt': timeSave,
        }
        db.diary.insert_one(doc)
        return jsonify({'msg': 'POST request complete!'})
    else:
        return jsonify({'msg': 'POST request failed!'})

if __name__ == '__main__':
    app.run("0.0.0.0",port=5000,debug=True)