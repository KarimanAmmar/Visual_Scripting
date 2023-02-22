import pandas as pd
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QPushButton, QFileDialog, QLabel, QTableWidget, QTableWidgetItem, QTableView, QHeaderView
from qtpy.QtCore import Qt
from examples.DataScience.datascience_conf import register_node, OP_NODE_SHOW_CSV
from examples.DataScience.datascience_node_base import DataScienceNode, DataScienceGraphicalNode

from nodeeditor.base_nodes.func_content_widget import AllContentWidgetFunctions
from nodeeditor.base_system_properties.utils_no_qt import dumpException


class DataScienceGraphicalOUTPUT(DataScienceGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 600
        self.height = 400
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10


class DataScienceOUTPUTContent(AllContentWidgetFunctions):
    def createContentWidget(self):
        self.edit = QLabel()

        df = pd.DataFrame({})

        self.model = QStandardItemModel(df.shape[0], df.shape[1])

        # Set horizontal header labels
        self.model.setHorizontalHeaderLabels(df.columns)

        # Add data to QStandardItemModel
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[i, j]))
                self.model.setItem(i, j, item)

        # Create QTableView and set model
        table = QTableView(self)
        table.setModel(self.model)

        # Set table properties
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)

        # table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # table.verticalHeader().setDefaultSectionSize(50)

        table.setEditTriggers(QTableView.NoEditTriggers)
        table.setSelectionBehavior(QTableView.SelectRows)
        table.setSelectionMode(QTableView.SingleSelection)

        table.setWordWrap(True)
        table.setShowGrid(False)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        table.resize(599,399)



    def drawTable(self,df):
        # table_widget = QTableWidget(self)
        # table_widget.setRowCount(dataframe.shape[0])
        # table_widget.setColumnCount(dataframe.shape[1])
        # table_widget.setHorizontalHeaderLabels(list(dataframe.columns))
        # table_widget.resize(900, 1200)
        # # table_widget.setWordWrap(True)
        # # table_widget.showMaximized()
        #
        # # # Populate the table widget with data from the data frame
        # for row in range(dataframe.shape[0]):
        #     for col in range(dataframe.shape[1]):
        #         item = QTableWidgetItem(str(dataframe.iloc[row, col]))
        #         table_widget.setItem(row, col, item)

        # Create QStandardItemModel
        model = QStandardItemModel(df.shape[0], df.shape[1])

        # Set horizontal header labels
        model.setHorizontalHeaderLabels(df.columns)

        # Add data to QStandardItemModel
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[i, j]))
                model.setItem(i, j, item)

        # Create QTableView and set model
        table = QTableView(self)
        table.setModel(model)

        # Set table properties
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableView.NoEditTriggers)
        table.setSelectionBehavior(QTableView.SelectRows)
        table.setSelectionMode(QTableView.SingleSelection)


    def update_table(self, dataframe):
        # Read data from CSV file and create DataFrame
        df = pd.DataFrame(dataframe)

        # Clear current data in model
        self.model.clear()

        # Set horizontal header labels
        self.model.setHorizontalHeaderLabels(df.columns)

        # Add data to model
        for i in range(df.shape[0]):
            row_items = []
            for j in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[i, j]))
                row_items.append(item)
            self.model.appendRow(row_items)

    def serialize(self):
        res = super().serialize()
        res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_SHOW_CSV)
class DataScienceNodeOUTPUT(DataScienceNode):
    icon = "icons/out.png"
    op_code = OP_NODE_SHOW_CSV
    op_title = "Show The Data Frame"
    content_label_objname = "calc_node_output"

    def __init__(self, scene):
        super().__init__(scene, inputs=[3], outputs=[])
        self.nodeEvaluation()  # eval() from the calculator node base

    def getInnerClasses(self):
        self.content = DataScienceOUTPUTContent(self)
        self.grNode = DataScienceGraphicalOUTPUT(self)

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        if finput_port is not None:
            self.nodeEvaluation()  # eval() ely fo2 3ala tol de, to be evaluated automaticlly when all inputs are connected!!

        else:
            self.markReady(True)

    def evaluationImplementation(self):
        # self.markReady(True)

        input_socket = self.getInput(0)

        # val = input_socket.nodeEvaluation()

        # if not input_socket:
        #     self.grNode.setToolTip("Input is not connected")
        #     self.markReady()
        #     return
        #
        # val = input_socket.nodeEvaluation()
        #
        # if val is None:
        #     self.grNode.setToolTip("Input is NaN")
        #     self.markInvalid()
        #     return

        # if val:
        # val = self.content.df
        # self.content.df = val

        # print(val)

        # self.content.drawTable(val)

        # self.content.drawTable(val)

        print("evaluated part ")

        print(input_socket.content.data_frame)

        dn = pd.DataFrame(input_socket.content.data_frame)

        # self.content.drawTable(dn)

        self.content.update_table(dn)

        # print(self.content.df)


        # self.content.drawTable(self.content.df)
        # self.content.lbl.setText(f"{val}")
        # self.markInvalid(False)
        # self.markReady(False)
        # self.grNode.setToolTip("")

        # elif not int(val):
        #     self.content.lbl.setText(f"{val}")
        #     self.markInvalid(False)
        #     self.markReady(False)
        #     self.grNode.setToolTip("")

        # return val
