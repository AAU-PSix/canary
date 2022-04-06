import unittest
from typing import List

from symbol_table.tree import Tree
from symbol_table.node import Node, TNode

class TestTraceParser(unittest.TestCase):
    def test_parse_trace_single_unit(self) -> None:

        root_node = LocationNode(None, list(), 'AddTest', None, None)
        tree = Tree[LocationNode](root_node)

        node1 = LocationNode(None, list(), 'AddTest', 'unit1', 'loc1')

        node1._idStateList.append(('ida','state1'))
        node1._idStateList.append(('idb','state2'))


        root_node.children.append(node1)

        test_string = ['StartTest=AddTest','EndTest=AddTest']

        parser_trace = Parser_trace()
        #ParseTrace = parser_trace.parse_list(test_string)
        
        self.assertEqual(tree.root.testName, 'AddTest')
        #self.assertTrue(len(ParseTrace) != 0)
        #print(ParseTrace)


    # def test_parse_trace_two_units(self) -> None:
    #     root_node = LocationNode(None, list(), None, None)
    #     tree = Tree(root_node)

    #     node1 = LocationNode(None, list(), 'test1', 'unit1', 'loc1')
    #     node2 = LocationNode(None, list(), 'test1', 'unit2', 'loc2')
    #     node3 = LocationNode(None, list(), 'test1', 'unit1', 'loc3')

    #     node1.idStateList.append(('ida','state1'))
    #     node1.idStateList.append(('idb','state2'))

    #     node2.idStateList.append(('idc','state3'))
    #     node2.idStateList.append(('idd','state4'))
        
    #     node3.idStateList.append(('ide','state5'))
    #     node3.idStateList.append(('idf','state6'))

    #     root_node.children.append(node1)
    #     node1.siblings.append(node2)
    #     node2.children.append(node3)

    #     test_string = ['StartTest=AddTest', 'UnitStart=unit1', 'location=loc1', 'id=ida', 'state=state1', 'id=idb', 'state=state2', 
    #     'UnitStart=unit2', 'location=loc2', 'id=idc', 'state=state3', 'id=idd', 'state=state4', 'UnitEnd=unit2', 'EndTest=AddTest']

    #     parser_trace = Parser_trace()
        
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
        
        traceTreeList: List[Tree[LocationNode]] = []

        testNameStack: List[str] = []
        unitNameStack: List[str] = []
        testTreeStack: List[Tree[LocationNode]] = []
        locationNodeStack: List[LocationNode] = []
      
        prevTrace : str = ''
        idStateTuple = (None, None)
        
        for trace in trace_list:
            
            trace.split("=")

            if "StartTest" in trace[0]:
            
                rootNode = LocationNode(None, list(), trace[1] ,None, None)
                
                locationNodeStack.append(rootNode)
                testNameStack.append([trace[1]])
         
                tree = Tree[LocationNode](rootNode)
                testTreeStack.append(tree)

            if "EndTest" in trace[0]:
                # if trace[1] != testTreeStack[-1].root.unitName:
                #     raise Exception('Test has not been ended correctly')
                traceTreeList.append(testTreeStack[-1])
                testNameStack.pop()
                #locationStack = []

            # if "UnitStart" in trace[0] and trace[1] not in unitNameStack[-1]:
            #     unitNameStack.append(trace[1])
                
            # if "UnitEnd" in trace[0]:
            #     if trace[1] == unitNameStack[-1]:
            #         unitNameStack.pop()
            #     else:
            #         raise Exception('locationStack top element does not match with UnitEnd')                
            
            # if "location" in trace[0]:
                
            #     if locationNodeStack[-1] is None:
            #         raise Exception('Stack containing location nodes is empty')

            #     if trace[1] == locationNodeStack[-1].locationName:
            #         raise Exception('sequantial location are idential')

            #     locationNode = LocationNode(testNameStack[-1], unitNameStack[-1], trace[1])
            #     locationNodeStack.append(locationNode)

            #     if locationNode.unitName == unitNameStack:
            #         locationNodeStack[-1].siblings.append(locationNode)
            #     else:
            #         locationNodeStack[-1].children.append(locationNode)

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