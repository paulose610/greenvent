from flask import current_app as app
from flask import render_template, redirect, url_for, flash,request,Response
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg') 
import io
import base64
from application.models import user,cat,prod,Cart
from application.forms import RegisterForm, LoginForm
from application.database import db
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func, desc

#mcl=['123ewq','123qwe','321wqe']

#@login_required
@app.route('/',methods=['GET','POST'])
@app.route('/home')
def hp():
    
    offers=prod.query.filter(prod.offer>0,prod.stock>0).limit(5)
    cate=cat.query.all()
    ocn={}
    for i in offers:
        ocn[i.id]=cat.query.filter(cat.id==i.catid).first().cname
    d={}
    if current_user.is_authenticated:
        for i in current_user.cart:
            d[i.Pid]=i.no

    return render_template('hp.html',cate=cate,d=d,offers=offers,ocn=ocn)


@app.route('/register', methods=['GET','POST'])
def reg():
    form=RegisterForm()
    if form.validate_on_submit():
        
        r=None
        if form.mancode.data=='123ewq':
            r='manager'
        elif form.mancode.data=='':
            r="User"  
             
        if r:
            newser=user(uname=form.uname.data,
                        password=form.password1.data,
                        role=r)
            db.session.add(newser)
            db.session.commit()
            login_user(newser)
            flash(f"Account created and logged in as {newser.uname}", category='success')
            return redirect(url_for('hp'))
        else:
            flash('incorrect manager-code!',category='danger')
                
    if form.errors !={}: 
        for errmsg in form.errors.values():
            flash(f'{errmsg}', category='danger')

    return render_template('reg.html',form=form)


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

#@login_required
@app.route('/fsearch',methods=['GET','POST'])
def fsearch():
    dropcat=cat.query.all()
    d={}
    if current_user.is_authenticated:
     for i in current_user.cart:
        d[i.Pid]=i.no

    fp = prod.query.all()
    cats=cat.query.all()
    ocn={}
    for i in fp:
        ocn[i.id]=cat.query.filter(cat.id==i.catid).first().cname

    m=False

    product=request.args.get('search')
    if product:
        query = "%"+product+"%"
        fp=prod.query.filter(prod.pname.like(query)).all()
        return render_template('fsearch.html',products=fp,cate=dropcat,ocn=ocn,d=d)
            
    category = request.args.get('category')
    price = request.args.get('price')
    expiry = request.args.get('expiry')

    
    m=False
    

    if category:
        #category="%"+category+"%"
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

    return render_template('fsearch.html', products=fp,cate=cats,d=d,ocn=ocn)

@login_required
@app.route('/modifycart/<int:prodid>', methods=['POST'])
def modifycart(prodid):
    action = request.form['action']
    product=prod.query.filter(prod.id==prodid).first()

    cartprod = Cart.query.filter_by(user_id=current_user.id, Pid=prodid).first()
    
    if cartprod:
        if action == 'add':
            if product.stock>0:
                cartprod.no += 1
                product.stock-=1
                product.sold+=1
            else:
                flash('sorry, out of stock!',category='danger')    
        elif action == 'remove':
            if cartprod.no>0:
                cartprod.no -= 1
                product.stock+=1
                product.sold-=1
            else:
                db.session.delete(cartprod)
    elif action=="add" and product.stock>0:
        product.stock-=1
        product.sold+=1
        cartprod = Cart(user_id=current_user.id, Pid=prodid, no=1,pname=product.pname,unit=product.unit,price=product.price,qty=product.qty)
        db.session.add(cartprod)
    else:
        pass
    db.session.commit()

    return redirect(request.referrer)

@login_required
@app.route('/cart',methods=['GET','POST'])
def cart():
    cate=cat.query.all()
    cart=Cart.query.filter(Cart.user_id==current_user.id)
    tp=0
    d={}
    for i in prod.query.all():
        if i.offer:
            d[i.pname]=i.price*(1-i.offer/100)
    #print(d)        
    for i in cart:
        if i.pname in d.keys():
            #print('yes')
            tp+=i.no*d[i.pname]
        else:    
            tp+=i.no*i.price
    return render_template('cart.html',cart=cart,tp=tp,cate=cate,d=d)

@app.route('/home/checkout',methods=['POST','GET'])
def checkout():
    cate=cat.query.all()
    if request.method=='POST':
        cart=Cart.query.filter(Cart.user_id==current_user.id)
        for i in cart:
            db.session.delete(i)
        db.session.commit()
        flash (f'Thank you for shopping. Order placed successfully.',category='success')
    return redirect(url_for('hp'))    

@login_required
@app.route('/manage', methods=['GET','POST'])
def managecat():
    cate=cat.query.all()
    img_base64=None
    if request.method in ['GET','POST'] and current_user.is_authenticated:
        if current_user.role=='manager':
            products=prod.query.order_by(desc(prod.sold)).all()
            num = len(products) * 20 // 100
            top20 = products[:num]
            names = [i.pname for i in top20]
            sold = [i.sold for i in top20]
            plt.figure(figsize=(10,6))
            plt.bar(names, sold)
            plt.xlabel('products')
            plt.ylabel('sales')
            plt.title('most sold products')
    
        
            img_stream = io.BytesIO()
            plt.tight_layout()
            plt.savefig(img_stream, format='png')
            img_stream.seek(0)
    
    
            img_base64 = base64.b64encode(img_stream.read()).decode('utf-8')
            #print(img)
    
    if request.method=='POST' and current_user.is_authenticated:
       if current_user.role=='manager': 
        nocat=True
        action = request.form['action']
        if action in ['add','modify','remove','clear']:
         n = request.form['cname']
         nn = request.form['cnewname']
         catid=None
         p=True
         for i in cate:
            if i.cname==n:
                catid=i.id
            if i.cname==nn:
                flash("new category name exists!",category="danger")
                p=False
                break 
          
        if action=='modify' and p:        
         if nn!='' and n!='' and n!=nn: 
            for i in cate:
                if i.cname==n:
                    i.cname=nn
                    nocat=False
                    flash('Modified Successfully',category='success')
                    break
            if nocat:
                 flash('that category does not exist!', category='info')    
         else:
            flash('provide  both category name and new name and they should not be the same', category='info') 
         
        if action=='remove':
         if n!='':
            for i in cate:
                if i.cname==n:
                    if prod.query.filter(prod.catid==catid).first():
                        flash('products of this category exists! First clear all products.',category='info')
                        nocat=False
                        break
                    else:
                        db.session.delete(i)
                        flash('successfully deleted',category='success')
                        nocat=False
                        break
            if nocat:        
             flash('no such category!',category='info')

         else:
            flash('provide category name!',category="info")  

        if action=='add':
         if n!='':    
            for i in cate:
                if i.cname==n:
                    flash('category name already exists!',category='info')
                    nocat=False
                    break
            if nocat:
                c=cat(cname=n)
                db.session.add(c) 
                flash('successfully added!',category='success')
         else:
             flash('provide category name!',category='info') 
        if action=='clear':
            if n!='':
             catprod=prod.query.filter(prod.catid==catid)
             for i in catprod:
                db.session.delete(i)
             flash(f'cleared all products from {n}',category='success')                    
            else:
             flash('provide category name!',category='info') 
    
        p=True
        if action in ['modifyp','addp']:
            pnewname=request.form['pnewname']
            pname=request.form['pname']
            category=request.form['cat']
            catid=cat.query.filter(cat.cname==category).first()
            if catid:
                catid=catid.id
            try:
                price=float(request.form['price'])
            except:
                flash('price is not right',category='danger')
                p=False    
            unit=request.form['unit']
            qty=request.form['qty']
            stock=request.form['stock']
            offer=request.form['offer']
            l=[pnewname,offer,pname,catid,unit,qty,stock,offer]
             

        if action=='addp' and p:
            if '' in l[2:]:
                flash('not all arguments are present!',category="info")
            elif  prod.query.filter(prod.pname==pname).first():
                #print(prod.query.filter(prod.pname==pname).first())
                flash('product already exists!',category="info")   
            elif catid==None:
                flash('category not found!',category="info")  
            elif float(offer)>90:
                flash('enter valid offer!',category="danger")       
            else:
                p=prod(pname=pname,catid=catid,price=price,qty=int(qty),unit=unit,stock=int(stock),sold=0,offer=offer)
                db.session.add(p) 
                db.session.commit()
                flash('added successfully!',category='success')

        if action=='modifyp' and p:
            if '' in l[2:]:
                flash('not all arguments are present!',category="info")   
            elif catid==None:
                flash('category not found!',category="info")
            elif float(offer)>90:
                flash('enter valid offer!',category="danger")  

            else:
                product=prod.query.filter(prod.pname==pname).first()
                if product:
                 if len(pnewname)>0:
                    product.pname=pnewname
                 else:
                    product.pname=pname
                 product.offer=offer  
                 product.price=price
                 product.unit=unit
                 product.qty=qty
                 product.stock=stock       
                
                 flash('product modified successfully!',category='info')
            db.session.commit() 

        if action=='removep':
            pname=request.form['pname']
            product=prod.query.filter(prod.pname==pname).first()
            if product:  
                db.session.delete(product)
                flash('product removed successfully!',category="success")
            else:
                flash('enter valid product name!',category="info")    

    db.session.commit()
    return render_template('manage.html',cate=cate,img=img_base64)

    

@app.route('/offers')
def offers():
    offers=prod.query.filter(prod.offer>0)
    cate=cat.query.all()
    d={}
    if current_user.is_authenticated:
        for i in current_user.cart:
            d[i.Pid]=i.no
    ocn={}
    for i in offers:
        ocn[i.id]=cat.query.filter(cat.id==i.catid).first().cname
    return render_template('/offers.html',offers=offers,ocn=ocn,d=d,cate=cate)

