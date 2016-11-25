import sys
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from PyQt4.QtCore import QTime, QTimer
from collections import deque
import time

class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        # PySide's QTime() initialiser fails miserably and dismisses args/kwargs
        #return [QTime().addMSecs(value).toString('mm:ss') for value in values]
        strns = []
        for value in values:
            timeArray = time.localtime(value)
            strns.append(time.strftime("%Y/%m/%d %H:%M:%S",timeArray))
        return strns

class MyApplication(QtGui.QApplication):
    def __init__(self, *args, **kwargs):
        super(MyApplication, self).__init__(*args, **kwargs)
        self.t = QTime()
        self.t.start()

        self.data = deque(maxlen=20)

        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.win.resize(1000,600)

        self.plot = self.win.addPlot(title='Timed data', axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.curve = self.plot.plot()

        self.tmr = QTimer()
        self.tmr.timeout.connect(self.update)
        self.tmr.start(1000)

    def update(self):
        self.data.append({'x': self.t.elapsed() + 1323587062, 'y': np.random.randint(0, 100)})
        x = [item['x'] for item in self.data]
        y = [item['y'] for item in self.data]
        self.curve.setData(x=x, y=y)

def main():
    app = MyApplication(sys.argv)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()