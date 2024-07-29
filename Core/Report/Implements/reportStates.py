from typing import List
from Core.Report.reportInterface import ReportInterface

class ReportStates(ReportInterface):

    def __init__(
            self,
            states: List[str],
            budget: List[float],
            expense: List[float],
            result: List[float],
            year: int
        ):
        self.states = states
        self.budget = budget
        self.expense = expense
        self.result = result
        self.year = year
    
    def createReport(self) -> None:
        report = 'files/reports/reportStates' + str(self.year) + '.txt'
        try:
            file = open(report, 'w+', encoding='utf-8')
            line = file.readlines()
            cont = 0
            while len(self.states) > cont:
                percentage = (100*self.result[cont])/self.budget[cont]
                line.append(
                    f"{self.states[cont]} \n"
                    + f"Arrecadação: {self.budget[cont]:.2f} \n"
                    + f"Gastos: {self.expense[cont]:.2f} \n"
                    + f"Saldo orçamentario: {self.result[cont]:.2f} "
                    + f"({percentage:.2f}%) da arrecadação\n"
                    + '---------------------------------- \n')
                cont += 1
            file.writelines(line)
        
        except IOError:
            print('Arquivo inexistente!')
        
        except Exception as erro:
            print('Erro: ', erro)
        
        finally:
            file.close()
        