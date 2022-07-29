from opensky_api import OpenSkyApi
import requests as req
import sys
import io
import folium
import csv
import time
import threading
import sched
import pandas as pd
from userinfo import LOGIN,PASSWORD
import sqlite3 as sq
from opsk import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget,QHBoxLayout,QVBoxLayout,QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from folium.plugins import MousePosition, LocateControl
from PyQt5 import QtWidgets, QtSql, QtCore, QtGui
from interlogindesign import Ui_LoginWindow
from rfdesign import Ui_RegFormWindow
from fildesign import Ui_Dialog
from PyQt5.QtSql import QSqlTableModel



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_11.clicked.connect(QtWidgets.qApp.quit)
        self.ui.pushButton_4.clicked.connect(self.get_info)
        self.ui.pushButton_4.clicked.connect(self.show_all)
        # self.ui.pushButton_4.clicked.connect(self.update_all_info)
        self.ui.tableView.setSelectionBehavior(True)
        self.ui.toolButton.clicked.connect(filter_window.show)
        self.ui.tableView.setMouseTracking(True)
        self.ui.tableView.clicked.connect(self.on_click_left_button)
        self.ui.tableView.clicked.connect(self.callsign_plane)
        self.ui.pushButton.clicked.connect(self.get_coordinates)
        self.ui.pushButton_2.clicked.connect(self.show_by_category)
        self.web_map = MainWindow.create_map(self)
        self.ui.verticalLayout.addWidget(self.web_map)



    def update_all_info(self):
        threading.Timer(5.0, self.update_all_info).start()  # Перезапуск через 5 секунд
        # window.get_coordinates()
        df = window.get_coordinates()
        # window.update_marker(df)

    def create_web_map(self):
        web_map = folium.Map(zoom_start=12, location=[48.8670, 2.4586], tiles="Stamen Terrain")
        return web_map






    def create_map(self):
        web_map = MainWindow.create_web_map(self)

        cur.execute("SELECT callsign,origin_country,time_position,last_contact,longitude,latitude FROM "
                    "planes WHERE (longitude or latitude) != 'None'")
        planes = cur.fetchall()
        for info_plane in planes:
            longitude = info_plane[4]
            latitude = info_plane[5]
            coordinates = [latitude, longitude]
            tooltip = str(info_plane[0]) + '\n' + str(info_plane[1])
            popup = "Callsign: {0} \nCountry: {1} \nTime position: {2} \n, Last contact: {3} \n Longitude: {4} \n" \
                    "Latitude: {5} ".format(info_plane[0],info_plane[1],info_plane[2],info_plane[3],info_plane[4],info_plane[5])
            folium.Marker(location=coordinates,tooltip=tooltip,popup=popup, icon=folium.Icon(icon="plane", color='green',draggable=True)).add_to(web_map)
        data = io.BytesIO()

        # res = m.get_bounds()
        web_map.add_child(folium.LatLngPopup())
        formatter = "function(num) {return L.Util.formatNum(num, 5);};"
        mouse_position = MousePosition(
            position='topright',
            separator=' Long: ',
            empty_string='NaN',
            lng_first=False,
            num_digits=20,
            prefix='Lat:',
            lat_formatter=formatter,
            lng_formatter=formatter)
        locate_control = LocateControl(auto_start=False)

        web_map.add_child(mouse_position)
        web_map.add_child(locate_control)

        web_map.save(data, close_file=False)

        web_view.setHtml(data.getvalue().decode())
        return web_view

    def update_marker(self,df):
        web_map = MainWindow.create_web_map(self)

        lon = df['Longitude']
        lat = df['Latitude']
        cal = df['Callsign']
        country = df['Country']
        timepos = df['Timeposition']
        lastcont = df['Lastcontact']
        for lat, lon,cal,country,timepos,lastcont in zip(lat, lon, cal,country,timepos,lastcont):
            folium.Marker(location=[lat, lon], tooltip= str(cal) + '\n' + str(country),
                          popup= "Callsign: {0} \nCountry: {1} \nTime position: {2} \n, "
                        "Last contact: {3} \n Longitude: {4} \n Latitude: {5} ".format(cal, country,
                                                                                       timepos, lastcont, lon,lat),
                          icon=folium.Icon(icon="plane", color='red')).add_to(web_map)
        data = io.BytesIO()
        # res = m.get_bounds()
        # m.add_child(folium.LatLngPopup())
        # formatter = "function(num) {return L.Util.formatNum(num, 5);};"
        # mouse_position = MousePosition(
        #     position='topright',
        #     separator=' Long: ',
        #     empty_string='NaN',
        #     lng_first=False,
        #     num_digits=20,
        #     prefix='Lat:',
        #     lat_formatter=formatter,
        #     lng_formatter=formatter)

        # m.add_child(mouse_position)

        web_map.save(data, close_file=False)

        web_view.setHtml(data.getvalue().decode())

    def get_info(self):
        api = OpenSkyApi("Irbis07","6pwhh4ceR" )
        states = api.get_states()
        # for s in states.states:
        #     print("(%r, %r, %r, %r)" % (s.longitude, s.latitude, s.baro_altitude, s.velocity))
        http_get = 'https://opensky-network.org/api/states/all?lamin=47.0500&lomin=-1.9358&lamax=50.2635&lomax=6.6773'
        r = req.get(http_get)
        r.encoding = 'utf-8'
        result = r.json()
        to_db = []
        con1.open()
        for get_val in result['states']:
            get_val = tuple(get_val)
            to_db.append(get_val)
        cur.executemany("INSERT OR IGNORE INTO planes (icao,callsign,origin_country ,time_position ,last_contact ,"
                    "longitude ,latitude ,baro_altitude ,on_ground ,velocity ,true_track ,vertical_rate ,sensors ,"
                    "geo_altitude ,squawk ,spi ,position_source) VALUES ( ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?);",to_db)
        con.commit()

    def get_coordinates(self):
        api = OpenSkyApi(LOGIN, PASSWORD)
        # bbox = (min latitude, max latitude, min longitude, max longitude)
        states = api.get_states(bbox=(47.0500, 50.2635, -1.9358, 6.6773))
        to_db2 = []
        for s in states.states:
            info_tuple = [s.callsign,s.origin_country,s.time_position, s.last_contact,s.longitude, s.latitude]
            to_db2.append(info_tuple)
        df = pd.DataFrame(to_db2, columns =["Callsign", "Country", "Timeposition", "Lastcontact","Longitude","Latitude"])
        print(df)
        return df

    def show_by_category(self):
        category = self.ui.lineEdit_2.text()
        tv = self.ui.tableView
        tv.setModel(stm)
        con1.open()
        stm.setTable('planes')

        if category != "":
            categoryfilter = f"icao = '{category}' or callsign = '{category}' or origin_country = '{category}' "
            stm.setFilter(categoryfilter)
            stm.select()
            MainWindow.set_column_tableview_width(self)
            count = stm.rowCount()
            self.ui.label_35.setText('<font color=green>Успешно! Отображено {} записей</font>'.format(count))
        else:
            self.ui.label_35.setText('<font color=red>Вы ничего не выбрали!</font>')




    def update_info(self):
        pass

    def show_all(self):
        tv = self.ui.tableView
        tv.setModel(stm)
        con1.open()
        stm.setTable('planes')
        stm.select()
        MainWindow.set_column_tableview_width(self)
        cur.execute("SELECT * FROM planes")
        count = len(cur.fetchall())
        self.ui.label_35.setText('<font color=green>Успешно! Отображено {} записей</font>'.format(count))

    def show_marker(self):
        pass

    def set_column_tableview_width(self):
        tv = self.ui.tableView
        tv.setModel(stm)
        # tv.setSortingEnabled(True)
        # tv.setColumnWidth(0, 70)
        # tv.setColumnWidth(1, 230)
        # tv.setColumnWidth(2, 120)
        # tv.setColumnWidth(3, 120)
        # tv.setColumnWidth(4, 60)
        # tv.setColumnWidth(5, 50)
        tv.hideColumn(3)
        tv.hideColumn(4)
        tv.hideColumn(7)
        tv.hideColumn(8)
        tv.hideColumn(9)
        tv.hideColumn(10)
        tv.hideColumn(11)
        tv.hideColumn(12)
        tv.hideColumn(13)
        tv.hideColumn(14)
        tv.hideColumn(15)
        tv.hideColumn(16)
        stm.setHeaderData(0, QtCore.Qt.Horizontal, 'Icao')
        stm.setHeaderData(1, QtCore.Qt.Horizontal, 'Callsign')
        stm.setHeaderData(2, QtCore.Qt.Horizontal, 'Country')
        stm.setHeaderData(5, QtCore.Qt.Horizontal, 'Longitude')
        stm.setHeaderData(6, QtCore.Qt.Horizontal, 'Latitude')

    def on_click_left_button(self, index):
        con1.open()
        result = self.ui.tableView.model().index(index.row(), 1).data()
        cur.execute("SELECT * FROM planes WHERE callsign = '{}'".format(result))
        sql_result = list(cur.fetchone())
        print(sql_result)
        MainWindow.show_more_information(self, sql_result)

        return result

    def show_more_information(self, sql_result):
        self.ui.label_3.setText(sql_result[0])
        self.ui.label_7.setText(sql_result[1])
        self.ui.label_8.setText(sql_result[2])
        self.ui.label_9.setText(str(sql_result[3]))
        self.ui.label_10.setText(str(sql_result[4]))
        self.ui.label_11.setText(str(sql_result[5]))
        self.ui.label_14.setText(str(sql_result[6]))
        self.ui.label_20.setText(str(sql_result[7]))
        self.ui.label_19.setText(str(sql_result[8]))
        self.ui.label_15.setText(str(sql_result[9]))
        self.ui.label_21.setText(str(sql_result[10]))
        self.ui.label_24.setText(str(sql_result[11]))
        self.ui.label_25.setText(str(sql_result[12]))
        self.ui.label_28.setText(str(sql_result[13]))
        self.ui.label_29.setText(str(sql_result[14]))
        self.ui.label_31.setText(str(sql_result[15]))
        self.ui.label_33.setText(str(sql_result[16]))


    def index_row(self):
        index_row = self.ui.tableView.currentIndex().row()
        return index_row

    def callsign_plane(self):
        callsign_plane = self.ui.tableView.model().index(MainWindow.index_row(self), 1).data()
        return callsign_plane


class User():
    def __init__(self, firstname, lastname, username, password, email):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.email = email

class RegistrationForm(QtWidgets.QMainWindow):
    def __init__(self):
        super(RegistrationForm, self).__init__()
        self.ui = Ui_RegFormWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.registration)
        self.ui.pushButton_2.clicked.connect(self.back_login_window)


    def registration(self):
        user = User(firstname=self.ui.lineEdit_2.text(),
                      lastname=self.ui.lineEdit_3.text(),
                      username=self.ui.lineEdit_4.text(),
                      password=self.ui.lineEdit_5.text(),
                      email=self.ui.lineEdit_6.text())
        cur.execute(f"SELECT username, password FROM users WHERE username = '{user.username}' AND password = '{user.password}'")

        if cur.fetchone() is None:
            cur.execute("INSERT OR IGNORE INTO users VALUES (?,?,?,?,?)",
                        (user.firstname, user.lastname, user.username, user.password, user.email))
            con.commit()
            self.ui.label_7.setText("<font color=green>Вы успешно зарегестрировались!</font>")
            time.sleep(1)
            RegistrationForm.back_login_window(self)
        else:
            self.ui.label_7.setText("<font color=red>Такой логин уже существует!</font>")

    def back_login_window(serf):
        login_window.show()
        reg_form.close()


class FilterWindow(QtWidgets.QDialog):
    def __init__(self):
        super(FilterWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.comboBox.currentTextChanged.connect(self.choose_callsign)
        self.ui.buttonBox.accepted.connect(self.show_by_filter)
        # self.ui.buttonBox.accepted.connect(self.zip_area)
        # self.ui.buttonBox.accepted.connect(self.calculate_distance_area)
        self.ui.buttonBox.rejected.connect(self.back_main_window)


        def combobox_info():  # функция для добавления информации о городах и почтовых зип в комбобокс
            cur.execute(f"SELECT origin_country FROM planes")
            self.sql = cur.fetchall()
            return self.sql

        combobox_info()
        self.country = set()
        for i in self.sql:
            self.country.update(i)
        self.ui.comboBox.addItems(self.country)

    def choose_callsign(self):
        self.choose_country = self.ui.comboBox.currentText()
        cur.execute("SELECT callsign FROM planes WHERE origin_country = '{}'".format(self.choose_country))
        self.sql_callsign = cur.fetchall()
        self.sql_callsign = set()
        for i in self.sql_callsign:
            self.sql_callsign.update(i)
        self.ui.comboBox_2.addItems(self.sql_callsign)

    def show_by_filter(self):
        filter_window.close()
        callsign = self.ui.comboBox_2.currentText()
        window.ui.tableView.setModel(stm)
        con1.open()
        stm.setTable('planes')
        # try:
        #     dist_var = float(self.ui.lineEdit.text())
        # except:
        #     "ValueError: could not convert string to float: ''"

        categoryfilter = f" callsign = '{callsign}'"
        stm.setFilter(categoryfilter)
        stm.select()
        window.set_column_tableview_width()
        count = stm.rowCount()
        con1.close()
        window.ui.label_35.setText('<font color=green>Успешно! Отображено {} записей</font>'.format(count))



    def back_main_window(self):
        filter_window.close()
        window.show()

    # def zip_area(self):
    #     con1.open()
    #     cur.execute("SELECT zip FROM maininfo")
    #     zips = cur.fetchall()
    #     zip_db = []
    #     zip_set = set(zips)
    #     zip1 = filter_window.get_zip()
    #     dist_var = float(self.ui.lineEdit.text())
    #     for zip2 in zip_set:
    #         zip_codes = util.read_zip_all()
    #         rezult = zip_app.process_dist(zip_codes, zip1, zip2[0])
    #         try:
    #             if rezult <= dist_var:
    #                 zip_db.append(zip2[0])
    #             print(rezult)
    #             print(zip_db)
    #         except:
    #             "TypeError: '<=' not supported between instances of 'NoneType' and 'float'"
    #     return zip_db



        # zip_codes = util.read_zip_all()
        # rezult = zip_app.process_dist(zip_codes, zip1, zip2)
        # print(zip_list)

    # def calculate_distance_area(self):
    #     zip1 = self.ui.comboBox_3.currentText()
    #     distance_area = self.ui.lineEdit.text()
    #     cur.execute("SELECT zip_code FROM zip_codes")
    #     zip_result2 = cur.fetchall()
    #     zip2 = []
    #     true_zip = []
    #     for i in zip_result2:
    #         zip2.append(i)
    #     for x in zip2:
    #         distance = zip_app.process_dist(zip1,zip2)
    #         if distance < distance_area:
    #             true_zip.append(x)
    #     print(true_zip)


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(QtWidgets.qApp.quit)
        self.ui.commandLinkButton_3.clicked.connect(self.registration)
        self.ui.pushButton.clicked.connect(self.sign_in)

    def sign_in(self):
        username = self.ui.lineEdit_2.text()
        password = self.ui.lineEdit.text()
        cur.execute(f"SELECT username, password FROM users WHERE username = '{username}' AND password = '{password}'")
        con1.commit()
        if not cur.fetchone():
            self.ui.label_4.setText("<font color=red>Неверный логин и/или пароль!</font>")
        else:
            self.ui.label_4.setText("<font color=green>Успешно!Добро пожаловать!</font>")
            window.show()
            cur.execute(f"SELECT firstname, lastname FROM users WHERE username = '{username}' AND password = '{password}'")
            name = cur.fetchone()
            # window.ui.label_113.setText(f"{name[0]} {name[1]}")
            login_window.close()
            return username

    def registration(self):
        login_window.close()
        reg_form.show()

with sq.connect("flights.db") as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS planes (
        icao TEXT,
        callsign TEXT PRIMARY KEY,
        origin_country TEXT,
        time_position INTEGER,
        last_contact INTEGER,
        longitude REAL,
        latitude REAL,
        baro_altitude REAL,
        on_ground NUMERIC,
        velocity REAL,
        true_track REAL,
        vertical_rate REAL,
        sensors INTEGER,
        geo_altitude REAL,
        squawk TEXT,
        spi NUMERIC,
        position_source INTEGER)""")


    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        lastname VARCHAR,
        firstname VARCHAR,
        username VARCHAR PRIMARY KEY,
        password VARCHAR,
        email VARCHAR )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS planes_coordinates (
            callsign VARCHAR,
            time_position INTEGER,
            longitude REAL,
            latitude REAL )""")
    con.commit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    s = sched.scheduler(time.time, time.sleep)
    s.run()
    web_view = QWebEngineView()
    # app.setStyleSheet('''
    #     QWidget {
    #         font-size: 35px;''')
    filter_window = FilterWindow()
    window = MainWindow()
    window.update_all_info()
    login_window = LoginWindow()
    reg_form = RegistrationForm()
    con1 = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    con1.setDatabaseName('flights.db')
    con1.open()
    stm = QtSql.QSqlRelationalTableModel(parent=window)
    con1.close()
    login_window.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window')