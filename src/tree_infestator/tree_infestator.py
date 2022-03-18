from ast import Raise
import imp
from ts import language_library
from ts.language_library import Language
from ts import Parser, Tree
from unit_analyser import UnitAnalyser
from cfa import CFA, CFANode, CFAEdge
from typing import List

class TreeInfestator:
    def __init__(self,  cfa:CFA, parser : Parser):
        if cfa is None:
            raise Exception("CFA Constructor argument is None.")
        if parser is None:
            raise Exception("ØV")
        self.cfa = cfa
        self.language = parser.language
        self.parser = parser
        self.found_nodes : List[CFANode] = []
        self._find_nests()
        


    def _find_nests(self):
        cfa = self.cfa
        def sortFrom(node:CFANode):
            return node.node.start_point.line

        
        for node in self.cfa.breadth_first_traverse(): 
            if node.node is not None:
                if node.node.type == "parenthesized_expression":
                    self.found_nodes.insert(0,node)
        self.found_nodes.sort(key=sortFrom, reverse=True)

    def infest_tree(self, tree : Tree) -> Tree:
        for node in self.found_nodes:
            sib = node.node.next_sibling
            t = self.parser.append(tree, sib.children[0],"TWEET();")
        print(t.text)
        return t
        #t = self.parser.parse(tree.text, tree)


            