import httplib2, argparse, os, sys, json
from oauth2client import tools, file, client
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.client import SignedJwtAssertionCredentials

"""Make single prediction for each question"""

#Project and model configuration
project_id = '575046039409'
model_id = 'question-chinese-model'

def init_api():
    try:
        api = get_prediction_api()
    except HttpError as e: 
        if e.resp.status == 404: #model does not exist, train it in google.py
            print("Model does not exist yet.")
            exit()
        else:
            print(e)
    return api

""" Use trained model to generate a new prediction """
def make_prediction(api,feature):
    #api = get_prediction_api()
    #print("Fetching model.")
    model = api.trainedmodels().get(project=project_id, id=model_id).execute()
    if model.get('trainingStatus') != 'DONE':
        print("Model is (still) training. \nPlease wait and run me again!") #no polling
        exit()
    #print("Model is ready.")

    #read new record from local file
    #with open('record.csv') as f:
     #   record = f.readline().split(',') #csv

    #obtain new prediction
    prediction = api.trainedmodels().predict(project=project_id, id=model_id, body={
        'input': {
                'csvInstance': feature
        },
    }).execute()

    #retrieve classified label and reliability measures for each class
    label = prediction.get('outputLabel')
    stats = prediction.get('outputMulti')

    #print("You asking question %s" % label)
    #print(stats)
    return label,stats

def get_prediction_api(service_account=True):
    scope = [
            'https://www.googleapis.com/auth/prediction',
            'https://www.googleapis.com/auth/devstorage.read_only'
    ]
    return get_api('prediction', scope, service_account)

""" Build API client based on oAuth2 authentication"""
def get_api(api, scope, service_account=True):
    with open("NLP-ML-bb13b6a378ae.json") as f:
        data = json.load(f)
        client_email = data['client_email']
        private_key = data['private_key']
    credentials = SignedJwtAssertionCredentials(client_email, private_key,scope=scope)
    #wrap http with credentials
    http_auth = credentials.authorize(httplib2.Http())
    return discovery.build(api, "v1.6", http=http_auth)

if __name__ == '__main__':
    main()
