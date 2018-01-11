from multiprocessing import Pool
from flask import Flask, render_template,request
import Verde

app = Flask(__name__)
_pool = None
verde = Verde.verde()

#http://wiki.glitchdata.com/index.php/Flask:_Multi-Processing_in_Flask

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

@app.route("/",methods=["GET","POST"])
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

    print ("De seguro Inicia aqui")
    f = _pool.apply_async(expensive_function)
    df = f.get(timeout=2)
    s= render_template("index.html",nombre="Resultado",tabla=df.to_html())
    print ("De seguro llega aqui")
    return unescape(s)



def expensive_function():
        # import packages that is used in this function
        # do your expensive time consuming process
        verde.CargarDatos()
        verde.Optimiza()
        df = verde.DataFrame_Resultado
        return df
        #return x*x


if __name__=='__main__':
        _pool = Pool(processes=4)
        try:
                # insert production server deployment code
                #app.run()
                app.run(host = '0.0.0.0',port=5005)
                #app.run(debug=True)
        except KeyboardInterrupt:
                _pool.close()
                _pool.join()
