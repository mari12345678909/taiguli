from flask import render_template
from flask_login import login_user, logout_user
from os import path

from forms import AddProductForm, RegisterForm, LoginForm
from extension import app, db
from models import Product, User
from extension import redirect

@app.route("/")
def home():
  products = Product.query.all()
  return render_template("index.html", products=products)

@app.route("/view_product/<int:product_id>")
def view_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return render_template("404.html")
    return render_template("product.html", product=product)

@app.route("/add_product", methods=["GET","POST"])
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        file = form.img.data
        filename = file.filename
        file.save(path.join(app.root_path, "static", filename))


        new_product = Product(name=form.name.data, price=form.price.data, img=filename)
        db.session.add(new_product)
        db.session.commit()



    return render_template ("add_product.html", form=form)

@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = Product.query.get(product_id)

    form = AddProductForm(name=product.name, price=product.price, img=product.img)
    if form.validate_on_submit():
        file = form.img.data
        filename = file.filename
        file.save((path.join(app.root_path, 'static', filename)))

        product.name = form.name.data
        product.price = form.price.data
        product.img = filename

        db.session.commit()

        return redirect("/")
    return render_template("add_product.html", form=form)

@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    product = Product.query.get(product_id)

    db.session.delete(product)
    db.session.commit()

    return redirect("/")
@app.route("/register", methods=["GET","POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        user.create()
    return render_template ("register.html", form=form)

@app.route("/login", methods =["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)

    return render_template("login.html", form=form)

@app.route("/about")
def about_us():
    return render_template('about_us.html')