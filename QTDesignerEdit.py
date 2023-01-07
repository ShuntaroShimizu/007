import glob
import sys
import os
import pandas as pd
import datetime
import math
import EditOpenFiles as OFS
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import *


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
        global TargetRow, TargetColumn
        sd, rk = OFS.config()
        datas = item.data()
        TargetRow = item.row() + int(rk)
        TargetColumn = item.column()
        if item.data().isalpha() is False:
            self.configdialog = candidate()
            self.configdialog.show()

    def fn_get_cell_Value(self, index):
        datas = index.data()
        print(datas)

# 勤務表
class shiftDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(shiftDialog, self).__init__(parent)
        self.initui()

    def initui(self):
        ui_path = "ui_files"
        self.ui = uic.loadUi(f"{ui_path}/dialog.ui", baseinstance=self)
        DFkinmuhyou, DFkinmuhyou_long, longday = OFS.kinmuhyou()
        data = DFkinmuhyou
        self.model = Model(data)
        self.ui.tableView.setModel(self.model)

# 編集用
class candidate(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(candidate, self).__init__(parent)
        self.initui()

    def initui(self):
        ui_path = "ui_files"
        self.ui = uic.loadUi(f"{ui_path}/dialog.ui", baseinstance=self)
        dfskillAY, dfskillMY, dfskillCY, dfskillFN, dfskill, dfjob1, DFrenzoku = OFS.Skill()
        DFkinmuhyou, DFkinmuhyou_long, longday = OFS.kinmuhyou()
        ed, dfshift, DFyakinhyou, data_list = OFS.shift()
        number_of_stuff, staff_list, dfstaff = OFS.stuff()

        DFkinmuhyou = DFkinmuhyou.iloc[:, [TargetRow, TargetRow+1]]
        DFkinmuhyou["UID"] = DFkinmuhyou.index.values

        #A夜勤の場合
        if TargetColumn == 0:
            dfskillAY = pd.merge(dfskillAY, DFkinmuhyou, on="UID", how='inner')

            for i in reversed(range(len(dfskillAY))):
                if len(dfskillAY.iat[i, 1]) >= 1 or len(dfskillAY.iat[i, 2]) >= 1:
                    dfskillAY.drop(i, inplace=True)

            for i in range(len(dfstaff)):
                dfskillAY = dfskillAY.replace({'UID': {dfstaff.iat[i, 2]: dfstaff.iat[i, 0]}})

            DFrenzoku["UID"] =DFrenzoku.index.values
            dfskillAY=dfskillAY["UID"]
            DFrenzoku = pd.merge(dfskillAY, DFrenzoku, on="UID", how='inner')
            print(DFrenzoku)
            DFrenzoku1 = DFrenzoku.T  # 転置

            print(DFrenzoku["UID"].to_list())
            DFrenzoku1.columns = DFrenzoku["UID"].to_list()
            DFrenzoku1 = DFrenzoku1.drop('UID')

            print(DFrenzoku1)
            DF = pd.DataFrame(index=DFrenzoku["UID"].to_list(), columns=['連続勤務日'])
            print(DF)
            for i in range(len(DFrenzoku["UID"])):  # 遅い
                y = DFrenzoku1.iloc[:, i]
                DFrenzoku1['new'] = y.groupby((y != y.shift()).cumsum()).cumcount() + 1
                print(DFrenzoku1['new'].max())
                DF.iat[i, 0] = DFrenzoku1['new'].max()
            print(DF)

            # 現状確認
            DFjob = pd.DataFrame(index=dfskill["UID"].to_list(), columns=['休日', '連続勤務回数', '夜勤回数', "日直回数"])
            DFjob["UID"] = dfskill["UID"].to_list()
            for i in range(len(dfskill)):
                # 休日計算(振＋休)
                DFjob.iat[i, 0] = (
                            (dfshift["Job"] == 10) & (dfshift['UID'] == dfskill.iat[i, 0]) | (dfshift["Job"] == 50) & (
                                dfshift['UID'] == dfskill.iat[i, 0])).sum().sum()
                # 連続勤務回数
                DFjob.iat[i, 1] = DF.iat[i, 0]
                # 夜勤回数(明で計算)
                DFjob.iat[i, 2] = ((dfshift["Job"] == 7) & (dfshift['UID'] == dfskill.iat[i, 0])).sum().sum()
                # 日直回数
                DFjob.iat[i, 3] = (
                            (dfshift["Job"] == 0) & (dfshift['UID'] == dfskill.iat[i, 0]) | (dfshift["Job"] == 1) & (
                                dfshift['UID'] == dfskill.iat[i, 0]) | (dfshift["Job"] == 2) & (
                                        dfshift['UID'] == dfskill.iat[i, 0]) | (dfshift["Job"] == 3) & (
                                        dfshift['UID'] == dfskill.iat[i, 0])).sum().sum()

            #data = dfskillAY[['UID', '休日', '連続勤務回数', '夜勤回数', "日直回数"]]
            print(DFjob)
            data = dfskillAY

        elif TargetColumn == 1:
            data = dfskillMY
        elif TargetColumn == 2:
            data = dfskillCY
        elif TargetColumn == 3:
            data = dfskillFN

        self.model = Model(data)
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.doubleClicked.connect(self.clickevent)
        # self.ui.tableView.selectionChanged.connect(self.clickevent)

    def clickevent(self, data):
        print(data)
        print("AAA")


"""
if __name__ =='__main__':
    app = QtWidgets.QApplication(sys.argv)
    dlg = nightshiftDialog()
    dlg.showMaximized()
    sys.exit(app.exec_())
"""

