import numpy as np
import pandas as pd
import pyomo.environ as pyomo
from pyomo.environ import *
import xlwings as xw

class verde(object):

    #def __init__(self):
    #    print("Iniciando la clase verde")

    def read_excel(self,filename="VerdeReducido2.xlsx"):
        wb = xw.Book(filename)
        
        try:
            sht = wb.sheets['Resultado']
        except:
            wb.sheets.add("Resultado")
        
        producto = wb.sheets["Producto"].range('A1').options(pd.DataFrame, expand='table',dtype="float64").value
        contribucion = wb.sheets["Contribucion"].range('A1').options(pd.DataFrame, expand='table').value
        requerimientos = wb.sheets["Balance"].range('A1').options(pd.DataFrame, expand='table').value
        Inventario = wb.sheets["Inventario"].range('A1').options(pd.DataFrame, expand='table').value
        Restricciones = wb.sheets["Restricciones"].range('A1').options(pd.DataFrame, expand='table').value


        data = {
            'Varproducto': producto,
            'contribucion': contribucion,
            'requeri': requerimientos,
            'Inventario': Inventario,
            "Restricciones":Restricciones}

        self.WB= wb
        return data

    def read_excel_old(self, filename="VerdeReducido2.xlsx"):
        """Read special Excel spreadsheet to input dict.

        Args:
            filename: path to a spreadsheet file

        Returns
            dict of DataFrames, to be passed to create_model()
        """
        with pd.ExcelFile(filename) as xls:
            producto = xls.parse('Producto').set_index('Materiales')
            contribucion = xls.parse('Contribucion').set_index('Materiales')
            requerimientos = xls.parse('Balance').set_index("Abreviaturas")
            Inventario = xls.parse('Inventario').set_index("Materiales")

        data = {
            'Varproducto': producto,
            'contribucion': contribucion,
            'requeri': requerimientos,
            'Inventario': Inventario}

        return data

    def CargarDatos(self,path='./VerdeReducido2.xlsx'):
        self.Datos = self.read_excel(path)

       
    def GuardarDatos(self):
        sht = self.WB.sheets["Resultado"]
        sht.range('A1').value = self.DataFrame_Resultado
       

    def Optimiza(self):
        #Generar un try y catch para ver si ya se cargo los datos o poner otros
        #Datos = read_excel('./VerdeReducido2.xlsx')
        Datos = self.Datos
        Datos["Varproducto"].fillna(0,inplace=True)
        Datos["contribucion"].fillna(0,inplace=True)
        Datos["requeri"]= Datos["requeri"][ Datos["requeri"]["MAX"]!= 0]
        #Datos["requeri"] # Eliminando variables
        # Variables a optimizar pollo carne arroz etc.
        Ingredients =  list(Datos["Varproducto"].index)
        #Ingredients
        Varproducto = Datos["Varproducto"]
        #Restriccion de minerales
        RestriMinerales = Datos["Inventario"][Datos["Inventario"]["MineralSiNo"]>0].index

        model = ConcreteModel(name="The Verde Problem")

        model.ingredient_vars = Var(Ingredients, bounds=(0,None), doc="The amount of each ingredient that is used")

        model.obj = Objective(expr=sum(Varproducto.Precio[i]*model.ingredient_vars[i] for i in Ingredients)/sum(model.ingredient_vars[i]*Datos["contribucion"]["Eficiencia"][i]  for i in Ingredients) ,sense=minimize, doc="Total Cost of Ingredients per can")

        #Restriccion de kg finales entonces depende de la eficiencia
        # Hay que modificar.
        model.c0 = Constraint(expr=sum(model.ingredient_vars[i]*Datos["contribucion"]["Eficiencia"][i]  for i in Ingredients) <= Datos["Restricciones"].loc["Kg"][1], doc="PercentagesSum")
        model.c02 = Constraint(expr=sum(model.ingredient_vars[i]*Datos["contribucion"]["Eficiencia"][i]  for i in Ingredients) >= Datos["Restricciones"].loc["Kg"][0], doc="PercentagesSum2")

        ### Restriccion dekg para los minerales sean menores a 1400
       
        if len(RestriMinerales)>0:
            #Con la eficiencia se calcula el kg
            #model.c03 = Constraint(expr=sum(model.ingredient_vars[i]*Datos["contribucion"]["Eficiencia"][i]  for i in RestriMinerales) <= Datos["Restricciones"].loc["Mineral"][1], doc="PercentagesSum3")
            #model.c04 = Constraint(expr=sum(model.ingredient_vars[i]*Datos["contribucion"]["Eficiencia"][i]  for i in RestriMinerales) >= Datos["Restricciones"].loc["Mineral"][0], doc="PercentagesSum4")
            model.c03 = Constraint(expr=sum(model.ingredient_vars[i]  for i in RestriMinerales) <= Datos["Restricciones"].loc["Mineral"][1], doc="PercentagesSum3")
            model.c04 = Constraint(expr=sum(model.ingredient_vars[i]  for i in RestriMinerales) >= Datos["Restricciones"].loc["Mineral"][0], doc="PercentagesSum4")        
        
        
        
        composicionesQ = list(Datos["requeri"].index)
        self.composicionesQ =composicionesQ
        #you can use rules to construct the constraints for all p \in P.

        def constraint1_ruleMin(m,p):
        #    return sum(Datos["contribucion"][p][i] * model.ingredient_vars[i] for i in Ingredients) >= Datos["requeri"]["MIN"][p]
            return ( (sum(Datos["contribucion"][p][i] * model.ingredient_vars[i]*Datos["contribucion"]["Eficiencia"][i] for i in Ingredients)/
                              (sum( model.ingredient_vars[i]*Datos["contribucion"]["Eficiencia"][i] for i in Ingredients)) )/100
                              >= Datos["requeri"]["MIN"][p])

        #model.c1 = Constraint([p for p in Ps],rule=constraint2_rule)

        def constraint1_ruleMax(m,p):
        #   return sum(Datos["contribucion"][p][i] * model.ingredient_vars[i] for i in Ingredients) <= Datos["requeri"]["MAX"][p]
            return ( (sum(Datos["contribucion"][p][i] * model.ingredient_vars[i]*Datos["contribucion"]["Eficiencia"][i] for i in Ingredients)/
                              (sum( model.ingredient_vars[i]*Datos["contribucion"]["Eficiencia"][i] for i in Ingredients)) )/100
                              <= Datos["requeri"]["MAX"][p])


        def constraint1_ruleInventario(m,p):
            return (model.ingredient_vars[p]  <= Datos["Inventario"]["Kgs"][p])

        model.c1 = Constraint(composicionesQ,rule=constraint1_ruleMin)

        model.c2 = Constraint(composicionesQ,rule=constraint1_ruleMax)

        model.c3 = Constraint(Ingredients,rule=constraint1_ruleInventario)

        solver = SolverFactory('ipopt')
        #status = solver.solve(model,tee=True)
        status = solver.solve(model)

        """
        print("Status = %s" % status.solver.termination_condition)

        for i in Ingredients:
            print("%s = %f" % (model.ingredient_vars[i], value(model.ingredient_vars[i])))

        print("Objective = %f" % value(model.obj))
        """

        ing = []
        canIng = []
        ing.append("Status = ")
        canIng.append(str(status.solver.termination_condition) )
        for i in Ingredients:
            ing.append(str(model.ingredient_vars[i]).replace("ingredient_vars[","").replace("]",""))
            canIng.append( round( float(value(model.ingredient_vars[i])) ,4) )

        ing.append("Objective = ")
        canIng.append(str(value(model.obj)))
        self.DataFrame_Resultado = pd.DataFrame(canIng,ing,columns=["Cantidad"])
        #return pd.DataFrame(canIng,ing,columns=["Cantidad"])
        
#    def GuardarTablaRequeri(self):

        indx=20
        sht = self.WB.sheets["Balance"]
        for p in composicionesQ:
            tmp =(sum(Datos["contribucion"][p][i] * value(model.ingredient_vars[i])* Datos["contribucion"]["Eficiencia"][i] for i in Ingredients)/ (sum(value(model.ingredient_vars[i])* Datos["contribucion"]["Eficiencia"][i] for i in Ingredients)  ) )/100
            #print("%s -> %f <= %f<= %f" % (p,Datos["requeri"]["MIN"][p] ,tmp, Datos["requeri"]["MAX"][p] ) )    
            sht.range('B'+str(indx)).value= (p,Datos["requeri"]["MIN"][p] ,tmp, Datos["requeri"]["MAX"][p] )
            indx+=1        

