from typing import List, Dict, Any
import numpy as np

from Core.Report.reportInterface import ReportInterface

class ReportCounties(ReportInterface):

    def __init__(
            self,
            counties: np.ndarray,
            budget: np.ndarray,
            expense: np.ndarray,
            population: np.ndarray,
            balance: np.ndarray,
            year: int,
            quartil_100to75: int,
            quartil_75to50: int,
            quartil_50to25: int

        ):
        self.counties = counties
        self.budget = budget
        self.expense = expense
        self.population = population
        self.balance = balance
        self.year = year
        self.quartil_100to75 = quartil_100to75
        self.quartil_75to50 = quartil_75to50
        self.quartil_50to25 = quartil_50to25
    
    def createReport(self) -> None:
        report = 'files/reports/reportCounties' + str(self.year) + '.txt'
        try:
            with open(report, 'w+', encoding='utf-8') as file:
                cont = 0
                prejuizo = 0
                lucro = 0
                lines = []
                while len(self.counties) > cont:
                    PIB = float(self.budget[cont].replace(",", ".")) / float(self.population[cont])
                    if self.balance[cont] > 0:
                        lucro += 1
                    elif self.balance[cont] < 0:
                        prejuizo += 1
                    lines.append(
                        f"{self.counties[cont]} \n"
                        + f"Arrecadação: {self.budget[cont]} \n"
                        + f"Gastos: {self.expense[cont]} \n"
                        + f"Saldo orçamentário: {self.balance[cont]:.2f} \n"
                        + f"Arrecadação per capita do município: {PIB:.2f} \n"
                        + f"Posição do município: {self.determinar_quartil(self.balance[cont], self.quartil_100to75, self.quartil_75to50, self.quartil_50to25)} \n"
                        + '---------------------------------- \n'
                    )
                    cont += 1
                lines.append(f"Total de municípios com superávit Orçamentário: {lucro} \n")
                lines.append(f"Total de municípios com déficit Orçamentário: {prejuizo} \n")
                file.writelines(lines)
        
        except IOError:
            print('Arquivo inexistente!')
        
        except Exception as erro:
            print('Erro: ', erro)
        
        finally:
            file.close()

    
    def determinar_quartil(self, valor: float, q1: float, q2: float, q3: float) -> str:
        if valor <= q1:
            return 'Entre os 25% piores'
        elif valor <= q2:
            return 'Entre os 25 e os 50%'
        elif valor <= q3:
            return 'Entre os 50 e os 75%'
        else:
            return 'Entre os 25% melhores'   
