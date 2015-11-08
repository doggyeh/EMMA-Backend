#!flask/bin/python
from flask import Flask, jsonify,abort,request
from questions import init,get_model,list_feature

#pagekite for public
#pagekite.py 5000 doggyeh.pagekite.me
app = Flask(__name__)

mydict,synonyms,synonyms_pinyin,features,features_pinyin = init()
m = get_model()

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    question = request.json['question']
    answer = list_feature(question.replace(' ',''),features,features_pinyin,mydict,synonyms,synonyms_pinyin,m,False)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
