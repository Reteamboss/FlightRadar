# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interlogin.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoginWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(513, 298)
        MainWindow.setAnimated(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(60, 10, 361, 177))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1, QtCore.Qt.AlignRight)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(27)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(60, 190, 361, 99))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/Login-icon (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 1, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 2)
        self.commandLinkButton_3 = QtWidgets.QCommandLinkButton(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.commandLinkButton_3.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/user-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.commandLinkButton_3.setIcon(icon1)
        self.commandLinkButton_3.setObjectName("commandLinkButton_3")
        self.gridLayout_2.addWidget(self.commandLinkButton_3, 2, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.action_CSV = QtWidgets.QAction(MainWindow)
        self.action_CSV.setObjectName("action_CSV")
        self.action_CSV_2 = QtWidgets.QAction(MainWindow)
        self.action_CSV_2.setObjectName("action_CSV_2")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setCheckable(True)
        self.action_2.setObjectName("action_2")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.actionFAQ = QtWidgets.QAction(MainWindow)
        self.actionFAQ.setObjectName("actionFAQ")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MoneyControl"))
        self.label_2.setText(_translate("MainWindow", "Login:"))
        self.label_3.setText(_translate("MainWindow", "Password:"))
        self.label.setText(_translate("MainWindow", "Welcome"))
        self.pushButton.setText(_translate("MainWindow", "Sign in"))
        self.pushButton_2.setText(_translate("MainWindow", "Cancel"))
        self.commandLinkButton_3.setText(_translate("MainWindow", "Registration"))
        self.action_CSV.setText(_translate("MainWindow", "Import from CSV"))
        self.action_CSV_2.setText(_translate("MainWindow", "Export to CSV"))
        self.action_2.setText(_translate("MainWindow", "Add info"))
        self.action.setText(_translate("MainWindow", "Выход"))
        self.actionFAQ.setText(_translate("MainWindow", "FAQ"))
