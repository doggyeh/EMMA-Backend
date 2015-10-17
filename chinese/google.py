import httplib2, argparse, os, sys, json
from oauth2client import tools, file, client
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.client import SignedJwtAssertionCredentials

"""Create and Training Model in Google Predicition API"""

#Project and model configuration
project_id = '575046039409'
model_id = 'question-chinese-model'

def main():
    """ Simple logic: train and make prediction """
    #delete_model()
    #train_model()
    try:
        make_prediction()
    except HttpError as e: 
        if e.resp.status == 404: #model does not exist
            print("Model does not exist yet.")
            train_model()
            make_prediction()
        else: #real error
            print(e)

""" Use trained model to generate a new prediction """
def make_prediction():

    api = get_prediction_api()

    print("Fetching model.")

    model = api.trainedmodels().get(project=project_id, id=model_id).execute()
    if model.get('trainingStatus') != 'DONE':
        print("Model is (still) training. \nPlease wait and run me again!") #no polling
        exit()

    print("Model is ready.")

    """
    #Optionally analyze model stats (big json!)
    analysis = api.trainedmodels().analyze(project=project_id, id=model_id).execute()
    print(analysis)
    exit()
    """
    ##read new record from local file
    #with open('record.csv') as f:
    #    record = f.readline().split(',') #csv
    record = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1]
    #print record
    #obtain new prediction
    prediction = api.trainedmodels().predict(project=project_id, id=model_id, body={
        'input': {
                'csvInstance': record
        },
    }).execute()

    #retrieve classified label and reliability measures for each class
    label = prediction.get('outputLabel')
    stats = prediction.get('outputMulti')

    print("You asking question %s" % label)
    print(stats)

""" Create new classification model """
def train_model():

    api = get_prediction_api()

    print("Creating new Model.")

    api.trainedmodels().insert(project=project_id, body={
            'id': model_id,
            'storageDataLocation': 'ml-data/question_chinese.csv',
            'modelType': 'CLASSIFICATION'
    }).execute()

def delete_model():
    api = get_prediction_api()
    print("Deleting Model.")
    api.trainedmodels().delete(project=project_id, id = model_id).execute()

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
