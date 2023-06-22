# Demo for customizing a QTableView, QHeaderView and table sorting with a QComboBox
# Includes how to sub-class QHeaderView, repain the header and styling
import sys
import copy
from PyQt6.QtCore import QAbstractTableModel, Qt, QAbstractItemModel, QSortFilterProxyModel
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QTableView, QApplication, QMainWindow, QHeaderView, QGridLayout, QWidget, QComboBox


class WindowHeaderView(QHeaderView):
    def __init__(self, orientation):
        self._orientation = orientation

        super().__init__(self._orientation)
        self.setSectionsMovable(True)
        self.setHighlightSections(True)
        self.setSectionsClickable(True)

        # For setting the customer header format, a dictionary will be used containing
        # {
        #     "column header text" : {
        #                             "color" : "value",
        #                             "index" : "value",
        #                            }
        # }
        self._columnDict = {}

    # This sets the column dictionary. I copy it incase the
    # original columnDict gets garbage collected
    def setColumnColors(self, columnDict):
        self._columnDict = copy.copy(columnDict)

    # Overriden
    def setModel(self, model):
        super().setModel(model)

    # Overridden
    # This is a very short custom painting routine for the header. This is where
    # all the work is done for painting the header. Basically, you are replacing
    # what the system does so... when you set the color, the cell won't have the
    # nice outset border, etc. All that has to be coded here. Luckily, the rect
    # is given to us for doing the work.
    def paintSection(self, painter, rect, logicalIndex):
        headertext = self.model().headerData(logicalIndex, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        try:
            self._index = self._columnDict[headertext]["index"]
            self._columncolor = self._columnDict[headertext]["color"]

            if self._orientation == Qt.Orientation.Horizontal and logicalIndex == self._index:
                # Custom painting
                painter.fillRect(rect, QColor(self._columncolor))
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, headertext)
                return
        except KeyError:
            self._index = -1
            super().paintSection(painter, rect, logicalIndex)

class WindowHeaderModel(QAbstractItemModel):
    def __init__(self):
        super().__init__()
        self._header = ""
    # Let us set the column headers using a list
    def setHeaderFromList(self, header):
        self._header = copy.copy(header)

    # Overriden
    # We can just set the headers... nothing special
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._header[section]

        if role == Qt.ItemDataRole.DisplayRole:
            return super().setHeaderData(section,orientation, role)

    # Overriden
    def setHeaderData(self, section, orientation, value, role=Qt.ItemDataRole.DisplayRole):

        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            self._header[section] = value
            self.headerDataChanged.emit(section, section)
            return True

        super().setHeaderData(self, section, orientation, value, role)
        self.headerDataChanged.emit(orientation, section, section)
        return True

    # Overridden
    def rowCount(self, index):
        return 1

    # Overridden
    def columnCount(self, index):
        return len(self._header)


class WindowTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return self._data[index.row()][index.column()]

        # This is a custom way to set a specific color for a cell value
        # This can easily be scoped to look a list of some type too
        # using a dictionary.
        if role == Qt.ItemDataRole.BackgroundRole:
            if self._data[index.row()][index.column()] > 7:
                return QColor('#DEF1BC')

    # Overridden
    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole:
            self._data[index.row()][index.column()] = value
            return True
        return False

    # Overridden
    def rowCount(self, index):
        return len(self._data)

    # Overridden
    def columnCount(self, index):
        return len(self._data[0])

    # Overridden
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemFlag.ItemIsEditable

        return super().flags(index) | Qt.ItemFlag.ItemIsEditable

    # This will give us the unique values for the combo box list
    def uniqueValues(self):
        values = set()
        thelist = []
        for i in range(self.rowCount(0)):
            for j in range(self.columnCount(0)):
                values.add(self._data[i][j])
        a=list(values)
        a.sort()
        a.insert(0, "All")
        for i in a:
            thelist.append(str(i))
        del values # let this be garbage collected
        return thelist

    # We can even let the model apply the filter
    # when we select from the combox
    def applyFilter(self, s, pmodel):
        if s == 'All':
            pmodel.setFilterWildcard('*')
        else:
            pmodel.setFilterFixedString(s)

if __name__ == '__main__':
    # Make the event loop for the application
    app = QApplication([])
    # Setup some data
    data = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
    ]

    # These are the models for the application
    # Even though there is a datamodel with the
    # data, we want to be able to sort and filter
    # and for that, we need an intermediate model.
    # The QSortFilterProxyModel is specifically
    # made for this.
    # First create the data model
    datamodel = WindowTableModel(data)

    # then create a proxy model and set the source
    # for the proxy model to the datamodel
    proxymodel = QSortFilterProxyModel()
    proxymodel.setSourceModel(datamodel)

    # Use our custom header class to setup the
    # header row so we can "draw" on it.
    headerview = WindowHeaderView(Qt.Orientation.Horizontal)
    headermodel = WindowHeaderModel()
    headermodel.setHeaderFromList(["A", "B", "C", "D", "E"])

    # The next couple of lines show the precedence of drawing
    # the headers. The stylesheet will be applied first and then
    # the custom header colors.
    headerview.setStyleSheet("::section {background-color: #F0F1BC;}")
    headerview.setColumnColors({
        "A": {
            "color": "#EDEDED",
            "index": 0
        },
        "D": {
            "color": "#FF0000",
            "index": 3
        },
    })
    # Set our "header list" to be the model
    headerview.setModel(headermodel)

    # Headers, Data and Models are setup ... let's
    # create a main window, a widget to hold our table
    # create the table and a combo box for filtering.
    mainwindow = QMainWindow()
    mainwidget = QWidget()
    tableview = QTableView()
    combobox = QComboBox()

    # Everything will be put on a 2 column
    # grid. The table will span columns 0 and 1
    # while the combo box will be in column 1 only.
    # Once our components are initialized, put them
    # on the layout
    layout = QGridLayout()
    layout.addWidget(combobox, 0, 1)
    layout.addWidget(tableview, 1, 0, 1, 2)

    # The table is created but it is blank.
    # We need to compose it a little by telling
    # it where the data is coming and if the
    # table can be sorted.
    tableview.setModel(proxymodel)
    tableview.setSortingEnabled(True)

    # Next, we will beautify it a little
    # by resizing the columns (header) to the
    # contents, applying our custom header
    # and establishing the sort order when the
    # table is initially drawn with data and
    # when we select "All" data in the combo box.
    tableview.setHorizontalHeader(headerview)
    tableview.resizeColumnsToContents()
    tableview.sortByColumn(0,Qt.SortOrder.AscendingOrder)

    # Add the unique data items to the combo box
    # and connect a listener to it
    combobox.addItems(datamodel.uniqueValues())
    combobox.currentTextChanged.connect(lambda s : datamodel.applyFilter(s, proxymodel))

    # Once the main widget has been composed,
    # put it in the main window
    mainwindow.setCentralWidget(mainwidget)

    # Finish up by sizing the main widget in
    # the main window. Then, show them
    mainwidget.setLayout(layout)
    mainwidget.resize(mainwidget.sizeHint())
    mainwindow.resize(mainwidget.sizeHint())
    mainwidget.show()
    mainwindow.show()

    # Enter the event loop
    sys.exit(app.exec())

