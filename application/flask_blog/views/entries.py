from flask import request,redirect,url_for,render_template,flash,session,Blueprint
from flask_blog import app
from flask_blog import db
from flask_blog.models.entries import Entry
from flask_blog.views.views import login_required
from  sqlalchemy.sql.expression import func
import os
import random
abc=Entry.query.order_by(Entry.id.desc()).all();
index=1
idx=1
state=0;
a=[]
def init():
    global a
    b=[]
    a=b
    for i in range(104, 999):
        if i % 4 == 0 and i % 5:
            a.append(i)
    random.shuffle(a)
def init2():
    global a
    b = []
    a = b
    for i in range(104, 999):
        if i % 5 == 0 and i % 10:
            a.append(i)
    random.shuffle(a)

def init3():
    global a
    b = []
    a = b
    for i in range(104, 999):
        if i % 3 == 0 and i % 10 and i%4 and i%5:
            a.append(i)
    random.shuffle(a)
@app.route('/')
@login_required#
def show_entries():
    global state
    global abc
    entries=abc
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
    a=list(entry.text.split(","))
    b=list(request.form['pms'].split(","))
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
    entry = Entry.query.get(1)
    b=[i for i in range(1,Entry.query.count()+1)]
    if state==0:
        index=1
        random.shuffle(b)
        state=1;
    if Entry.query.count() >= index:
        entry = Entry.query.get(b[index - 1])
        index += 1
        return render_template('entries/quiz.html', entry=entry)
    state=0;
    flash("Finished.")
    return redirect(url_for('show_entries'))
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

@app.route('/entries/<int:id>/judge2',methods=['POST','GET'])
@login_required
def judge2(id):
    b=list(request.form['pms'].split(","))
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
        flash("WA.  The Answer is "+str(a)+"and your input is"+str(b))
    os.system("mpg123 " + ("wa.mp3" if not a == b else "ac.mp3")+ " &")
    return redirect(url_for('show_entries')) if state==0 else redirect(url_for('q2'))
