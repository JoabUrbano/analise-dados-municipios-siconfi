from abc import ABC, abstractmethod
from typing import List

class ReportInterface:

    @abstractmethod
    def createReport(self) -> None:
        pass    
