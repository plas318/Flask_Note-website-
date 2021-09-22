from flask import Blueprint, render_template, flash,request, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.sql.sqltypes import DateTime
from .models import User, Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) <1 :
            flash('Note is too short!', category="failure")
        else:
            new_note = Note(data=note, date =current_timestamp() , user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category="success")
    return render_template("home.html", user=current_user)

@views.route('/about')
@login_required
def about():
    return render_template("about.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
        else : 
            flash('Unable to delete note!', category='failure')

    return jsonify({})

@views.route('/tracker')
def tracker():

    return render_template('index.html')