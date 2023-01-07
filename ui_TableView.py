import os
from datetime import datetime
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui_TableView import *
from ui_tableviewone import *
import readdata


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, hheader, vheader):
        super(TableModel, self).__init__()
        self._data = data
        self._hheader = hheader
        self._vheader = vheader

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._hheader[section]
            if orientation == Qt.Vertical:
                return self._vheader[section]

            return ''

    def flags(self, index):
        return super(TableModel, self).flags(index) | Qt.ItemIsEditable

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            return True
        return False


class Delegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None, setModelDataEvent=None):
        super(Delegate, self).__init__(parent)
        self.setModelDataEvent = setModelDataEvent

    def createEditor(self, parent, option, index):
        return QtWidgets.QLineEdit(parent)

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        editor.setText(str(value))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())
        if not self.setModelDataEvent is None:
            self.setModelDataEvent()

    # def paint(self, painter, option, index):
    #     data = index.model().data(index)


class ConfigVarTableView(QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        headers = ['作成月', '夜勤日勤回数上限', '連続勤務日数', '所定労働時間', '休日数', '2連休', '3連休', '4連休',
                   '休診日の休日数', '勤務間隔1日係数', '勤務間隔2日係数', '勤務間隔3日係数', '勤務間隔4日係数', '勤務回数係数']
        self.ui = Ui_TableViewDialog()
        self.ui.setupUi(self)
        self.setWindowTitle('ConfigVar')
        data = self.setConfigVar()
        self.model = TableModel(data, [''], headers)
        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setItemDelegate(Delegate())
        self.ui.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # ダブルクリックイベントの時にセルの編集モードにしない
        self.ui.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setDialogSize()
        self.connectMethod()

    def connectMethod(self):

        self.ui.tableView.doubleClicked.connect(self.getDoubleClicked)

    def getDoubleClicked(self, item):

        subWind = EditForm(item, self)
        subWind.show()

    def setParam(self, value, item):

        index = self.model.index(item.row(), item.column())
        self.model.setData(index, value)

    def setDialogSize(self):
        h = self.ui.tableView.horizontalHeader().height()
        w = self.ui.tableView.verticalHeader().width()
        for i in range(self.model.rowCount(0)):
            h += self.ui.tableView.rowHeight(i)
        for i in range(self.model.columnCount(0)):
            w += self.ui.tableView.columnWidth(i)
        self.resize(w, h)

    def setConfigVar(self):
        createDate, epsilon, iota, kappa, myu, nyu, rho, lam = readdata.read_config_var()

        data = [[0 for i in range(1)] for j in range(14)]
        data[0][0] = str(createDate.strftime('%Y/%m/%d'))
        data[1][0] = epsilon
        data[2][0] = iota
        data[3][0] = kappa
        data[4][0] = myu
        for i in range(len(nyu)):
            data[5 + i][0] = nyu[i]
        data[8][0] = rho
        for i in range(len(lam)):
            data[9 + i][0] = lam[i]

        return data


class EditForm(QDialog):
    def __init__(self, item: QModelIndex, parent=None):
        super(EditForm, self).__init__()
        self.w = QDialog()
        self.parent = parent
        self.item = item
        label = QLabel()
        label.setText('Input Value')
        self.edit = QLineEdit()
        self.edit.setText(str(item.data(0)))
        button = QPushButton('変更')
        button.clicked.connect(self.setParamOriginal)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.edit)
        layout.addWidget(button)

        self.w.setLayout(layout)

    def setParamOriginal(self):
        self.parent.setParam(self.edit.text(), self.item)
        self.w.close()

    def show(self):
        self.w.exec_()


class AlphaTableView(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()