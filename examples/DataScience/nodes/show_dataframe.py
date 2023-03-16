import pandas as pd
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTableView, QHeaderView
from PyQt5.QtCore import Qt
from examples.DataScience.datascience_conf import register_node, OP_NODE_SHOW_CSV
from examples.DataScience.datascience_node_base import DataScienceNode, DataScienceGraphicalNode, DataScienceContent

from nodeeditor.base_system_properties.utils_no_qt import dumpException


class DataScienceGraphicalShow(DataScienceGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()

        self.width = 600
        self.height = 400
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

class DataScienceShowContent(DataScienceContent):

    def createContentWidget(self):

        self.table = QTableView(self)
        self.model = QStandardItemModel()

        # Create QTableView and set model
        self.table.setModel(self.model)

        self.table.horizontalHeader().setVisible(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.table.verticalHeader().setVisible(True)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.table.setEditTriggers(QTableView.NoEditTriggers)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)

        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.table.resize(600,375)


    def update_table(self, dataframe):
        # Read data from CSV file and create DataFrame
        df = pd.DataFrame(dataframe)

        # Clear current data in model
        self.model.clear()

        # set the index column and add the column headers to the model
        self.model.setColumnCount(df.shape[1])
        self.model.setRowCount(df.shape[0])

        # Set table properties
        self.model.setHorizontalHeaderLabels(df.columns)

        # Add data to model
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QStandardItem(str(df.iloc[i, j]))
                self.model.setItem(i, j, item)

        # # set the index column as row headers
        # index_column = df.index.tolist()
        # for row, item in enumerate(index_column):
        #     self.model.setVerticalHeaderItem(row, QStandardItem(str(item)))

        # self.model.setVerticalHeaderLabels(df.index.astype(str))

        # self.model.setVerticalHeaderLabels(list(map(str, df.index)))

        # header_labels = [str(label) for label in df.index]
        # self.model.setVerticalHeaderLabels(header_labels)

        # self.model.setVerticalHeaderLabels(df.index.map(lambda label: str(label)).tolist())

        # self.model.setVerticalHeaderLabels(df.index.values.astype(str).tolist())

        # self.model.setVerticalHeaderLabels(df.index)

        index_as_list = df.index.astype(str).tolist()
        self.model.setVerticalHeaderLabels(index_as_list)

@register_node(OP_NODE_SHOW_CSV)
class DataScienceNodeShow(DataScienceNode):
    icon = "icons/show.png"
    op_code = OP_NODE_SHOW_CSV
    op_title = "Show Full Data Frame"

    def __init__(self, scene):
        super().__init__(scene, inputs=[3], outputs=[])
        self.nodeEvaluation()

    def getInnerClasses(self):
        self.content = DataScienceShowContent(self)
        self.grNode = DataScienceGraphicalShow(self)

    def evaluationImplementation(self):

        input_socket = self.getInput(0)

        if input_socket is None:
            self.markReady()
            self.grNode.setToolTip("Input is not connected")
            return

        elif input_socket.value.empty:
            self.markInvalid()
            self.grNode.setToolTip("Empty Data Frame")

            self.markDescendantsInvalid()
            self.markDescendantsReady(False)

            return

        elif input_socket.value is not None:
            self.content.update_table(input_socket.value)
            self.grNode.setToolTip("")

            self.markInvalid(False)
            self.markReady(False)

            self.markDescendantsInvalid(False)
            self.markDescendantsReady()

            return

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        if finput_port is not None:
            # self.nodeEvaluation()  # eval() ely fo2 3ala tol de, to be evaluated automaticlly when all inputs are connected!!
            self.markReady()

        else:
            self.markInvalid()

