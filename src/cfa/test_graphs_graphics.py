import unittest
from typing import List, Tuple

from graphviz import Digraph

from src.cfa import CFA

from src.ts import (
    LanguageLibrary,
    Parser,
    Query,
    Tree,
    TreeCFAVisitor,
)
from src.ts.node import Node


class TestGraphsGraphics(unittest.TestCase):
    def setUp(self) -> None:
        LanguageLibrary.build()
        self._language = LanguageLibrary.c()
        self._parser = Parser.create_with_language(self._language)

        self._compound_assignment_query: Query = self._language.query(self._language.syntax.query_compound_assignment)
        self._assignment_query: Query = self._language.query(self._language.syntax.query_assignment)
        self._binary_expression_query: Query = self._language.query(self._language.syntax.query_binary_expression)
        return super().setUp()

    def test_create_graphs_graphics(self) -> None:
        programs: List[Tuple[str, str]] = [
            ("if_1",  "a=1; if(a==2) { }"),
            ("if_2",  "a=1; if(a==2) { } else { }"),
            ("if_3",  "a=1; if(a==2) { } else { } a=2;"),
            ("if_4",  "a=1; if(a==2) { } else if(a==3) { } else { }"),
            ("if_5",  "a=1; if(a==2) { } else if(a==3) { } a=2;"),
            ("if_6",  "a=1; if(a==1) { a=2; }"),
            ("if_7",  "a=1; if(a==1) { a=2; } a=3;"),
            ("if_8",  "a=1; if(a==1) { a=2; } else { a=3; }"),
            ("if_9",  "a=1; if(a==1) { a=2; } else { a=3; } a=4;"),
            ("if_10", "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } a=4;"),
            ("if_11", "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } a=4;"),
            ("if_12", "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } else { a=4; } a=5; a=6;"),
            ("if_13", "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } else if(a==3) { a=4; } a=5;"),
            ("if_14", "a=1; if(a==1) { a=2; } else if(a==2) { } else if(a==3) { a=4; } else if(a==4) { a=5; } else { a=6; } a=7;"),
            ("if_15", "a=1; if(a==1) { a=2; } else if(a==2) { a=3; } else if(a==3) { a=4; } else if(a==4) { a=5; } else { a=6; } a=7;"),
            ("if_16",  "a=1; if(a==1) { a=2; } a=3; if(a==2) { a=2; } a=3; if(a==3) { a=2; } a=3;"),
            ("while_1", "while(a==1) { }"),
            ("while_2", "while(a==1) { } a=3;"),
            ("while_3", "while(a==1) { a=2; } a=3;"),
            ("while_4", "while(a==1) { a=1; a=2; a=3; } a=4;"),
            ("while_4", "while(a==1) { a=1; a=2; a=3; } a=4;"),
            ("while_5", "while(a==1) { if(a==1) { a=1; } a=2; a=3; a=4; a=5; } a=6;"),
            ("while_6", "while(a==1) { if(a==1) { a=1; } else { a=2; } a=3; } a=4;"),
            ("while_7", "while(a==1) { if(a==1) { a=1; } else if(a==2) { a=2; } else { a=3; } a=4; } a=5;"),
            ("while_8", "while(a==1) { if(a==1) { a=1; } a=2; if(a==2) { a=3; } a=4; a=5; a=6; } a=7;"),
            ("while_9", "while(a==1) { a=1; break; a=2; } a=3;"),
            ("while_10", "while(a==1) { a=1; continue; a=2; } a=3;"),
            ("while_11", "while(a) { a=1; while(a) { a=2; } a=2; } a=2;"),
            ("while_12", "while(a) { break; a=1; while(a) { break; a=2; } a=2; } a=2;"),
            ("while_13", "while(a==1) { if(a==1) { a=1; } else if(a==2) { a=2; } else { a=3; return; } a=4; } a=5;"),
            ("while_14", "while(a==1) { if(a==1) { a=1; break; } else if(a==2) { a=2; } else { a=3; return; } a=4; } a=5;"),
            ("while_15", "while(a==1) { if(a==1) { a=1; break; } else if(a==2) { continue; a=2; } else { a=3; return; } a=4; } a=5;"),
            ("do_while_1", "do { a=1; } while(a==1); a=2;"),
            ("do_while_2", "do { if(a==1) { a=1; } a=2; } while(a==1); a=2;"),
            ("do_while_3", "do { a=0; if(a==1) { a=1; } a=2; } while(a==1); a=2;"),
            ("for_1", "for(int i=0; i<5; ++i) { a=2; } a=3;"),
            ("for_2", "for(int i=0; i<5; ++i) { a=2; for(int i=0; i<5; ++i) { a=2; } a=2; } a=3;"),
            ("for_3", "for(int i=0; i<5; ++i) { break; a=2; } a=3;"),
            ("for_4", "for(int i=0; i<5; ++i) { break; a=2; for(int i=0; i<5; ++i) { continue; a=2; } a=2; } a=3;"),
            ("switch_1", """
            switch (a)
            {
                case 1: a=1;
            }
             """),
            ("switch_2", """
            switch (a)
            {
                case 3: { a=2; }
            }
             """),
            ("switch_3", """
            switch (a)
            {
                case 1: a=1;
                case 2: a=1;
                case 3: { a=2; }
                default: a=3;
            }
             """),
            ("switch_4", """
            switch (a)
            {
                case 1: 
                case 2: a=1;
                case 3: { a=2; }
                default: a=3;
            }
             """),
            ("switch_5", """
            switch (a)
            {
                case 1: 
                case 2: a=1;
                case 3: { a=2; }
                default: a=3;
            }
            a=10;
             """),
            ("switch_6", """
            switch (a)
            {
                case 1: 
                case 2: a=1;
                case 3: { a=2; }
                default: a=3;
            }
             """),
            ("switch_7", """
            if(a==1) {
                switch (a)
                {
                    case 2: a=1;
                }
                a=4;
            } else {
                a=9;
            }
            a=-1;
             """),
            ("switch_8", """
            if(a==1) {
                switch (a)
                {
                    case 1: 
                    case 2: a=1;
                    case 3: { a=2; }
                    default: a=3;
                }
                a=3;
                while (a==1) { a=2; }
                a=4;
            } else {
                a=9;
            }
            a=-1;
             """),
            ("switch_9", """
            if(a==1) {
                switch (a)
                {
                    case 1: 
                    case 2: a=1;
                    case 3: { a=2; }
                    default: a=3;
                }
                while (a==1) { a=2; }
                a=4;
            } else {
                a=9;
            }
            a=-1;
             """),
            ("function_1", """
            void foo() {
                a=2;
                return;
                a=2;
            }
             """),
            ("function_2", """
            void foo() {
            target:
                a=2;
                a=3;
                goto target;
            }
             """),
            ("function_3", """
            void foo() {
                goto target;
                a=3;
            target:
                a=2;
            }
             """)
        ]

        for program in programs:
            name: str = program[0]
            prog: str = program[1]
            tree: Tree = self._parser.parse(prog)
            visitor: TreeCFAVisitor = TreeCFAVisitor(tree)
            root: Node = tree.root_node
            if root.named_children[0].type == "function_definition":
                root = root.named_children[0].child_by_field_name("body")
            cfa: CFA = visitor.create(root, False)
            dot = cfa.draw(tree, name)
            dot.save(directory="graphs")