LISTBOX_MIMETYPE = "application/x-item"

OP_NODE_READ_CSV = 1
OP_NODE_SHOW_CSV = 2
OP_NODE_SHOW_HEAD_CSV = 3
OP_NODE_SHOW_TAIL_CSV = 4
OP_NODE_PRINT_OUTPUT = 5
OP_NODE_CALC_MEAN = 6
OP_NODE_CALC_STD = 7
OP_NODE_CALC_COUNT = 8
OP_NODE_FIND_MAX_MIN = 9
OP_NODE_CONCATENATE_CSV = 10
OP_NODE_DROP_NANS = 11
OP_NODE_DROP_COL_BY_NAME = 12
OP_NODE_DROP_ROW = 13
OP_NODE_SLICING_DATAFRAME = 14
OP_NODE_RENAME_COL = 15
OP_NODE_SORT_DF = 16
OP_NODE_SET_INDEX = 17
OP_NODE_GROUP_BY = 18
OP_NODE_DESCRIBE = 19
OP_NODE_DROP_DUPLICATE = 20
OP_NODE_MELT = 21
OP_NODE_DATA_VISUALIZATION = 60




DS_NODES = {
}

class ConfException(Exception): pass


class InvalidNodeRegistration(ConfException): pass


class OpCodeNotRegistered(ConfException): pass


def register_node_now(op_code, class_reference):
    if op_code in DS_NODES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" % (
            op_code, DS_NODES[op_code]
        ))
    DS_NODES[op_code] = class_reference


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class

    return decorator


def get_class_from_opcode(op_code):
    if op_code not in DS_NODES: raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return DS_NODES[op_code]


# import all nodes and register them
from examples.DataScience.nodes import *