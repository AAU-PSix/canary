from typing import Iterable, List
from graphviz import Digraph
from instrumentation_trace import Trace, Location
from ts import Tree
from .cfa import CFA
from .localised_node import LocalisedNode

class LocalisedCFA(CFA[LocalisedNode]):
    def __init__(self, root: LocalisedNode) -> None:
        super().__init__(root)

    def follow(self, unit_name: str, trace: Trace) -> Iterable[LocalisedNode]:
        if unit_name is not None:
            locations = [ location.id for location in trace.in_unit(unit_name) ]
        else:
            locations = [ location.id for location in trace.sequence ]

        current = self.root

        for idx, location in enumerate(locations):
            if idx + 1 < len(locations):
                next_location = locations[idx + 1]
            else: next_location = None

            # Step 1: Find the next location node
            if current.location != location:
                for outgoing in self.outgoing(current):
                    if outgoing.location == location:
                        current = outgoing

            # Step 2: Follow the current trace location
            for trace_node in self.follow_location(
                location,
                current,
                next_location
            ):
                current = trace_node
                yield trace_node

    def follow_location(self, location: str, start: LocalisedNode, next_location: str = None) -> Iterable[LocalisedNode]:
        if start.location != location:
            return

        found_end = False
        current = start
        while not found_end:
            yield current

            found_end = True
            for outgoing in self.outgoing(current):
                if next_location is not None and \
                    outgoing.location == next_location:
                    found_end = True
                    break

                elif outgoing.location == location:
                    current = outgoing
                    found_end = False

    def split_on_finals(self, trace: Trace) -> List["Trace"]:
        finals = [ node[0].location for node in self.finals ]
        
        traces: List["Trace"] = list()
        sequence: List[Location] = list()
        for curr in trace.sequence:
            sequence.append(curr)
            if curr.id in finals:
                if sequence is not None:
                    traces.append(Trace(sequence))
                sequence = list()
        return traces

    def draw_along_paths(
        self,
        _: Trace,
        tree: Tree,
        name: str,
        dot: Digraph = None
    ) -> Digraph:
        if dot is None: dot = Digraph(name)

        colors = [
            "aliceblue", "antiquewhite", "aqua", "aquamarine", "azure", "beige", "bisque", "black", "blanchedalmond",
            "blue", "blueviolet", "brown", "burlywood", "cadetblue", "chartreuse", "chocolate", "coral",
            "cornflowerblue", "cornsilk", "crimson", "cyan", "darkblue", "darkcyan", "darkgoldenrod", "darkgray",
            "darkgreen", "darkgrey", "darkkhaki", "darkmagenta", "darkolivegreen", "darkorange", "darkorchid", "darkred",
            "darksalmon", "darkseagreen", "darkslateblue", "darkslategray", "darkslategrey", "darkturquoise", "darkviolet", "deeppink",
            "deepskyblue", "dimgray", "dimgrey", "dodgerblue", "firebrick", "floralwhite", "forestgreen", "fuchsia", "gainsboro",
            "ghostwhite", "gold", "goldenrod", "gray", "grey", "green", "greenyellow", "honeydew",
            "hotpink", "indianred", "indigo", "ivory", "khaki", "lavender", "lavenderblush", "lawngreen", "lemonchiffon",
            "lightblue", "lightcoral", "lightcyan", "lightgoldenrodyellow", "lightgray", "lightgreen", "lightgrey", "lightpink", "lightsalmon",
            "lightseagreen", "lightskyblue", "lightslategray", "lightslategrey", "lightsteelblue", "lightyellow", "lime", "limegreen", "linen",
            "magenta", "maroon", "mediumaquamarine", "mediumblue", "mediumorchid", "mediumpurple", "mediumseagreen", "mediumslateblue", "mediumspringgreen", "mediumturquoise",
            "mediumvioletred", "midnightblue", "mintcream", "mistyrose", "moccasin", "navajowhite", "navy", "oldlace", "olive",
            "olivedrab", "orange", "orangered", "orchid", "palegoldenrod", "palegreen", "paleturquoise", "palevioletred", "papayawhip",
            "peachpuff", "peru", "pink", "plum", "powderblue", "purple", "red", "rosybrown", "royalblue", "saddlebrown", "salmon",
            "sandybrown", "seagreen", "seashell", "sienna", "silver", "skyblue", "slateblue", "slategray", "slategrey",
            "snow", "springgreen", "steelblue", "tan", "teal", "thistle", "tomato", "turquoise", "violet", "wheat", "white", "whitesmoke", "yellow", "yellowgreen",
        ]
        traces = [
            self.follow(None, trace) for trace in self.split_on_finals(trace)
        ]

        def edge_color(source: LocalisedNode, destination: LocalisedNode) -> str:
            found_colors: List[str] = list()
            for idx, trace in enumerate(traces):
                if source in trace and \
                    destination in trace:
                        found_colors.append(colors[idx])
            return ":".join(found_colors)

        dot.node("initial", shape="point")
        dot.edge("initial", self._cfa_node_name(tree, self.root))

        finals: List[LocalisedNode] = self.finals
        if len(finals) > 0:
            dot.node("final", shape="point")
            for final in self.finals:
                dot.edge(self._cfa_node_name(tree, final), "final")

        for source in self._nodes:
            dot.node(self._cfa_node_name(tree, source))
            for outgoing in self.outgoing_edges(source):
                destination = outgoing.destination
                dot.edge(
                    self._cfa_node_name(tree, source),
                    self._cfa_node_name(tree, destination),
                    outgoing.label,
                    color=edge_color(source, destination)
                )