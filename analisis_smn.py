def viento(campo_viento):
    """ 
    convierte el dato 'Norte 3' en ('Norte', 3.0).
    en caso de que sea 'Calma', se le asignara un valor de 0.0
    """
    campo_viento = campo_viento.strip()

    if campo_viento.lower() == 'calma':
        return("Calma", 0.0)
    partes= campo_viento.split()

    if len(partes) == 2:
        v_texto = partes [-1]
        dire= " ".join(partes[:-1])
        try:
            velo= float(v_texto)
            return(dire, velo)
        except ValueError:
            return(campo_viento, None)
    return(campo_viento, None)

if __name__ == "__main__":
    print(viento("Sur 5"))
    print(viento("Calma"))
