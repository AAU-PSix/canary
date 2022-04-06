import unittest
from typing import List

from numpy import test
from symbol_table.tree import Tree, Node, TNode


class TestTraceParser(unittest.TestCase):
    def test_parse_trace_single_unit(self) -> None:

        root_node = LocationNode(None, list(), 'AddTest', None, None)
        tree = Tree[LocationNode](root_node)
    
        node1 = LocationNode(None, list(), 'AddTest', 'unit1', 'loc1')
        node2 = LocationNode(None, list(), 'AddTest', 'unit1', 'loc2')

        node1._idStateList.append(('ida','state1'))
        node2._idStateList.append(('idb','state2'))

        root_node.children.append(node1)
        root_node.children.append(node2)
        root_node.children[-1].children.append(node1)
        #print(root_node.children[-1].unitName)
        #print(root_node.children[-1].child_count)

        test_string = ['StartTest=AddTest', 'UnitStart=newUnit', 'location=a1', 'location=a2', 'UnitEnd=newUnit', 'EndTest=AddTest']

        parser_trace = Parser_trace()
        ParseTrace = parser_trace.parse_list(test_string)
        
        self.assertEqual(tree.root.testName, 'AddTest')
        self.assertTrue(len(ParseTrace) != 0)
        #print(tree.root.child_count)
        #print(tree.root.children[0])
        #print(ParseTrace[0].root.child_count)
        #print(ParseTrace[0].root.sibling_count)
        print(ParseTrace[0].root.children[0].sibling_count)
        print(node1.sibling_count)

class LocationNode(Node):
    def __init__(self, parent: TNode, children: List[TNode], testName: str, unitName: str = None, locationName: str = None, ) -> None:
        super().__init__(parent, children)
        self._testName = testName
        self._unitName = unitName
        self._locationName = locationName
        self._idStateList : List[tuple] = []
    
    @property
    def testName(self) -> str:
        return self._testName
    
    @property
    def unitName(self) -> str:
        return self._unitName
    
    @property
    def locationName(self) -> str:
        return self._locationName

    @property
    def idStateList(self) -> List[tuple]:
        return self._idStateList

class Parser_trace():
    def __init__(self) -> None:
        pass  
    
    def parse_list(self, trace_list: List[str]) -> List[Tree[LocationNode]]:
        
        #return list
        traceTreeList: List[Tree[LocationNode]] = []

        testTreeStack: List[Tree[LocationNode]] = []

        testNameStack: List[str] = []
        unitNameStack: List[str] = []

        treeRootNodeStack: List[LocationNode] = []
        locationNodeStack: List[LocationNode] = []
    
        prevTrace : str = ''
        idStateTuple = (None, None)
        
        for trace in trace_list:
            
            trace = trace.split("=")

            if "StartTest" in trace[0]:
            
                rootNode = LocationNode(None, list(), trace[1] ,None, None)

                testNameStack.append(trace[1])       

                treeRootNodeStack.append(rootNode)

                #testTreeStack.append(tree)

            if "EndTest" in trace[0]:
                if trace[1] != testNameStack[-1]:
                    raise Exception('Test has not been ended correctly')

                tree = Tree[LocationNode](treeRootNodeStack[-1])
                tree.root.children.append(locationNodeStack[-1])

                testNameStack.pop()
                #traceTreeList[-1].root.children.append()
                traceTreeList.append(tree)
                #locationStack = []

            if "location" in trace[0]:
                
                if testNameStack[-1] is None:
                    raise Exception('top element in testNameStack is None')

                if unitNameStack[-1] is None:
                    raise Exception('top element in unitNameStack is None')

                if trace[1] is None:
                    raise Exception('value from trace is None')  

                newlocationNode = LocationNode(None, list(), testNameStack[-1], unitNameStack[-1], trace[1])
                
                locationNodeStack.append(newlocationNode)

                if newlocationNode.unitName != unitNameStack[-1]:
                    locationNodeStack[-1].children.append(newlocationNode)
                else:
                    locationNodeStack[-1].siblings.append(newlocationNode)

            if "UnitStart" in trace[0]:
                unitNameStack.append(trace[1])
                
            if "UnitEnd" in trace[0]:
                if trace[1] == unitNameStack[-1]:
                    unitNameStack.pop()
                else:
                    raise Exception('locationStack top element does not match with UnitEnd')                
            
            # if "id" in trace[0]:
            #     if not idStateTuple:
            #         raise Exception('Id_state tuple is not empty!')

            #     prevTrace = 'id'
            #     idStateTuple[0] = trace[1]
                
            # if "state" in trace[0]:
            #     if idStateTuple[0] is None:
            #         raise Exception('id in id_state tuple is None')
            #     if idStateTuple[1] is not None:
            #         raise Exception('state in id_state tuple is not None!')

            #     if prevTrace != "id":
            #         raise Exception('previous trace was not an id!')
                
            #     if trace[1] in locationStack[-1].idStateList:
            #         [x for x, y in enumerate(locationStack[-1].idStateList) if y[0] == idStateTuple[0]]
            #         [trace[1]]

            #     idStateTuple[1] = trace[1]
            #     prevTrace = ""
            #     locationNodeStack[-1].idStateList.append(idStateTuple)
            #     idStateTuple = (None, None)

        return traceTreeList