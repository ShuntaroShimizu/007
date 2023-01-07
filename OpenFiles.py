import datetime
import pandas as pd
import math

def config():#勤務表作成における必要変数を格納
    #ShiftManager ⇒　20221220/sample1
    fti = pd.read_table("C:/Users/pelu0/Desktop/20221220/sample1/configvar.dat")
    #基準日
    sd = fti.columns.values
    sd = sd[0]
    sd = sd[-10:]
    sd = datetime.datetime.strptime(sd,'%Y/%m/%d')
    rk = fti.iloc[1, :].values
    rk = rk[0]
    rk = rk[-2:]
    kn = fti.iloc[2, :].values
    kn = kn[0]
    kn = kn[4:]
    return sd, rk , kn#基準日(yyyy/mm/dd),連続勤務

def beta(): #各モダリティにおける最低限必要な正規スタッフ人数を格納、各行がそれぞれのモダリティ，2列目移行に1日から月末までの最低限必要な正規スタッフ人数を記載
    DFbeta = pd.read_table("C:/Users/pelu0/Desktop/20221220/sample1/beta.dat", sep=',',header=None)
    return DFbeta

def gamma() :#各モダリティにおける責任者クラスの必要人数を格納各行がそれぞれのモダリティ，2列目移行に1日から月末までの最低限必要な責任者クラスの人数を記載
    DFgamma = pd.read_table("C:/Users/pelu0/Desktop/20221220/sample1/gamma.dat", sep=',',header=None)
    return DFgamma

def Nrdeptcore():#スケジュールの対象となるスタッフUIDとその所属モダリティ，各モダリティスキルを格納。
    #0=X,1=△,2=〇,3=▲,4=●,5=★,6=◎
    DFNrdeptcore = pd.read_table("C:/Users/pelu0/Desktop/20221220/sample1/Nrdeptcore.dat", sep=',', header=None)
    DFNrdeptcore.columns = ["UID", "Mo", "RT", "MR", "TV", "KS", "NM", "XP", "CT", "XO", "AG", "MG", "MT"]
    DFNrdeptcore.to_csv("C:/Users/pelu0/Desktop/20221220/sample1/DFNrdeptcore.csv")
    RawDFNrdeptcore = DFNrdeptcore
    DFNrdeptcore = DFNrdeptcore[["UID","Mo"]]
    return DFNrdeptcore,RawDFNrdeptcore

def stuff():
    #スタッフ
    dfstaff = pd.read_table("C:/Users/pelu0/Desktop/20221220/sample1/staffinfo.dat", sep=',', header=None)
    dfstaff.columns = ["No", "ID", "Name"]
    #人数数え
    number_of_stuff = len(dfstaff)
    staff_list = dfstaff["No"].to_list()
    return number_of_stuff, staff_list, dfstaff

def converttable ():
    dfconverttable = pd.read_table("C:/Users/pelu0/Desktop/20221220/sample1/converttable.dat", sep=',', header=None)
    dfconverttable.columns = ["Job", "No"]
    return dfconverttable

def shift():
    #シフト
    input_data = open("C:/Users/pelu0/Desktop/20221220/sample1/shift.dat", 'r')
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
    DFyakinhyou.to_csv("C:/Users/pelu0/Desktop/20221220/sample1/DFyakinhyou.csv")
    DFyakinhyou.columns = ["Angio夜勤", "MRI夜勤", "CT夜勤", "Angio日勤", "MRI日勤", "CT日勤", "Free日勤", "Free日勤"]
    sd, rk , kn= config()
    dates = pd.date_range(sd, periods=ed + 1, freq='D').strftime('%m/%d')
    DFyakinhyou.index = dates

    #名前に変換
    number_of_stuff, staff_list, dfstaff = stuff()
    for j in range(number_of_stuff):
        DFyakinhyou = DFyakinhyou.replace(dfstaff.iat[j, 0], dfstaff.iat[j, 2])
    DFyakinhyou.to_csv("C:/Users/pelu0/Desktop/20221220/sample1/DFyakinhyouname.csv", encoding='Shift_JIS')
    return ed, dfshift, DFyakinhyou, data_list

#リクエスト
def request():
    dfrequest = pd.read_table("C:/Users/pelu0/Desktop/20221220/sample1/request.dat", sep=',', header=None)
    dfrequest.columns = ["UID", "Date", "Job"]
    return dfrequest

#先月データ
def previous():
    #先月データ
    dfprevious = pd.read_table("C:/Users/pelu0/Desktop/20221220/sample1/previous.dat", sep=',', header=None)
    dfprevious.columns = ["UID", "Date", "Job"]
    dfprevious.to_csv("C:/Users/pelu0/Desktop/20221220/sample1/dfprevious.csv")
    return dfprevious

def kinmuhyou():
    dfrequest = request()    #リクエスト
    ed, dfshift, DFyakinhyou, data_list = shift()    #夜勤
    dfprevious = previous() #先月データ
    sd, rk, kn = config()
    dfconverttable = converttable()

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
    DFkinmuhyou_long = pd.DataFrame(index = staff_list, columns = list_cols)

    for i in range(len(dfconverttable)):
        dfprevious_dfshift = dfprevious_dfshift.replace({'Job': {dfconverttable.iat[i, 1]: dfconverttable.iat[i, 0]}})

    # 値代入
    for i in range(len(dfprevious_dfshift)):
        a = dfprevious_dfshift.iat[i, 0]
        b = dfprevious_dfshift.iat[i, 1]
        c = dfprevious_dfshift.iat[i, 2]
        DFkinmuhyou_long.at[a, b] = c

    list_row1 = dfstaff["Name"].to_list()
    list_row1.extend([900, 901, 902, 903, 904, 905, 906, 907, 908, 909])
    DFkinmuhyou_long.index = list_row1
    DFkinmuhyou_long.to_csv("C:/Users/pelu0/Desktop/20221220/sample1/DFkinmuhyou_long.csv", encoding='Shift_JIS')

    #DFkinmuhyou_long = DFkinmuhyou_long.replace({0: "A日", 1: "M日", 2: "C日", 3: "F日", 4: "A夜", 5: "M夜", 6: "C夜", 7: "明", 8: "日勤", 9: "他勤"})
    #DFkinmuhyou_long = DFkinmuhyou_long.replace({10: "休日", 11: "休暇", 12: "ダ"})

    #今月(夜勤のみ)+リクエスト
    #夜勤以外を空に
    for i in range(len(dfshift)):
        if dfshift.iat[i, 2] > 7:
            dfshift.iat[i, 2] = ""
    #DataFrame今月(夜勤のみ)+リクエスト
    dfkinmuhyou = pd.concat([dfprevious, dfshift, dfrequest])

    #基準日から日付計算
    for i in range(len(dfkinmuhyou)):
        IntVar = dfkinmuhyou.iat[i, 1]
        dfkinmuhyou.iat[i, 1] = sd + datetime.timedelta(days=1)*IntVar
        dfkinmuhyou.iat[i, 1] = dfkinmuhyou.iat[i, 1].strftime('%m/%d')
    #DataFrame
    number_of_stuff, staff_list, dfstaff = stuff()
    DFkinmuhyou = pd.DataFrame(index=staff_list, columns=list_cols)

    for i in range(len(dfconverttable)):
        dfkinmuhyou= dfkinmuhyou.replace({'Job': {dfconverttable.iat[i, 1]: dfconverttable.iat[i, 0]}})

    #値代入
    for i in range(len(dfkinmuhyou)):
        a = dfkinmuhyou.iat[i, 0]
        b = dfkinmuhyou.iat[i, 1]
        c = dfkinmuhyou.iat[i, 2]
        DFkinmuhyou.at[a, b] = c

    DFkinmuhyou.index = list_row1
    DFkinmuhyou.to_csv("C:/Users/pelu0/Desktop/20221220/sample1/DFkinmuhyou.csv", encoding='Shift_JIS')

    #DFkinmuhyou = DFkinmuhyou.replace({0: "A日", 1: "M日", 2: "C日", 3: "F日", 4: "A夜", 5: "M夜", 6: "C夜", 7: "明", 8: "日勤", 9: "他勤"})
    #DFkinmuhyou = DFkinmuhyou.replace({10: "休日", 11: "休暇", 12: "ダ"} )

    DFkinmuhyou.to_csv("C:/Users/pelu0/Desktop/20221220/sample1/DFkinmuhyouname.csv", encoding='Shift_JIS')
    return DFkinmuhyou, DFkinmuhyou_long, longday  #DFkinmuhyou:今月のリクエスト＋夜勤 DFkinmuhyou_long:先月からのシフト連続勤務計算

def Skill():
    dfskill = pd.read_table("C:/Users/pelu0/Desktop/20221220/sample1/Skill.dat", sep=',', header=None)
    dfskill.columns = ["UID", "A夜", "M夜", "C夜", "F日", "夜勤", "日直"]
    dfskill = dfskill.sort_values("UID", ascending=True)
    ed, dfshift, DFyakinhyou, data_list = shift()
    DFkinmuhyou, DFkinmuhyou_long, longday = kinmuhyou()
    dfprevious = previous()
    number_of_stuff, staff_list, dfstaff = stuff()

    #勤務日を1に置き換える
    dfjob1 = pd.concat([dfprevious, dfshift])

    dfjob1 = dfjob1.replace({"Job" : {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}})
    dfjob1 = dfjob1.replace({"Job" : {10: 0, 11: 0, 12: 0,  50: 0, 60: 0, 61: 0, 63: 0}})
    dfjob1.loc[dfjob1["Job"] > 0, "Job"] = 1
    dfjob1.loc[dfjob1["Job"] == 0, "Job"] = ""

    DFrenzoku = pd.DataFrame(index=staff_list, columns=longday)
    for i in range(len(dfjob1)):
        a = dfjob1.iat[i, 0]
        b = dfjob1.iat[i, 1]
        c = dfjob1.iat[i, 2]
        DFrenzoku.at[a, b] = c
    DFrenzoku.to_csv("C:/Users/pelu0/Desktop/20221220/sample1/DFrenzoku.csv", encoding='Shift_JIS')
    return dfskill, dfjob1, DFrenzoku
