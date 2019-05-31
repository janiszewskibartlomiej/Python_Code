from flask import Blueprint, request, get_flashed_messages, render_template, session, redirect, flash
from werkzeug.security import check_password_hash

from get_connection import polaczenie

login_panel = Blueprint('/login', __name__)


@login_panel.route('/login', methods=['GET', 'POST'])
def log_in():
    if request.method == 'GET':
        messages = get_flashed_messages()
        return render_template('log_in.html', messages=messages)

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = polaczenie()
        c = conn.cursor()

        print('user: ', username, 'password: ', password)

        zapytanie_password = """
            SELECT id, user, password, admin FROM "login" WHERE user = ?;
            """
        c.execute(zapytanie_password, (username,))
        line_from_base = c.fetchone()

        print('hasła:', password, line_from_base)

        if line_from_base:
            password_hash = line_from_base['password']

            if check_password_hash(password_hash, password):
                session['user_id'] = line_from_base['id']
                session['user'] = line_from_base['user']
                session['is_admin'] = bool(line_from_base['admin'])

                if line_from_base['admin']:
                    return redirect('/dodaj')

                return redirect('/ankieta')

        flash('Błędna nazwa użytkownika lub hasło')
        return redirect('/login')
