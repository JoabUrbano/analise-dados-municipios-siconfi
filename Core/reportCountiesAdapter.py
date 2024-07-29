import numpy as np
import pandas as pd

from Core.Report.Implements.reportCounties import ReportCounties

class ReportCountiesAdapter:
    def __init__(self, dataset: pd.DataFrame, year: int):
        self.dataset = dataset
        self.year = year

    def adapterToReport(self):
        self.dataset = self.dataset.sort_values(by="Saldo", ascending=False)
        
        quartil_100to75 = self.dataset['Saldo'].quantile(0.75)
        quartil_75to50 = self.dataset['Saldo'].quantile(0.50)
        quartil_50to25 = self.dataset['Saldo'].quantile(0.25)

        reportCounties = ReportCounties(
            self.dataset["Municipios"].to_numpy(),
            self.dataset["Arrecadacao"].to_numpy(),
            self.dataset["Gastos"].to_numpy(),
            self.dataset["Populacao"].to_numpy(),
            self.dataset["Saldo"].to_numpy(),
            self.year,
            quartil_100to75,
            quartil_75to50,
            quartil_50to25
        )

        reportCounties.createReport()
