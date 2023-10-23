import os, secrets
from flask_login import login_required, logout_user, login_user, current_user
from flask import abort, session
from app import app, db
from app.model import Compani, User
from flask import render_template, send_from_directory, request, flash, url_for, redirect, jsonify
from PIL import Image
from app.form import Sign_in, Sign_up, Create_Compani, Edit_Compani
from sqlalchemy.exc import IntegrityError


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('sign_in'))

@app.route('/')
def about():
    if current_user.is_admin:
        # page = request.args.get('page', 1, type=int)
        # comp = Compani.query.paginate(page=page, per_page=12)
        # product=comp
        return render_template('about.html', is_admin=current_user.is_admin)    
    else:
        # page = request.args.get('page', 1, type=int)
        # comp = Compani.query.paginate(page=page, per_page=12)
        #product=comp,
        return render_template('about.html', is_admin=False)

@app.route('/sign_in/', methods=('GET', 'POST'))
def sign_in():
    form = Sign_in()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.user_name == form.user.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('about'))

    return render_template('sign_in.html', form=form)


@app.route('/<id>/compani/')
def card_compani(id):
    if current_user.is_admin:
        comp = Compani.query.filter(Compani.id == id).first()
        return render_template('card_compani.html', product=comp, is_admin=current_user.is_admin)
    comp = Compani.query.filter(Compani.id == id).first()
    return render_template('card_compani.html', product=comp)


@app.route('/sign_up/', methods=['POST', 'GET'])
def sign_up():
    form = Sign_up()
    if form.validate_on_submit():
        user = User(user_name=form.user.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()        
        return redirect(url_for('sign_in'))
    return render_template('sign_up.html', form=form)


@app.route('/api_comapni/', methods=['POST', 'GET'])
def api_search():
    data = Compani.query.all()

    return jsonify(data)

@app.route('/api/search_com/<search_word>', methods=['POST', 'GET'])
def api_search_word(search_word):
    data = Compani.query.filter((Compani.Campaning_Name.contains(f"{search_word}"))).all()
    
    return jsonify(data)


def save_file(file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    pdf_fn = random_hex + f_ext
    pdf_path = os.path.join(app.root_path, app.config['UPLOAD_FILE'], pdf_fn)

    print(f"{pdf_path}, {pdf_fn}")
    file.save(os.path.join(app.root_path, app.config['UPLOAD_FILE'], pdf_fn))


    return pdf_fn


@app.route('/create_product/', methods=('GET', 'POST'))
@login_required
def create_product():
    if current_user.is_admin:
        form = Create_Compani()
        if form.validate_on_submit():
            file = save_file(form.file.data)   
            comp = Compani(Campaning_Name=form.campaning_name.data,
                        Collection_Pointer=form.collection_pointer.data,
                        Buffer_Pointer=form.buffer_pointer.data,
                        Status=form.status.data,
                        Attempts=form.attempts.data,
                        License_In_Use=form.license_in_use.data,
                        First_Call_Time=form.first_call_time.data,
                        Last_Call_Time=form.last_call_time.data)
            db.session.add(comp)
            db.session.commit()
            return redirect(url_for('about'))
            
        return render_template('create_compani.html', form=form)
    elif not current_user.is_admin:
        return abort(404)


@app.route('/<int:compani_id>/edit/', methods=('GET', 'POST'))
@login_required
def edit(compani_id):
    if current_user.is_admin:
        comp = Compani.query.get_or_404(compani_id)
        form = Edit_Compani()
        if form.validate_on_submit():
            comp.Campaning_Name = form.campaning_name.data
            comp.Collection_Pointer = form.collection_pointer.data
            comp.Buffer_Pointer = form.buffer_pointer.data
            comp.Status = form.status.data
            comp.Attempts = form.attempts.data
            comp.License_In_Use = form.license_in_use.data
            comp.First_Call_Time = form.first_call_time.data
            comp.Last_Call_Time = form.last_call_time.data
            try:
                db.session.commit()
                return redirect(url_for('about'))
            except IntegrityError:
                db.session.rollback()
                flash('Произошла ошибка: такая compani уже есть в базе', 'error')
                return render_template('edit.html', form=form)
      
            
        elif request.method == 'GET':
            form.campaning_name.data = comp.Campaning_Name
            form.collection_pointer.data = comp.Collection_Pointer
            form.buffer_pointer.data = comp.Buffer_Pointer
            form.status.data = comp.Status
            form.attempts.data = comp.Attempts
            form.license_in_use.data = comp.License_In_Use
            form.first_call_time.data = comp.First_Call_Time
            form.last_call_time.data = comp.Last_Call_Time

        return render_template('edit.html', form=form)
    elif not current_user.is_admin:
        return abort(404)      

@app.post('/<int:compani_id>/delete/')
@login_required
def delete(compani_id):
    if current_user.is_admin:
        book = Compani.query.get_or_404(compani_id)
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('about'))
    elif not current_user.is_admin:
        return abort(404)   

# @app.route('/test/')
# def test():
#     page = request.args.get('page', 1, type=int)
#     comp = Compani.query.paginate(page=page, per_page=12)
#     x = lambda x: for i in comp
#     return "hello"


@app.before_first_request
def create_tables():
    app.app_context().push()
    db.create_all()