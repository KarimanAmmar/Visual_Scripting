import pandas as pd
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QImage, QFont, QColor, QPen, QBrush, QPainterPath
from PyQt5.QtWidgets import QLabel, QPushButton, QComboBox

from examples.DataScience.datascience_conf import register_node, OP_NODE_SLICING_DATAFRAME
from examples.DataScience.datascience_node_base import DataScienceNode, DataScienceGraphicalNode, DataScienceContent
from nodeeditor.base_nodes.func_content_widget import AllContentWidgetFunctions


class DataScienceGraphicalSlicing(DataScienceGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 320
        self.height = 130
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10

    def drawingAssets(self):
        # super().drawingAssets()

        self.icons = QImage("icons/status_icons.png")

        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 10)

        self._color = QColor("#ef974d")
        self._color_selected = QColor("#F87217")
        self._color_hovered = QColor("#F87217")

        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(2.0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(2.0)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(3.0)

        self._brush_title = QBrush(QColor("#131922"))
        self._brush_background = QBrush(QColor("#1A202C"))

    # to draw the states of each node of the calculator nodes
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # super().paint(painter, QStyleOptionGraphicsItem, widget)

        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_roundness, self.edge_roundness)
        path_title.addRect(0, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        path_title.addRect(self.width - self.edge_roundness, self.title_height - self.edge_roundness, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())


        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(0, self.title_height, self.edge_roundness, self.edge_roundness)
        path_content.addRect(self.width - self.edge_roundness, self.title_height, self.edge_roundness, self.edge_roundness)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())


        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(-1, -1, self.width+2, self.height+2, self.edge_roundness, self.edge_roundness)
        painter.setBrush(Qt.NoBrush)
        if self.hovered:
            painter.setPen(self._pen_hovered)
            painter.drawPath(path_outline.simplified())
            painter.setPen(self._pen_default)
            painter.drawPath(path_outline.simplified())
        else:
            painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
            painter.drawPath(path_outline.simplified())


        # to determin the hight of the picture that we will take the status from
        offset = 24.0

        if self.node.isReady(): offset = 0.0

        #to detirmin the which picture we will take of the three picturs
        if self.node.isInvalid(): offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )

class DataScienceSlicingContent(DataScienceContent):

    def createContentWidget(self):

        self.data_frame = pd.DataFrame({})

        self.lbl = QLabel("Start Slicing From: ", self)
        self.lbl.move(5, 15)
        self.lbl.setStyleSheet("font: bold 13px;")

        self.lbl = QLabel("To: ", self)
        self.lbl.move(200, 15)
        self.lbl.setStyleSheet("font: bold 13px;")

        self.combobox1 = QComboBox(self)
        self.combobox1.move(10, 60)
        self.combobox1.resize(150, 28)
        self.combobox1.setStyleSheet("background-color: #5885AF;"
                                "border-radius: 10px;"
                                "font: bold 14px;"
                                 "padding: 6px;")
        # self.combobox1.setCurrentIndex(0)


        self.combobox2 = QComboBox(self)
        self.combobox2.move(170, 60)
        self.combobox2.resize(150, 28)
        self.combobox2.setStyleSheet("background-color: #5885AF;"
                                "border-radius: 10px;"
                                "font: bold 14px;"
                                 "padding: 6px;")
        # self.combobox2.setCurrentIndex(0)

        self.combobox1.currentIndexChanged.connect(self.printSelectedColumnsCombo1)
        self.combobox2.currentIndexChanged.connect(self.printSelectedColumnsCombo2)

    def printSelectedColumnsCombo1(self):
        column1 = self.combobox1.currentText()
        return column1

    def printSelectedColumnsCombo2(self):
        column2 = self.combobox2.currentText()
        return column2



@register_node(OP_NODE_SLICING_DATAFRAME)
class DataScienceNodeSlice(DataScienceNode):
    # icon = "icons/in.png"
    op_code = OP_NODE_SLICING_DATAFRAME
    op_title = "Slicing Dataframe"
    content_label = "SD"

    def __init__(self, scene, inputs=[3], outputs=[3]):
        super().__init__(scene, inputs, outputs)

    def getInnerClasses(self):
        self.content = DataScienceSlicingContent(self)
        self.grNode = DataScienceGraphicalSlicing(self)

    def evaluationImplementation(self):
        super().evaluationImplementation()
        first_input = self.getInput(0)

        if first_input is None:
            self.markInvalid()
            self.markDescendantsInvalid()
            self.grNode.setToolTip("Please connect all inputs")

            return None

        else:
            val = self.evaluationOperation(first_input.nodeEvaluation())
            self.value = val

            # to paint the Evaluated State with the green sign
            # self.markReady(False)
            # self.markInvalid(False)

            self.grNode.setToolTip("")

            return val

    def onInputChanged(self, socket=None):
        finput_port = self.getInput(0)
        foutput_port = self.getOutputs(0)
        self.content.combobox1.clear()
        self.content.combobox2.clear()


        if finput_port and foutput_port is not None:
            self.nodeEvaluation()

        elif finput_port or foutput_port is None:
            self.markInvalid()

        elif finput_port and foutput_port is None:
            self.markReady()

    def evaluationOperation(self, input1, **kwargs):

        dataframe = pd.DataFrame(input1)

        for col in dataframe.columns:

            self.content.combobox1.addItem(col)
            self.content.combobox2.addItem(col)


        df_col = dataframe.columns

        index1 = df_col.get_loc(self.content.printSelectedColumnsCombo1())
        index2 = df_col.get_loc(self.content.printSelectedColumnsCombo2())

        print(self.content.printSelectedColumnsCombo1())
        print(self.content.printSelectedColumnsCombo2())


        print('selected columns: ', self.content.printSelectedColumnsCombo1(),'at index: ',index1, self.content.printSelectedColumnsCombo2(),'at index: ',index2)

        df_subset = dataframe.iloc[:,index1:index2 + 1]
        # df_str = df_subset.to_string()


        return df_subset