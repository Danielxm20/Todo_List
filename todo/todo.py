from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)
from werkzeug.exceptions import abort
from todo.auth import login_required
from todo.db import get_db

bp = Blueprint('todo', __name__)

@bp.route('/')
@login_required
def index():
    db, c =get_db()
    c.execute('SELECT t.id, t.description, u.username, t.completed, t.created_at from todo t JOIN user u on t.created_by = u.id order by created_at desc')
    todos = c.fetchall()

    return render_template('todo/index.html', todos= todos)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method =='POST':
        description = request.form['description']
        error= None
        
        if not description:
            error ='Description es requerida'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute('insert into todo(description, completed, created_by) values(%s, %s, %s)',(description, False, g.user['id']))
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/create.html')

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    return render_template('todo/update.html', todo={
        "description": "Mi todo",
        "id": 2,
        "Completed": 0
    })

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    return ''