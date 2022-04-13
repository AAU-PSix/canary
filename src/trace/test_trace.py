import unittest

from decorators import LocalisedCFA
from src.decorators.location_decorator import LocalisedNode

from . import (
    TraceTreeBuilder,
)

class TestTrace(unittest.TestCase):
    def test_follow_1(self) -> None:
        builder = TraceTreeBuilder()
        builder.start_test("Test") \
            .start_unit("add") \
            .enter_location("0") \
            .end_unit() \
            .end_test()

        cfa_0 = LocalisedNode(None, "0")
        cfa = LocalisedCFA(cfa_0)

        trace = builder.build()
        path = [ *trace.follow("add", cfa) ]

        self.assertEqual(len(path), 1)
        self.assertEqual(path[0], cfa_0)

    def test_follow_2(self) -> None:
        #    0
        #    |
        #    0
        builder = TraceTreeBuilder()
        builder.start_test("Test") \
            .start_unit("add") \
            .enter_location("0") \
            .end_unit() \
            .end_test()

        cfa_0 = LocalisedNode(None, "0")
        cfa_1 = LocalisedNode(None, "0")
        cfa = LocalisedCFA(cfa_0)
        cfa.branch(cfa_0, cfa_1)

        trace = builder.build()
        path = [ *trace.follow("add", cfa) ]

        self.assertEqual(len(path), 2)
        self.assertEqual(path[0], cfa_0)
        self.assertEqual(path[1], cfa_1)

    def test_follow_3(self) -> None:
        #    0
        #    |
        #    0
        #    |
        #    0
        builder = TraceTreeBuilder()
        builder.start_test("Test") \
            .start_unit("add") \
            .enter_location("0") \
            .end_unit() \
            .end_test()

        cfa_0 = LocalisedNode(None, "0")
        cfa_1 = LocalisedNode(None, "0")
        cfa_2 = LocalisedNode(None, "0")
        cfa = LocalisedCFA(cfa_0)
        cfa.branch(cfa_0, cfa_1)
        cfa.branch(cfa_1, cfa_2)

        trace = builder.build()
        path = [ *trace.follow("add", cfa) ]

        self.assertEqual(len(path), 3)
        self.assertEqual(path[0], cfa_0)
        self.assertEqual(path[1], cfa_1)
        self.assertEqual(path[2], cfa_2)

    def test_follow_4(self) -> None:
        #    0
        #    |
        #    0
        #    |
        #    0
        #    |
        #    1
        builder = TraceTreeBuilder()
        builder.start_test("Test") \
            .start_unit("add") \
            .enter_location("0") \
            .end_unit() \
            .end_test()

        cfa_0 = LocalisedNode(None, "0")
        cfa_1 = LocalisedNode(None, "0")
        cfa_2 = LocalisedNode(None, "0")
        cfa_3 = LocalisedNode(None, "1")
        cfa = LocalisedCFA(cfa_0)
        cfa.branch(cfa_0, cfa_1)
        cfa.branch(cfa_1, cfa_2)
        cfa.branch(cfa_2, cfa_3)

        trace = builder.build()
        path = [ *trace.follow("add", cfa) ]

        self.assertEqual(len(path), 3)
        self.assertEqual(path[0], cfa_0)
        self.assertEqual(path[1], cfa_1)
        self.assertEqual(path[2], cfa_2)

    def test_follow_5(self) -> None:
        #    0
        #    |
        #    0
        #    |
        #    0
        #    |
        #    1
        builder = TraceTreeBuilder()
        builder.start_test("Test") \
            .start_unit("add") \
            .enter_location("0") \
            .enter_location("1") \
            .end_unit() \
            .end_test()

        cfa_0 = LocalisedNode(None, "0")
        cfa_1 = LocalisedNode(None, "0")
        cfa_2 = LocalisedNode(None, "0")
        cfa_3 = LocalisedNode(None, "1")
        cfa = LocalisedCFA(cfa_0)
        cfa.branch(cfa_0, cfa_1)
        cfa.branch(cfa_1, cfa_2)
        cfa.branch(cfa_2, cfa_3)

        trace = builder.build()
        path = [ *trace.follow("add", cfa) ]

        self.assertEqual(len(path), 4)
        self.assertEqual(path[0], cfa_0)
        self.assertEqual(path[1], cfa_1)
        self.assertEqual(path[2], cfa_2)
        self.assertEqual(path[3], cfa_3)

    def test_follow_6(self) -> None:
        #    0
        #    |
        #    0
        #   / \
        #  1   2
        builder = TraceTreeBuilder()
        builder.start_test("Test") \
            .start_unit("add") \
            .enter_location("0") \
            .enter_location("1") \
            .end_unit() \
            .end_test()

        cfa_0 = LocalisedNode(None, "0")
        cfa_1 = LocalisedNode(None, "0")
        cfa_2 = LocalisedNode(None, "1")
        cfa_3 = LocalisedNode(None, "2")
        cfa = LocalisedCFA(cfa_0)
        cfa.branch(cfa_0, cfa_1)
        cfa.branch(cfa_1, cfa_2)
        cfa.branch(cfa_1, cfa_3)

        trace = builder.build()
        path = [ *trace.follow("add", cfa) ]

        self.assertEqual(len(path), 3)
        self.assertEqual(path[0], cfa_0)
        self.assertEqual(path[1], cfa_1)
        self.assertEqual(path[2], cfa_2)