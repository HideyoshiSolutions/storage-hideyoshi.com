from storage_service.config.config_virus_checker import (
    get_virus_checker_api_key,
)
from storage_service.service.virus_checker.virus_checker_none_service import (
    VirusCheckerNoneService,
)
from storage_service.service.virus_checker.virus_checker_service import (
    VirusCheckerService,
)
from storage_service.service.virus_checker.virus_total_service import (
    VirusTotalService,
)
from storage_service.utils.enums.virus_checker_type import VirusCheckerType

from dotenv import load_dotenv
from virustotal_python import Virustotal

import os
from functools import cache


@cache
def dependency_virus_checker_service() -> VirusCheckerService:
    load_dotenv()

    checker_type = VirusCheckerType(os.environ.get("VIRUS_CHECKER_TYPE", "total_virus"))

    match checker_type:
        case VirusCheckerType.TOTAL_VIRUS:
            virus_checker = Virustotal(get_virus_checker_api_key())
            return VirusTotalService(virus_checker)
        case VirusCheckerType.NONE:
            return VirusCheckerNoneService()
