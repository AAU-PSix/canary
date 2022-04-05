from dataclasses import dataclass
from math import factorial
from cfa import (
    CCFAFactory
)
from cfa.decorators.location_decorator import *
from cfa.cfa_factory import CFAFactory
from tree_infestator.c_canary_factory import CCanaryFactory
from tree_infestator.c_tree_infestator import CTreeInfestator
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

@dataclass
class InfestProgramResponse(UseCaseResponse): pass
    


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
            graph = cfa.draw(request.tree, "cfa_fut_org")
            graph.save(directory=request.save_graph_directory)



        # Step 2: Infest
        canary_factory = CCanaryFactory()
        infestator = CTreeInfestator(request.parser, canary_factory)
        infested_tree = infestator.infect(request.tree, cfa)

        # Step 3: Write the infested file
        file: FileHandler = open(request.filepath, "w+")
        file.write(infested_tree.text)
        file.close()

        # Step 4: Decorate CFA with locations
        factory = CFAFactory(infested_tree)
        cfa = factory.create(infested_tree.root_node)
        decorator = LocationDecorator(cfa)
        decoratedCFA = decorator.decorate()
        



        return InfestProgramResponse()
