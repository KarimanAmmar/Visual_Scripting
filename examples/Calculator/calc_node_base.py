from qtpy.QtGui import QImage
from qtpy.QtCore import QRectF
from qtpy.QtWidgets import QLabel

from nodeeditor.base_nodes.func_node import AllNodeFunctions
from nodeeditor.base_nodes.func_content_widget import AllContentWidgetFunctions
from nodeeditor.base_nodes.graphical_node import DrawGraphicalNode
from nodeeditor.base_sockets.func_socket import LEFT_CENTER, RIGHT_CENTER
from nodeeditor.base_system_properties.utils_no_qt import dumpException


class CalcGraphicsNode(DrawGraphicalNode):
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

        #to detirmin the which picture we will take of the three picturs
        if self.node.isInvalid(): offset = 48.0

        painter.drawImage(
            QRectF(-10, -10, 24.0, 24.0),
            self.icons,
            QRectF(offset, 0, 24.0, 24.0)
        )
class CalcContent(AllContentWidgetFunctions):
    def createContentWidget(self):
        lbl = QLabel(self.node.content_label, self)
        lbl.setObjectName(self.node.content_label_objname)

class CalcNode(AllNodeFunctions):
    icon = ""
    op_code = 0
    op_title = "Undefined"
    content_label = ""
    content_label_objname = "calc_node_bg"

    GraphicsNode_class = CalcGraphicsNode
    NodeContent_class = CalcContent

    def __init__(self, scene, inputs=[4,4], outputs=[4]):
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
            print(" _> returning cached %s value:" % self.__class__.__name__, self.value)
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
        return 123

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