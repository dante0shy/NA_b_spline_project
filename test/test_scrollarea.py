from PyQt5 import QtWidgets
import sys


class MyScrollWidget(QtWidgets.QWidget):

    def __init__(self):
        super(MyScrollWidget, self).__init__()
        lay = QtWidgets.QVBoxLayout(self)

        # abutton = QtWidgets.QPushButton(lay)
        # abutton.setText('add')
        # abutton.setFixedSize(100, 32)

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        lay.addWidget(scrollArea)
        top_widget = QtWidgets.QWidget()
        self.top_layout = QtWidgets.QVBoxLayout()

        for i in range(1):
            group_box = QtWidgets.QGroupBox()

            group_box.setTitle('GroupBox For Item {0}'.format(i))
            group_box.setMinimumHeight(100)
            layout = QtWidgets.QHBoxLayout(group_box)

            label = QtWidgets.QLabel()
            label.setText('Label For Item {0}'.format(i))
            layout.addWidget(label)

            push_button = QtWidgets.QPushButton(group_box)
            push_button.setText('Run Button')
            push_button.setFixedSize(100, 32)
            push_button.clicked.connect(self.add_button)

            layout.addWidget(push_button)

            self.top_layout.addWidget(group_box)

        top_widget.setLayout(self.top_layout)
        scrollArea.setWidget(top_widget)
        self.resize(200, 500)

    def add_button(self,):
        i =10
        group_box = QtWidgets.QGroupBox()
        group_box.setMinimumHeight(100)

        group_box.setTitle('GroupBox For Item {0}'.format(i))

        layout = QtWidgets.QHBoxLayout(group_box)

        label = QtWidgets.QLabel()
        label.setText('Label For Item {0}'.format(i))
        layout.addWidget(label)

        push_button = QtWidgets.QPushButton(group_box)
        push_button.setText('Run Button')
        push_button.setFixedSize(100, 32)
        push_button.clicked.connect(self.add_button)

        layout.addWidget(push_button)

        self.top_layout.addWidget(group_box)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = MyScrollWidget()
    widget.show()
    sys.exit(app.exec_())