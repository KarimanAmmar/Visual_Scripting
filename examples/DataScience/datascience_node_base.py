import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPen, QBrush, QPainterPath
from qtpy.QtGui import QImage
from qtpy.QtCore import QRectF
from qtpy.QtWidgets import QLabel

from nodeeditor.base_nodes.func_node import AllNodeFunctions
from nodeeditor.base_nodes.func_content_widget import AllContentWidgetFunctions
from nodeeditor.base_nodes.graphical_node import DrawGraphicalNode
from nodeeditor.base_sockets.func_socket import LEFT_CENTER, RIGHT_CENTER
from nodeeditor.base_system_properties.utils_no_qt import dumpException


class DataScienceGraphicalNode(DrawGraphicalNode):
    def nodeSizes(self):
        super().nodeSizes()
        self.width = 160
        self.height = 74
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

class DataScienceContent(AllContentWidgetFunctions):
    def createContentWidget(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)

class DataScienceNode(AllNodeFunctions):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"

    GraphicsNode_class = DataScienceGraphicalNode
    NodeContent_class = DataScienceContent

    def __init__(self, scene, inputs=[3,3], outputs=[3]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)

        self.value = None

        # it's really important to mark all nodes Ready (Undefined = (Dirty) ) by default
        self.markReady()  # (markDirty)

    def nodeSettings(self):
        super().nodeSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def nodeEvaluation(self):  # eval >> which was inherted from  All Node Functions Class  = BASE NODE CLASS
        if not self.isReady() and not self.isInvalid():
            # print(" _> returning cached %s value:" % self.__class__.__name__, self.value)
            return self.value

        try:
            val = self.evaluationImplementation()
            return val

        except ValueError as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            self.markDescendantsInvalid()

        except Exception as e:
            self.markInvalid()
            self.grNode.setToolTip(str(e))
            dumpException(e)

    def evaluationImplementation(self):  # evalImplementation
        first_input = self.getInput(0)
        seconed_input = self.getInput(1)

        if first_input is None or seconed_input is None:
            self.markInvalid()
            self.markDescendantsInvalid()
            self.grNode.setToolTip("Please connect all inputs")

            return None

        else:
            val = self.evaluationOperation(first_input.nodeEvaluation(), seconed_input.nodeEvaluation())
            self.value = val

            # to paint the Evaluated State with the green sign
            self.markReady(False)
            self.markInvalid(False)

            self.grNode.setToolTip("")

            return val

    def evaluationOperation(self, input1, input2):  # evalOperation()

        data_frame = pd.DataFrame({})

        return data_frame

    def onInputChanged(self, socket=None):
        # print("%s::__onInputChanged" % self.__class__.__name__)
        self.markReady()
        # self.markInvalid()
        # self.nodeEvaluation()  # eval() ely fo2 3ala tol de, to be evaluated automaticlly when all inputs are connected!!

    def serialize(self):
        res = super().serialize()
        res['op_code'] = self.__class__.op_code
        return res

    def deserialize(self, data, hashmap={}, restore_id=True):
        res = super().deserialize(data, hashmap, restore_id)
        # print("Deserialized CalcNode '%s'" % self.__class__.__name__, "res:", res)
        return res