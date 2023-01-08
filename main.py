from flask import Flask, render_template, request, send_file, redirect, url_for, session
from database import *
from werkzeug.utils import secure_filename
from csv import writer
import os
import pandas as pd
import shutil

app = Flask(__name__, template_folder='templates')
app.secret_key = 'DBMS'
usn = ''
Studname = ''
Scheme = ''
StdPh = ''
StdMail = ''
Profname = ''
Profid = ''


@app.route('/')
def show():
    return render_template('main.html')


@app.route('/LoginPage')
def loginpage():
    return render_template('loginpage.html')


@app.route('/LoginProf')
def loginp():
    return render_template('login.html')


@app.route('/LoginStu')
def logins():
    return render_template('loginpage.html')


@app.route('/StudentAuthentication', methods=['GET', 'POST'])
def authstudent():
    global usn, Studname, Scheme, StdPh, StdMail
    usn = request.form['usn']
    psw = request.form['psw']
    repsw = request.form['reppsw']
    if (psw != repsw):
        return render_template('loginpage.html', match=1)
    flag = StudentAuth(usn, psw)
    info = getInfo(usn)
    if (flag):
        Studname = flag[1]
        Scheme = flag[2]
        StdPh = info[2]
        StdMail = info[3]
        session['loggedins'] = True
        session['usn'] = usn
        session['studname'] = Studname
        return render_template('StudentMain.html', uname=Studname, scheme=Scheme, usn=usn, ph=StdPh, email=StdMail)
    return render_template('loginpage.html', res=1)


@app.route('/ProfAuthentication', methods=['GET', 'POST'])
def authprof():
    uname = request.form['uname']
    global Profname, Profid
    Profname = uname
    psw = request.form['profpsw']
    repsw = request.form['profreppsw']
    if (psw != repsw):
        return render_template('login.html', match=1)
    flag = ProfAuth(uname, psw)
    if (flag):
        Profid = flag[0][1]
        session['loggedinp'] = True
        session['proid'] = Profid
        session['proname'] = Profname
        return render_template('ProfMain.html', name=Profname, id=Profid)
    return render_template('login.html', res=1)


@app.route('/CreateStudentId\'s', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        cscheme = request.form['scheme']
        f = request.files['file']
        f.save(secure_filename(f.filename))
        data = pd.read_csv(secure_filename(f.filename), on_bad_lines='skip')
        df = pd.DataFrame(data)
        flag = CreateStudentIds(cscheme, df)
        os.remove(secure_filename(f.filename))
        if flag == 1:
            return render_template('ProfMain.html', name=Profname, id=Profid,
                                   status='STUDENTs IDs CREATED SUCCESSFULLY')
        else:
            return render_template('ProfMain.html', name=Profname, id=Profid,
                                   err='ERROR IN CREATING STUDENT(NOTE:USN MUST BE UNIQUE)')
    return render_template('ProfMain.html', name=Profname, id=Profid, err='ERROR')


@app.route('/1semresult', methods=['GET', 'POST'])
def semres1():
    sem = 1
    info = getInfo(usn)
    scheme = info[1]
    got = getres(scheme, sem, usn)
    if got:
        return render_template('Marks.html', name=got, uname=Studname, sem=sem)
    else:
        return render_template('Marks.html', error='NO RECORD FOUND')


@app.route('/2semresult', methods=['GET', 'POST'])
def semres2():
    sem = 2
    info = getInfo(usn)
    scheme = info[1]
    got = getres(scheme, sem, usn)
    if got:
        return render_template('Marks.html', name=got, uname=Studname, sem=sem)
    else:
        return render_template('Marks.html', error='NO RECORD FOUND')


@app.route('/3semresult', methods=['GET', 'POST'])
def semres3():
    sem = 3
    info = getInfo(usn)
    scheme = info[1]
    got = getres(scheme, sem, usn)
    if got:
        return render_template('Marks.html', name=got, uname=Studname, sem=sem)
    else:
        return render_template('Marks.html', error='NO RECORD FOUND')


@app.route('/4semresult', methods=['GET', 'POST'])
def semres4():
    sem = 4
    info = getInfo(usn)
    scheme = info[1]
    got = getres(scheme, sem, usn)
    if got:
        return render_template('Marks.html', name=got, uname=Studname, sem=sem)
    else:
        return render_template('Marks.html', error='NO RECORD FOUND')


@app.route('/5semresult', methods=['GET', 'POST'])
def semres5():
    sem = 5
    info = getInfo(usn)
    print(info)
    scheme = info[1]
    got = getres(scheme, sem, usn)
    if got:
        return render_template('Marks.html', name=got, uname=Studname, sem=sem)
    else:
        return render_template('Marks.html', error='NO RECORD FOUND')


@app.route('/6semresult', methods=['GET', 'POST'])
def semres6():
    sem = 6
    info = getInfo(usn)
    scheme = info[1]
    got = getres(scheme, sem, usn)
    if got:
        return render_template('Marks.html', name=got, uname=Studname, sem=sem)
    else:
        return render_template('Marks.html', error='NO RECORD FOUND')


@app.route('/7semresult', methods=['GET', 'POST'])
def semres7():
    sem = 7
    info = getInfo(usn)
    scheme = info[1]
    got = getres(scheme, sem, usn)
    if got:
        return render_template('Marks.html', name=got, uname=Studname, sem=sem)
    else:
        return render_template('Marks.html', error='NO RECORD FOUND')


@app.route('/8semresult', methods=['GET', 'POST'])
def semres8():
    sem = 8
    info = getInfo(usn)
    scheme = info[1]
    got = getres(scheme, sem, usn)
    if got:
        return render_template('Marks.html', name=got, uname=Studname, sem=sem)
    else:
        return render_template('Marks.html', error='NO RECORD FOUND')


@app.route('/dowloadFormat', methods=['GET', 'POST'])
def down():
    return send_file('format/Marks format.csv', as_attachment=True)


@app.route('/dowloadSFormat', methods=['GET', 'POST'])
def down1():
    return send_file('format/Id format.csv', as_attachment=True)


@app.route('/dowloadUFormat', methods=['GET', 'POST'])
def down3():
    return send_file('format/Up format.csv', as_attachment=True)


@app.route('/uploadmarkssheet', methods=['POST'])
def upload():
    if request.method == 'POST':
        scheme = request.form['scheme']
        pid = request.form['pid']
        sem = request.form['sem']
        subcode = request.form['subcode']
        subname = request.form['subname']
        f = request.files['file']
        f.save(secure_filename(f.filename))
        data = pd.read_csv(secure_filename(f.filename), on_bad_lines='skip')
        df = pd.DataFrame(data)
        markCsvUpload(int(scheme), int(pid), int(sem), subcode, subname, df)
        os.remove(secure_filename(f.filename))
        return render_template('ProfMain.html', name=Profname, id=Profid, status='MARKS UPDATED')
    return render_template('ProfMain.html', name=Profname, id=Profid, err='AN UNKNOWN ERROR OCCURED')


@app.route('/getmarksformat', methods=['POST'])
def getformat():
    if os.path.exists('GEN/Marks format.csv'):
        os.remove('GEN/Marks format.csv')
    usnf = request.form['usn']
    res = getList(usnf)
    shutil.copy('format/Marks format.csv', 'GEN/')
    with open('GEN/Marks format.csv', 'a') as f_object:
        writer_object = writer(f_object)
        for i in range(len(res)):
            writer_object.writerow(tuple(res[i]))
        f_object.close()
    return send_file('GEN/Marks format.csv', as_attachment=True)


@app.route('/checkMarks', methods=['POST'])
def check():
    scheme = request.form['scheme']
    usn = request.form['susn']
    sem = request.form['sem']
    got = getres(scheme, sem, usn)
    print(got)
    if got:
        return render_template('Marks.html', name=got, usn=usn, ssm=sem, sch=scheme)
    else:
        return render_template('Marks.html', error='NO RECORD FOUND')


@app.route('/login')
def logouts():
    session.pop('loggedins', None)
    session.pop('usn', None)
    session.pop('studname', None)
    return redirect(url_for('show'))


@app.route('/Login')
def logoutp():
    session.pop('loggedinp', None)
    session.pop('profid', None)
    session.pop('profname', None)
    return redirect(url_for('show'))


@app.route('/deleteRecord', methods=['GET', 'POST'])
def delFun():
    usn = request.form['susn']
    scheme = request.form['scheme']
    sem = request.form['sem']
    subcode = request.form['sub']
    f = delData(usn, scheme, sem, subcode)
    if f == 1:
        return render_template('ProfMain.html', name=Profname, id=Profid, status='MARKS UPDATED')
    return render_template('ProfMain.html', name=Profname, id=Profid, err='AN UNKNOWN ERROR OCCURED')


@app.route('/updateRecord', methods=['GET', 'POST'])
def update():
    scheme = request.form['scheme']
    sem = request.form['sem']
    sub = request.form['sub']
    fia = request.files['file']
    fia.save(secure_filename(fia.filename))
    data = pd.read_csv(secure_filename(fia.filename), on_bad_lines='skip')
    df = pd.DataFrame(data)
    f = updateMarks(scheme, sem, sub, df)
    os.remove(secure_filename(fia.filename))
    if f == 1:
        return render_template('ProfMain.html', name=Profname, id=Profid, status='MARKS UPDATED')
    return render_template('ProfMain.html', name=Profname, id=Profid, err='AN UNKNOWN ERROR OCCURED')


if __name__ == "__main__":
    app.run(debug=True, port=3400)
