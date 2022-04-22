from application import (
    InitializeSystemRequest,
    InitializeSystemUseCase,
    UnitAnalyseFileRequest,
    UnitAnalyseFileUseCase,
    CreateCFGRequest,
    CreateCFGUseCase
)
from ts import (
    LanguageLibrary,
)

def create_cfg(
    file: str,
    unit: str,
    out: str,
    base: str = "",
) -> None:
    # Step 0: Initialize the system
    initialize_system_request = InitializeSystemRequest()
    InitializeSystemUseCase().do(initialize_system_request)

    # Step 1: Unit analysis
    unit_analysis_request = UnitAnalyseFileRequest(
        f'{base}/{file}', LanguageLibrary.c(), unit
    )
    unit_analysis_response = UnitAnalyseFileUseCase().do(
        unit_analysis_request
    )

    # Step 2: Create CFG
    create_cfg_request = CreateCFGRequest(
        unit_analysis_response.tree,
        unit_analysis_response.unit_functions
    )
    create_cfg_response = CreateCFGUseCase().do(
        create_cfg_request
    )

    # Step 3: Draw and save cfg
    dot = create_cfg_response.cfa.draw(
        unit_analysis_response.tree, f'{unit}_cfg'
    )
    dot.save(directory=f'{base}/{out}')