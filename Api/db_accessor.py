import sqlite3
import pandas as pd
from datetime import date, datetime

class DbAccessor:
    
    def __init__(self):
        self.database = 'Api/AppData/SZData.db'
        self.connection = sqlite3.connect(self.database) 

    def add_patient(self):
        # jd = str(date.today())
        query = 'insert into Patient (Join_Date) values (?)'
        c = self.connection.cursor()
        # c.execute(query + '(' + str(date.today())+')')
        c.execute(query, (date.today().strftime('%Y-%m-%d'),))
        self.connection.commit()
        last_id = c.lastrowid
        c.close()
        return last_id

    def getSessionCount(self, Patient_ID=0):
        c = self.connection.cursor()
        select_session_query = 'select count(Session_no) from SZondiData where Patient_ID = ?'
        c.execute(select_session_query, (Patient_ID,))
        session_number = int(c.fetchone()[0])
        c.close()
        return session_number

    def getSessionTimer(self, Patient_ID=0):
        c = self.connection.cursor()
        query = """select Run_Date from SZondiData where Patient_ID = ? order by Run_Date desc limit 1"""
        c.execute(query, (Patient_ID,))
        row = c.fetchone()
        if row is None:
            return False
        last_session = datetime.strptime(row[0], '%Y-%m-%d')
        today = datetime.today()
        delta = today - last_session
        if delta.days < 2:
            return False
        else:
            return True
        c.close()
    

    def add_session(self, selected_cards, Patient_ID):
        c = self.connection.cursor()
        session_number = self.getSessionCount(Patient_ID) + 1
        selected_cards = list(selected_cards)
        selected_cards.insert(0, date.today().strftime('%Y-%m-%d'))
        selected_cards.insert(0, session_number)
        selected_cards.insert(0, Patient_ID)
        query = """insert into SZondiData (Patient_ID, Session_no, Run_Date, Draw_1_S_1, Draw_1_S_2, Draw_1_A_1, Draw_1_A_2,
        Draw_2_S_1,
        Draw_2_S_2,
        Draw_2_A_1,
        Draw_2_A_2,
        Draw_3_S_1,
        Draw_3_S_2,
        Draw_3_A_1,
        Draw_3_A_2,
        Draw_4_S_1,
        Draw_4_S_2,
        Draw_4_A_1,
        Draw_4_A_2,
        Draw_5_S_1,
        Draw_5_S_2,
        Draw_5_A_1,
        Draw_5_A_2,
        Draw_6_S_1,
        Draw_6_S_2,
        Draw_6_A_1,
        Draw_6_A_2) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        c.execute(query, selected_cards)
        self.connection.commit()
        c.close()

    def calc_int_result(self, cardsDictionary):
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

                
        