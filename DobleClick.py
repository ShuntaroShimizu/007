import pandas as pd
import OpenFiles as OFS

dfskill, dfjob1, DFrenzoku = OFS.Skill()
DFkinmuhyou, DFkinmuhyou_long, longday = OFS.kinmuhyou()
ed, dfshift, DFyakinhyou, data_list = OFS.shift()
number_of_stuff, staff_list, dfstaff = OFS.stuff()

TargetRow = 19
TargetColumn = 0

TargetDay = TargetRow + 1
DFkinmuhyou = DFkinmuhyou.iloc[:, [TargetRow, TargetDay]]
DFkinmuhyou["UID"] = DFkinmuhyou.index.values

#日当直に入れるかの予定確認(UID出力)
for i in reversed(range(len(DFkinmuhyou))):
    if DFkinmuhyou.iat[i, 0] != "" or DFkinmuhyou.iat[i, 1] != "":
        DFkinmuhyou.drop(DFkinmuhyou.index[[i]],inplace=True)

for j in range(len(dfskill)):
    dfskill= dfskill.replace({'UID': {dfstaff.iat[j, 0]: dfstaff.iat[j, 2]}})

DFkakunin = pd.merge(dfskill, DFkinmuhyou, on="UID", how='inner')

if TargetColumn == 0:
    DFkakunin = DFkakunin[(DFkakunin["A夜"] > 0) & (DFkakunin["夜勤"] > 0)]
elif TargetColumn == 1:
    DFkakunin = DFkakunin[(DFkakunin["M夜"] > 0) & (DFkakunin["夜勤"] > 0)]
elif TargetColumn == 2:
    DFkakunin = DFkakunin[(DFkakunin["C夜"] > 0) & (DFkakunin["夜勤"] > 0)]
elif TargetColumn == 3:
    DFkakunin = DFkakunin[(DFkakunin["A夜"] > 0) & (DFkakunin["日直"] > 0)]
elif TargetColumn == 4:
    DFkakunin = DFkakunin[(DFkakunin["M夜"] > 0) & (DFkakunin["日直"] > 0)]
elif TargetColumn == 5:
    DFkakunin = DFkakunin[(DFkakunin["C夜"] > 0) & (DFkakunin["日直"] > 0)]
elif TargetColumn == 6:
    DFkakunin = DFkakunin[(DFkakunin["日直"] > 0)]

DFkakuninUID = DFkakunin["UID"]

for i in range(len(dfstaff)):
    DFkakuninUID = DFkakuninUID.replace(dfstaff.iat[i, 2], dfstaff.iat[i, 0])

DFkakuninUID.index = DFkakuninUID

DFr = pd.merge(DFrenzoku, DFkakuninUID, how='inner', left_index=True, right_index=True)
DFrenzokuRAW = DFr.drop('UID', axis=1)
DFrenzoku = DFrenzokuRAW

#TargetColumnに勤務入力
DFrenzoku[TargetRow] = 1
DFrenzoku[20] = 1


# 連続勤務
DFrenzoku1 = DFrenzoku.T  # 転置
DF = pd.DataFrame(index=DFkakuninUID.to_list(), columns=['連続勤務日'])
for item in DFrenzoku1.columns:  # 遅い
    y = DFrenzoku1.loc[:, item]
    DFrenzoku1['new'] = y.groupby((y != y.shift()).cumsum()).cumcount() + 1
    DF.loc[item, ['連続勤務日']] = DFrenzoku1['new'].max()


# 現状確認
DFjob = pd.DataFrame(index=DFkakuninUID.to_list(), columns=['休日', '連続勤務回数', '夜勤回数', "日直回数"])
DFjob["UID"] = DFkakuninUID.to_list()
DFrenzoku1 = DFrenzoku1.drop('new',axis=1)
dfshiftRAW = dfshift

#0勤務7明
for item in DFrenzoku1.columns:
    IV = dfshift[(dfshift['UID'] == item) & (dfshift['Date'] == TargetRow)]['UID'].index.values
    if TargetColumn == 0:
        dfshift.at[IV[0], 'Job'] = 4
    IV = dfshift[(dfshift['UID'] == item) & (dfshift['Date'] == 20)]['UID'].index.values
    dfshift.at[IV[0], 'Job'] = 7

for item in DFrenzoku1.columns:
    # 休日計算(振＋休)
    DFjob.at[item, '休日'] = ((dfshift["Job"] == 10) & (dfshift["UID"] == item) | (dfshift["Job"] == 50) & (dfshift["UID"] == item) ).sum().sum()
    #連続回数
    DFjob.at[item, '連続勤務回数'] = DF.at[item, '連続勤務日']
    # 夜勤回数(明で計算)
    DFjob.at[item, '夜勤回数'] = ((dfshift["Job"] == 7) & (dfshift["UID"] == item)).sum().sum()
    # 日直回数
    DFjob.at[item, '日直回数'] = ((dfshift["Job"] == 0) & (dfshift["UID"] == item) | (dfshift["Job"] == 1) & (dfshift["UID"] == item) | (dfshift["Job"] == 2) & (dfshift["UID"] == item) | (dfshift["Job"] == 3) & (dfshift["UID"] == item)).sum().sum()
print(DFjob)


