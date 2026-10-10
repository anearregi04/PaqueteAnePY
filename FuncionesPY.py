
################################################################################
# En este script se presentan las funciones que se han usado durante los ejercicios del curso #
# *****************************************************************************#
# Autor/a: Ane Arregi Beitia #
# Email: aarregi015@ikasle.ehu.eus #
# Fecha: 17-09-2026 #
################################################################################# 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def discretize (x, cut_points): #La funcion recibe un vector x y una vector con los puntos de corte que se utilizaran para crear los intervalos
    cut_points= sorted(cut_points) #Por si estan desordenados
    limites = np.concatenate(([-np.inf], cut_points, [np.inf])) #Ademas de los puntos definidos, anadimos -Inf e Inf a los puntos de corte para definir los limites inferior y superior de todos los intervalos.
    x_moztuta= pd.cut(x,bins=limites,labels=[f"I{i}" for i in range(1,len(cut_points) +2)]) #Se utiliza la funcion cut() para asignar cada valor de x al intervalo correspondiente. Se crean n+1 intervalos, siendo n la longitud de cut.points, y se etiquetan como I1, I2, ...
    return x_moztuta 



def discretize_dataset (datos,cut_points):
    resultado=datos
    for columna in datos.columns:
        if pd.api.types.is_numeric_dtype(datos[columna]):
            resultado[columna]=discretize(datos[columna],cut_points) #Vamos pasando a la funcion anterior todas las columnas, una a una.
    
    return resultado

def discretizeEW (x,num_bins): #La funcion recibe u vector x tipo numerico y un numero num.bins que indica el numero de intervalos
    x=list(x)
    luzeera= (max(x)-min(x))/num_bins #Calculamos la amplitud de cada rango
    #Creamos vectores y listas vacias que rellenaremos posteriormente
    listaI=[None] * len(x)
    intervalos= [None] * num_bins
    nombres_intervalos=[None] * num_bins
    puntos_corte=[None] * (num_bins-1)


    for i in range(1,num_bins+1):
    #Calculamos los limites inferior y superiores para cada rango
        limite_inf= min(x) + (i-1)*luzeera
        limite_sup = min(x) + (i)*luzeera
        intervalos[i-1]=[limite_inf,limite_sup]

    #Para mejorar la legibilidad del resultado, se quieren indicar los limites correspondientes a cada intervalo. Se tienen que distingir los escenarios de las esquinas para indicar los infinitos. 
        if i==1:
            nombres_intervalos[i-1] = f"I{i} = (-Inf,{limite_sup}]"
        elif i==num_bins:
            nombres_intervalos[i-1] = f"I{i} = ({limite_inf},Inf]"
        else:
            nombres_intervalos[i-1] = f"I{i} = ({limite_inf},{limite_sup}]"

        if i<num_bins:
            puntos_corte[i-1]=limite_sup

    for j, valor in enumerate(x): # j es el contador que indicara en que indice del valor de x estamos
        for contador in range(1, num_bins + 1): #Aqui estamos buscando a que rango pertenece cada elemento.
            inferior, superior = intervalos[contador - 1]
            if valor >= inferior and valor <= superior:
                listaI[j] = f"I{contador}"        

    categorias = [f"I{i}" for i in range(1, num_bins + 1)]
    valores = pd.Categorical(listaI, categories=categorias, ordered=True)
    #Devolvemos una lista con los valores categorizados, los intervalos y los puntos de corte.    
    return {"valores": valores,"intervalos": nombres_intervalos,"puntos de corte": puntos_corte,}



def discretizeEW_dataset(datos, num_bins):
    resultado = datos.copy()
    for columna in datos.columns: #Vamos pasando a la funcion anterior todas las columnas, una a una, comprobando que es numérico
        if pd.api.types.is_numeric_dtype(datos[columna]):
            resultado[columna] = discretizeEW(datos[columna], num_bins)["valores"]
    return resultado


def discretizeEF(x, num_bins=3):
    x = list(x)
    x_ordenado = np.argsort(np.asarray(x), kind="stable") + 1 #Ordenamos el vector para poder sacar mas facilmente los grupos. x.ordenado indica el indice de los valores ordenados.


  #En caso de que el numero de elementos sea multiplo del numero de grupos, todos los grupos tendran los mismos elementos. 
  #Esto lo podemos comprobar mirando el resto de la division. 
    tamano_v = len(x) // num_bins
    resto = len(x) % num_bins

  #Creamos grupos vacios para poder llenarlos con los resultados. 
    resultado = [None] * len(x)
    grupos = [None] * num_bins
    inicio = 1 #Contador que ira de 1 y se le ira sumando el numero de elementos que hay en cada grupo

    for i in range(1, num_bins + 1):

        #Si el grupo numero i es mas grande que (num.bins - resto) significa que ese grupo recibira un elemento extra.
        if i > (num_bins - resto):
            fin = inicio + tamano_v

        #Por ejemplo, si tenemos 7 elementos y queremos hacer 5 grupos.
        #tamano.v=7%/5=1
        #resto=7%%5 =2
        #num.bins-resto = 5-2 = 3
        #Los tres primeros grupos tendran el tamano de tamano.v (1), y los dos ultimos grupos (I4 e I5) tendran un elemento mas (2). 
  
        #Si el numero de elementos es multiplo del numero de grupos, resto sera 0 y todos los grupos tendran el mismo tamano.    
        else:
            fin = inicio + tamano_v - 1

        #Seleccionamos las posiciones de x que corresponden al grupo actual, desde la posicion 'inicio' hasta la posicion 'fin'.
        posiciones_r = x_ordenado[inicio - 1:fin]
        posiciones = [p - 1 for p in posiciones_r]


        for posicion in posiciones: #Asignamos cada valor a su intervalo
            resultado[posicion] = f"I{i}"

        valores_grupo = [x[posicion] for posicion in posiciones]  #Guardamos los valores que forman cada grupo I
        grupos[i - 1] = f"I{i}=(" + ", ".join(str(v) for v in valores_grupo) + ")"
        inicio = fin + 1 #Ahora el nuevo inicio del siguiente grupo sera el siguiente indice del valor "fin" guardado anteriormente

    valores = pd.Categorical(resultado,categories=[f"I{i}" for i in range(1, num_bins + 1)],ordered=True,)
    
    #Devolvemos una lista con los valores categorizados y los grupos formados.
    return {"valores": valores, "grupos": grupos}


def discretizeEF_dataset(datos, num_bins=3):
    resultado = datos.copy()
    for columna in datos.columns:
        if pd.api.types.is_numeric_dtype(datos[columna]): #Vamos pasando a la funcion anterior todas las columnas, una a una.
            resultado[columna] = discretizeEF(datos[columna], num_bins)["valores"]
    return resultado



def entropy(x):
    # Comprobamos que x sea una variable categórica
    if not isinstance(x, pd.Series) or not isinstance(x.dtype, pd.CategoricalDtype):
        raise TypeError("x debe ser una variable discretizada de tipo category")
    
    frecuencias = pd.Series(x).value_counts(sort=False, dropna=False) #nos cuenta las veces que aparece cada variable
    probabilidades = frecuencias / len(x) #Calculamos las probabilidades
    probabilidades = probabilidades[probabilidades > 0] 
    return float(-np.sum(probabilidades * np.log2(probabilidades))) #Aplicamos la formula de la entropia

def varianza(x):
  #Aplicamos la formula para la varianza
    n = len(x)
    media = sum(x) / len(x)
    suma = 0
    for i in range(n):
        suma += (x[i] - media) ** 2
    return (1 / (n - 1)) * suma



def calcular_punto_ROC(datos, num_corte):
    predicho = np.where(datos["valor"] < num_corte, False, True)
    
    #Aplicamos las formulas
    TP = np.sum((predicho == True) & (np.asarray(datos["etiqueta"]) == True))
    FP = np.sum((predicho == True) & (np.asarray(datos["etiqueta"]) == False))
    TN = np.sum((predicho == False) & (np.asarray(datos["etiqueta"]) == False))
    FN = np.sum((predicho == False) & (np.asarray(datos["etiqueta"]) == True))

    TPR = TP / (TP + FN)
    FPR = FP / (FP + TN)
    return {"FPR": FPR, "TPR": TPR}


def integraOptimizada(x, y): #Esta funcion calcula una aproximacion numerica de una integral usando la regla del trapecio
    delta_x = np.diff(np.asarray(x))
    y = np.asarray(y)
    mean_y = (y[1:] + y[:-1]) / 2
    return np.sum(delta_x * mean_y)


def AUC(x, clase):
    datos = pd.DataFrame({"valor": x, "etiqueta": clase})
    cortes = np.linspace(np.min(x), np.max(x), 100) #Para calcular la curva ROC hay que ir cambiando los puntos de corte
    puntos = pd.DataFrame(columns=["FPR", "TPR"]) #Creamos un dataset vacio

    for corte in cortes:
        punto = calcular_punto_ROC(datos, corte) #Para cada punto de corte calculamos el punto 
        puntos.loc[len(puntos)] = [punto["FPR"], punto["TPR"]]

    #Para utilizar la funcion integraOptimizada los puntos tienen que estar ordenados. 
    puntos_ordenados = puntos.sort_values("FPR", kind="stable")
    FPR = puntos_ordenados["FPR"].to_numpy()
    TPR = puntos_ordenados["TPR"].to_numpy()
    auc = integraOptimizada(FPR, TPR)
    return auc


def calcular_metricas(dataset, clase):
    resultados = []
    for nombre in dataset.columns:
        if nombre == clase:
            continue
          #Saltamos la variable clase porque este solamente es para comparar

        x = dataset[nombre] #Accedemos a cada columna individualmente
        if isinstance(x.dtype, pd.CategoricalDtype): #Si esa columna es de tipo factor calculamos la entropia
            resultado = {
                "variable": nombre, "tipo": "discreta", "varianza": np.nan,
                "AUC": np.nan, "entropia": entropy(x)
            }

        elif pd.api.types.is_numeric_dtype(x): # Si la columna es numerica calculamos la varianza y AUC
            resultado = {
                "variable": nombre, "tipo": "continua", "varianza": varianza(x),
                "AUC": AUC(x, dataset[clase]), "entropia": np.nan
            }
        else:
            resultado = {
                "variable": nombre, "tipo": "-", "varianza": np.nan,
                "AUC": np.nan, "entropia": np.nan
            }
        resultados.append(resultado)

    return pd.DataFrame(
        resultados,
        columns=["variable", "tipo", "varianza", "AUC", "entropia"]
    )


def normalizar(x):
    x = np.asarray(x)
    return (x - np.min(x)) / (np.max(x) - np.min(x)) #Aplicamos la formula para normalizar


def normalizar_dataset(datos):
    resultado = datos.copy()
    for columna in datos.columns:
        if pd.api.types.is_numeric_dtype(datos[columna]):
            resultado[columna] = normalizar(datos[columna]) #Aplicamos la funcion normalizar para cada valor numerico del dataset
    return resultado


def estandarizar(x):
    varianza_x = varianza(x)
    media = sum(x) / len(x)
    x_estand = (np.asarray(x) - media) / np.sqrt(varianza_x) #Aplicamos la formula para estandarizar
    return x_estand



def estandarizar_dataset(datos):
    resultado = datos.copy()
    for columna in datos.columns:
        if pd.api.types.is_numeric_dtype(datos[columna]): #comprobamos que es numerico
            resultado[columna] = estandarizar(datos[columna]) #Aplicamos la funcion estandarizar para cada valor numerico del dataset
    return resultado

def filtrado_variables(data, umbral_varianza, umbral_auc, umbral_entropia):
    seleccion = (
        ((data["tipo"] == "continua") & (data["varianza"] > umbral_varianza) & (data["AUC"] > umbral_auc))
        | #Guarda los valores continuos que superan el umbral
        ((data["tipo"] == "discreta") & (data["entropia"] > umbral_entropia))
    )
    return data.loc[seleccion, "variable"].tolist()





def cor_par(x, y):  #Teniendo dos variables nos calcula la correlacion o la informacion mutua
    
    x = pd.Series(x)
    y = pd.Series(y)

    # Variables numéricas:
    if pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y):
        #Comprobar que tienen la misma longitud
        if len(x) != len(y):
            raise ValueError("las dos columnas deben tener la misma longitud")
        
        #Medias
        media_x = sum(x) / len(x)
        media_y = sum(y) / len(y)

        #Calculamos la correlacion de Pearson
        numerador = np.sum((x - media_x) * (y - media_y))
        denominador = np.sqrt(
            np.sum((x - media_x) ** 2) * np.sum((y - media_y) ** 2)
        )
        return numerador / denominador

    # Variables categóricas:
    x_categorica = isinstance(x.dtype, pd.CategoricalDtype) or not pd.api.types.is_numeric_dtype(x)
    y_categorica = isinstance(y.dtype, pd.CategoricalDtype) or not pd.api.types.is_numeric_dtype(y)

    if x_categorica and y_categorica:
        tabla = pd.crosstab(x, y, dropna=False)
        pxy = tabla.to_numpy(dtype=float) / tabla.to_numpy(dtype=float).sum()
        px = pxy.sum(axis=1)
        py = pxy.sum(axis=0)
        mi = 0
        for i in range(pxy.shape[0]):
            for j in range(pxy.shape[1]):
                if pxy[i, j] > 0:
                    mi += pxy[i, j] * np.log(
                        pxy[i, j] / (px[i] * py[j])
                    )
        return mi

    return np.nan #Para los pares numerico-categorico devolvemos NA


def cor_dataset(datos):
    n = datos.shape[1]
    resultado = pd.DataFrame(
        np.nan, index=datos.columns, columns=datos.columns
    ) #Creamos un dataset vacio donde vamos a meter los resultados
    for i in range(n):
        for j in range(n):
            resultado.iloc[i, j] = cor_par(datos.iloc[:, i], datos.iloc[:, j]) #Para cada par, calculamos la correlacion utilizando la funcion cor_par
    return resultado


def grafica_ROC(x, clase):
    #Lo del principio es lo mismo que la funcion AUC()
    datos = pd.DataFrame({"valor": x, "etiqueta": clase})
    cortes = np.linspace(np.min(x), np.max(x), 100)
    puntos = pd.DataFrame(columns=["FPR", "TPR"])

    for corte in cortes:
        punto = calcular_punto_ROC(datos, corte)
        puntos.loc[len(puntos)] = [punto["FPR"], punto["TPR"]]
    
    #Cuando ordenamos los puntos, graficamos: 
    puntos_ordenados = puntos.sort_values("FPR", kind="stable")
    plt.plot(puntos_ordenados["FPR"], puntos_ordenados["TPR"], linestyle="-")
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.title("Curva ROC")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.show()



def plot_correlaciones(datos):
    #Sacamos la matriz de correlaciones utilizando la funcion cor_dataset
    matriz_cor = cor_dataset(datos)
    fig, ax = plt.subplots()

    #Convertimos la matriz a formato largo y anadimos los valores de la matriz 
    valores = matriz_cor.to_numpy(dtype=float)
    
    #Graficamos
    image = ax.imshow(valores, aspect="equal", cmap="bwr", vmin=-1, vmax=1)

    ax.set_xticks(range(len(matriz_cor.columns)))
    ax.set_xticklabels(matriz_cor.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(matriz_cor.index)))
    ax.set_yticklabels(matriz_cor.index)

    for i in range(valores.shape[0]):
        for j in range(valores.shape[1]):
            texto = "" if np.isnan(valores[i, j]) else str(round(valores[i, j], 2))
            ax.text(j, i, texto, ha="center", va="center")

    ax.set_title("Matriz de correlaciones")
    fig.colorbar(image, ax=ax, label="Valor")
    fig.tight_layout()
    plt.show()
