from flask import render_template, flash, redirect, url_for
from datetime import datetime, timedelta
from app import app, db
from app.forms import CreateTopForm
from app.models import Top


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', time=datetime.utcnow())


@app.route('/tops/create', methods=['GET', 'POST'])
def tops_create():
    form = CreateTopForm()
    if form.validate_on_submit():
        t = Top(titel=form.titel.data, eingereicht_von=form.eingereicht_von.data,
                eingereicht_am=datetime.utcnow() + timedelta(hours=1), frist=form.frist.data, \
                beschreibung=form.beschreibung.data, abstimmungsfragen=form.abstimmungsfragen.data)
        db.session.add(t)
        db.session.commit()
        flash("Danke {}, dein TOP mit dem Titel \"{}\" wurde erfolgreich eingereicht.".format(form.eingereicht_von.data, \
                                                                                              form.titel.data))
        return redirect(url_for('tops_list'))
    return render_template('tops/create.html', form=form)


@app.route('/tops/list')
def tops_list():
    tops = Top.query.all()
    return render_template('tops/list.html', tops=tops)
