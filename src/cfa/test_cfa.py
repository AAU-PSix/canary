from unittest import TestCase
from . import *

class TestCFA(TestCase):
    def test_outgoing(self) -> None:
        root: CFANode = CFANode(None)
        node_1: CFANode = CFANode(None)
        cfa: CFA[CFANode] = CFA(root)
        cfa.branch(root, node_1)
        outgoing: List[CFANode] = cfa.outgoing(root)
        self.assertEqual(len(outgoing), 1)
        self.assertEqual(outgoing[0], node_1)

    def test_ingoing(self) -> None:
        root: CFANode = CFANode(None)
        node_1: CFANode = CFANode(None)
        cfa: CFA[CFANode] = CFA(root)
        cfa.branch(root, node_1)
        ingoing: List[CFANode] = cfa.ingoing(node_1)
        self.assertEqual(len(ingoing), 1)
        self.assertEqual(ingoing[0], root)

    def test_remove(self) -> None:
        root: CFANode = CFANode(None)
        node_1: CFANode = CFANode(None)
        node_2: CFANode = CFANode(None)
        cfa: CFA[CFANode] = CFA(root)

        cfa.branch(root, node_1)
        cfa.branch(node_1, node_2)
        cfa.remove(node_1)

        ingoing: List[CFANode] = cfa.ingoing(node_2)
        self.assertEqual(len(ingoing), 1)
        self.assertTrue(root in ingoing)

        outgoing: List[CFANode] = cfa.outgoing(root)
        self.assertEqual(len(outgoing), 1)
        self.assertTrue(node_2 in outgoing)

        self.assertFalse(node_1 in cfa._ingoing_edges)
        self.assertFalse(node_1 in cfa._outgoing_edges)
        
        for node in cfa._ingoing_edges:
            for edge in cfa._ingoing_edges[node]:
                self.assertFalse(node_1 is edge.source)
                self.assertFalse(node_1 is edge.destination)
        
        for node in cfa._outgoing_edges:
            for edge in cfa._outgoing_edges[node]:
                self.assertFalse(node_1 is edge.source)
                self.assertFalse(node_1 is edge.destination)

    def test_remove_last(self) -> None:
        root: CFANode = CFANode(None)
        node_1: CFANode = CFANode(None)
        node_2: CFANode = CFANode(None)
        cfa: CFA[CFANode] = CFA(root)

        cfa.branch(root, node_1)
        cfa.branch(node_1, node_2)
        cfa.remove(node_2)

        outgoing: List[CFANode] = cfa.outgoing(node_1)
        self.assertEqual(len(outgoing), 0)

        self.assertFalse(node_2 in cfa._ingoing_edges)
        self.assertFalse(node_2 in cfa._outgoing_edges)
        
        for node in cfa._ingoing_edges:
            for edge in cfa._ingoing_edges[node]:
                self.assertFalse(node_2 is edge.source)
                self.assertFalse(node_2 is edge.destination)
        
        for node in cfa._outgoing_edges:
            for edge in cfa._outgoing_edges[node]:
                self.assertFalse(node_2 is edge.source)
                self.assertFalse(node_2 is edge.destination)

    def test_remove_center(self) -> None:
        node_0: CFANode = CFANode(None)
        node_1: CFANode = CFANode(None)

        node_2: CFANode = CFANode(None)

        node_3: CFANode = CFANode(None)
        node_4: CFANode = CFANode(None)

        cfa: CFA[CFANode] = CFA(node_2)

        cfa.branch(node_0, node_2)
        cfa.branch(node_1, node_2)
        cfa.branch(node_2, node_3)
        cfa.branch(node_2, node_4)
        cfa.remove(node_2)

        node_0_outgoing: List[CFANode] = cfa.outgoing(node_0)
        self.assertTrue(node_0 not in node_0_outgoing)
        self.assertTrue(node_1 not in node_0_outgoing)
        self.assertTrue(node_2 not in node_0_outgoing)
        self.assertTrue(node_3 in node_0_outgoing)
        self.assertTrue(node_4 in node_0_outgoing)
        self.assertEqual(len(node_0_outgoing), 2)
        node_0_ingoing: List[CFANode] = cfa.ingoing(node_0)
        self.assertEqual(len(node_0_ingoing), 0)

        node_1_outgoing: List[CFANode] = cfa.outgoing(node_1)
        self.assertFalse(node_0 in node_1_outgoing)
        self.assertFalse(node_1 in node_1_outgoing)
        self.assertFalse(node_2 in node_1_outgoing)
        self.assertTrue(node_3 in node_1_outgoing)
        self.assertTrue(node_4 in node_1_outgoing)
        self.assertEqual(len(node_1_outgoing), 2)
        node_1_ingoing: List[CFANode] = cfa.ingoing(node_1)
        self.assertEqual(len(node_1_ingoing), 0)

        node_3_outgoing: List[CFANode] = cfa.outgoing(node_3)
        self.assertEqual(len(node_3_outgoing), 0)
        node_3_ingoing: List[CFANode] = cfa.ingoing(node_3)
        self.assertEqual(len(node_3_ingoing), 2)
        self.assertTrue(node_0 in node_3_ingoing)
        self.assertTrue(node_1 in node_3_ingoing)

        node_4_outgoing: List[CFANode] = cfa.outgoing(node_4)
        self.assertEqual(len(node_4_outgoing), 0)
        node_4_ingoing: List[CFANode] = cfa.ingoing(node_4)
        self.assertEqual(len(node_4_ingoing), 2)
        self.assertTrue(node_0 in node_4_ingoing)
        self.assertTrue(node_1 in node_4_ingoing)

    def test_replace(self) -> None:
        root: CFANode = CFANode(None)
        node_1: CFANode = CFANode(None)
        node_2: CFANode = CFANode(None)
        cfa: CFA[CFANode] = CFA(root)

        cfa.branch(root, node_1)
        cfa.replace(node_1, node_2)

        outgoing: List[CFANode] = cfa.outgoing(root)
        self.assertEqual(len(outgoing), 1)
        self.assertTrue(node_2 in outgoing)