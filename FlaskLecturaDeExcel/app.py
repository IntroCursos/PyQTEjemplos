from flask import Flask, render_template,request

import pandas as pd
import numpy as np
import Verde

app = Flask(__name__)

#Objecto de la clase verde
verde = Verde.verde()
verde.CargarDatos()
verde.Optimiza()

def Crear_Tabla(nombre):
    verde.CargarDatos()
    df = verde.Datos[nombre]
    s= render_template("index.html",nombre=nombre,tabla=df.to_html())
    return unescape (s)

def unescape(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")     # this has to be last:
    s = s.replace("&amp;", "&")
    return s

@app.route("/Varproducto",methods=["GET","POST"])
def Varproducto():
    if request.method == "POST":
        age= request.form["age"]

        return render_template('age.html',age=age)
    return Crear_Tabla("Varproducto")

@app.route("/Contribucion",methods=["GET","POST"])
def Contribucion():
    if request.method == "POST":
        age= request.form["age"]

        return render_template('age.html',age=age)

    return Crear_Tabla("contribucion")



@app.route("/Requerimientos",methods=["GET","POST"])
def Requerimientos():
    if request.method == "POST":
        age= request.form["age"]

        return render_template('age.html',age=age)

    return Crear_Tabla("requeri")


@app.route("/Inventario",methods=["GET","POST"])
def Inventario():
    if request.method == "POST":
        age= request.form["age"]

        return render_template('age.html',age=age)

    return Crear_Tabla("Inventario")



@app.route("/Resultado",methods=["GET","POST"])
def Resultado():
    if request.method == "POST":
        age= request.form["age"]

        return render_template('age.html',age=age)
    verde.CargarDatos()
    verde.Optimiza()
    df = verde.DataFrame_Resultado
    s= render_template("index.html",nombre="Resultado",tabla=df.to_html())
    return unescape (s)


if __name__ == "__main__":
    #app.run()
    app.run(debug=True)
