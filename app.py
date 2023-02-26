from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
engine = create_engine('postgresql://postgres:zxzx@localhost:5432/todo', echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class ToDo(Base):
    __tablename__ = 'ToDo'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    content = Column(Text)
    complete = Column(Boolean)


# Base.metadata.create_all(engine)


@app.route('/')
def index():
    all_todos = session.query(ToDo)
    return render_template("index.html",todos=all_todos)


@app.route('/add', methods = ["POST"])
def add_todo():
    new_title = request.form.get('title')
    new_content = request.form.get('content')

    new_todo = ToDo(title=new_title, content=new_content, complete=False)
    session.add(new_todo)
    session.commit()

    return redirect(url_for('index'))


@app.route('/complete/<string:id>')
def complete_todo(id):
    todo = session.query(ToDo).filter(ToDo.id == id).first()
    if todo.complete == False:
        todo.complete = True
    else:
        todo.complete = False

    session.commit()

    return redirect(url_for('index'))


@app.route('/delete/<string:id>')
def delete_todo(id):
    todo = session.query(ToDo).filter(ToDo.id == id).first()
    session.delete(todo)
    session.commit()

    return redirect(url_for('index'))

@app.route('/detail/<string:id>')
def detail_todo(id):
    todo = session.query(ToDo).filter(ToDo.id == id).first()

    return render_template("detail.html",todo=todo)


if __name__ == '__main__':
    app.run()
