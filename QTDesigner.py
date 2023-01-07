import glob
import sys
import os
import pandas as pd
import datetime
import math
import OpenFiles as OFS
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from tkinter import messagebox


class Model(QtCore.QAbstractTableModel):
    def __init__(self, dataframe: pd.DataFrame):
        super(Model, self).__init__()
        self._dataframe = dataframe

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return str(self._dataframe.iloc[index.row(), index.column()])
        # 色付けのコード追記

    def rowCount(self, index):
        return len(self._dataframe)

    def columnCount(self, index):
        return len(self._dataframe.columns)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: QtCore.Qt.ItemDataRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return str(self._dataframe.columns[section])

            if orientation == QtCore.Qt.Vertical:
                return str(self._dataframe.index[section])
        return None


# 夜勤表
class nightshiftDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(nightshiftDialog, self).__init__(parent)
        self.initui()

    def initui(self):
        ui_path = "ui_files"
        self.ui = uic.loadUi(f"{ui_path}/dialog.ui", baseinstance=self)
        ed, dfshift, DFyakinhyou, data_list = OFS.shift()
        data = DFyakinhyou
        self.model = Model(data)
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.doubleClicked.connect(self.dclickevent)

    def dclickevent(self, item):
        global TargetRow, TargetColumn, TargetData
        sd, rk , kn = OFS.config()
        TargetData = item.data()
        TargetRow = item.row() + int(rk)
        TargetColumn = item.column()
        if item.data().isalpha() is False:
            self.configdialog = candidate()
            self.configdialog.show()

    def fn_get_cell_Value(self, index):
        datas = index.data()

# 勤務表
class shiftDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(shiftDialog, self).__init__(parent)
        self.initui()

    def initui(self):
        ui_path = "ui_files"
        self.ui = uic.loadUi(f"{ui_path}/dialog.ui", baseinstance=self)

        DFkinmuhyou, DFkinmuhyou_long, longday = OFS.kinmuhyou()
        DFNrdeptcore, RawDFNrdeptcore = OFS.Nrdeptcore()
        data = DFkinmuhyou_long
        self.model = Model(data)
        self.ui.tableView.setModel(self.model)


# ダブルクリックイベント-編集用
class candidate(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(candidate, self).__init__(parent)
        self.initui()

    def initui(self):
        ui_path = "ui_files"
        self.ui = uic.loadUi(f"{ui_path}/dialog.ui", baseinstance=self)
        #必要データ読み込み
        sd, rk , kn = OFS.config()
        dfskill, dfjob1, DFrenzoku = OFS.Skill()
        DFkinmuhyou, DFkinmuhyou_long, longday = OFS.kinmuhyou()
        ed, dfshift, DFyakinhyou, data_list = OFS.shift()
        number_of_stuff, staff_list, dfstaff = OFS.stuff()
        DFNrdeptcore,RawDFNrdeptcore = OFS.Nrdeptcore()
        #ダブルクリックしたセルからターゲットの日付(0-30)
        TargetDayS = TargetRow - int(rk)
        print(TargetDayS)
        TargetDayE = TargetDayS + 1
        DFkinmuhyou = DFkinmuhyou.iloc[:, [TargetRow, TargetRow+1]]
        DFkinmuhyou["UID"] = DFkinmuhyou.index.values
        print(DFkinmuhyou)
        DFkinmuhyou.to_csv("C:/Users/pelu0/Desktop/20221220/sample1/DFrenzoku21.csv", encoding='Shift_JIS')

        #Coreメンバーの数計算
        # IDから名前へ
        for j in range(len(RawDFNrdeptcore)):
            RawDFNrdeptcore = RawDFNrdeptcore.replace({'UID': {dfstaff.iat[j, 0]: dfstaff.iat[j, 2]}})

        DFRTCore = RawDFNrdeptcore.query('RT== 6 ')
        DFMRCore = RawDFNrdeptcore.query('MR== 6 ')
        DFTVCore = RawDFNrdeptcore.query('TV== 6 ')
        DFKSCore = RawDFNrdeptcore.query('KS== 6 ')
        DFNMCore = RawDFNrdeptcore.query('NM== 6 ')
        DFXPCore = RawDFNrdeptcore.query('XP== 6 ')
        DFCTCore = RawDFNrdeptcore.query('CT== 6 ')
        DFXOCore = RawDFNrdeptcore.query('XO== 6 ')
        DFAGCore = RawDFNrdeptcore.query('AG== 6 ')
        DFMGCore = RawDFNrdeptcore.query('MG== 6 ')
        DFMTCore = RawDFNrdeptcore.query('MT== 6 ')

        DFkinmuhyou_longS = DFkinmuhyou_long.iloc[:, [TargetRow]]
        DFkinmuhyou_longE = DFkinmuhyou_long.iloc[:, [TargetRow+1]]

        #本当は勤務
        for i in reversed(range(len(DFkinmuhyou_longS))):
            if DFkinmuhyou_longS.iat[i, 0] != "休":
                DFkinmuhyou_longS.drop(DFkinmuhyou_longS.index[[i]], inplace=True)

        for i in reversed(range(len(DFkinmuhyou_longE))):
            if DFkinmuhyou_longE.iat[i, 0] != "休":
                DFkinmuhyou_longE.drop(DFkinmuhyou_longE.index[[i]], inplace=True)

        DFkinmuhyou_longS["UID"] = DFkinmuhyou_longS.index.values
        DFkinmuhyou_longE["UID"] = DFkinmuhyou_longE.index.values

        CoreRT=pd.merge(DFRTCore, DFkinmuhyou_longS, on="UID", how='inner')
        CoreRTNo=CoreRT.shape[0]
        CoreMR=pd.merge(DFMRCore, DFkinmuhyou_longS, on="UID", how='inner')
        CoreMRNo=CoreMR.shape[0]
        CoreTV=pd.merge(DFTVCore, DFkinmuhyou_longS, on="UID", how='inner')
        CoreTVNo=CoreTV.shape[0]
        CoreKS=pd.merge(DFKSCore, DFkinmuhyou_longS, on="UID", how='inner')
        CoreKSNo=CoreKS.shape[0]
        CoreNM=pd.merge(DFNMCore, DFkinmuhyou_longS, on="UID", how='inner')
        CoreNMNo=CoreNM.shape[0]
        CoreXP=pd.merge(DFXPCore, DFkinmuhyou_longS, on="UID", how='inner')
        CoreXPNo=CoreXP.shape[0]
        CoreCT=pd.merge(DFCTCore, DFkinmuhyou_longS, on="UID", how='inner')
        CoreCTNo=CoreCT.shape[0]
        CoreXO=pd.merge(DFXOCore, DFkinmuhyou_longS, on="UID", how='inner')
        CoreXONo=CoreXO.shape[0]
        CoreAG=pd.merge(DFAGCore, DFkinmuhyou_longS, on="UID", how='inner')
        CoreAGNo=CoreAG.shape[0]
        CoreMG=pd.merge(DFMGCore, DFkinmuhyou_longS, on="UID", how='inner')
        CoreMGNo=CoreMG.shape[0]
        CoreMT=pd.merge(DFMTCore, DFkinmuhyou_longS, on="UID", how='inner')
        CoreMTNo=CoreMT.shape[0]


        DFCoreNoS = pd.DataFrame({DFkinmuhyou_longS.columns[0] + " Core" :[CoreRTNo,CoreMRNo,CoreTVNo,CoreKSNo,CoreNMNo,CoreXPNo,CoreCTNo,CoreXONo,CoreAGNo,CoreMGNo,CoreMTNo]},
                                index=['RT','MR','TV','KS','NM','XP','CT','XO','AG','MG','MT'])
        DFCoreNoS["Mo"] = DFCoreNoS.index.values
        print(DFCoreNoS)

        CoreRT=pd.merge(DFRTCore, DFkinmuhyou_longE, on="UID", how='inner')
        CoreRTNo=CoreRT.shape[0]
        CoreMR=pd.merge(DFMRCore, DFkinmuhyou_longE, on="UID", how='inner')
        CoreMRNo=CoreMR.shape[0]
        CoreTV=pd.merge(DFTVCore, DFkinmuhyou_longE, on="UID", how='inner')
        CoreTVNo=CoreTV.shape[0]
        CoreKS=pd.merge(DFKSCore, DFkinmuhyou_longE, on="UID", how='inner')
        CoreKSNo=CoreKS.shape[0]
        CoreNM=pd.merge(DFNMCore, DFkinmuhyou_longE, on="UID", how='inner')
        CoreNMNo=CoreNM.shape[0]
        CoreXP=pd.merge(DFXPCore, DFkinmuhyou_longE, on="UID", how='inner')
        CoreXPNo=CoreXP.shape[0]
        CoreCT=pd.merge(DFCTCore, DFkinmuhyou_longE, on="UID", how='inner')
        CoreCTNo=CoreCT.shape[0]
        CoreXO=pd.merge(DFXOCore, DFkinmuhyou_longE, on="UID", how='inner')
        CoreXONo=CoreXO.shape[0]
        CoreAG=pd.merge(DFAGCore, DFkinmuhyou_longE, on="UID", how='inner')
        CoreAGNo=CoreAG.shape[0]
        CoreMG=pd.merge(DFMGCore, DFkinmuhyou_longE, on="UID", how='inner')
        CoreMGNo=CoreMG.shape[0]
        CoreMT=pd.merge(DFMTCore, DFkinmuhyou_longE, on="UID", how='inner')
        CoreMTNo=CoreMT.shape[0]

        DFCoreNoE = pd.DataFrame({DFkinmuhyou_longE.columns[0] + " Core" :[CoreRTNo,CoreMRNo,CoreTVNo,CoreKSNo,CoreNMNo,CoreXPNo,CoreCTNo,CoreXONo,CoreAGNo,CoreMGNo,CoreMTNo]},
                                index=['RT','MR','TV','KS','NM','XP','CT','XO','AG','MG','MT'])
        DFCoreNoE["Mo"] = DFCoreNoE.index.values
        print(DFCoreNoE)

        # 日当直に入れるかの予定確認(UID出力)
        print(TargetColumn)
        if TargetColumn == 0 or 1 or 2 :
            for i in reversed(range(len(DFkinmuhyou))):
                if DFkinmuhyou.iat[i, 0] != "" or DFkinmuhyou.iat[i, 1] != "":
                    DFkinmuhyou.drop(DFkinmuhyou.index[[i]], inplace=True)
            print(dfskill)
        else:
            for i in reversed(range(len(DFkinmuhyou))):
                if DFkinmuhyou.iat[i, 0] != "":
                    DFkinmuhyou.drop(DFkinmuhyou.index[[i]], inplace=True)

        for j in range(len(dfskill)):
            dfskill = dfskill.replace({'UID': {dfstaff.iat[j, 0]: dfstaff.iat[j, 2]}})
        print(dfskill)
        print(DFkinmuhyou)

        DFkakunin = pd.merge(dfskill, DFkinmuhyou, on="UID", how='inner')
        print(DFkakunin)
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
        print(len(DFkakuninUID.index))

        if len(DFkakuninUID.index) >> 0:
            for i in range(len(dfstaff)):
                DFkakuninUID = DFkakuninUID.replace(dfstaff.iat[i, 2], dfstaff.iat[i, 0])

            DFkakuninUID.index = DFkakuninUID

            DFr = pd.merge(DFrenzoku, DFkakuninUID, how='inner', left_index=True, right_index=True)
            DFrenzokuRAW = DFr.drop('UID', axis=1)
            DFrenzoku = DFrenzokuRAW
            DFrenzoku.to_csv("C:/Users/pelu0/Desktop/20221220/sample1/DFrenzoku2.csv", encoding='Shift_JIS')
            # TargetColumnに勤務入力
            DFrenzoku[TargetDayS] = 1
            DFrenzoku[TargetDayE] = 1
            DFrenzoku.to_csv("C:/Users/pelu0/Desktop/20221220/sample1/DFrenzoku1.csv", encoding='Shift_JIS')
            # 連続勤務
            print('start')
            DFrenzoku1 = DFrenzoku.T  # 転置
            DF = pd.DataFrame(index=DFkakuninUID.to_list(), columns=['連続勤務日'])
            for item in DFrenzoku1.columns:  # 遅い
                y = DFrenzoku1.loc[:, item]
                DFrenzoku1['new'] = y.groupby((y != y.shift()).cumsum()).cumcount() + 1
                DF.loc[item, ['連続勤務日']] = DFrenzoku1['new'].max()
            print('end')

            # 現状確認
            DFjob = pd.DataFrame(index=DFkakuninUID.to_list(), columns=['休日', '連続勤務回数', '夜勤回数', "日直回数"])
            DFjob["UID"] = DFkakuninUID.to_list()
            DFrenzoku1 = DFrenzoku1.drop('new', axis=1)
            dfshiftRAW = dfshift

            # 0勤務7明
            for item in DFrenzoku1.columns:
                IV = dfshift[(dfshift['UID'] == item) & (dfshift['Date'] == TargetDayS)]['UID'].index.values
                if TargetColumn == 0:
                    dfshift.at[IV[0], 'Job'] = 4
                IV = dfshift[(dfshift['UID'] == item) & (dfshift['Date'] == TargetDayE)]['UID'].index.values
                dfshift.at[IV[0], 'Job'] = 7

            print(dfshift)

            for item in DFrenzoku1.columns:
                # 休日計算(振＋休)
                DFjob.at[item, '休日'] = ((dfshift["Job"] == 10) & (dfshift["UID"] == item) | (dfshift["Job"] == 50) & (
                            dfshift["UID"] == item)).sum().sum()
                # 連続回数
                DFjob.at[item, '連続勤務回数'] = DF.at[item, '連続勤務日']
                # 夜勤回数(明で計算)
                DFjob.at[item, '夜勤回数'] = ((dfshift["Job"] == 4) & (dfshift["UID"] == item) | (dfshift["Job"] == 5) & (dfshift["UID"] == item) | (dfshift["Job"] == 6) & (dfshift["UID"] == item)).sum().sum()
                # 日直回数
                DFjob.at[item, '日直回数'] = ((dfshift["Job"] == 0) & (dfshift["UID"] == item) | (dfshift["Job"] == 1) & (
                            dfshift["UID"] == item) | (dfshift["Job"] == 2) & (dfshift["UID"] == item) | (
                                                      dfshift["Job"] == 3) & (dfshift["UID"] == item)).sum().sum()
            DFjob = DFjob.reindex(columns=['UID','休日','連続勤務回数','夜勤回数','日直回数'])
            DFjob=pd.merge(DFjob, DFNrdeptcore, on="UID", how='inner')
            for j in range(len(dfskill)):
                DFjob = DFjob.replace({'UID': {dfstaff.iat[j, 0]: dfstaff.iat[j, 2]}})

            DFjob= pd.merge(DFjob, DFCoreNoS,on="Mo", how='inner')
            DFjob= pd.merge(DFjob, DFCoreNoE,on="Mo", how='inner')
            DFjob = DFjob.reindex(columns=['UID','Mo', DFkinmuhyou_longS.columns[0] + " Core",DFkinmuhyou_longE.columns[0] + " Core",'休日','連続勤務回数','夜勤回数','日直回数'])
            data = DFjob
            DFjob.to_csv("C:/Users/pelu0/Desktop/20221220/sample1DFjob.csv", encoding='Shift_JIS')

            self.model = Model(data)
            self.ui.tableView.setModel(self.model)
            self.ui.tableView.doubleClicked.connect(self.clickevent)

        else:
            messagebox.showinfo('注意!!!','候補者がいません.')





    def clickevent(self, item):
        ed, dfshift, DFyakinhyou, data_list = OFS.shift()
        number_of_stuff, staff_list, dfstaff = OFS.stuff()
        sd, rk, kn = OFS.config()
        DFjob = pd.read_csv("C:/Users/pelu0/Desktop/20221220/sample1DFjob.csv", encoding='Shift_JIS')

        messagebox.showwarning(title="Warning", message="一度変更すると戻せません.")
        TargetR = item.row()
        TargetC = item.column()
        TargetD = item.data()

        b=DFjob.iloc[TargetR, 2]
        #名前変換(名前→ID)
        DFTargetDID = dfstaff[dfstaff['Name'] == TargetD]
        TargetDID = DFTargetDID.iloc[0,0]
        TargetDayS = TargetRow - int(rk)
        TargetDayE = TargetDayS + 1

        if TargetColumn == 0:
            dfshift.to_csv("C:/Users/pelu0/Desktop/20221220/sample1Predfshift.csv", encoding='Shift_JIS')
            ret = messagebox.askokcancel('最終確認!!!',TargetD + 'さんのA夜勤を'+'入れますか？')
            if ret == True:
                IV = dfshift[(dfshift['UID'] == TargetDID) & (dfshift['Date'] == TargetDayS)]['UID'].index.values
                dfshift.at[IV[0], 'Job'] = 4
                IV = dfshift[(dfshift['UID'] == TargetDID) & (dfshift['Date'] == TargetDayE)]['UID'].index.values
                dfshift.at[IV[0], 'Job'] = 7
                c=int(kn)
                b=int(b)
                a = c - b
                a = str(a)
                messagebox.showinfo('決定', TargetD +'さんの振替休日'+ a +'日を設定してください.')


"""
if __name__ =='__main__':
    app = QtWidgets.QApplication(sys.argv)
    dlg = nightshiftDialog()
    dlg.showMaximized()
    sys.exit(app.exec_())
"""

