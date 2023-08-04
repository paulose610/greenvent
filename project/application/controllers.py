from flask import current_app as app
from flask import render_template, redirect, url_for, flash,request
from application.models import user,cat,prod,Cart
from application.forms import RegisterForm, LoginForm
from application.database import db
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func



@login_required
@app.route('/home')
def hp():
    cate=cat.query.all()
    c=5
    d={}
    for i in current_user.cart:
        d[i.Pid]=i.no

    return render_template('hp.html',cate=cate,c=c,d=d)


@app.route('/register', methods=['GET','POST'])
def reg():
    form=RegisterForm()
    if form.validate_on_submit():
        utc=user(uname=form.uname.data,
                 password=form.password1.data
                 )
        db.session.add(utc)
        db.session.commit()
        login_user(utc)
        flash(f"account created and logged in as {utc.uname}", category='success')
        return redirect(url_for('hp'))
    if form.errors !={}: 
        for errmsg in form.errors.values():
            flash(f'{errmsg}', category='danger')

    return render_template('reg.html',form=form)

@app.route('/',methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user=user.query.filter_by(uname=form.uname.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
            ):
              login_user(attempted_user)
              flash (f'successfully logged in as: {attempted_user.uname}',category='success')
              return redirect(url_for('hp'))
        else:
            flash("username or password is not correct! Please try again.", category='danger')
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("you've been logged out", category='info')
    return redirect(url_for("login"))

@login_required
@app.route('/fsearch',methods=['GET','POST'])
def fsearch():
    
    d={}
    for i in current_user.cart:
        d[i.Pid]=i.no

    fp = prod.query.all()
    cats=cat.query.all()
    m=False

    product=request.args.get('search')
    if product:
        query = "%"+product+"%"
        fp=prod.query.filter(prod.pname.like(query)).all()
        return render_template('fsearch.html',products=fp)
            
    category = request.args.get('category')
    price = request.args.get('price')
    expiry = request.args.get('expiry')

    
    fp = prod.query.all()
    cats=cat.query.all()
    m=False
    

    if category:
        category="%"+category+"%"
        cate=cat.query.filter(cat.cname.like(category)).first()
        if cate:
            cid=cate.id
            fp = prod.query.filter(prod.catid==cid)
            m=True
        else:
            return render_template('fsearch.html',products=None)            

    if price:
        try:
            price = float(price)
            fp = [p for p in fp if p.price<=price]
        except ValueError:
            return render_template('fsearch.html',products=None)
        m=True    

    if expiry:
        fp = [p for p in fp if p.expiry<=expiry]
        m=True

    if not m:
        return render_template('fsearch.html',products=None)   

    return render_template('fsearch.html', products=fp,cate=cats,d=d)


@app.route('/modifycart/<int:prodid>', methods=['POST'])
def modifycart(prodid):
    action = request.form['action']
    product=prod.query.filter(prod.id==prodid).first()
    cart = current_user.cart

    cartprod = Cart.query.filter_by(user_id=current_user.id, Pid=prodid).first()

    if cartprod:
        if action == 'add':
            cartprod.no += 1
            product.stock-=1
            product.sold+=1
        elif action == 'remove':
            if cartprod.no>0:
                cartprod.no -= 1
                product.stock+=1
                product.sold-=1
            else:
                db.session.delete(cartprod)
    elif action=="add":
        product.stock-=1
        product.sold+=1
        cartprod = Cart(user_id=current_user.id, Pid=prodid, no=1,pname=product.pname,unit=product.unit,price=product.price,qty=product.qty)
        db.session.add(cartprod)
    else:
        pass
    db.session.commit()

    return redirect(request.referrer)


@app.route('/cart',methods=['GET','POST'])
def cart():
    tp=db.session.query(func.sum(Cart.no*Cart.price)).scalar()
    print(tp)
    cart=current_user.cart
    return render_template('cart.html',cart=cart,tp=tp)

@app.route('/home/checkout',methods=['POST','GET'])
def checkout():
    if request.method=='POST':
        tp=db.session.query()
        cart=current_user.cart
        for i in cart:
            db.session.delete(i)
        db.session.commit()
        flash (f'Thank you for shopping. Order placed successfully',category='success')
    return redirect(url_for('hp'))    
