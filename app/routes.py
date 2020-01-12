from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for
from sqlalchemy import desc, or_
from app import app, db
from app.forms import CreateTopForm
from app.models import Top


@app.route('/')
@app.route('/index')
def index():
    tops = Top.query.order_by(desc(Top.eingereicht_am)).filter(
        or_(Top.archiviert == False, Top.archiviert == None)).all()
    return render_template('index.html', tops=tops)


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
    tops = Top.query.order_by(desc(Top.eingereicht_am)).filter(
        or_(Top.archiviert == False, Top.archiviert == None)).all()
    return render_template('tops/list.html', tops=tops, title="Aktuelle TOPs")


@app.route('/tops/archiv')
def tops_archiv():
    tops = Top.query.order_by(desc(Top.eingereicht_am)).filter(Top.archiviert == True).all()
    return render_template('tops/list.html', tops=tops, title="Archiv")


@app.route('/tops/<id>/archivieren')
def tops_archivieren(id):
    top = Top.query.get(id)
    top.archiviert = not top.archiviert
    db.session.add(top)
    db.session.commit()
    if top.archiviert:
        return redirect(url_for('tops_list'))
    else:
        return redirect(url_for('tops_archiv'))


@app.route('/tops/<id>/delete')
def tops_delete(id):
    top = Top.query.get(id)
    return render_template('tops/delete.html', top=top)
