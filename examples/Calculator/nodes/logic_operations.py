from examples.Calculator.calc_conf import register_node, OP_NODE_GREATER, OP_NODE_EQUAL, OP_NODE_LESS
from examples.Calculator.calc_node_base import CalcNode

@register_node(OP_NODE_GREATER)
class CalcNode_Greater(CalcNode):
    icon = "icons/grater_than.png"
    op_code = OP_NODE_GREATER
    op_title = "Greater Than"
    content_label = ">"

    def evaluationOperation(self, input1, input2):
        self.resultF = 'False'
        if input1 > input2:
            return input1
        elif input2 > input1:
            return input2
        elif input1 == input2:
            return input1


@register_node(OP_NODE_LESS)
class CalcNode_Less(CalcNode):
    icon = "icons/less_than.png"
    op_code = OP_NODE_LESS
    op_title = "Less Than"
    content_label = "<"

    def evaluationOperation(self, input1, input2):
        self.resultF = 'False'
        if input1 < input2:
            return input1
        elif input2 < input1:
            return input2
        elif input1 == input2:
            return input1


@register_node(OP_NODE_EQUAL)
class CalcNode_Equal(CalcNode):
    icon = "icons/equal.png"
    op_code = OP_NODE_EQUAL
    op_title = "Equal"
    content_label = "="

    def evaluationOperation(self, input1, input2):

        if input1 == input2:
            return input1
        else:
            return 0