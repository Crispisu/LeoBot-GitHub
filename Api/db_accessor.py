import psycopg2
from datetime import date, datetime
import os
import urllib.parse as urlparse

class DbAccessor:
    
    def __init__(self):
        # self.database = 'dbname=SZData user= password='
        # self.connection = psycopg2.connect(self.database) 
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port

        self.connection = psycopg2.connect(
                            dbname=dbname,
                            user=user,
                            password=password,
                            host=host,
                            port=port
                            )

    def close(self):
        self.connection.close()

    def add_patient(self):
        # jd = str(date.today())
        query = 'insert into "Patient" ("Join_Date") values (%s) RETURNING "ID"'
        c = self.connection.cursor()
        queryParamms = (date.today().strftime('%Y-%m-%d'),)
        c.execute(query, queryParamms)
        self.connection.commit()
        last_id = c.fetchone()[0]
        c.close()
        return last_id

    def getSessionCount(self, Patient_ID=0):
        c = self.connection.cursor()
        select_session_query = 'select count("Session_no") from "SzondiData" where "Patient_ID" = %s'
        c.execute(select_session_query, (Patient_ID,))
        session_number = int(c.fetchone()[0])
        c.close()
        return session_number

    def getSessionTimer(self, Patient_ID=0):
        c = self.connection.cursor()
        query = """select "Run_Date" from "SzondiData" where "Patient_ID" = %s order by "Run_Date" desc limit 1"""
        c.execute(query, (Patient_ID,))
        row = c.fetchone()
        c.close()
        if row is None:
            return True
        last_session = datetime.strptime(row[0], '%Y-%m-%d')
        today = datetime.today()
        delta = today - last_session
        if delta.days < 2:
            return False
        else:
            return True
    

    def add_session(self, selected_cards, Patient_ID):
        c = self.connection.cursor()
        session_number = self.getSessionCount(Patient_ID) + 1
        selected_cards = list(selected_cards)
        selected_cards.insert(0, date.today().strftime('%Y-%m-%d'))
        selected_cards.insert(0, session_number)
        selected_cards.insert(0, Patient_ID)
        query = """insert into "SzondiData" ("Patient_ID", "Session_no", "Run_Date", "Draw_1_S_1", "Draw_1_S_2", "Draw_1_A_1", "Draw_1_A_2",
        "Draw_2_S_1",
        "Draw_2_S_2",
        "Draw_2_A_1",
        "Draw_2_A_2",
        "Draw_3_S_1",
        "Draw_3_S_2",
        "Draw_3_A_1",
        "Draw_3_A_2",
        "Draw_4_S_1",
        "Draw_4_S_2",
        "Draw_4_A_1",
        "Draw_4_A_2",
        "Draw_5_S_1",
        "Draw_5_S_2",
        "Draw_5_A_1",
        "Draw_5_A_2",
        "Draw_6_S_1",
        "Draw_6_S_2",
        "Draw_6_A_1",
        "Draw_6_A_2") values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING "ID" """
        c.execute(query, selected_cards)
        self.connection.commit()
        last_id = c.fetchone()[0]
        c.close()
        return last_id

    def calc_int_result(self, cardsDictionary, session_id):
        items = dict(cardsDictionary).items()
        h = []
        s = []
        e = []
        hy = []
        k = []
        p = []
        d = []
        m = []
        for key, value in items:
            if str(key).__contains__('_S_'):
                if str(value).__contains__('H') and not str(value).__contains__('Hy'):
                    h.append('+')
                if str(value).__contains__('S'):
                    s.append('+')
                if str(value).__contains__('E'):
                    e.append('+')
                if str(value).__contains__('Hy'):
                    hy.append('+')
                if str(value).__contains__('K'):
                    k.append('+')
                if str(value).__contains__('P'):
                    p.append('+')
                if str(value).__contains__('D'):
                    d.append('+')
                if str(value).__contains__('M'):
                    m.append('+')
            else:
                if str(value).__contains__('H') and not str(value).__contains__('Hy'):
                    h.append('-')
                if str(value).__contains__('S'):
                    s.append('-')
                if str(value).__contains__('E'):
                    e.append('-')
                if str(value).__contains__('Hy'):
                    hy.append('-')
                if str(value).__contains__('K'):
                    k.append('-')
                if str(value).__contains__('P'):
                    p.append('-')
                if str(value).__contains__('D'):
                    d.append('-')
                if str(value).__contains__('M'):
                    m.append('-')
        h = self.calc_final_result(h)
        s = self.calc_final_result(s)
        e = self.calc_final_result(e)
        hy = self.calc_final_result(hy)
        k = self.calc_final_result(k)
        p = self.calc_final_result(p)
        d = self.calc_final_result(d)
        m = self.calc_final_result(m)
        result = [session_id, h, s, e, hy, k, p, d, m]
        print(result)
        query = """insert into "SessionResults" ("Session_ID", "h", "s", "e", "hy", "k", "p", "d", "m") 
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        c = self.connection.cursor()
        c.execute(query, result)
        self.connection.commit()
        c.close()

    def calc_final_result(self, column):
        zero = [(0,0), (1,0), (0,1), (1,1)]
        plus = [(3,0), (2,1), (2,0), (3,1)]
        minus = [(0,2), (0,3), (1,2), (1,3)]
        plus_minus = [(2,2), (3,3), (2, 3), (2,4), (4,2),(3,2)]
        exclamation_plus = [(4,0), (4,1)]
        exclamation_double_plus = [(5,0), (5,1)]
        exclamation_triple_plus = [(6,0)]
        exclamation_minus = [(0,4), (1,4)]
        exclamation_double_minus = [(0,5), (1,5)]
        exclamation_triple_minus = [(0,6)]
        result = (list(column).count('+'),list(column).count('-'))
        if result in zero:
            return '0'
        if result in plus:
            return '+'
        if result in minus:
            return '-'
        if result in plus_minus:
            return '±'
        if result in exclamation_plus:
            return '+!'
        if result in exclamation_double_plus:
            return '+!!'
        if result in exclamation_triple_plus:
            return '+!!!'
        if result in exclamation_minus:
            return '-!'
        if result in exclamation_double_minus:
            return '-!!'
        if result in exclamation_triple_minus:
            return '-!!!'

                
        