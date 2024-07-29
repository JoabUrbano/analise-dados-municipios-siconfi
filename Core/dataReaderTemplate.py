import numpy as np
import pandas as pd

from Core.statesAdapter import StatesAdapter
from Core.reportCountiesAdapter import ReportCountiesAdapter

from typing import Tuple

class DataReaderTemplate:

    def __init__(self, pathExpense: str, pathBudget: str, year: int):
        self.pathExpense = pathExpense
        self.pathBudget = pathBudget
        self.year = year

    def openfile(self, path: str) -> pd.DataFrame:
        data = pd.read_csv(
            path, sep=";", encoding="latin-1", escapechar="\n", skiprows=3
        )
        return data

    def cleanData(self, dataFrame: pd.DataFrame, population: bool) -> pd.DataFrame:
        dataFrame.drop(columns=["Identificador da Conta"], inplace=True)
        dataFrame.drop(columns=["Cod.IBGE"], inplace=True)
        if population:
            dataFrame.drop(columns=["População"], inplace=True)

        return dataFrame

    def initialization(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        ######## Expense ########
        dataExpense = self.openfile(self.pathExpense)
        dataExpense = self.cleanData(dataExpense, True)

        ######## Budget ########
        dataBudget = self.openfile(self.pathBudget)
        dataBudget = self.cleanData(dataBudget, False)

        return self.sumForStates(dataExpense, dataBudget)

    def sumForStates(
        self,
        dataExpense: pd.DataFrame,
        dataBudget: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        onlyPaidExpense = dataExpense[dataExpense["Coluna"] == "Despesas Pagas"]

        onlyPaidExpenseAndTotal = onlyPaidExpense[
            onlyPaidExpense["Conta"] == "Total Geral da Despesa"
        ]

        uniqueEstados = pd.unique(dataExpense["UF"])

        sumListExpense = []
        statesExpense = []
        for uf in uniqueEstados:
            cidades = onlyPaidExpenseAndTotal[onlyPaidExpenseAndTotal["UF"] == uf]
            soma = 0
            for saldo in cidades["Valor"]:
                if saldo == "Instituição":
                    continue
                fSoma = float(saldo.replace(",", "."))
                soma += fSoma
            statesExpense.append(uf)
            sumListExpense.append(soma)

        onlyPaidBudget = dataBudget[
            dataBudget["Coluna"] == "Receitas Brutas Realizadas"
        ]

        onlyPaidBudgetAndTotal = onlyPaidBudget[
            onlyPaidBudget["Conta"].str.contains(pat="TOTAL DAS RECEITAS")
        ]

        sumListBudget = []
        statesBudget = []
        for uf in uniqueEstados:
            cidades = onlyPaidBudgetAndTotal[onlyPaidBudgetAndTotal["UF"] == uf]
            soma = 0
            for saldo in cidades["Valor"]:
                if saldo == "Instituição":
                    continue
                fSoma = float(saldo.replace(",", "."))
                soma += fSoma
            statesBudget.append(uf)
            sumListBudget.append(soma)

        ######## Saldo das contas do estado ########
        resultStates = []
        cont = 0
        while len(sumListBudget) > cont:
            resultStates.append(sumListBudget[cont] - sumListExpense[cont])
            cont += 1

        # Criar gráficos e relatorios de estados
        dataBalance = {
            "Estados": statesBudget,
            "Saldo": resultStates,
            "Arrecadacao": sumListBudget,
            "Gastos": sumListExpense,
        }

        dfStatesBalance = pd.DataFrame(dataBalance)
        dfStatesBalance = dfStatesBalance.sort_values(by="Saldo", ascending=False)

        statesAdapter = StatesAdapter(dfStatesBalance)
        statesAdapter.adapterToStates()

        dfCountiesBalance = self.calculateCounties(onlyPaidBudgetAndTotal, onlyPaidExpenseAndTotal)

        return dfStatesBalance,  dfCountiesBalance

    def calculateCounties(self, validBudget: pd.DataFrame, validExpense: pd.DataFrame) -> pd.DataFrame:
        ### Filtrando prefeituras que não estão presentes em ambos os relatorios
        onlyPaidBudgetAndTotalFiltered, onlyPaidExpenseAndTotalFiltered = (
            self.removeMissingCities(validBudget, validExpense)
        )

        resultBalance = []
        budgetCounties = onlyPaidBudgetAndTotalFiltered["Valor"].to_numpy()
        expenseCountis = onlyPaidExpenseAndTotalFiltered["Valor"].to_numpy()

        for b, e in zip(budgetCounties, expenseCountis):
            resultBalance.append(float(b.replace(",", ".")) - float(e.replace(",", ".")))

        dataCountie = {
            "Municipios": onlyPaidExpenseAndTotalFiltered["Instituição"].to_numpy(),
            "Arrecadacao": budgetCounties,
            "Gastos": expenseCountis,
            "Populacao": onlyPaidBudgetAndTotalFiltered["População"].to_numpy(),
            "Saldo": resultBalance
        }

        dfBCountie = pd.DataFrame(dataCountie)
        dfBCountie = dfBCountie.sort_values(by="Saldo", ascending=False)

        quartil_100to75 = dfBCountie['Saldo'].quantile(0.75)
        quartil_75to50 = dfBCountie['Saldo'].quantile(0.50)
        quartil_50to25 = dfBCountie['Saldo'].quantile(0.25)

        reportCountiesAdapter = ReportCountiesAdapter(
            dfBCountie,
            self.year,
            quartil_100to75,
            quartil_75to50,
            quartil_50to25
        )
        reportCountiesAdapter.adapterToReport()

        return dfBCountie

    def removeMissingCities(self, receitas: pd.DataFrame, despesas: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        ids_comuns = pd.merge(
            receitas[["Instituição"]],
            despesas[["Instituição"]],
            on="Instituição",
            how="inner",
        )["Instituição"]
        # Filtrando os DataFrames para manter apenas os valores que estão na interseção
        receitas_filtrado = receitas[
            receitas["Instituição"].isin(ids_comuns)
        ].reset_index(drop=True)
        despesas_filtrado = despesas[
            despesas["Instituição"].isin(ids_comuns)
        ].reset_index(drop=True)
        return receitas_filtrado, despesas_filtrado
