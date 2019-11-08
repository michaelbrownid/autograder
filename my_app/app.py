from flask import Flask

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024




# from flask import Flask, render_template, request
# from werkzeug import secure_filename
# import json
# import pickle
# from flask_pymongo import PyMongo
# from preprocess import *
# from predict import *
# import random

# app = Flask(__name__)
# client = pymongo.MongoClient("mongodb+srv://Galvanize:HelloWorld@galvanize-bafqh.mongodb.net/test?retryWrites=true")
# db = client.Fraud_Case_Study
# collection =db.json


# localclient = pymongo.MongoClient("mongodb://localhost:27017/fraud")
# localdb = localclient.fraud
# localcollection =localdb.json
# localprob_collection = localdb.probs

# # home page
# @app.route('/')
# def index():
#     return render_template('jumbotron.html', title='Hello!')

# @app.route('/table')
# def table():
#     return render_template('table.html', title='Hello!')

# gb_model = pickle.load(open('static/GB_model.pkl', 'rb'))

# @app.route('/fill_probs')
# def fill_probs():
#     documents = localcollection.find()
#     response = []
#     for document in documents:
#         document['_id'] = str(document['_id'])
#         response.append(document)
#         filename = 'tempfile.json'
#         with open('tempfile.json','w') as f: 
#             json.dump(document, f, ensure_ascii=False, indent=4)   
#         df,raw_df = preprocess_json(filename)
#         seq_num = raw_df['sequence_number'][0]
#         prob = predict_fraud(df,gb_model)
        
#         d = document.copy()
#         del d['_id']
#         d['Fraud']=prob
#         collection.insert_one(d)
#     return 'hello'

# @app.route('/get_probs')
# def get_probs():
#     probs = prob_collection.find()
#     response = []
#     for prob in probs:
#         response.append(prob)
#         print(repr(prob))
#     return "hello"

# @app.route('/fraud', methods=['GET','POST'])
# def fraud():
#     entries = collection.find()[240:280]    #[60:90]
#     df = pd.DataFrame(entries)
#     df = df[[ 'Fraud','name','venue_name',  'org_name', 'venue_address', 'venue_country','email_domain',  'user_type','venue_state','channels', 'country', 'currency',
#        'delivery_method', 
#      'fb_published', 'venue_latitude',
#        'venue_longitude',
#        'has_analytics', 'has_logo', 'listed', 
#          'org_facebook',
#        'org_twitter', 'payee_name', 'payout_type', 
#        'sale_duration', 'show_map',  'user_age', 
#        ]]
#     colnames = list(df.columns)
#     newcols = []
#     for col in colnames:
#         c = col.capitalize()
#         newcols.append(c.replace('_', ' '))
#     df.columns = newcols
#     return render_template("table.html",tables=[df.to_html(classes='data')], titles=df.columns.values)



# @app.route('/more/')
# def more():
#     return render_template('starter_template.html')


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080, debug=True)
