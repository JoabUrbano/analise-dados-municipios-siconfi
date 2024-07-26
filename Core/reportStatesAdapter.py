import numpy as np
import pandas as pd

from Core.Graphic.Implements.graphics import GraphicsImpl
from Core.Report.Implements.reportStates import ReportStates

class StatesAdapter:
    def __init__(self, dataset: pd.DataFrame):
        self.dataset = dataset
        self.states = self.dataset['Estados'].to_numpy()
        self.valuesExpense = self.dataset['Gastos'].to_numpy()
        self.valuesBudget = self.dataset['Arrecadacao'].to_numpy()
        self.valuesBalance = self.dataset['Saldo'].to_numpy()
    
    def graphicExpense(self) -> None:
        dataExpenses = {"Estados": self.states, "Gastos": self.valuesExpense}
        dfExpenses = pd.DataFrame(dataExpenses)
        dfExpenses = dfExpenses.sort_values(by="Gastos", ascending=False)
        
        graphicsExpense = GraphicsImpl(
            dfExpenses["Estados"].to_numpy(),
            dfExpenses["Gastos"].to_numpy(),
            "Despesas Pagas por Estado",
            "Estados",
            "Total de Despesas Pagas",
        )
        graphicsExpense.createGraphics()
    
    def graphicBudget(self) -> None:
        dataBudget = {"Estados": self.states, "Arrecadacao": self.valuesBudget}
        dfBudget = pd.DataFrame(dataBudget)
        dfBudget = dfBudget.sort_values(by="Arrecadacao", ascending=False)

        graphicsBudget = GraphicsImpl(
            dfBudget["Estados"].to_numpy(),
            dfBudget["Arrecadacao"].to_numpy(),
            "Arrecadação por Estado",
            "Estados",
            "Total de Arrecadações",
        )
        graphicsBudget.createGraphics()
    
    def graphicBalance(self) -> None:
        graphicsBalance = GraphicsImpl(
            self.states,
            self.valuesBalance,
            'Saldo dos Estado',
            'Estados',
            'Total do Saldo'
        )
        graphicsBalance.createGraphics()

    def adapterToStates(self) -> None:
        self.graphicExpense()
        self.graphicBudget()
        self.graphicBalance()
        
        self.adapterToReport()

    def adapterToReport(self) -> None:
        reportStates = ReportStates(
            self.states,
            self.valuesBudget,
            self.valuesExpense,
            self.valuesBalance,
            2020
        )

        reportStates.createReport()
