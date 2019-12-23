from flask import request,redirect,url_for,render_template,flash,session,Blueprint
from flask_blog import app
from flask_blog import db
from flask_blog.models.entries import Entry
from flask_blog.views.views import login_required
from  sqlalchemy.sql.expression import func
import os
import random
import numpy as np
abc=Entry.query.order_by(Entry.id.desc()).all();
index=0
idx=1
state=0;
a,b,temp,=[],[],[]
def poyo(n):
    global b;
    for i in range(1,n+1):
        b.append(i)
    return
def init():
    global a,temp
    b = []
    a = b
    temp = b
    for i in range(104, 999):
        if i % 4 == 0 and i % 5:
            a.append(i)
    random.shuffle(a)
def is_prime(x):
    for i in range(2,1+int(np.sqrt(x))):
        if x%i==0:
            return 0
    return 1

def init2():
    global a,temp
    b = []
    a = b
    temp = b
    for i in range(1001, 1400):
        if is_prime(i)^1 and i%10 :
            a.append(i)
    random.shuffle(a)
def init3():
    global a,temp
    b = []
    a = b
    temp = b
    for i in range(104, 999):
        if i % 3 == 0 and i % 10 and i%4 and i%5:
            a.append(i)
    random.shuffle(a)

def init4():
    global a, temp
    b = []
    a = b
    temp = b
    for i in range(1000, 5000):
        if i % 2 == 0 and i % 10 :
            a.append(i)
    random.shuffle(a)
def init5():
    global a,temp
    b = []
    a = b
    temp = b
    for i in range(1000,5000):
        if i % 3 == 0 and i % 10 and i%2 :
            a.append(i)
    random.shuffle(a)
def init6():
    global a,temp
    b = []
    a = b
    temp = b
    for i in range(1000,10000):
        if i % 5 == 0 and i % 10 and i%4:
            a.append(i)
    random.shuffle(a)





@app.route('/')
@login_required#
def show_entries():
    global state
    global abc
    abc = Entry.query.order_by(Entry.id.desc()).all();
    entries = abc
    flash('現在の個数は'+str(Entry.query.count()))
    ent1 = entries[:int(len(entries)/2)]
    ent2 = entries[len(ent1):]
    entries=zip(ent1,ent2)
    return render_template('entries/index.html',entries=entries)
@app.route('/entries',methods=['POST'])
@login_required
def add_entry():
    global idx
    entry=Entry(
        title=request.form['title'],
        text=request.form['text'],
        body='未提出',
        stat='',
        cnt=0
    )
    db.session.add(entry)
    db.session.commit()
    idx+=1
    flash('新しい問題が追加された.')
    return redirect(url_for('show_entries'))
@app.route('/entries/new',methods=['GET'])
@login_required
def new_entry():
    return render_template('entries/new.html')
@app.route('/entries/<int:id>',methods=['GET'])
@login_required
def show_entry(id):
    entry=Entry.query.get(id)
    return render_template('entries/show.html',entry=entry)
@app.route('/entries/<int:id>/edit',methods=['GET'])
@login_required
def edit_entry(id):
    entry=Entry.query.get(id)
    return render_template('entries/edit.html',entry=entry)
@app.route('/entries/<int:id>/update',methods=['POST'])
@login_required
def update_entry(id):
    entry=Entry.query.get(id)
    entry.title=request.form['title']
    entry.text=request.form['text']
    entry.body='未提出'
    db.session.merge(entry)
    db.session.commit()
    flash('The article has been updated.')
    return redirect(url_for('show_entries'))
@app.route('/entries/<int:id>/delete',methods=['POST'])
@login_required
def delete_entry(id):
    entry=Entry.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    flash('指定された問題が削除された.')
    return redirect(url_for('show_entries'))
@app.route('/entries/<int:id>/judge',methods=['POST','GET'])
@login_required
def judge(id):
    flash(id)
    entry=Entry.query.get(id)
    a=list(entry.text.split("*"))
    b=list(request.form['pms'].split("*"))
    a.sort()
    b.sort()
    print(a)
    print(b)
    entry.body = '正答' if a == b else '誤答'
    if a==b:
        flash("AC")
    else:
        flash("WA.  The Answer is "+entry.text)
    entry.cnt += (a == b)
    db.session.merge(entry)
    db.session.commit()
    os.system("mpg123 " + ("wa.mp3" if not a == b else "ac.mp3")+ " &")
    return redirect(url_for('show_entries')) if state==0 else redirect(url_for('quiz'))
@app.route('/entries')
@login_required
def shuffle():
    entries=Entry.query.order_by(func.random()).all()
    global abc
    abc=entries
    ent1 = entries[:int(len(entries) / 2)]
    ent2 = entries[len(ent1):]
    entries = zip(ent1, ent2)
    return render_template('entries/index.html',entries=entries)
@app.route('/entries/quiz')
@login_required
def quiz():
    global index,state
    global b
    if state==0:
        poyo(Entry.query.count())
        index=1
        random.shuffle(b)
        state=1;
    print("状況"+str(state))
    print("指数"+str(index))
    print("配列bの要素数"+str(len(b)))
    flash("配列bの要素数"+str(len(b)))
    if Entry.query.count() < (index):
        state=0
        print("終了しました終了しました終了しました終了しました")
        flash("Finished.")
        return redirect(url_for('show_entries'))
    if Entry.query.count() >= (index-1):
        entry = Entry.query.get(b[index - 1])
        flash(b[index - 1])
        print("通過済み with"+str(index))
        index += 1
        return render_template('entries/quiz.html', entry=entry)
    return
@app.route('/entries/q2')
@login_required
def q2():
    global state,index
    global a
    n = len(a)
    if state==0:
        index=0;
        state=1
        init()
    index+=1;
    if index-1 < n:
        flash("今"+str(index)+"個目."+str(len(a)))
        return render_template('entries/q2.html', entry=a[index-1])
    state=0;
    flash("finished")
    return redirect(url_for('show_entries'))
@app.route('/entries/q3')
@login_required
def q3():
    global state,index
    global a
    n = len(a)
    if state==0:
        index=0;
        state=1
        init2()
    index+=1;
    if index-1 < n:
        flash("今"+str(index)+"個目."+str(len(a)))
        return render_template('entries/q2.html', entry=a[index-1])
    state=0;
    flash("finished")
    return redirect(url_for('show_entries'))
@app.route('/entries/q4')
@login_required
def q4():
    global state,index
    global a
    n = len(a)
    if state==0:
        index=0;
        state=1
        init3()
    index+=1;
    if index-1 < n:
        flash("今"+str(index)+"個目."+str(len(a)))
        return render_template('entries/q2.html', entry=a[index-1])
    state=0;
    flash("finished")
    return redirect(url_for('show_entries'))
@app.route('/entries/q5')
@login_required
def q5():
    global state,index
    global a
    n = len(a)
    if state==0:
        index=0;
        state=1
        init4()
    index+=1;
    if index-1 < n:
        flash("今"+str(index)+"個目."+str(len(a)))
        return render_template('entries/q2.html', entry=a[index-1])
    state=0;
    flash("finished")
    return redirect(url_for('show_entries'))
@app.route('/entries/q6')
@login_required
def q6():
    global state,index
    global a
    n = len(a)
    if state==0:
        index=0;
        state=1
        init5()
    index+=1;
    if index-1 < n:
        flash("今"+str(index)+"個目."+str(len(a)))
        return render_template('entries/q2.html', entry=a[index-1])
    state=0;
    flash("finished")
    return redirect(url_for('show_entries'))
@app.route('/entries/q7')
@login_required
def q7():
    global state,index
    global a
    n = len(a)
    if state==0:
        index=0;
        state=1
        init6()
    index+=1;
    if index-1 < n:
        flash("今"+str(index)+"個目."+str(len(a)))
        return render_template('entries/q2.html', entry=a[index-1])
    state=0;
    flash("finished")
    return redirect(url_for('show_entries'))


@app.route('/entries/<int:id>/judge2',methods=['POST','GET'])
@login_required
def judge2(id):
    global temp
    b=list(request.form['pms'].split("*"))
    a=[]
    m=id
    for i in range(2,id):
        while m%i==0:
            a.append(str(i))
            m/=i;
    if m!=1:
        a.append(str(m))
    a.sort()
    b.sort()
    print(a)
    print(b)
    if a==b:
        flash("AC")
    else:
        flash("WA.  The Answer is "+str(a)+"and your input is"+str(b)+"."+str(id))
        temp.append(id)
    os.system("mpg123 " + ("wa.mp3" if not a == b else "ac.mp3")+ " &")
    if state==0:
        print(temp)
    return redirect(url_for('show_entries')) if state==0 else redirect(url_for('q2'))
