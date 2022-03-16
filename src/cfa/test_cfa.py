import unittest
from . import *

class TestCFA(unittest.TestCase):
    def test_outgoing(self) -> None:
        root: CFANode = CFANode(None)
        node_1: CFANode = CFANode(None)
        cfa: CFA = CFA(root)
        cfa.branch(root, node_1)
        outgoing: List[CFANode] = cfa.outgoing(root)
        self.assertEqual(len(outgoing), 1)
        self.assertEqual(outgoing[0], node_1)

    def test_ingoing(self) -> None:
        root: CFANode = CFANode(None)
        node_1: CFANode = CFANode(None)
        cfa: CFA = CFA(root)
        cfa.branch(root, node_1)
        ingoing: List[CFANode] = cfa.ingoing(node_1)
        self.assertEqual(len(ingoing), 1)
        self.assertEqual(ingoing[0], root)

    def test_remove(self) -> None:
        root: CFANode = CFANode(None)
        node_1: CFANode = CFANode(None)
        node_2: CFANode = CFANode(None)
        cfa: CFA = CFA(root)

        cfa.branch(root, node_1)
        cfa.branch(node_1, node_2)
        cfa.remove(node_1)

        ingoing: List[CFANode] = cfa.ingoing(node_2)
        self.assertEqual(len(ingoing), 1)
        self.assertTrue(root in ingoing)

        outgoing: List[CFANode] = cfa.outgoing(root)
        self.assertEqual(len(outgoing), 1)
        self.assertTrue(node_2 in outgoing)

    def test_replace(self) -> None:
        root: CFANode = CFANode(None)
        node_1: CFANode = CFANode(None)
        node_2: CFANode = CFANode(None)
        cfa: CFA = CFA(root)

        cfa.branch(root, node_1)
        cfa.replace(node_1, node_2)

        outgoing: List[CFANode] = cfa.outgoing(root)
        self.assertEqual(len(outgoing), 1)
        self.assertTrue(node_2 in outgoing)