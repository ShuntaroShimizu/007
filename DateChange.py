import calendar
import datetime
import pandas as pd
import numpy as np
import datetime as dt
from pandas import Series
import math

def config():
    #config
    fti=pd.read_table("C:/Users/pelu0/Desktop/ShiftManager/configvar.dat")
    #基準日
    sd=fti.columns.values
    sd=sd[0]
    sd=sd[-10:]
    sd=datetime.datetime.strptime(sd,'%Y/%m/%d')
    #fti.close()
    return sd

def stuff():
    #スタッフ
    fsi=pd.read_table("C:/Users/pelu0/Desktop/ShiftManager/staffinfo.dat",sep=',', header=None)
    fsi.columns=["No", "ID", "Name"]
    #人数数え
    pn=len(fsi)
    list_rows=fsi["No"].to_list()
    fsi.close()
    return pn, list_rows

def shift():
    #シフト
    input_data = open("C:/Users/pelu0/Desktop/ShiftManager/shift.dat", 'r')
    b = []
    # 一行ずつ読み込んでは表示する
    for rows in input_data:
        # コメントアウト部分を省く処理
        if rows[0] == '#':
            s=rows
            continue
        # 値を変数に格納する
        row = rows.rstrip('\n').split(',')
        month =[int(i) for i in row]
        b.append(month)
    # ファイルを閉じる
    fsh=pd.DataFrame(b)
    fsh.columns=["UID", "Date", "Job"]
    input_data.close()
    ed=fsh['Date'].max()

    #夜勤表
    fa=fsh[(fsh["Job"] == 4)|(fsh["Job"] == 5)|(fsh["Job"] == 6)|(fsh["Job"] == 0)|(fsh["Job"] == 1)|(fsh["Job"] == 2)|(fsh["Job"] == 3)|(fsh["Job"] == 30)]
    rl=fsh.drop_duplicates(subset="Date")
    rl=rl["Date"].tolist()
    cols=[4,5,6,0,1,2,3,30]
    fyh=[]
    fyh=pd.DataFrame(index=rl,columns=cols)

    for i in range(len(fa)):
        r=fa.iat[i, 1]
        c=fa.iat[i, 2]
        y = fa.iat[i, 0]

        if math.isnan(fyh.at[r, c]):
            fyh.at[r, c] = y
        elif not math.isnan(fyh.at[r, c]) and c == 3:
            fyh.at[r,30] = y
    print(fyh)
    fyh.to_csv("C:/Users/pelu0/Desktop/ShiftManager/fyh.csv")
    return ed,fsh,fyh,rl,cols


def request():
    #リクエスト
    frq=pd.read_table("C:/Users/pelu0/Desktop/ShiftManager/request.dat",sep=',', header=None)
    frq.columns=["UID", "Date", "Job"]
    frq=frq[(frq["Job"] == 4)|(frq["Job"] == 5)|(frq["Job"] == 6)|(frq["Job"] == 0)|(frq["Job"] == 1)|(frq["Job"] == 2)|(frq["Job"] == 3)|(frq["Job"] == 30)]
    ed,fsh,fyh,rl,cols=shift()
    fyhrq=[]
    fyhrq=pd.DataFrame(index=rl,columns=cols)
    for i in range(len(frq)):
        r=frq.iat[i, 1]
        c=frq.iat[i, 2]
        y = frq.iat[i, 0]
        fyhrq.at[r, c] = y

    print(fyhrq)
    fyhrq.to_csv("C:/Users/pelu0/Desktop/ShiftManager/fyhrq.csv")
    return fyhrq

def previous():
    #先月データ
    fpr=pd.read_table("C:/Users/pelu0/Desktop/ShiftManager/previous.dat",sep=',', header=None)
    fpr.columns=["UID", "Date", "Job"]

    #先月+今月
    fkh=[]
    ed,fsh,fyh,rl,cols=shift()
    fkh=pd.concat([fpr,fsh])
    l=len(fkh)

    sd=config()
    #基準日から日付計算
    for i in range(l):
        IntVar = fkh.iat[i, 1]
        fkh.iat[i, 1] = sd + datetime.timedelta(days=1)*IntVar
        fkh.iat[i, 1] =fkh.iat[i, 1].strftime('%Y/%m/%d')

    #日付ダブり削除＋Nan削除
    fkh1=fkh.loc[:,['Date']]
    fkh1=fkh1.drop_duplicates()
    fkh1=fkh1.dropna(subset=['Date'])
    list_cols = fkh1["Date"].to_list()

    #DataFrame
    pn, list_rows=stuff()
    cols = [list_cols]
    rows= [list_rows]
    fyh= pd.DataFrame(index=rows,columns=cols)

    #値代入
    for i in range(l):
        a=fkh.iat[i, 0]
        b=fkh.iat[i, 1]
        c = fkh.iat[i, 2]
        fyh.at[a, b] = c
    print(fyh)
    fyh.to_csv("C:/Users/pelu0/Desktop/ShiftManager/fsh.csv")

    fyh1=fyh.replace({0:"A日",1:"M日",2:"C日",3:"F日",4:"A夜",5:"M夜",6:"C夜",7:"明",8:"日勤",9:"他勤"} )
    fyh1=fyh1.replace({10:"休日",11:"休暇",12:"ダ"} )
    print(fyh1)
    fyh1.to_csv("C:/Users/pelu0/Desktop/ShiftManager/fshn.csv",encoding='Shift_JIS')

sd=config()
ed, fsh, fyh, rl, cols = shift()
#作成月の日付
#月末#
#month_range = calendar.monthrange(2020, 2)[1]
y=sd.year
m=sd.month
print(y)
#rows=pd.date_range(sd,'2023-04-30')
#print(rows)

dates = pd.date_range(sd, periods=ed+1,  freq='D')
print(dates)
ts = Series(range(ed+1), index=dates)
print(ts)

