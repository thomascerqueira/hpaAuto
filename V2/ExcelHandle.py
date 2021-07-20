from re import T
from typing import Type
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

def findInArray(array, value):
    for i in range(len(array)):
        if value == array[i]:
            return i
    return -1

class ExcelHandle:
    Types = ["Réglé", "Sécurité", "Mutuelle", "Non réglé", "Pas d'écriture"]

    def writeInCell(self, worksheet, row, col, value):
        cell = xl_rowcol_to_cell(row, col)
        worksheet.write(cell, value)
    
    def writeFormula(self, worksheet, row, col, value):
        cell = xl_rowcol_to_cell(row, col)
        worksheet.write_formula(cell, value)

    def writeInFile(self, path, patients, regle, secu, mut, nr, pe):
        tab = [regle, secu, mut, nr, pe]
        actual = 1
        name = ((path.split('/'))[-1].split('.'))[0]

        workbook = xlsxwriter.Workbook(name + ".xlsx")
        worksheet = workbook.add_worksheet()

        worksheet.write('A1', 'Dossier')
        for i in range(len(self.Types)):
            cell = xl_rowcol_to_cell(0, i + 1)
            worksheet.write(cell, self.Types[i])

        for patient in patients:
            cell = xl_rowcol_to_cell(actual, 0)
            worksheet.write(cell, patient["Code"])
            cell = xl_rowcol_to_cell(actual, findInArray(self.Types, patient["Type"]) + 1)
            worksheet.write(cell, "x")
            actual += 1

        for i in range(len(tab)):
            topCell = xl_rowcol_to_cell(1, i + 1)
            endCell = xl_rowcol_to_cell(actual - 1, i + 1)
            form = "=NBVAL(" + topCell + ":" + endCell + ')'
            self.writeInCell(worksheet, actual, i + 1, form)
        workbook.close()

