from PyQt5.QtWidgets import *
import sys
import tableview as tv
import QTDesigner as QTD
from tkinter import messagebox
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title of main window
        self.setWindowTitle('Tokai-Rad Schedule')

        # set the size of window

        # self.Width = w
        # self.height = h
        # self.resize(self.Width, self.height)
		
		# add all widgets
        self.btn_1 = QPushButton('1', self)
        self.btn_2 = QPushButton('2', self)
        self.btn_3 = QPushButton('3', self)
        self.btn_4 = QPushButton('4', self)
        self.button_style = self.pushButtonWidgetStyle(height = '60px',
                                                       width = '90px',
                                                       color = 'black',
                                                       font = '30px',
                                                       borderStyle = 'solid',
                                                       borderWidth = '2px', 
                                                       borderColor = 'gray',
                                                       borderRadius = '15px',
                                                       backgroundColor = 'white',
                                                       hoverBorderStyle = 'solid',
                                                       hoverBorderWidth = '2px',
                                                       hoverBorderColor = '#1E90FF',
                                                       hoverBorderRadius = '15px',
                                                       hoverBackgroundColor = '#98fb98',
                                                       pressedBackgroundColor = None
                                                       )
        self.btn_1.setStyleSheet(self.button_style)
        self.btn_2.setStyleSheet(self.button_style)
        self.btn_3.setStyleSheet(self.button_style)
        self.btn_4.setStyleSheet(self.button_style)

        self.btn_1.clicked.connect(self.showConfigDialog)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)

        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()
        self.tab1 = QTD.nightshiftDialog()
        self.tab1.show()
        self.tab2 = QTD.shiftDialog()
        self.tab2.show()
        self.initUI()

        #タブクリックしたら
        #self.tabWidget.tabBarClicked(1).connect()

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '夜勤表')
        self.right_widget.addTab(self.tab2, '勤務表')
        self.right_widget.addTab(self.tab3, 'tab3')
        self.right_widget.addTab(self.tab4, 'tab4')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet(self.tabWidgetStyle())
        
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 20)
        main_layout.setStretch(1, 180)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)


    # ----------------- 
    # buttons

    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)

    def button4(self):
        self.right_widget.setCurrentIndex(3)
    
    def showConfigDialog(self):
        self.configdialog = tv.ConfigVarTableView()
        self.configdialog.show()

	# ----------------- 
    # pages

    def ui1(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 1'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui2(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 2'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main
        
    def ui3(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 3'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui4(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 4'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def pushButtonWidgetStyle(self,
                            height = None, # px
                            width = None, # px
                            color = None,
                            font = None, # px
                            borderStyle = None, 
                            borderWidth = None, # px
                            borderColor = None,
                            borderRadius = None, # px
                            backgroundColor = None,
                            hoverBorderStyle = None,
                            hoverBorderWidth = None, # px
                            hoverBorderColor = None,
                            hoverBorderRadius = None, # px
                            hoverBackgroundColor = None,
                            pressedBackgroundColor = None,
                            ):
        # styleを統合する
        widgetStyle = ''

        # 基本設定
        _height = str.format('height: {};', height)
        _width = str.format('width: {};', width)
        _color = str.format('color: {};', color)
        _font = str.format('font: {};', font)
        _borderStyle = str.format('border-style: {};', borderStyle)
        _borderWidth = str.format('border-width: {};', borderWidth)
        _borderColor = str.format('border-color: {};', borderColor)
        _borderRadius = str.format('border-radius: {};', borderRadius)
        _backgroundColor = str.format('background-color: {};', backgroundColor)
        style = 'QPushButton {%s %s %s %s %s %s %s %s %s}'% (_height, _width, _color, _font, _borderStyle, _borderWidth, _borderColor, _borderRadius, _backgroundColor)
        widgetStyle += style

        # hover設定
        _hoverBorderStyle = str.format('border-style: {};', hoverBorderStyle)
        _hoverBorderWidth = str.format('border-width: {};', hoverBorderWidth)
        _hoverBorderColor = str.format('border-color: {};', hoverBorderColor)
        _hoverBorderRadius = str.format('border-radius: {};', hoverBorderRadius)
        _hoverBackgroundColor = str.format('background-color: {};', hoverBackgroundColor)
        hoverStyle = 'QPushButton:hover {%s %s %s %s %s}' % (_hoverBorderStyle, _hoverBorderWidth, _hoverBorderColor, _hoverBorderRadius, _hoverBackgroundColor)
        widgetStyle += hoverStyle

        # pressed設定
        _pressedBackgroundColor = str.format('background-color: {};', pressedBackgroundColor)
        pressedStyle = 'QPushButton:pressed {%s}' % (_pressedBackgroundColor)
        widgetStyle += pressedStyle

        return widgetStyle        

    def tabWidgetStyle(self):

        style = 'QTabWidget::pane { \
                border-top: 2px solid #C2C7CB;} \
                QTabWidget::tab-bar { \
                left: 5px;} \
                QTabBar::tab { \
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, \
                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD, \
                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3); \
                border: 2px solid #C4C4C3; \
                border-bottom-color: #C2C7CB; \
                border-top-left-radius: 4px; \
                border-top-right-radius: 4px; \
                min-width: 8ex; \
                padding: 2px;} \
                QTabBar::tab:selected, QTabBar::tab:hover { \
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, \
                stop: 0 #fafafa, stop: 0.4 #f4f4f4, \
                stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);}; \
                QTabBar::tab:selected { \
                border-color: #9B9B9B; \
                border-bottom-color: #C2C7CB; }'

        return style