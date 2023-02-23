from PyQt5.QtWidgets import QComboBox, QWidgetAction
#from Qt import QtWidgets
from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtCore import QDataStream, QIODevice, Qt
from qtpy.QtWidgets import QAction, QGraphicsProxyWidget, QMenu

from examples.DataScience.datascience_conf import DS_NODES, get_class_from_opcode, LISTBOX_MIMETYPE
from nodeeditor.base_system_properties.home_widget import NodeEditorWidget
from nodeeditor.base_edges.func_edge import EDGE_TYPE_DIRECT, EDGE_TYPE_BEZIER, EDGE_TYPE_SQUARE
from nodeeditor.base_system_properties.graphical_view import MODE_EDGE_DRAG
from nodeeditor.base_system_properties.utils_no_qt import dumpException
from nodeeditor.base_nodes.func_node import AllNodeFunctions

from examples.DataScience.datascience_drag_listbox import *
from examples.DataScience.datascience_node_base import DataScienceNode


DEBUG = False
DEBUG_CONTEXT = False


class DataScienceSubWindow(NodeEditorWidget):
    def __init__(self):
        super().__init__()
        # self.setAttribute(Qt.WA_DeleteOnClose)

        self.setTitle()

        self.initNewNodeActions()

        self.scene.addHasBeenModifiedListener(self.setTitle)
        self.scene.history.addHistoryRestoredListener(self.onHistoryRestored)
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)
        self.scene.setNodeClassSelector(self.getNodeClassFromData)

        self._close_event_listeners = []


    # def windowaction(self):
    #     sub = QtWidgets.QMdiSubWindow()
    #     Load_Input = LoadInput()
    #     sub.setWidget(Load_Input)
    #     sub.setObjectName("Load_Input_window")
    #     sub.setWindowTitle("Load Input")
    #     self.mdiArea.addSubWindow(sub)
    #     sub.show()


    def getNodeClassFromData(self, data):
        if 'op_code' not in data: return AllNodeFunctions
        return get_class_from_opcode(data['op_code'])

    def doEvalOutputs(self):
        # eval all output nodes
        for node in self.scene.nodes:
            # if node.__class__.__name__ == "CalcNode_Output":
                node.nodeEvaluation()

    def onHistoryRestored(self):
        self.doEvalOutputs()

    def fileLoad(self, filename):
        if super().fileLoad(filename):
            self.doEvalOutputs()
            return True

        return False

    def initNewNodeActions(self):
        self.node_actions = {}
        keys = list(DS_NODES.keys())
        keys.sort()
        for key in keys:
            node = DS_NODES[key]
            self.node_actions[node.op_code] = QAction(QIcon(node.icon), node.op_title)
            self.node_actions[node.op_code].setData(node.op_code)

    def setTitle(self):
        self.setWindowTitle(self.getUserFilenames())

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)

    def onDragEnter(self, event):
        # print("CalcSubWnd :: ~onDragEnter")
        # print("text: '%s'" % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            # print(" ... denied drag enter event")
            event.setAccepted(False)

    def onDrop(self, event):
        # print("CalcSubWnd :: ~onDrop")
        # print("text: '%s'" % event.mimeData().text())
        if event.mimeData().hasFormat(LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readInt()
            text = dataStream.readQString()

            mouse_position = event.pos()
            scene_position = self.scene.grScene.views()[0].mapToScene(mouse_position)

            if DEBUG: print("GOT DROP: [%d] '%s'" % (op_code, text), "mouse:", mouse_position, "scene:", scene_position)

            try:
                node = get_class_from_opcode(op_code)(self.scene)
                node.setPos(scene_position.x(), scene_position.y())
                self.scene.history.storeHistory("Created node %s" % node.__class__.__name__)
            except Exception as e:
                dumpException(e)

            event.setDropAction(Qt.MoveAction)
            event.accept()

            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            # print(" ... drop ignored, not requested format '%s'" % LISTBOX_MIMETYPE)
            event.ignore()

    def contextMenuEvent(self, event):
        try:
            item = self.scene.getItemAt(event.pos())
            if DEBUG_CONTEXT: print(item)

            if type(item) == QGraphicsProxyWidget:
                item = item.widget()

            if hasattr(item, 'node') or hasattr(item, 'socket'):
                self.nodeContextMenu(event)

            elif hasattr(item, 'edge'):
                self.edgeContextMenu(event)
            # elif item is None:
            else:  # THIS WILL SHOW THE CONTEXT OF ANY EMPTY SPACE AT SCENE
                self.emptySpaceContextMenu(event)

            return super().contextMenuEvent(event)

        except Exception as e:
            dumpException(e)

    def nodeContextMenu(self, event):
        if DEBUG_CONTEXT: print("CONTEXT: NODE")
        context_menu = QMenu(self)
        # readyAct = context_menu.addAction("State: Ready")  # Mark Dirty >> (READY)  WILL BE THE DEFUALT OF ANY NODE AT THE SCENE EXECPT THE NODES WITH WRONG (INVALID) INPUT TYPES

        # markDirtyDescendantsAct = context_menu.addAction("State: Mark Descendant Dirty")

        # validAct = context_menu.addAction("State: Valid")  # Unmarked Invalid >> Valid (we don't need it cuz when the node become invalid we can't make it valid by force becasue the output will be wrong

        # invalidAct = context_menu.addAction("State: Invalid")  # if user entered wrong inputs for the node >> WE DON"T NEED IT TO BE SHOWN IN NODE CONTEXT MENUE

        evaluatedAct = context_menu.addAction("State: Evaluated")

        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if type(item) == QGraphicsProxyWidget:
            item = item.widget()

        if hasattr(item, 'node'):
            selected = item.node
        if hasattr(item, 'socket'):
            selected = item.socket.node

        if DEBUG_CONTEXT: print("got item:", selected)

        # if selected and action == readyAct: selected.markReady()

        # if selected and action == markDirtyDescendantsAct: selected.markDescendantsDirty()

        # if selected and action == invalidAct: selected.markInvalid()

        # if selected and action == validAct: selected.markInvalid(False)

        if selected and action == evaluatedAct:
            val = selected.nodeEvaluation()

            if DEBUG_CONTEXT: print("EVALUATED:", val)

    def edgeContextMenu(self, event):
        if DEBUG_CONTEXT: print("CONTEXT: EDGE")
        context_menu = QMenu(self)
        bezierAct = context_menu.addAction("Bezier Edge")
        directAct = context_menu.addAction("Direct Edge")
        squareAct = context_menu.addAction("Square Edge")
        action = context_menu.exec(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if hasattr(item, 'edge'):
            selected = item.edge

        if selected and action == bezierAct: selected.edge_type = EDGE_TYPE_BEZIER
        if selected and action == directAct: selected.edge_type = EDGE_TYPE_DIRECT
        if selected and action == squareAct: selected.edge_type = EDGE_TYPE_SQUARE

    def emptySpaceContextMenu(self, event):  # CONTEXT OF ANY EMPTY SPACE AT SCENE TO CREATE NODES FROM EXCISTING

        if DEBUG_CONTEXT: print("CONTEXT: EMPTY SPACE")

        context_menu = self.showNodesMenu()

        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if action == self.runact:
            self.doEvalOutputs()

        if action is not None:
            new_calc_node = get_class_from_opcode(action.data())(self.scene)
            scene_pos = self.scene.getView().mapToScene(event.pos())
            new_calc_node.setPos(scene_pos.x(), scene_pos.y())
            if DEBUG_CONTEXT: print("Selected node:", new_calc_node)

            if self.scene.getView().mode == MODE_EDGE_DRAG:
                # if we were dragging an edge...
                target_socket = self.determine_target_socket_of_node(
                    self.scene.getView().dragging.drag_start_socket.is_output, new_calc_node)
                if target_socket is not None:
                    self.scene.getView().dragging.edgeDragEnd(target_socket.grSocket)
                    self.finish_new_node_state(new_calc_node)
            else:
                self.scene.history.storeHistory("Created %s" % new_calc_node.__class__.__name__)

    def showNodesMenu(self): # this method to show all the existing nodes that we have in our editor and categorizing it

        context_menu = QMenu(self)
        keys = list(DS_NODES.keys())
        keys.sort()

        # for INPUT AND OUTPUT NODES
        for key in keys:
            context_menu.addAction(self.node_actions[key])

        # # for INPUT AND CALCULATIONS NODES
        # calc = QMenu(context_menu)
        # calc.setTitle('Calculations')
        # context_menu.addMenu(calc)
        # for key in keys[2:6]: calc.addAction(self.node_actions[key])

        # # for INPUT AND LOGIC OPERATORS NODES
        # logic = QMenu(context_menu)
        # logic.setTitle('Logic Operations')
        # context_menu.addMenu(logic)
        # for key in keys[6:8]:
        #     logic.addAction(self.node_actions[key])

        context_menu.addSeparator()

        self.runact = context_menu.addAction("RUN ALL CELLS")

        return context_menu



    # helper functions
    def determine_target_socket_of_node(self, was_dragged_flag, new_calc_node):
        target_socket = None
        if was_dragged_flag:
            if len(new_calc_node.inputs) > 0: target_socket = new_calc_node.inputs[0]
        else:
            if len(new_calc_node.outputs) > 0: target_socket = new_calc_node.outputs[0]
        return target_socket

    def finish_new_node_state(self, new_calc_node):
        self.scene.doDeselectItems()
        new_calc_node.grNode.doSelect(True)
        new_calc_node.grNode.onSelected()