from time import sleep
from application import (
    InitializeSystemRequest,
    InitializeSystemUseCase,
    UnitAnalyseFileRequest,
    UnitAnalyseFileUseCase,
    RunTestRequest,
    RunTestUseCase,
    InfestProgramRequest,
    InfestProgramUseCase,
    RevertRequest,
    RevertUseCase
)
from ts import (
    Parser,
)

def mutation_analysis(
    file: str,
    unit: str,
    out: str,
    persist: bool,
    mutations: int,
    log: bool,
    build_command: str,
    test_command: str,
    base: str = "",
) -> None:
    print(persist)
    print(mutations)
    print(log)

    # Step 0: Initialize the system
    initialize_system_request = InitializeSystemRequest()
    InitializeSystemUseCase().do(initialize_system_request)

    # Step 1: Unit analysis
    unit_analysis_request = UnitAnalyseFileRequest(
        f'{base}/{file}', Parser.c(), unit
    )
    unit_analysis_response = UnitAnalyseFileUseCase().do(
        unit_analysis_request
    )

    # Step 2: Instrument the mutable version
    instrumentation_request = InfestProgramRequest(
        Parser.c(),
        unit_analysis_response.tree,
        unit_analysis_response.unit_function,
        unit_analysis_request.filepath
    )
    InfestProgramUseCase().do(instrumentation_request)

    # Step 3: Run tests on original program
    original_test_request = RunTestRequest(
        build_command, test_command, f'{base}/{out}/original_test_results.txt'
    )
    RunTestUseCase().do(original_test_request)

    # Step 4: Revert the file contents to before unit analysis
    revert_request = RevertRequest(
        unit_analysis_request.filepath,
        unit_analysis_response.tree.text
    )
    RevertUseCase().do(revert_request)

    # Step 5: Parse test results