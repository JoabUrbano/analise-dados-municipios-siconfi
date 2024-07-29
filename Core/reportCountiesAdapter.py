import numpy as np
import pandas as pd

from Core.Report.Implements.reportCounties import ReportCounties

class ReportCountiesAdapter:
    def __init__(
            self,
            dataset: pd.DataFrame,
            year: int,
            quartil_100to75: int,
            quartil_75to50: int,
            quartil_50to25: int
        ):
        self.dataset = dataset
        self.year = year
        self.quartil_100to75 = quartil_100to75
        self.quartil_75to50 = quartil_75to50
        self.quartil_50to25 = quartil_50to25

    def adapterToReport(self):
        reportCounties = ReportCounties(
            self.dataset["Municipios"].to_numpy(),
            self.dataset["Arrecadacao"].to_numpy(),
            self.dataset["Gastos"].to_numpy(),
            self.dataset["Populacao"].to_numpy(),
            self.dataset["Saldo"].to_numpy(),
            self.year,
            self.quartil_100to75,
            self.quartil_75to50,
            self.quartil_50to25
        )

        reportCounties.createReport()
