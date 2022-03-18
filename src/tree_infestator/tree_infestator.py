from ast import Raise
from src.ts import language_library
from src.ts.language_library import Language
from ts import Parser, Tree
from unit_analyser import UnitAnalyser
from cfa import CFA, CFANode, CFAEdge

class TreeInfestator:
    def __init__(self,  cfa:CFA, language:Language):
        if cfa is None:
            raise Exception("CFA Constructor argument is None.")
        if language is None:
            raise Exception("ØV")
        self.cfa = cfa
        self.language = language
        self.sought_nodes : list(CFANode) = []
        self._find_nests()
        


    def _find_nests(self):
        cfa = self.cfa
        def sortFrom(node:CFANode):
            return node.node.end_point.line
        for node in self.cfa.breadth_first_traverse(): 
            if node.node.type == self.language.syntax.get_if_query:
                self.sought_nodes.insert(node)
        self.sought_nodes.sort(key=sortFrom, reverse=True)