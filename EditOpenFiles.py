import datetime
import pandas as pd
import math

def config():
    #config
    fti = pd.read_table("C:/Users/pelu0/Desktop/ShiftManager/configvar.dat")
    #基準日
    sd = fti.columns.values
    sd = sd[0]
    sd = sd[-10:]
    sd = datetime.datetime.strptime(sd,'%Y/%m/%d')
    rk=fti.iloc[1,:].values
    rk = rk[0]
    rk=rk[-2:]
    return sd,rk #基準日(yyyy/mm/dd),連続勤務

def stuff():
    #スタッフ
    dfstaff = pd.read_table("C:/Users/pelu0/Desktop/ShiftManager/staffinfo.dat",sep=',', header=None)
    dfstaff.columns = ["No", "ID", "Name"]
    #人数数え
    number_of_stuff = len(dfstaff)
    staff_list = dfstaff["No"].to_list()
    return number_of_stuff, staff_list,dfstaff

def shift():
    #シフト
    input_data = open("C:/Users/pelu0/Desktop/ShiftManager/shift.dat", 'r')
    b = []
    # 一行ずつ読み込んでは表示する
    for rows in input_data:
        # コメントアウト部分を省く処理
        if rows[0] == '#':
            s = rows
            continue
        # 値を変数に格納する
        row = rows.rstrip('\n').split(',')
        month = [int(i) for i in row]
        b.append(month)
    # ファイルを閉じる
    dfshift = pd.DataFrame(b)
    dfshift.columns = ["UID", "Date", "Job"]
    input_data.close()
    ed = dfshift['Date'].max()

    #夜勤表
    #シフトから日直・夜勤の抽出
    dfnightshift = dfshift[(dfshift["Job"] == 4) | (dfshift["Job"] == 5) | (dfshift["Job"] == 6) | (dfshift["Job"] == 0) | (dfshift["Job"] == 1) | (dfshift["Job"] == 2) | (dfshift["Job"] == 3) | (dfshift["Job"] == 30)]
    data_list = dfshift.drop_duplicates(subset="Date")["Date"].tolist()
    cols = [4, 5, 6, 0, 1, 2, 3, 30]
    DFyakinhyou = pd.DataFrame(index=data_list, columns=cols)

    for i in range(len(dfnightshift)):
        day = dfnightshift.iat[i, 1]
        job = dfnightshift.iat[i, 2]
        name = dfnightshift.iat[i, 0]

        if math.isnan(DFyakinhyou.at[day, job]):
            DFyakinhyou.at[day, job] = name
        elif not math.isnan(DFyakinhyou.at[day, job]) and job == 3:
            DFyakinhyou.at[day, 30] = name
    DFyakinhyou.to_csv("C:/Users/pelu0/Desktop/ShiftManager/DFyakinhyou.csv")
    DFyakinhyou.columns = ["Angio夜勤", "MRI夜勤", "CT夜勤", "Angio日勤", "MRI日勤", "CT日勤", "Free日勤", "Free日勤"]
    sd,rk = config()
    dates = pd.date_range(sd, periods=ed + 1, freq='D').strftime('%m/%d')
    DFyakinhyou.index = dates

    #名前に変換
    number_of_stuff, staff_list, dfstaff = stuff()
    for j in range(number_of_stuff):
        DFyakinhyou = DFyakinhyou.replace(dfstaff.iat[j, 0], dfstaff.iat[j, 2])
    DFyakinhyou.to_csv("C:/Users/pelu0/Desktop/ShiftManager/DFyakinhyouname.csv", encoding='Shift_JIS')
    return ed, dfshift, DFyakinhyou, data_list

#リクエスト
def request():
    dfrequest=pd.read_table("C:/Users/pelu0/Desktop/ShiftManager/request.dat",sep=',', header=None)
    dfrequest.columns=["UID", "Date", "Job"]
    return dfrequest

#先月データ
def previous():
    #先月データ
    dfprevious=pd.read_table("C:/Users/pelu0/Desktop/ShiftManager/previous.dat",sep=',', header=None)
    dfprevious.columns=["UID", "Date", "Job"]
    dfprevious.to_csv("C:/Users/pelu0/Desktop/ShiftManager/dfprevious.csv")
    return dfprevious

#勤務表
def kinmuhyou():
    dfrequest = request()    #リクエスト
    ed, dfshift, DFyakinhyou, data_list = shift()    #夜勤
    dfprevious = previous() #先月データ
    sd,rk=config()

    #先月＋今月
    dfprevious_dfshift = pd.concat([dfprevious, dfshift])
    longday = dfprevious_dfshift.loc[:, ['Date']].drop_duplicates().dropna(subset=['Date'])
    longday = longday["Date"].to_list()

    # 基準日から日付計算
    for i in range(len(dfprevious_dfshift)):
        IntVar = dfprevious_dfshift.iat[i, 1]
        dfprevious_dfshift.iat[i, 1] = sd + datetime.timedelta(days=1) * IntVar
        dfprevious_dfshift.iat[i, 1] = dfprevious_dfshift.iat[i, 1].strftime('%m/%d')
    # 列名(日付)日付ダブり削除＋Nan削除
    list_cols = dfprevious_dfshift.loc[:, ['Date']].drop_duplicates().dropna(subset=['Date'])
    list_cols = list_cols["Date"].to_list()

    # DataFrame(先月+今月)
    number_of_stuff, staff_list, dfstaff = stuff()
    DFkinmuhyou_long = pd.DataFrame(index=staff_list, columns=list_cols)

    # 値代入
    for i in range(len(dfprevious_dfshift)):
        a = dfprevious_dfshift.iat[i, 0]
        b = dfprevious_dfshift.iat[i, 1]
        c = dfprevious_dfshift.iat[i, 2]
        DFkinmuhyou_long.at[a, b] = c

    list_row1 = dfstaff["Name"].to_list()
    list_row1.extend([900, 901, 902, 903, 904, 905, 906, 907, 908, 909])
    DFkinmuhyou_long.index = list_row1
    DFkinmuhyou_long.to_csv("C:/Users/pelu0/Desktop/ShiftManager/DFkinmuhyou_long.csv")
    DFkinmuhyou_long = DFkinmuhyou_long.replace({0: "A日", 1: "M日", 2: "C日", 3: "F日", 4: "A夜", 5: "M夜", 6: "C夜", 7: "明", 8: "日勤", 9: "他勤"})
    DFkinmuhyou_long = DFkinmuhyou_long.replace({10: "休日", 11: "休暇", 12: "ダ"})

    #今月(夜勤のみ)+リクエスト
    #夜勤以外を空に
    for i in range(len(dfshift)):
        if dfshift.iat[i,2] > 7:
            dfshift.iat[i,2] = ""
    #DataFrame今月(夜勤のみ)+リクエスト
    dfkinmuhyou=pd.concat([dfprevious, dfshift, dfrequest])

    #基準日から日付計算
    for i in range(len(dfkinmuhyou)):
        IntVar = dfkinmuhyou.iat[i, 1]
        dfkinmuhyou.iat[i, 1] = sd + datetime.timedelta(days=1)*IntVar
        dfkinmuhyou.iat[i, 1] = dfkinmuhyou.iat[i, 1].strftime('%m/%d')
    #DataFrame
    number_of_stuff, staff_list, dfstaff = stuff()
    DFkinmuhyou = pd.DataFrame(index=staff_list, columns=list_cols)
    #値代入
    for i in range(len(dfkinmuhyou)):
        a = dfkinmuhyou.iat[i, 0]
        b = dfkinmuhyou.iat[i, 1]
        c = dfkinmuhyou.iat[i, 2]
        DFkinmuhyou.at[a, b] = c

    DFkinmuhyou.index=list_row1
    DFkinmuhyou.to_csv("C:/Users/pelu0/Desktop/ShiftManager/DFkinmuhyou.csv")

    DFkinmuhyou=DFkinmuhyou.replace({0: "A日", 1: "M日", 2: "C日", 3: "F日", 4: "A夜", 5: "M夜", 6: "C夜", 7: "明", 8: "日勤", 9: "他勤"})
    DFkinmuhyou=DFkinmuhyou.replace({10: "休日", 11: "休暇", 12: "ダ"} )

    DFkinmuhyou.to_csv("C:/Users/pelu0/Desktop/ShiftManager/DFkinmuhyouname.csv", encoding='Shift_JIS')
    return DFkinmuhyou, DFkinmuhyou_long, longday  #DFkinmuhyou:今月のリクエスト＋夜勤 DFkinmuhyou_long:先月からのシフト

#スキル
def Skill():
    dfskill = pd.read_table("C:/Users/pelu0/Desktop/ShiftManager/Skill.dat", sep=',', header=None)
    dfskill.columns = ["UID", "A夜", "M夜", "C夜", "F日", "夜勤", "日直"]
    dfskill = dfskill.sort_values("UID", ascending=True)
    ed, dfshift, DFyakinhyou, data_list = shift()
    DFkinmuhyou, DFkinmuhyou_long, longday = kinmuhyou()
    dfprevious = previous()

    #勤務日を1に置き換える
    dfjob1=pd.concat([dfprevious, dfshift])
    dfjob1 = dfjob1.replace({"Job":{0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}})
    dfjob1 = dfjob1.replace({"Job":{10: 0, 11: 0, 50: 0, 60: 0, 61: 0}})
    dfjob1.loc[dfjob1["Job"]>0, "Job"] = 1
    dfjob1.loc[dfjob1["Job"] == 0, "Job"] = ""

    DFrenzoku = pd.DataFrame(index=dfskill["UID"].to_list(),columns=longday)
    for i in range(len(dfjob1)):
        a = dfjob1.iat[i, 0]
        b = dfjob1.iat[i, 1]
        c = dfjob1.iat[i, 2]
        DFrenzoku.at[a, b] = c
    DFrenzoku.to_csv("C:/Users/pelu0/Desktop/ShiftManager/DFrenzoku.csv", encoding='Shift_JIS')

    #名前に変換
    number_of_stuff, staff_list, dfstaff = stuff()

    dfskillAY = (dfskill[dfskill["A夜"]>0])
    for j in range(number_of_stuff):
        dfskillAY=dfskillAY[["UID"]]
        dfskillAY = dfskillAY.replace({'UID': {dfstaff.iat[j, 0]: dfstaff.iat[j, 2]}})

    dfskillMY = (dfskill[dfskill["M夜"]>0])
    for j in range(number_of_stuff):
        dfskillMY = dfskillMY.replace({'UID': {dfstaff.iat[j, 0]: dfstaff.iat[j, 2]}})

    dfskillCY = (dfskill[dfskill["C夜"] > 0])
    for j in range(number_of_stuff):
        dfskillCY = dfskillCY.replace({'UID' : {dfstaff.iat[j, 0]: dfstaff.iat[j, 2]}})

    dfskillAN = (dfskill[dfskill["A夜"] > 0])
    for j in range(number_of_stuff):
        dfskillAN = dfskillAN.replace({'UID': {dfstaff.iat[j, 0]: dfstaff.iat[j, 2]}})

    dfskillFN = (dfskill[dfskill["F日"] > 0])
    for j in range(number_of_stuff):
        dfskillFN = dfskillFN.replace({'UID': {dfstaff.iat[j, 0]: dfstaff.iat[j, 2]}})

    return dfskillAY, dfskillMY, dfskillCY, dfskillFN, dfskill, dfjob1, DFrenzoku







