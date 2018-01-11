import Verde
import pandas as pd

import xlwings as xw

if __name__ == "__main__":
    verde = Verde.verde()
    verde.CargarDatos('./info.xlsx')
    verde.Optimiza()

    
    writer = pd.ExcelWriter('info.xlsx', engine='xlsxwriter')
    writer = pd.ExcelWriter('info.xlsx', engine='openpyxl')
    verde.DataFrame_Resultado.to_excel(writer, sheet_name='resul')
    writer.save()


