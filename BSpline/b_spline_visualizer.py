import sys,os
from BSpline.GUI import Ui_MainWindow,Ui_Form
# from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox,QGraphicsScene
# from PyQt5 import QtGui
from BSpline.bSpliner import b_spline
import numpy as np
import matplotlib.pyplot as plt
import hashlib,datetime

class MainWindow(QMainWindow):
    tmp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'tmp')
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self.ui.widget.setLayout(self.ui.verticalLayout_2)
        # self.ui.scrollArea.setWidget(self.ui.widget)

        self.ui.addButton.clicked.connect(self.add_button)
        self.ui.drawButton.clicked.connect(self.draw_b_spline)

        scene = QGraphicsScene()
        scene.addText("Input the coordinate and use draw button to draw the curve!")
        self.ui.graphicsView.setScene(scene)
        # self.t.move(10, 10)
        self.ui.graphicsView.show()

        self.kp_container = []
        # self.ui.scrollArea.ver.verticalScrollBar().valueChanged.connect(onScrollBarValueChanged)
        for i in range(5):
            self.add_button()
        # self.add_button()
        # self.del_button(self.kp_container[0])
        # self.draw_b_spline()

    def add_button(self):
        # scroll_widget = QGroupBox()
        new_input = Ui_Form()
        new_input.setupUi()
        self.ui.scrollAreaWidgetContents.setMinimumHeight((new_input.horizontalLayoutWidget.height())*1.5 * len(self.kp_container))
        self.kp_container.append(new_input)
        self.ui.verticalLayout_2.addWidget(new_input.horizontalLayoutWidget)
        new_input.delButton.clicked.connect(lambda:self.del_button(new_input))

    def draw_b_spline(self):
        degree = self.ui.degreeEdit.text().strip()
        try:
            degree = int(degree)
        except Exception:
            QMessageBox.warning(self, 'Error', 'Input can only be a int')
            return
            pass
        method = 0 if self.ui.radioButton.isChecked() else 1
        points = []
        for w in self.kp_container:
            x = self.check_float(w.lineEdit.text())
            if x[0]:
                x = x[1]
            else:
                QMessageBox.warning(self, 'Error', 'Input can only be a float')
                return

            y = self.check_float(w.lineEdit_2.text())
            if y[0]:
                y = y[1]
            else:
                QMessageBox.warning(self, 'Error', 'Input can only be a float')
                return
            points.append([x,y])
        b_splines = b_spline.BSpline(degree=degree,p_mode=method)
        control_points = np.array(points)
        b_splines.fit(control_points)
        curve = b_splines.get_interpolation()
        fig = plt.figure()
        ax = fig.gca()
        tmp = np.vstack((control_points,b_splines.c))
        r = np.nan_to_num([-1, tmp[:,0].max(0)+1.5, -1, tmp[:,1].max(0)+1.5],nan = 50)
        ax.axis(r)
        ax.plot(curve[:, 0], curve[:, 1], label='curve')
        ax.scatter(control_points[:, 0], control_points[:, 1], marker='^')

        ax.scatter(b_splines.c[:, 0], b_splines.c[:, 1], marker='o', c='b')
        ax.plot(b_splines.c[:, 0], b_splines.c[:, 1], "b--", linewidth=1, c='b')
        day = datetime.datetime.now()
        day = '{}-{}-{}'.format(day.year,day.month,day.day)
        cfg = b_splines.org_config()
        cfg = hashlib.sha224(str.encode(cfg)).hexdigest()
        self.show_path = os.path.join(self.tmp_path,'{}-{}.png'.format(day,cfg))
        plt.savefig(self.show_path)
        # plt.show()
        pic = QPixmap(self.show_path)
        scene = QGraphicsScene()
        scene.addPixmap(pic)
        self.ui.graphicsView.setScene(scene)
        # self.t.move(10, 10)
        self.ui.graphicsView.show()
        # scene.addItem(QGraphicsPixmapItem(pic))
        # view = self.gv
        # view.setScene(scene)
        # view.setRenderHint(QtGui.QPainter.Antialiasing)
        pass

    def check_float(self,f):
        try:
            return True,float(f.strip())
        except Exception:
            return False,0.

    def del_button(self,input_line):
        w = self.kp_container.pop(self.kp_container.index(input_line))
        self.ui.verticalLayout_2.removeWidget(w.horizontalLayoutWidget)
        self.ui.scrollAreaWidgetContents.setMinimumHeight((w.horizontalLayoutWidget.height())*1.5 * len(self.kp_container))
        w.horizontalLayoutWidget.deleteLater()
        print(len(self.kp_container))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())