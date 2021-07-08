from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

from environment import get_env
from flaskblog import app, login_manager
from flaskblog.models import BlogPost, User, db, LoginForm, SingUpForm, ProfileFormPassword

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
mail = Mail(app)
app.config.from_object(get_env())


@app.errorhandler(404)
def error_404(e):
    data = {
        "error_text": "Page not found",
        "error_number": "404"
    }
    return render_template('error.html', data=data)


@app.errorhandler(403)
def error_403(e):
    data = {
        "error_text": "403 Forbidden: : You don’t have permission to access this page",
        "error_number": "403"
    }
    return render_template('error.html', data=data)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/user")
@login_required
def user():
    get_user = User.query.filter_by(id=current_user.id).first()
    user_posts = get_user.posts
    return render_template('user.html', user_posts=user_posts)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    posts = BlogPost.query.all()
    return render_template('index.html', blogs=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    post_details = BlogPost.query.get_or_404(post_id)
    return render_template('post.html', post=post_details)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/edit_text')
def edit_text():
    return render_template('text_editor.html')


@app.route('/add_new_post', methods=["GET", "POST"])
@login_required
def add_new_post():

    if request.method == "POST":
        title = request.form.get("title").strip()
        content = request.form.get("content").strip()
        subtitle = request.form.get("subtitle").strip()
        image_url = request.form.get("image_url").strip()
        author = User.query.filter_by(id=current_user.id).first()

        if post_valid(title=title, subtitle=subtitle, image_url=image_url, content=content):
            try:
                new_post = BlogPost(
                    title=title,
                    content=content,
                    subtitle=subtitle,
                    image_url=image_url,
                    owner=author,
                )
                db.session.add(new_post)
                db.session.flush()
                db.session.commit()
                flash('New post added successful', category="success")
                return redirect(url_for('add_new_post'))
            except:
                db.session.rollback()
                print('error')
        else:
            return redirect('add_new_post')

    return render_template('add_new_post.html')


def post_valid(**kwargs):
    validator = True
    for key, value in kwargs.items():
        if key == "title":
            if len(value) < 10 or len(value) > 100:
                validator = False
                flash('Title min 10 max 100', category="error")

        elif key == "subtitle":
            if len(value) < 10 or len(value) > 150:
                validator = False
                flash('Subtitle min 10 max 150', category="error")

        elif key == "image_url":
            if len(value) < 4 or len(value) > 500:
                validator = False
                flash('Image url min 4 max 500', category="error")

        elif key == "content":
            if len(value) < 30:
                validator = False
                flash("Content can't be lase then 30", category="error")
    return validator


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        text = f'Name - {data["name"]}, Email - {data["email"]}, Phone - {data["phone"]}, Message - {data["message"]}'
        flash('Successfully sent your message', category="success")
        return render_template('contact.html', msg_sent=True)

    return render_template('contact.html', msg_sent=False)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = request.form.get("email")
            password = request.form.get("password")
            remember_me = True if request.form.get('remember') else False
            find_user = User.query.filter_by(email=email).first()
            if find_user is None:
                flash('User not found', category="error")
                return render_template('login.html', form=form)
            else:
                if check_password_hash(find_user.password, password):
                    login_user(find_user, remember=remember_me)
                    return redirect(request.args.get('next') or url_for('profile'))
                else:
                    flash('Wrong User name or password', category="error")
                    return render_template('login.html', form=form)
    return render_template('login.html', form=form)


def sent_token(email):
    try:
        token = s.dumps(email)
        msg = Message('Confirm Email', sender="d33652@gmail.com", recipients=[email])
        link = url_for('confirm_email', token=token, _external=True)
        msg.body = f"{link}"
        mail.send(msg)
        print(msg)
    except ConnectionRefusedError:
        print("Email wasn't sent (ConnectionRefusedError)")
    except Exception as error:
        print(error)


@app.route('/sing_up', methods=["GET", "POST"])
def sing_up():
    form = SingUpForm()
    if request.method == "POST" and form.validate():
        email = request.form.get("email").strip()
        password = generate_password_hash(request.form.get("password")).strip()
        name = request.form.get("name").strip()
        find_user = User.query.filter_by(email=email).first()
        if find_user is None:
            try:
                new_user = User(email=email, password=password, name=name, email_confirm=False)
                db.session.add(new_user)
                db.session.flush()
                db.session.commit()
                print('New user was added')
                sent_token(email)
                flash("User was created, please login.", category="success")
                return redirect(url_for('login'))
            except SignatureExpired:
                db.session.rollback()
                print("User wasn't added DB")
        else:
            flash('User already exist', category="error")
            return redirect(url_for('login'))
    return render_template('sing_up.html', form=form)


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, max_age=3600)
        confirm_email_user = User.query.filter_by(email=email).first()
        confirm_email_user.email_confirm = True
        db.session.commit()
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    except:
        return '<h1>The token is incorrect!</h1>'
    flash("Email confirmed", category="success")
    return redirect(url_for('login'))
    # return render_template('profile.html', user_info=confirm_email_user, form=form)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileFormPassword()
    user_info = User.query.filter_by(id=current_user.id).first()
    if request.method == "POST":
        if form.validate():
            password = generate_password_hash(request.form.get("password")).strip()
            user_info.password = password
            try:
                db.session.flush()
                db.session.commit()
                flash('Password updated', category="success")
            except:
                db.session.rollback()
                flash('Error to update', category="error")

            return redirect(url_for('profile'))
        flash('Password not valid', category="error")
        return redirect(url_for('profile'))
    else:
        return render_template('profile.html', user_info=user_info, form=form)


@app.route('/delete_users')
def delete_users():
    users = User.query.all()
    for delete_user in users:
        print(delete_user)
        db.session.delete(delete_user)
        db.session.commit()
    return str(users)


@app.route('/edit_post/<int:post_id>', methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post_details = BlogPost.query.get_or_404(post_id)
    if post_details.owner.id != current_user.id:
        abort(403)
    if request.method == "POST":
        title = request.form.get("title").strip()
        content = request.form.get("content").strip()
        subtitle = request.form.get("subtitle").strip()
        image_url = request.form.get("image_url").strip()
        
        if post_valid(title=title, subtitle=subtitle, image_url=image_url, content=content):
            post_details.title = title
            post_details.content = content
            post_details.subtitle = subtitle
            post_details.image_url = image_url
            db.session.commit()
            flash('Your post has been updated!', 'success')
            return render_template('edit_post.html', post=post_details)
        else:
            return redirect(post_id)
    return render_template('edit_post.html', post=post_details)


@app.route('/delete_post/<int:post_id>', methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post_delete = BlogPost.query.get_or_404(post_id)
    if post_delete.owner.id != current_user.id:
        abort(403)
    db.session.delete(post_delete)
    db.session.commit()
    flash(f"Post id {post_delete.id} was deleted", category="success")
    return redirect(url_for('user'))
