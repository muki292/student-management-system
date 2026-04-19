from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from config import MONGO_URI

app = Flask(__name__)

client = MongoClient(MONGO_URI)
db = client.student_db
collection = db.students


@app.route('/')
def index():
    students = list(collection.find())
    return render_template('index.html', students=students)


@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        collection.insert_one({
            "name": name,
            "age": age,
            "course": course
        })

        return redirect('/')

    return render_template('add.html')


@app.route('/delete/<id>')
def delete_student(id):
    from bson.objectid import ObjectId
    collection.delete_one({"_id": ObjectId(id)})
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)