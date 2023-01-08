import pymysql


def StudentAuth(usn, psw):
    flag = 0
    db = pymysql.connect(host="SagarPatil.mysql.pythonanywhere-services.com", user="SagarPatil", passwd='Sagar@2002',
                         database="SagarPatil$MiniPro")
    mycur = db.cursor()
    try:
        sql = "select StudPass,StudName,StudScheme from StudentLogin where StudUsn = %s"
        mycur.execute(sql, [usn])
        results = mycur.fetchone()
        flag = 1
    finally:
        if flag:
            if results:
                if psw in results:
                    db.close()
                    return results
        else:
            db.close()
            return 0


def CreateStudentIds(scheme, df):
    flag = 0
    db = pymysql.connect(host="SagarPatil.mysql.pythonanywhere-services.com", user="SagarPatil", passwd='Sagar@2002',
                         database="SagarPatil$MiniPro")
    mycur = db.cursor()
    try:
        for row in df.itertuples():
            sql = "INSERT INTO StudentLogin VALUES (%s, %s, %s, %s)"
            val = [row.USN, row.NAME, '123456', scheme]
            mycur.execute(sql, val)
            sql = "INSERT INTO StudInfo VALUES (%s, %s, %s)"
            val = [row.USN, row.PHONE, row.EMAIL]
            mycur.execute(sql, val)
        db.commit()
        flag = 1
    finally:
        if flag == 1:
            db.close()
            return 1
        db.close()
        return 0


def ProfAuth(uname, psw):
    db = pymysql.connect(host="SagarPatil.mysql.pythonanywhere-services.com", user="SagarPatil", passwd='Sagar@2002',
                         database="SagarPatil$MiniPro")
    mycur = db.cursor()
    try:
        sql = "select ProfPass,ProfId from ProfLogin where ProfName = %s"
        mycur.execute(sql, [uname])
        results = mycur.fetchall()
    finally:
        if psw in results[0]:
            db.close()
            return results
        else:
            db.close()
            return 0


def getInfo(usn):
    try:
        db = pymysql.connect(host="SagarPatil.mysql.pythonanywhere-services.com", user="SagarPatil", passwd='Sagar@2002',
                             database="SagarPatil$MiniPro")
        mycur = db.cursor()
        sql = 'SELECT StudName,StudScheme,StudPh,StudEmail FROM StudentLogin S,StudInfo I WHERE S.StudUsn=I.StudUsn AND S.StudUsn=%s'
        mycur.execute(sql, [usn])
        res = mycur.fetchone()
        db.close()
        return res
    except:
        return 0


def getres(scheme, sem, usn):
    try:
        db = pymysql.connect(host="SagarPatil.mysql.pythonanywhere-services.com", user="SagarPatil", passwd='Sagar@2002',
                             database="SagarPatil$MiniPro")
        mycurs = db.cursor()
        sql = 'SELECT I.SubCode,SubName,Ia1,Ia2,Ia3,AvgIa,Marks,S.AttdPer,ProfName FROM ProfLogin P,IaMarks I,FinalMarks F,StudAttd S WHERE I.ProfId=P.ProfId AND S.StudUsn=I.StudUsn AND I.StudUsn=F.StudUsn AND S.SubCode=I.SubCode AND I.SubCode=F.SubCode AND I.StudUsn=%s AND I.Sem=%s AND I.Scheme=%s'
        mycurs.execute(sql, [usn, sem, scheme])
        res = mycurs.fetchall()
        db.close()
        return res
    except:
        return 0


def markCsvUpload(scheme, profId, sem, subcode, subname, df):
    db = pymysql.connect(host="SagarPatil.mysql.pythonanywhere-services.com", user="SagarPatil", passwd='Sagar@2002',
                         database="SagarPatil$MiniPro")
    mycurs = db.cursor()
    for row in df.itertuples():
        sql = 'INSERT INTO IaMarks VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        val = [row.USN, profId, subcode, subname, row.IA1, row.IA2, row.IA3, ((row.IA1 + row.IA2 + row.IA3) / 3) * 0.6,
               scheme, sem]
        mycurs.execute(sql, val)
        sql = 'INSERT INTO FinalMarks VALUES(%s, %s, %s)'
        val = [row.USN, subcode, row.ExternalMarks]
        mycurs.execute(sql, val)
        sql = 'INSERT INTO StudAttd VALUES(%s, %s, %s)'
        val = [row.USN, row.AttendancePercentage, subcode]
        mycurs.execute(sql, val)
    db.commit()
    db.close()


def getList(usn):
    try:
        db = pymysql.connect(host="SagarPatil.mysql.pythonanywhere-services.com", user="SagarPatil", passwd='Sagar@2002',
                             database="SagarPatil$MiniPro")
        mycur = db.cursor()
        sql = 'SELECT StudUsn FROM StudentLogin WHERE StudUsn LIKE %s OR %s ORDER BY StudUsn'
        mycur.execute(sql, [usn[0:7] + '%', usn[7:] + '%'])
        res = mycur.fetchall()
        db.close()
        return res
    except:
        return 0


def delData(usn, scheme, sem, sub):
    try:
        db = pymysql.connect(host="SagarPatil.mysql.pythonanywhere-services.com", user="SagarPatil",
                             passwd='Sagar@2002',
                             database="SagarPatil$MiniPro")
        mycur = db.cursor()
        sql = 'DELETE FROM IaMarks WHERE StudUsn=%s AND Scheme=%s AND Sem=%s AND SubCode=%s'
        val = [usn, int(scheme), int(sem), sub]
        mycur.execute(sql, val)
        sql = 'DELETE FROM FinalMarks WHERE StudUsn=%s AND SubCode=%s'
        val = [usn, sub]
        mycur.execute(sql, val)
        sql = 'DELETE FROM StudAttd WHERE StudUsn=%s AND SubCode=%s'
        val = [usn, sub]
        mycur.execute(sql, val)
        db.commit()
        db.close()
        return 1
    except:
        db.close()
        return 0


def updateMarks(scheme, sem, subcode, df):
    try:
        db = pymysql.connect(host="SagarPatil.mysql.pythonanywhere-services.com", user="SagarPatil",
                             passwd='Sagar@2002',
                             database="SagarPatil$MiniPro")
        mycur = db.cursor()
        for row in df.itertuples():
            sql = 'UPDATE IaMarks SET ProfId = %s,Ia1 = %s,Ia2 = %s,Ia3 = %s,AvgIa = %s WHERE StudUsn = %s AND SubCode=%s AND Scheme=%s AND Sem =%s'
            val = [row.ProfId, row.IA1, row.IA2, row.IA3, ((row.IA1 + row.IA2 + row.IA3) / 3) * 0.6, row.USN, subcode,
                   int(scheme), int(sem)]
            mycur.execute(sql, val)
            sql = 'UPDATE FinalMarks SET Marks = %s WHERE StudUsn = %s AND SubCode=%s'
            val = [row.ExternalMarks, row.USN, subcode]
            mycur.execute(sql, val)
            sql = 'UPDATE StudAttd SET AttdPer = %s WHERE StudUsn = %s AND SubCode=%s'
            val = [row.AttendancePercentage, row.USN, subcode]
            mycur.execute(sql, val)
        db.commit()
        db.close()
        return 1
    except:
        db.close()
        return 0
