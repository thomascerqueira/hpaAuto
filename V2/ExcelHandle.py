import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import os

Types = ["Réglé", "Sécurité", "Mutuelle", "Non réglé", "Pas d'écriture", "Nom Mutuelle"]
TypesMUT = ["Payé", "Non payé", "Mutuelle"]

def findInArray(array, value):
    for i in range(len(array)):
        if value == array[i]:
            return i
    return -1

class ExcelHandle:
    realType = []

    def writeInCell(self, worksheet, row, col, value):
        cell = xl_rowcol_to_cell(row, col)
        worksheet.write(cell, value)
    
    def writeFormula(self, worksheet, row, col, value):
        cell = xl_rowcol_to_cell(row, col)
        worksheet.write_formula(cell, value)

    def writePatients(self, workbook, worksheet, patients, code):
        actual = 1
        formatCoche = workbook.add_format()
        formatFit = workbook.add_format()

        formatCoche.set_align('right')
        formatFit.set_align('left')
        formatFit.set_shrink()
        worksheet.write('A1', 'Dossier')
        for i in range(len(self.realType)):
            cell = xl_rowcol_to_cell(0, i + 1)
            worksheet.write(cell, self.realType[i], formatFit)

        for patient in patients:
            cell = xl_rowcol_to_cell(actual, 0)
            worksheet.write(cell, patient["Code"], formatFit)
            cell = xl_rowcol_to_cell(actual, findInArray(self.realType, patient["Type"]) + 1)
            worksheet.write(cell, "x", formatCoche)
            if code == 2:
                self.writeInCell(worksheet, actual, 3, patient["Mut"])
            else:
                self.writeInCell(worksheet, actual, 6, patient["Mut"])
            actual += 1

    def writeTOTAL(self, worksheet, actual, tab):
        for i in range(len(tab)):
            topCell = xl_rowcol_to_cell(1, i + 1)
            endCell = xl_rowcol_to_cell(actual - 1, i + 1)
            form = "=COUNTA(" + topCell + ":" + endCell + ')'
            self.writeFormula(worksheet, actual, i + 1, form)
        topCell = xl_rowcol_to_cell(actual, 1)
        endCell = xl_rowcol_to_cell(actual, len(tab))
        form = "=SUM(" + topCell + ":" + endCell + ")"
        self.writeFormula(worksheet, actual, len(tab) + 1, form)

    def writeInFile(self, path, patients, tab, code):
        try:
            os.mkdir("Résultats")
        except:
            pass
        name = ((path.split('/'))[-1].split('.'))[0]
        if code == 1:
            newPath = "Résultats/" + name + ".xlsx"
            self.realType = Types.copy()
        elif code == 2:
            newPath = "Résultats/" + name + "_MUT.xlsx"
            self.realType = TypesMUT.copy()
        workbook = xlsxwriter.Workbook(newPath)
        worksheet = workbook.add_worksheet()
        self.writePatients(workbook, worksheet, patients, code)
        self.writeTOTAL(worksheet, len(patients) + 1, tab)
        workbook.close()