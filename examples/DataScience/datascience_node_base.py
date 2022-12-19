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
        super().drawingAssets()

        self.icons = QImage("icons/status_icons.png")

    # to draw the states of each node of the calculator nodes
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)

        # to determin the hight of the picture that we will take the status from
        offset = 24.0

        if self.node.isReady(): offset = 0.0

        # to detirmin the which picture we will take of the three picturs
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

    def __init__(self, scene, inputs=[1,1], outputs=[1,1]):
        super().__init__(scene, self.__class__.op_title, inputs, outputs)

        self.value = None

        # it's really important to mark all nodes Ready (Undefined = (Dirty) ) by default
        self.markReady()  # (markDirty)

    def nodeSettings(self):
        super().nodeSettings()
        self.input_socket_position = LEFT_CENTER
        self.output_socket_position = RIGHT_CENTER

    def initInnerClasses(self):
        self.content = DataScienceContent(self)
        self.grNode = DataScienceGraphicalNode(self)
