
from cfa import (
    CCFAFactory
)
from instrumentor import CCanaryFactory, CTreeInfestator
from cfa import Node
from cfa.c_cfa_factory import CCFAFactory

from utilities import FileHandler
from ts import (
    Tree,
    Node,
    CField,
    Parser,
)
from .use_case import *

class InfestProgramRequest(UseCaseRequest):
    def __init__(
        self,
        parser: Parser,
        tree: Tree,
        unit_function: Node,
        filepath: str,
        save_graph: bool = True,
        save_graph_directory: str = "/"
    ) -> None:
        self._parser = parser
        self._tree = tree
        self._unit_function = unit_function
        self._filepath = filepath
        self._save_graph = save_graph
        self._save_graph_directory = save_graph_directory
        super().__init__()

    @property
    def parser(self) -> Parser:
        return self._parser

    @property
    def tree(self) -> Tree:
        return self._tree

    @property
    def unit_function(self) -> Node:
        return self._unit_function

    @property
    def filepath(self) -> str:
        return self._filepath

    @property
    def save_graph(self) -> bool:
        return self._save_graph

    @property
    def save_graph_directory(self) -> str:
        return self._save_graph_directory

class InfestProgramResponse(UseCaseResponse):
    def __init__(
        self,
        instrumented_tree: Tree,
    ) -> None:
        self._instrumented_tree = instrumented_tree
        super().__init__()

    @property
    def instrumented_tree(self) -> Tree:
        return self._instrumented_tree

class InfestProgramUseCase(
    UseCase[InfestProgramRequest, InfestProgramResponse]
):
    def do(self, request: InfestProgramRequest) -> InfestProgramResponse:
        # Step 1: Create CFA for the unit function
        cfa_factory = CCFAFactory(request.tree)
        unit_function_body = request.unit_function.child_by_field(
            CField.BODY
        )
        cfa = cfa_factory.create(unit_function_body)
        if request.save_graph:
            graph = cfa.draw(request.tree, "cfg")
            graph.save(directory=request.save_graph_directory)

        # Step 2: Instrument
        canary_factory = CCanaryFactory()
        infestator = CTreeInfestator(request.parser, canary_factory)
        instrumented_tree = infestator.infect(request.tree, cfa)

        # Step 3: Write the instrumented file
        file = open(request.filepath, "w+")
        file.write(instrumented_tree.text)
        file.close()

        return InfestProgramResponse(
            request.parser.parse(instrumented_tree.text)
        )
