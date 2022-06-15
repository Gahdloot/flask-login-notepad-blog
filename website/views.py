from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        print(note)
        print(type(note))

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_Note = Note(data=note, user_id=current_user.id)
            flash('Note Added !!!', category='success')
            db.session.add(new_Note)
            db.session.commit()


    return render_template('home.html', user=current_user)

@views.route('/delete-note', methods=['Post'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})