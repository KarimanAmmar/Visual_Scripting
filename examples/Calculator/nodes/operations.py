from examples.Calculator.calc_conf import register_node, OP_NODE_GREATER, OP_NODE_EQUAL, OP_NODE_LESS, OP_NODE_ADD, \
    OP_NODE_SUB, OP_NODE_MUL, OP_NODE_DIV
from examples.Calculator.calc_node_base import CalcNode


@register_node(OP_NODE_ADD)
class CalcNode_Add(CalcNode):
    icon = "icons/add.png"
    op_code = OP_NODE_ADD
    op_title = "Add"
    content_label = "+"
    content_label_objname = "calc_node_bg"

    def evalOperation(self, input1, input2):
        return input1 + input2


@register_node(OP_NODE_SUB)
class CalcNode_Sub(CalcNode):
    icon = "icons/sub.png"
    op_code = OP_NODE_SUB
    op_title = "Substract"
    content_label = "-"
    content_label_objname = "calc_node_bg"

    def evalOperation(self, input1, input2):
        return input1 - input2


@register_node(OP_NODE_MUL)
class CalcNode_Mul(CalcNode):
    icon = "icons/mul.png"
    op_code = OP_NODE_MUL
    op_title = "Multiply"
    content_label = "*"
    content_label_objname = "calc_node_mul"

    def evalOperation(self, input1, input2):
        print('foo')
        return input1 * input2


@register_node(OP_NODE_DIV)
class CalcNode_Div(CalcNode):
    icon = "icons/divide.png"
    op_code = OP_NODE_DIV
    op_title = "Divide"
    content_label = "/"
    content_label_objname = "calc_node_div"

    def evalOperation(self, input1, input2):
        return input1 / input2


@register_node(OP_NODE_GREATER)
class CalcNode_Greater(CalcNode):
    icon = "icons/grater_than.png"
    op_code = OP_NODE_GREATER
    op_title = "Greater Than"
    content_label = ">"

    # content_label_objname = "calc_node_gt"

    def evalOperation(self, input1, input2):
        if input1 > input2:
            return input1
        elif input2 > input1:
            return input2


@register_node(OP_NODE_LESS)
class CalcNode_Greater(CalcNode):
    icon = "icons/less_than.png"
    op_code = OP_NODE_GREATER
    op_title = "Less Than"
    content_label = "<"

    # content_label_objname = "calc_node_gt"

    def evalOperation(self, input1, input2):
        if input1 < input2:
            return input1
        elif input2 < input1:
            return input2


@register_node(OP_NODE_EQUAL)
class CalcNode_Equal(CalcNode):
    icon = "icons/equal.png"
    op_code = OP_NODE_EQUAL
    op_title = "Equal"
    content_label = "="

    # content_label_objname = "calc_node_gt"

    def evalOperation(self, input1, input2):
        self.resultT = 'True'
        self.resultF = 'False'

        if input1 == input2:
            return self.resultT
        else:
            return self.resultF

# way how to register by function call
# register_node_now(OP_NODE_ADD, CalcNode_Add)
