from PySide2.QtWidgets import QMainWindow , QPushButton , QHBoxLayout , QVBoxLayout , QWidget, QLabel , QDialog,QCheckBox,QLineEdit,QRadioButton,QSlider,QComboBox,QProgressBar,QTabBar

from PySide2.QtCore import Qt

class NewWindow(QMainWindow):
    def __init__(self):
        super(NewWindow,self).__init__()
        self.setWindowTitle("QMainWindow")
        self.createUI()
        self.setFixedSize(300,300)
    
    def createUI(self):

        #declare some widgets
        central_Widget = QWidget()
        self.widget1 = QPushButton()
        self.widget2 = QLabel()
        self.widget3 = QLineEdit()
        self.widget4 = QCheckBox()
        self.widget5 = QRadioButton()
        self.widget6 = QSlider(Qt.Horizontal)
        self.widget7 = QComboBox()
        self.widget8 = QProgressBar()
        self.widget9 = QTabBar()

        #widget parameters
        self.widget1.setText("QPushButton")
        self.widget2.setText("QLabel")
        self.widget3.setPlaceholderText("QLineEdit")
        self.widget4.setText("QCheckBox")
        self.widget5.setText("QRadioButton")
        self.widget7.setEditable(True)
        self.widget8.setValue(25)
        self.widget9.addTab("QTabBar1")
        self.widget9.addTab("QTabBar2")
        self.widget9.addTab("QTabBar3")


        #declare some layouts
        layout1 = QVBoxLayout()

        #Add widget to Layout
        layout1.addWidget(self.widget1)
        layout1.addWidget(self.widget2)
        layout1.addWidget(self.widget3)
        layout1.addWidget(self.widget4)
        layout1.addWidget(self.widget5)
        layout1.addWidget(self.widget6)
        layout1.addWidget(self.widget7)
        layout1.addWidget(self.widget8)
        layout1.addWidget(self.widget9)

        #set Layout to centralwidget
        central_Widget.setLayout(layout1)
        self.setCentralWidget(central_Widget)



window = NewWindow()
window.show()
