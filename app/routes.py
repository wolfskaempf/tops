import platform
import subprocess
import shlex
from datetime import datetime, timedelta
from flask import render_template, flash, redirect, url_for, current_app, make_response, request, json
from sqlalchemy import desc, or_
from app import app, db
from app.forms import CreateTopForm, LoginForm
from app.models import Top

@app.route('/')
def index():
    tops = Top.query.order_by(desc(Top.eingereicht_am)).filter(
        or_(Top.archiviert == False, Top.archiviert == None)).all()
    return render_template('index.html', tops=tops)


def render_top_to_telegram_html(top):
    return render_template('tops/telegram.html', top=top)


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

        # This might introduce a RCE-Vulnerability, so don't actually use this until this notice is revoked
        telegram_active = current_app.config['ENABLE_TELEGRAM_INTEGRATION']
        if telegram_active:
            telegram_bot_token = current_app.config['TELEGRAM_BOT_TOKEN']
            telegram_chat_id = current_app.config['TELEGRAM_CHAT_ID']
            message = render_top_to_telegram_html(t)
            command = './telegram -t "{}" -c "{}" -H "{}"'.format(telegram_bot_token, telegram_chat_id, message)
            if platform.system() == "Windows":
                command = "bash.exe " + command
            command = shlex.split(command)
            print(command)
            subprocess.Popen(command)

        return redirect(url_for('tops_list'))
    return render_template('tops/create.html', form=form)


@app.route('/tops/list')
def tops_list():
    tops = Top.query.order_by(Top.frist.asc().nullslast(), Top.eingereicht_am.asc()).filter(
        or_(Top.archiviert == False, Top.archiviert == None)).all()
    return render_template('tops/list.html', tops=tops, title="Aktuelle TOPs")


@app.route('/tops/list.json')
def tops_list_json():
    tops = Top.query.order_by(Top.frist.asc().nullslast(), Top.eingereicht_am.asc()).filter(
        or_(Top.archiviert == False, Top.archiviert == None)).all()
    return json.jsonify([dict(top.as_dict()) for top in tops])


@app.route('/tops/list/markdown')
def tops_list_markdown():
    tops = Top.query.order_by(Top.frist.asc().nullslast(), Top.eingereicht_am.asc()).filter(
        or_(Top.archiviert == False, Top.archiviert == None)).all()
    return render_template('tops/list_markdown.html', tops=tops, title="TOPs als Markdown")


@app.route('/tops/table')
def tops_table():
    tops = Top.query.order_by(Top.frist.asc().nullslast(), Top.eingereicht_am.asc()).filter(
        or_(Top.archiviert == False, Top.archiviert == None)).all()
    return render_template('tops/table.html', tops=tops)


@app.route('/tops/archiv')
def tops_archiv():
    tops = Top.query.order_by(desc(Top.eingereicht_am)).filter(Top.archiviert == True).all()
    return render_template('tops/list.html', tops=tops, title="Archiv")


@app.route('/tops/<id>/archivieren', defaults={'destination': None})
@app.route('/tops/<id>/archivieren/<destination>')
def tops_archivieren(id, destination):
    management_password = current_app.config['MANAGEMENT_PASSWORD']
    if management_password is not None:
        management_cookie_value = request.cookies.get('management_password')
        if management_cookie_value is None or management_cookie_value != management_password:
            flash("Du bist nicht autorisiert dies zu tun.")
            return redirect(url_for('login'))
    top = Top.query.get(id)
    top.archiviert = not top.archiviert
    db.session.add(top)
    db.session.commit()
    if destination is not None:
        return redirect(url_for(destination))
    elif top.archiviert:
        return redirect(url_for('tops_list'))
    else:
        return redirect(url_for('tops_archiv'))


@app.route('/tops/<id>/delete')
def tops_delete(id):
    top = Top.query.get(id)
    return render_template('tops/delete.html', top=top)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Dein Autorisierungstoken wurde gesetzt.")
        response = make_response(redirect(url_for('index')))
        response.set_cookie('management_password', form.management_password.data)
        return response
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.set_cookie('management_password', '', expires=0)
    return response
