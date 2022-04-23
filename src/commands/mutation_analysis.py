from shutil import register_unpack_format
import time
from typing import Dict
from urllib import request
from application import (
    InitializeSystemRequest,
    InitializeSystemUseCase,
    UnitAnalyseFileRequest,
    UnitAnalyseFileUseCase,
    RunTestRequest,
    RunTestUseCase,
    InfestProgramRequest,
    InfestProgramUseCase,
    ParseTestResultRequest,
    ParseTestResultUseCase,
    UnitAnalyseTreeRequest,
    UnitAnalyseTreeUseCase,
    MutateAlongAllTracesRequest,
    MutateAlongAllTracesUseCase,
    MutateRandomlyRequest,
    MutateRandomlyUseCase,
)
from cfa import CCFAFactory
from decorators import LocationDecorator
from mutator import MutationStrategyFactory
from test_results_parsing import ResultsParserFactory
from ts import (
    Parser,
    LanguageLibrary,
)

def mutation_analysis(
    file: str,
    unit: str,
    build_command: str,
    test_command: str,
    out: str = "",
    base: str = "",
    testing_backend: str = "ffs_gnu_assert",
    placement_strategy: str = "randomly",
    mutation_strategy: str = "obom",
    unit_whitelist: str = None,
    unit_blacklist: str = None
) -> None:
    # Step 0: Initialize the system
    initialize_system_request = InitializeSystemRequest()
    InitializeSystemUseCase().do(initialize_system_request)

    # Step 1: Unit analysis
    unit_analysis_of_file_request = UnitAnalyseFileRequest(
        f'{base}/{file}', LanguageLibrary.c(), unit
    )
    unit_analysis_of_file_response = UnitAnalyseFileUseCase().do(
        unit_analysis_of_file_request
    )
    
    whitelist = (unit_whitelist or "").split()
    blacklist = (unit_blacklist or "").split()

    for u_idx, unit_tuple in enumerate(unit_analysis_of_file_response.unit_functions):
        start_time = time.perf_counter()

        unit_node = unit_tuple[0]
        unit_name = unit_tuple[1]
        print(unit_name)
        
        if (len(whitelist) > 0 and unit_name not in whitelist) or \
            (len(blacklist) > 0 and unit_name in blacklist):
            continue

        # Step 2: Instrument the mutable version
        instrumentation_request = InfestProgramRequest(
            Parser.c(),
            unit_analysis_of_file_response.tree,
            unit_node,
            unit_analysis_of_file_request.filepath
        )
        instrumentation_response = InfestProgramUseCase().do(
            instrumentation_request
        )

        # Step 3: Instrumented tree unit analysis
        instrumented_unit_analysis_of_file_request = UnitAnalyseFileRequest(
            unit_analysis_of_file_request.filepath, LanguageLibrary.c(), unit_name
        )
        instrumented_unit_analysis_of_file_response = UnitAnalyseFileUseCase().do(
            instrumented_unit_analysis_of_file_request
        )

        # Step 4: Get the localised CFG
        unit_analysis_of_tree_request = UnitAnalyseTreeRequest(
            instrumented_unit_analysis_of_file_response.tree,
            LanguageLibrary.c(),
            unit_analysis_of_file_request.unit
        )
        unit_analysis_of_tree_response = UnitAnalyseTreeUseCase().do(
            unit_analysis_of_tree_request
        )
        instrumented_cfg = CCFAFactory(instrumentation_response.instrumented_tree).create(
            unit_analysis_of_tree_response.unit_functions[u_idx][0]
        )
        localised_cfg = LocationDecorator(instrumentation_response.instrumented_tree).decorate(
            instrumented_cfg
        )

        # Step 5: Run tests on original program
        original_test_request = RunTestRequest(
            build_command, test_command, f'{base}/{out}/original_test_results.txt'
        )
        RunTestUseCase().do(original_test_request)

        # Step 6: Parse test results
        test_results_parser = ResultsParserFactory().create(
            testing_backend
        )
        parse_test_results_request = ParseTestResultRequest(
            original_test_request.out,
            test_results_parser
        )
        parse_test_results_response = ParseTestResultUseCase().do(
            parse_test_results_request
        )
        
        # Step 7: Create mutation strategy
        applied_mutation_strategy = MutationStrategyFactory().create(
            mutation_strategy, instrumentation_request.parser
        )

        if placement_strategy == "randomly":
            # Step 7: Mutate 'randomly'
            randomly_mutate_request = MutateRandomlyRequest(
                instrumented_unit_analysis_of_file_response.unit_functions,
                instrumentation_response.instrumented_tree,
                instrumentation_request.parser,
                applied_mutation_strategy,
                build_command,
                test_command,
                test_results_parser,
                unit_analysis_of_file_request.filepath,
                out,
                base,
            )
            MutateRandomlyUseCase().do(
                randomly_mutate_request
            )
        elif placement_strategy == "pathbased":
            # Step 7: Get individual unit sequences
            unit_traces = localised_cfg.split_on_finals(
                parse_test_results_response.test_results.trace
            )

            # Step 8: Mutate 'pathbased'
            mutate_along_trace_request = MutateAlongAllTracesRequest(
                unit_traces,
                localised_cfg,
                instrumentation_response.instrumented_tree,
                instrumentation_request.parser,
                applied_mutation_strategy,
                build_command,
                test_command,
                test_results_parser,
                unit_analysis_of_file_request.filepath,
                out,
                base,
            )
            mutation_start_time = time.perf_counter()
            mutate_along_trace_response = MutateAlongAllTracesUseCase().do(
                mutate_along_trace_request
            )
            mutation_end_time = time.perf_counter()
            mutation_duration = mutation_end_time - mutation_start_time

            results_file = open(f"{mutate_along_trace_request.base}/{mutate_along_trace_request.out}/{unit_name}_{u_idx}", "w+")
            results_file.write(f"Mutation took {mutation_duration} seconds\n")
            
            results_file.write(f"Original execution trace count {mutate_along_trace_response.trace_count}\n")

            results_file.write("Visted count\n")
            for location in mutate_along_trace_response.amount_visited_locations:
                amount = mutate_along_trace_response.amount_visited_locations[location]
                results_file.write(f"{location} was visited {amount} times\n")
            results_file.write("\n")

            results_file.write(f"Visited locations " + ", ".join(mutate_along_trace_response.visited_locations) + "\n")
            results_file.write(f"Unvisited locations " + ", ".join(mutate_along_trace_response.unvisited_locations) + "\n")
            amount_visited = len(mutate_along_trace_response.visited_locations)
            amount_unvisited = len(mutate_along_trace_response.unvisited_locations)
            results_file.write(f"Visited {amount_visited}, Unvisted {amount_unvisited}")
            if amount_visited + amount_unvisited > 0:
                results_file.write(f", percentage visited {amount_visited / (amount_visited + amount_unvisited)}")
            results_file.write("\n")

            results_file.write("\n")

            results_file.write(f"Visited nodes {len(mutate_along_trace_response.visited_nodes)}\n")
            results_file.write(f"Unvisited nodes {len(mutate_along_trace_response.unvisited_nodes)}\n")
            nodes_total = len(mutate_along_trace_response.visited_nodes) + len(mutate_along_trace_response.unvisited_nodes)
            if nodes_total > 0:
                results_file.write(f"Percentage visited {len(mutate_along_trace_response.visited_nodes) / nodes_total}\n")

            results_file.write("\n")

            results_file.write(f"Visited candidates {mutate_along_trace_response.visited_candidates}\n")
            results_file.write(f"Unvisited candidates {mutate_along_trace_response.unvisited_candidates}\n")
            candidates_total = mutate_along_trace_response.visited_candidates + mutate_along_trace_response.unvisited_candidates
            if candidates_total > 0:
                results_file.write(f"Percentage visited {mutate_along_trace_response.visited_candidates / candidates_total}\n")

            results_file.write("\n")

            results_file.write(f"Tested mutations {mutate_along_trace_response.visited_mutations}\n")
            results_file.write(f"Untested mutations {mutate_along_trace_response.unvisited_mutations}\n")
            mutations_total = mutate_along_trace_response.visited_mutations + mutate_along_trace_response.unvisited_mutations
            if mutations_total > 0:
                results_file.write(f"Percentage visited {mutate_along_trace_response.visited_mutations / mutations_total}\n")

            all_locations_total_killed = 0
            all_locations_total_survied = 0
            total_if_conditional_killed = 0
            total_if_conditional_survived = 0
            total_for_initilisation_killed = 0
            total_for_initilisation_survived = 0
            total_for_condition_killed = 0
            total_for_condition_survived = 0
            total_for_update_killed = 0
            total_for_update_survived = 0
            total_do_while_condition_killed = 0
            total_do_while_condition_survived = 0
            total_while_condition_killed = 0
            total_while_condition_survived = 0
            total_switch_condition_killed = 0
            total_switch_condition_survived = 0
            c_syntax = LanguageLibrary.c().syntax
            for visited_locaiton in mutate_along_trace_response.visited_locations:
                results_file.write(f"\nLocation {visited_locaiton}\n")
                if len(mutate_along_trace_response.random_mutations_runs) == 0:
                    results_file.write("No runs\n")
                    continue
                results_file.write(f"{len(mutate_along_trace_response.random_mutations_runs)} Runs\n")

                location_total_killed = 0
                location_total_survied = 0
                for mutation_run in mutate_along_trace_response.random_mutations_runs:
                    cfa_node = mutation_run[0]
                    run_result = mutation_run[1]

                    if cfa_node.location == visited_locaiton:
                        continue
                    results_file.write("\n")

                    results_file.write(f"Code :: '{mutate_along_trace_request.tree.contents_of(cfa_node.node)}'\n")

                    if run_result.amount_killed + run_result.amount_survived == 0:
                        results_file.write("No mutations\n")
                        continue

                    amount_killed = 0
                    amount_survived = 0

                    # "if"-condition
                    if c_syntax.is_condition_of_if(cfa_node.node):
                        results_file.write("Is :: if-condition\n")
                    # "for" initialisation
                    if c_syntax.is_initialisation_of_for(cfa_node.node):
                        results_file.write("Is :: for-initalisation\n")
                    # "for" conditional
                    if c_syntax.is_condition_of_for(cfa_node.node):
                        results_file.write("Is :: for-condition\n")
                    # "for" update
                    if c_syntax.is_update_of_for(cfa_node.node):
                        results_file.write("Is :: for-udapte\n")
                    # "do while" condition
                    if c_syntax.is_condition_of_do_while(cfa_node.node):
                        results_file.write("Is :: do_while-condition\n")
                    # "while" condition
                    if c_syntax.is_condition_of_while(cfa_node.node):
                        results_file.write("Is :: while-condition\n")
                    # "switch" condition
                    if c_syntax.is_condition_of_switch(cfa_node.node):
                        results_file.write("Is :: switch-condition\n")

                    if len(run_result.mutation_tests) == 0: continue

                    for mutation_test in run_result.mutation_tests:
                        mutation_amount_location_visitation: Dict[str, int] = dict()
                        for location in mutation_test.test_results.trace.sequence:
                            if location == "" or location is None: continue
                            if location.id not in mutation_amount_location_visitation:
                                mutation_amount_location_visitation[location.id] = 0
                            else: mutation_amount_location_visitation[location.id] += 1

                        for location in mutation_amount_location_visitation:
                            amount = mutation_amount_location_visitation[location]
                            results_file.write(f"{location} was visited {amount} times\n")

                        results_file.write(f"[{mutation_test.candidate.start_point}, {mutation_test.candidate.end_point}]")
                        results_file.write(f" {str(mutation_test.mutation)}")
                        if mutation_test.test_results.summary.failure_count > 0:
                            amount_killed += 1
                            mutation_state = "KILLED"
                        else:
                            amount_survived += 1
                            mutation_state = "SURVIVED"
                        results_file.write(f" :: {mutation_state}\n")
                        results_file.write("\n")

                    # "if"-condition
                    if c_syntax.is_condition_of_if(cfa_node.node):
                        total_if_conditional_killed += amount_killed
                        total_if_conditional_survived += amount_survived
                    # "for" initialisation
                    if c_syntax.is_initialisation_of_for(cfa_node.node):
                        total_for_initilisation_killed += amount_killed
                        total_for_initilisation_survived += amount_survived
                    # "for" conditional
                    if c_syntax.is_condition_of_for(cfa_node.node):
                        total_for_condition_killed += amount_killed
                        total_for_condition_survived += amount_survived
                    # "for" update
                    if c_syntax.is_update_of_for(cfa_node.node):
                        total_for_update_killed += amount_killed
                        total_for_update_survived += amount_survived
                    # "do while" condition
                    if c_syntax.is_condition_of_do_while(cfa_node.node):
                        total_do_while_condition_killed += amount_killed
                        total_do_while_condition_survived += amount_survived
                    # "while" condition
                    if c_syntax.is_condition_of_while(cfa_node.node):
                        total_while_condition_killed += amount_killed
                        total_while_condition_survived += amount_survived
                    # "switch" condition
                    if c_syntax.is_condition_of_switch(cfa_node.node):
                        total_switch_condition_killed += amount_killed
                        total_switch_condition_survived += amount_survived
                    
                    results_file.write(f"Killed {amount_killed} and {amount_survived} survived")
                    amount_total = amount_killed + amount_survived
                    if amount_total > 0:
                        results_file.write(f", mutation score of {amount_killed / (amount_killed + amount_survived)}")
                    results_file.write("\n")

                    location_total_killed += amount_killed
                    location_total_survied += amount_survived

                all_locations_total_killed += location_total_killed
                all_locations_total_survied += location_total_survied

                location_total_sum = location_total_killed + location_total_survied
                results_file.write(f"\nLocation Killed {location_total_killed} and {location_total_survied} survived")
                if location_total_sum > 0:
                    results_file.write(f", mutation score of {location_total_killed / (location_total_sum)}")
                results_file.write("\n\n")

            results_file.write(f"\nTotal killed {all_locations_total_killed} and {all_locations_total_survied} total survived")
            if all_locations_total_killed + all_locations_total_survied > 0:
                results_file.write(f", with a total mutations score of {all_locations_total_killed/(all_locations_total_killed + all_locations_total_survied)}")
            results_file.write("\n")

            mutate_along_trace_request.localised_cfg.draw(
                mutate_along_trace_request.tree, f"{unit_name}_{u_idx}"
            ).save(directory=f"{mutate_along_trace_request.base}/{mutate_along_trace_request.out}")

        results_file.write("\n")
        results_file.write(f"Took {time.perf_counter() - start_time} seconds")
        results_file.close()

        # Step 6: Revert to the original program after mutation
        file = open(unit_analysis_of_file_request.filepath, "w+")
        file.write(unit_analysis_of_file_response.tree.text)
        file.close()