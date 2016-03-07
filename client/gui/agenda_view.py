from client.abstract.page import *


class Agenda(Page):
    def __init__(self, info_agenda, function):
        Page.__init__(self)

        self.info_agenda = info_agenda

        self.function = function

        self.bold = QtGui.QFont()
        self.bold.setBold(True)

        self.font_12 = QtGui.QFont()
        self.font_12.setPointSize(12)

        self.combobox_align_center = QtGui.QLineEdit()
        self.combobox_align_center.setAlignment(QtCore.Qt.AlignCenter)

        self.background_transparent = "background-color: transparent;"

        # ------------------------------------- Pagina -------------------------------------
        # Creazione della pagina e del suo layout: gdr_agenda(lyt_agenda)
        self.gdr_agenda = QtGui.QWidget(self)

        self.lyt_agenda = QtGui.QGridLayout()

        # Creazione lista dei progetti
        self.create_projects_list()

        # Creazione del contenitore delle operazioni
        self.create_operation_list()

        # Creazione calendario
        self.calendar = QtGui.QCalendarWidget(self.gdr_agenda)
        self.calendar.setFirstDayOfWeek(QtCore.Qt.Monday)
        self.calendar.setSelectedDate(QtCore.QDate.currentDate())
        self.calendar.setMinimumDate(QtCore.QDate(2016, 1, 1))
        self.calendar.setVerticalHeaderFormat(QtGui.QCalendarWidget.NoVerticalHeader)
        self.connect(self.calendar, QtCore.SIGNAL("clicked(QDate)"), self.function.change_day)

        # Creazione informazioni progetto
        self.lbl_date_begin = QtGui.QLabel("Data inizio:", self.gdr_agenda)
        self.lbl_date_begin.setFont(self.bold)
        self.lbl_date_begin.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.dted_date_begin = QtGui.QDateEdit(self.gdr_agenda)
        self.dted_date_begin.setReadOnly(True)
        self.dted_date_begin.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.dted_date_begin.setFrame(False)
        self.dted_date_begin.setStyleSheet(self.background_transparent)
        self.dted_date_begin.setDate(QtCore.QDate(
            self.info_agenda['project']['begin']['year'],
            self.info_agenda['project']['begin']['month'],
            self.info_agenda['project']['begin']['day']
        ))

        self.lbl_date_end = QtGui.QLabel("Data fine:", self.gdr_agenda)
        self.lbl_date_end.setFont(self.bold)
        self.lbl_date_end.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.dted_date_end = QtGui.QDateEdit(self.gdr_agenda)
        self.dted_date_end.setReadOnly(True)
        self.dted_date_end.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.dted_date_end.setFrame(False)
        self.dted_date_end.setStyleSheet(self.background_transparent)
        self.dted_date_end.setDate(QtCore.QDate(
            self.info_agenda['project']['end']['year'],
            self.info_agenda['project']['end']['month'],
            self.info_agenda['project']['end']['day']
        ))

        self.lbl_mail_lbl = QtGui.QLabel("Project manager mail:", self.gdr_agenda)
        self.lbl_mail_lbl.setFont(self.bold)
        self.lbl_mail_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.lbl_mail = QtGui.QLabel(self.info_agenda['email'], self.gdr_agenda)
        self.lbl_mail.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.lbl_status_lbl = QtGui.QLabel("Stato:", self.gdr_agenda)
        self.lbl_status_lbl.setFont(self.bold)
        self.lbl_status_lbl.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.lbl_status = QtGui.QLabel("status", self.gdr_agenda)
        self.create_lbl_status()

        # Creazione data selezionata
        self.create_date_show()

        # Creazione lista delle attivita'
        self.create_activities_list()

        # Aggiunta degli oggeti nel lyt_agenda
        self.lyt_agenda.addWidget(self.cmb_project, 0, 0, 2, 1)
        self.lyt_agenda.addWidget(self.scrl_operation, 2, 0, 4, 1)
        self.lyt_agenda.addWidget(self.calendar, 6, 0, 4, 1)
        self.lyt_agenda.addWidget(self.lbl_date_begin, 0, 1, 1, 1)
        self.lyt_agenda.addWidget(self.dted_date_begin, 0, 2, 1, 1)
        self.lyt_agenda.addWidget(self.lbl_date_end, 0, 3, 1, 1)
        self.lyt_agenda.addWidget(self.dted_date_end, 0, 4, 1, 1)
        self.lyt_agenda.addWidget(self.lbl_mail_lbl, 1, 1, 1, 1)
        self.lyt_agenda.addWidget(self.lbl_mail, 1, 2, 1, 1)
        self.lyt_agenda.addWidget(self.lbl_status_lbl, 1, 3, 1, 1)
        self.lyt_agenda.addWidget(self.lbl_status, 1, 4, 1, 1)
        self.lyt_agenda.addWidget(self.hrz_date, 2, 1, 1, 1)
        self.lyt_agenda.addWidget(self.scrl_activities, 3, 1, 7, 7)

        # Set del layout della pagina
        self.gdr_agenda.setLayout(self.lyt_agenda)

        # Set del widget della pagina
        self.setCentralWidget(self.gdr_agenda)

        # ------------------------------------- Menu bar -------------------------------------

        self.logout = QtGui.QAction(QtGui.QIcon(LOGOUT), "Logout", self)
        self.connect(self.logout, QtCore.SIGNAL('triggered()'), self.function.logout)
        self.logout.setShortcut("Ctrl+L")
        self.logout.setStatusTip("Logout")

        sep = QtGui.QAction(self)
        sep.setSeparator(True)

        self.m_file.addAction(sep)
        self.m_file.addAction(self.logout)

    def create_projects_list(self):
        self.cmb_project = QtGui.QComboBox(self.gdr_agenda)
        self.cmb_project.setLineEdit(self.combobox_align_center)
        self.cmb_project.setFont(self.font_12)
        for key, value in self.info_agenda['projects'].items():
            self.cmb_project.addItem(value)
        self.connect(self.cmb_project, QtCore.SIGNAL("currentIndexChanged(int)"), self.change_project)

    def create_operation_list(self):
        self.scrl_operation = QtGui.QScrollArea(self.gdr_agenda)
        self.scrl_operation.setBackgroundRole(QtGui.QPalette.NoRole)

        # Creazione del contenitore delle operazioni e del suo layout: vrt_opreations(lyt_opreations)
        self.vrt_opreations = QtGui.QWidget(self.scrl_operation)
        self.vrt_opreations.setStyleSheet("text-align: left;")

        self.lyt_opreations = QtGui.QVBoxLayout()

        list_operations = []
        # Creazione bottoni operazioni
        self.cmd_create_holiday = QtGui.QPushButton("Inserisci le vacanze", self.vrt_opreations)
        self.cmd_create_holiday.setFlat(True)
        self.cmd_create_holiday.setStatusTip("Inserisci le vacanze")
        self.connect(self.cmd_create_holiday, QtCore.SIGNAL("clicked()"), self.function.create_holiday)
        list_operations.append(self.cmd_create_holiday)

        self.cmd_create_single_activity = QtGui.QPushButton("Inserisci una tua attivita'", self.vrt_opreations)
        self.cmd_create_single_activity.setFlat(True)
        self.cmd_create_single_activity.setStatusTip("Inserisci un tua attivita'")
        self.connect(self.cmd_create_single_activity, QtCore.SIGNAL("clicked()"), self.function.create_single_activity)
        list_operations.append(self.cmd_create_single_activity)

        if self.info_agenda['level'] == 'teamleader':
            self.cmd_create_group_activity = QtGui.QPushButton("Inserisci un'attivita' di gruppo", self.vrt_opreations)
            self.cmd_create_group_activity.setFlat(True)
            self.cmd_create_group_activity.setStatusTip("Inserisci un'attivita' di gruppo")
            self.connect(self.cmd_create_group_activity, QtCore.SIGNAL("clicked()"),
                         self.function.create_group_activity)
            list_operations.append(self.cmd_create_group_activity)

            self.cmd_create_group = QtGui.QPushButton("Crea un nuovo gruppo", self.vrt_opreations)
            self.cmd_create_group.setFlat(True)
            self.cmd_create_group.setStatusTip("Crea un nuovo gruppo")
            self.connect(self.cmd_create_group, QtCore.SIGNAL("clicked()"), self.function.create_group)
            list_operations.append(self.cmd_create_group)

            self.cmd_modify_group = QtGui.QPushButton("Modifica un gruppo", self.vrt_opreations)
            self.cmd_modify_group.setFlat(True)
            self.cmd_modify_group.setStatusTip("Modifica un gruppo")
            self.connect(self.cmd_modify_group, QtCore.SIGNAL("clicked()"), self.function.modify_group)
            list_operations.append(self.cmd_modify_group)

        elif self.info_agenda['level'] == 'projectmanager':
            self.cmd_create_project = QtGui.QPushButton("Crea un nuovo progetto", self.vrt_opreations)
            self.cmd_create_project.setFlat(True)
            self.cmd_create_project.setStatusTip("Crea un nuovo progetto")
            self.connect(self.cmd_create_project, QtCore.SIGNAL("clicked()"), self.function.create_project)
            list_operations.append(self.cmd_create_project)

            self.cmd_modify_role = QtGui.QPushButton("Modifica ruolo ad un partecipante", self.vrt_opreations)
            self.cmd_modify_role.setFlat(True)
            self.cmd_modify_role.setStatusTip("Modifica ruolo ad un partecipante")
            self.connect(self.cmd_modify_role, QtCore.SIGNAL("clicked()"), self.function.modify_role)
            list_operations.append(self.cmd_modify_role)

            self.cmd_modify_project = QtGui.QPushButton("Modifica progetto", self.vrt_opreations)
            self.cmd_modify_project.setFlat(True)
            self.cmd_modify_project.setStatusTip("Modifica progetto")
            self.connect(self.cmd_modify_project, QtCore.SIGNAL("clicked()"), self.function.modify_project)
            list_operations.append(self.cmd_modify_project)

            self.cmd_create_activity_project = QtGui.QPushButton("Crea nuova attivita' di progetto",
                                                                 self.vrt_opreations)
            self.cmd_create_activity_project.setFlat(True)
            self.cmd_create_activity_project.setStatusTip("Crea nuova attivita' di progetto")
            self.connect(self.cmd_create_activity_project, QtCore.SIGNAL("clicked()"),
                         self.function.create_activity_project)
            list_operations.append(self.cmd_create_activity_project)

        # Aggiunta bottoni al layout
        for cmd in list_operations:
            self.lyt_opreations.addWidget(cmd)

        # Set del layout della pagina
        self.vrt_opreations.setLayout(self.lyt_opreations)

        # Set layout dello scroll
        self.scrl_operation.setWidget(self.vrt_opreations)

    def create_lbl_status(self):
        print self.info_agenda['project']['status']
        if self.info_agenda['project']['status']:
            message = "Attivo"
            style = "background-color: rgb(0, 255, 0);"
        else:
            message = "Terminato"
            style = "background-color: rgb(255, 0, 0);"

        self.lbl_status.setText(message)
        self.lbl_status.setStyleSheet(style)
        self.lbl_status.setAlignment(QtCore.Qt.AlignCenter)

    def create_date_show(self):
        # Creazione del contenitore della data e del suo layout: hrz_date(lyt_date)
        self.hrz_date = QtGui.QWidget(self.gdr_agenda)
        self.hrz_date.setObjectName("hrz_date")
        self.hrz_date.setStyleSheet("""
            #hrz_date {
                border-style: double;
                border-width: 2px;
                border-radius: 8px;
                border-color: black;
            }
        """)

        self.lyt_date = QtGui.QHBoxLayout()

        # Creazione del giorno mese e anno
        self.lbl_day = QtGui.QLabel(str(QtCore.QDate.currentDate().day()), self.hrz_date)
        self.lbl_day.setAlignment(QtCore.Qt.AlignCenter)

        self.lbl_month = QtGui.QLabel(QtCore.QDate.longMonthName(QtCore.QDate.currentDate().month()), self.hrz_date)
        self.lbl_month.setAlignment(QtCore.Qt.AlignCenter)

        self.lbl_year = QtGui.QLabel(str(QtCore.QDate.currentDate().year()), self.hrz_date)
        self.lbl_year.setAlignment(QtCore.Qt.AlignCenter)

        # Aggiunta del giorno mese anno nel hrz_date
        self.lyt_date.addWidget(self.lbl_day)
        self.lyt_date.addWidget(self.lbl_month)
        self.lyt_date.addWidget(self.lbl_year)

        # Set del layout della pagina
        self.hrz_date.setLayout(self.lyt_date)

    def create_activities_list(self):
        self.scrl_activities = QtGui.QScrollArea(self.gdr_agenda)
        self.scrl_activities.setBackgroundRole(QtGui.QPalette.NoRole)

        # Creazione del contenitore delle attivita' e del suo layout: vrt_activities(lyt_activities)
        self.vrt_activities = QtGui.QWidget(self.scrl_activities)

        self.lyt_activities = QtGui.QVBoxLayout()

        if self.info_agenda['activities']:
            self.sort_activity()

        # Aggiunta delle attivita' nella lista
        for activity in self.info_agenda['activities']:
            self.lyt_activities.addWidget(self.create_activity(activity))

        self.holiday_to_activity()

        # Aggiunta delle vacanze nella lista
        for holiday in self.info_agenda['holidays']:
            self.lyt_activities.addWidget(self.create_activity(holiday))

        # Set del layout della lista
        self.vrt_activities.setLayout(self.lyt_activities)

        # Set layout dello scroll
        self.scrl_activities.setWidget(self.vrt_activities)

    def create_activity(self, activity):
        # Creazione del contenitore dell'attivita' e del suo layout: gdr_activity(lyt_activity)
        gdr_activity = QtGui.QWidget(self.vrt_activities)
        gdr_activity.setFixedSize(QtCore.QSize(400, 120))
        gdr_activity.setObjectName("gdr_activity")
        gdr_activity.setStyleSheet("""
            #gdr_activity {
                border-style: double;
                border-width: 2px;
                border-radius: 8px;
                border-color: black;
            }
        """)

        lyt_activity = QtGui.QGridLayout()

        # Creazione elementi dell'attivita'
        lbl_color = QtGui.QLabel("", gdr_activity)
        if activity['type'] == "project":
            style = "background-color: rgb(255, 0, 0);"
        elif activity['type'] == "group":
            style = "background-color: rgb(255, 255, 0);"
        elif activity['type'] == "single":
            style = "background-color: rgb(0, 255, 255);"
        else:
            style = "background-color: rgb(0, 255, 0);"
        lbl_color.setStyleSheet(style)
        lbl_color.setFixedSize(QtCore.QSize(15, 100))

        lbl_begin = QtGui.QLabel(
            self.set_time(activity['begin']['hour']) + " : " + self.set_time(activity['begin']['minute']),
            gdr_activity
        )

        lbl_end = QtGui.QLabel(
            self.set_time(activity['end']['hour']) + " : " + self.set_time(activity['end']['minute']),
            gdr_activity
        )

        # Creazione del contenitore del nome e del suo layout: hrz_name(lyt_name)
        hrz_name = QtGui.QWidget(gdr_activity)

        lyt_name = QtGui.QHBoxLayout()

        # Creazione del nome e della stanza
        lbl_room = QtGui.QLabel(activity['room'], hrz_name)

        lbl_name = QtGui.QLabel(activity['name'], hrz_name)
        lbl_name.setFont(self.font_12)

        # Aggiunta del nome e della stanza nel hrz_name
        lyt_name.addWidget(lbl_room)
        lyt_name.addWidget(lbl_name)

        # Set del layout della pagina
        hrz_name.setLayout(lyt_name)

        # Creazione icona info
        icon = QtGui.QLabel(self)
        icon.setPixmap(QtGui.QIcon(INFO).pixmap(QtCore.QSize(24, 24)))
        icon.setStatusTip("Ottieni piu informazioni o modifica")
        if activity['type'] != "holiday":
            icon.mouseReleaseEvent = lambda (event): self.view_activity(activity['ID'])
        else:
            icon.mouseReleaseEvent = lambda (event): self.view_holiday(activity['ID'])

        # Aggiunta degli oggeti nel lyt_agenda
        lyt_activity.addWidget(lbl_color, 0, 0, 3, 1)
        lyt_activity.addWidget(lbl_begin, 0, 1, 1, 1)
        lyt_activity.addWidget(lbl_end, 2, 1, 1, 1)
        lyt_activity.addWidget(hrz_name, 1, 1, 1, 2)
        lyt_activity.addWidget(icon, 1, 3, 2, 1)

        # Set del layout
        gdr_activity.setLayout(lyt_activity)

        return gdr_activity

    def set_list_activities(self, new_list_activity, new_list_holiday):
        self.info_agenda['activities'] = new_list_activity

        self.info_agenda['holidays'] = new_list_holiday

        self.lyt_agenda.removeWidget(self.scrl_activities)

        self.scrl_activities.deleteLater()

        self.create_activities_list()

        self.lyt_agenda.addWidget(self.scrl_activities, 3, 1, 7, 7)

    @staticmethod
    def set_time(time):
        if time < 10:
            time = "0" + str(time)
        else:
            time = str(time)

        return time

    def sort_activity(self):
        self.info_agenda['activities'] = sorted(
            self.info_agenda['activities'],
            key=lambda k: (k['begin']['hour'], k['begin']['minute'], k['name'])
        )

    def view_activity(self, _id):
        self.function.exec_activity_view(_id)

    def view_holiday(self, _id):
        self.function.exec_holiday_view(_id)

    def holiday_to_activity(self):
        list_app = []

        for _id, holidays in self.info_agenda['holidays'].items():
            for holiday in holidays:
                activity = dict()
                activity['ID'] = holiday['ID']
                activity['type'] = "holiday"
                activity['begin'] = dict()
                activity['begin']['hour'] = str(holiday['begin']['day']) + "/" + str(holiday['begin']['month'])
                activity['begin']['minute'] = holiday['begin']['year']
                activity['end'] = dict()
                activity['end']['hour'] = str(holiday['end']['day']) + "/" + str(holiday['end']['month'])
                activity['end']['minute'] = holiday['end']['year']
                activity['room'] = str(_id) + "/" + str(holiday['ID'])
                activity['name'] = holiday['name']
                list_app.append(activity)

        self.info_agenda['holidays'] = list_app

    def change_project(self, index):
        self.info_agenda = self.function.change_project(index)

        self.create_operation_list()

        self.dted_date_begin.setDate(QtCore.QDate(
            self.info_agenda['project']['begin']['year'],
            self.info_agenda['project']['begin']['month'],
            self.info_agenda['project']['begin']['day']
        ))

        self.dted_date_end.setDate(QtCore.QDate(
            self.info_agenda['project']['end']['year'],
            self.info_agenda['project']['end']['month'],
            self.info_agenda['project']['end']['day']
        ))

        self.lbl_mail.setText(self.info_agenda['email'])

        self.create_lbl_status()

        self.function.change_day(self.calendar.selectedDate())
