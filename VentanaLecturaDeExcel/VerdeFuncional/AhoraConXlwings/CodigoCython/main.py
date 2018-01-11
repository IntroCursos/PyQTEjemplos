import Verde


if __name__ == "__main__":
    verde = Verde.verde()
    verde.CargarDatos('./info.xlsx')
    verde.Optimiza()
    verde.GuardarDatos()
 


