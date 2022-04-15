import unittest

from . import (
    TraceParser,
    TraceTreeBuilder,
    Location
)

class TestTraceParser(unittest.TestCase):
    def test_trace_tree_builder_empty_test_trace(self) -> None:
        builder = TraceTreeBuilder()

        builder \
            .start_test("Tommy") \
            .end_test() \
            .build()

        self.assertIsNone(builder.current_unit)
        self.assertEqual(builder.current_depth, 0)
        self.assertIsNotNone(builder.current_test)
        self.assertEqual(builder.current_test.name, "Tommy")

    def test_trace_tree_builder_single_unit_test_trace(self) -> None:
        builder = TraceTreeBuilder()

        builder \
            .start_test("Andreas") \
            .start_unit("Tommy")

        self.assertEqual(builder.current_test.name, "Andreas")
        self.assertEqual(builder.current_depth, 1)
        self.assertEqual(builder.current_unit.name, "Tommy")

    def test_trace_tree_builder_two_unit_test_trace(self) -> None:
        builder = TraceTreeBuilder()

        builder \
            .start_test("Andreas") \
            .start_unit("Tommy") \
            .start_unit("Magnus") \
            .end_unit()

        self.assertEqual(builder.current_test.name, "Andreas")
        self.assertEqual(builder.current_depth, 1)
        self.assertEqual(builder.current_unit.name, "Tommy")

    def test_trace_tree_builder_single_unit_single_location_test_trace(self) -> None:
        builder = TraceTreeBuilder()

        trace = builder \
            .start_test("Andreas") \
            .start_unit("Tommy") \
            .enter_location("1") \
            .end_unit() \
            .end_test() \
            .build()

        sequence = [ *trace.sequence ]

        self.assertEqual(len(sequence), 1)

        location_1: Location = sequence[0]
        self.assertIsInstance(location_1, Location)
        self.assertEqual(location_1.test.name, "Andreas")
        self.assertEqual(location_1.unit.name, "Tommy")
        self.assertEqual(location_1.id, "1")

    def test_trace_tree_builder_two_units_two_locations_test_trace(self) -> None:
        builder = TraceTreeBuilder()

        trace = builder \
            .start_test("Andreas") \
            .start_unit("Tommy1") \
            .enter_location("1") \
                .start_unit("Tommy2") \
                .enter_location("2") \
                .end_unit() \
            .end_unit() \
            .end_test() \
            .build()

        sequence = [ *trace.sequence ]

        self.assertEqual(len(sequence), 2)

        location_1: Location = sequence[0]
        self.assertEqual(location_1.test.name, "Andreas")
        self.assertEqual(location_1.unit.name, "Tommy1")
        self.assertEqual(location_1.id, "1")

        location_2: Location = sequence[1]
        self.assertEqual(location_2.test.name, "Andreas")
        self.assertEqual(location_2.unit.name, "Tommy2")
        self.assertEqual(location_2.id, "2")
        
        self.assertEqual(location_1.test, location_2.test)

    def test_trace_tree_builder_two_units_three_locations_test_trace(self) -> None:
        builder = TraceTreeBuilder()

        trace = builder \
            .start_test("Andreas") \
            .start_unit("Tommy1") \
            .enter_location("1") \
                .start_unit("Tommy2") \
                .enter_location("2") \
                .end_unit() \
            .enter_location("3") \
            .end_unit() \
            .end_test() \
            .build()

        sequence = [ *trace.sequence ]

        self.assertEqual(len(sequence), 3)

        location_1: Location = sequence[0]
        self.assertEqual(location_1.unit.name, "Tommy1")
        self.assertEqual(location_1.id, "1")

        location_2: Location = sequence[1]
        self.assertEqual(location_2.unit.name, "Tommy2")
        self.assertEqual(location_2.id, "2")

        location_3: Location = sequence[2]
        self.assertEqual(location_3.unit.name, "Tommy1")
        self.assertEqual(location_3.id, "3")
        
        self.assertEqual(location_1.test, location_2.test)
        self.assertEqual(location_2.test, location_3.test)

    def test_trace_tree_builder_many_units_many_locations_test_trace(self) -> None:
        builder = TraceTreeBuilder()

        trace = builder \
            .start_test("Andreas") \
            .start_unit("Tommy1") \
            .enter_location("1") \
                .start_unit("Tommy2") \
                .enter_location("2") \
                .enter_location("3") \
                    .start_unit("Tommy3") \
                    .enter_location("4") \
                    .end_unit() \
                .enter_location("5") \
                .end_unit() \
            .enter_location("6") \
                .start_unit("Tommy4") \
                .enter_location("7") \
                    .start_unit("Tommy5") \
                    .enter_location("8") \
                    .end_unit() \
                .enter_location("9") \
                .end_unit() \
            .enter_location("10") \
            .end_unit() \
            .end_test() \
            .build()

        sequence = [ *trace.sequence ]
        self.assertEqual(len(sequence), 10)

        location_1: Location = sequence[0]
        self.assertEqual(location_1.test.name, "Andreas")
        self.assertEqual(location_1.unit.name, "Tommy1")
        self.assertEqual(location_1.id, "1")

        location_2: Location = sequence[1]
        self.assertEqual(location_2.test.name, "Andreas")
        self.assertEqual(location_2.unit.name, "Tommy2")
        self.assertEqual(location_2.id, "2")

        location_3: Location = sequence[2]
        self.assertEqual(location_3.test.name, "Andreas")
        self.assertEqual(location_3.unit.name, "Tommy2")
        self.assertEqual(location_3.id, "3")

        location_4: Location = sequence[3]
        self.assertEqual(location_4.test.name, "Andreas")
        self.assertEqual(location_4.unit.name, "Tommy3")
        self.assertEqual(location_4.id, "4")

        location_5: Location = sequence[4]
        self.assertEqual(location_5.test.name, "Andreas")
        self.assertEqual(location_5.unit.name, "Tommy2")
        self.assertEqual(location_5.id, "5")

        location_6: Location = sequence[5]
        self.assertEqual(location_6.test.name, "Andreas")
        self.assertEqual(location_6.unit.name, "Tommy1")
        self.assertEqual(location_6.id, "6")

        location_7: Location = sequence[6]
        self.assertEqual(location_7.test.name, "Andreas")
        self.assertEqual(location_7.unit.name, "Tommy4")
        self.assertEqual(location_7.id, "7")

        location_8: Location = sequence[7]
        self.assertEqual(location_8.test.name, "Andreas")
        self.assertEqual(location_8.unit.name, "Tommy5")
        self.assertEqual(location_8.id, "8")

        location_9: Location = sequence[8]
        self.assertEqual(location_9.test.name, "Andreas")
        self.assertEqual(location_9.unit.name, "Tommy4")
        self.assertEqual(location_9.id, "9")

        location_10: Location = sequence[9]
        self.assertEqual(location_10.test.name, "Andreas")
        self.assertEqual(location_10.unit.name, "Tommy1")
        self.assertEqual(location_10.id, "10")

    def test_trace_in_unit(self) -> None:
        builder = TraceTreeBuilder()

        trace = builder \
            .start_test("Andreas") \
            .start_unit("Tommy1") \
            .enter_location("1") \
                .start_unit("Tommy2") \
                .enter_location("2") \
                .enter_location("3") \
                    .start_unit("Tommy3") \
                    .enter_location("4") \
                    .end_unit() \
                .enter_location("5") \
                .end_unit() \
            .enter_location("6") \
                .start_unit("Tommy4") \
                .enter_location("7") \
                    .start_unit("Tommy5") \
                    .enter_location("8") \
                    .end_unit() \
                .enter_location("9") \
                .end_unit() \
            .enter_location("10") \
            .end_unit() \
            .end_test() \
            .build()

        actual = [ *trace.in_unit("Tommy1") ]
        self.assertEqual(len(actual), 3)

        location_1: Location = actual[0]
        self.assertEqual(location_1.test.name, "Andreas")
        self.assertEqual(location_1.unit.name, "Tommy1")
        self.assertEqual(location_1.id, "1")

        location_6: Location = actual[1]
        self.assertEqual(location_6.test.name, "Andreas")
        self.assertEqual(location_6.unit.name, "Tommy1")
        self.assertEqual(location_6.id, "6")

        location_10: Location = actual[2]
        self.assertEqual(location_10.test.name, "Andreas")
        self.assertEqual(location_10.unit.name, "Tommy1")
        self.assertEqual(location_10.id, "10")

    def test_parse_single_deferred_trace_no_unit_no_test(self) -> None:
        parser = TraceParser(
            TraceTreeBuilder()
        )
        lines_1 = [
            "Location=1",
            "Location=2"
        ]
        lines_2 = [
            "Location=3"
        ]

        parser.parse(lines_1)
        parser.parse(lines_2)
        trace = parser.finish()
        sequence = [ *trace.sequence ]

        location_1 = sequence[0]
        self.assertEqual(location_1.id, "1")
        self.assertIsNone(location_1.test)
        self.assertIsNone(location_1.unit)

        location_2 = trace.sequence[1]
        self.assertEqual(location_2.id, "2")
        self.assertIsNone(location_2.test)
        self.assertIsNone(location_2.unit)

        location_3 = trace.sequence[2]
        self.assertEqual(location_3.id, "3")
        self.assertIsNone(location_3.test)
        self.assertIsNone(location_3.unit)

    def test_parse_invalid_input_stop_at_it(self) -> None:
        parser = TraceParser(
            TraceTreeBuilder()
        )
        lines = iter([
            "Location=1",
            "THIS IS AN ERROR",
            "Location=2"
        ])

        parser.parse(lines)
        trace = parser.finish()
        sequence = [ *trace.sequence ]

        self.assertEqual(len(sequence), 1)

        location_1 = sequence[0]
        self.assertEqual(location_1.id, "1")
        self.assertIsNone(location_1.test)
        self.assertIsNone(location_1.unit)

    def test_parse_trace_log(self) -> None:
        parser = TraceParser(
            TraceTreeBuilder()
        )
        lines = [
            "BeginTest=Andreas",
            "BeginUnit=Tommy1",
            "Location=1",
                "BeginUnit=Tommy2",
                "Location=2",
                "Location=3",
                    "BeginUnit=Tommy3",
                    "Location=4",
                    "EndUnit",
                "Location=5",
                "EndUnit",
            "Location=6",
                "BeginUnit=Tommy4",
                "Location=7",
                    "BeginUnit=Tommy5",
                    "Location=8",
                    "EndUnit",
                "Location=9",
                "EndUnit",
            "Location=10",
            "EndUnit",
            "EndTest",
        ]
        parser.parse(lines)
        trace = parser.finish()
        sequence = [ *trace.sequence ]

        sequence = [ *trace.sequence ]
        self.assertEqual(len(sequence), 10)

        location_1: Location = sequence[0]
        self.assertEqual(location_1.test.name, "Andreas")
        self.assertEqual(location_1.unit.name, "Tommy1")
        self.assertEqual(location_1.id, "1")

        location_2: Location = sequence[1]
        self.assertEqual(location_2.test.name, "Andreas")
        self.assertEqual(location_2.unit.name, "Tommy2")
        self.assertEqual(location_2.id, "2")

        location_3: Location = sequence[2]
        self.assertEqual(location_3.test.name, "Andreas")
        self.assertEqual(location_3.unit.name, "Tommy2")
        self.assertEqual(location_3.id, "3")

        location_4: Location = sequence[3]
        self.assertEqual(location_4.test.name, "Andreas")
        self.assertEqual(location_4.unit.name, "Tommy3")
        self.assertEqual(location_4.id, "4")

        location_5: Location = sequence[4]
        self.assertEqual(location_5.test.name, "Andreas")
        self.assertEqual(location_5.unit.name, "Tommy2")
        self.assertEqual(location_5.id, "5")

        location_6: Location = sequence[5]
        self.assertEqual(location_6.test.name, "Andreas")
        self.assertEqual(location_6.unit.name, "Tommy1")
        self.assertEqual(location_6.id, "6")

        location_7: Location = sequence[6]
        self.assertEqual(location_7.test.name, "Andreas")
        self.assertEqual(location_7.unit.name, "Tommy4")
        self.assertEqual(location_7.id, "7")

        location_8: Location = sequence[7]
        self.assertEqual(location_8.test.name, "Andreas")
        self.assertEqual(location_8.unit.name, "Tommy5")
        self.assertEqual(location_8.id, "8")

        location_9: Location = sequence[8]
        self.assertEqual(location_9.test.name, "Andreas")
        self.assertEqual(location_9.unit.name, "Tommy4")
        self.assertEqual(location_9.id, "9")

        location_10: Location = sequence[9]
        self.assertEqual(location_10.test.name, "Andreas")
        self.assertEqual(location_10.unit.name, "Tommy1")
        self.assertEqual(location_10.id, "10")