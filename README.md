# PaqueteAnePY

**Paquete de Python para análisis matemático y estadístico.**

## Descripción

`PaqueteAnePY` es un proyecto desarrollado en Python que reúne funciones de utilidad para realizar cálculos y trabajar con problemas matemáticos y estadísticos.

Este repositorio contiene el código fuente del paquete, un notebook con ejemplos y una versión HTML para facilitar la consulta de su contenido.

El paquete incluye funciones para:

- discretización de variables
- cálculo de métricas
- normalización y estandarización
- filtrado de variables
- cálculo de correlaciones e información mutua
- representación gráfica de curvas ROC y matrices de correlación.

## Contenido del repositorio

- `FuncionesPY.py`: módulo con las funciones implementadas.
- `PaqueteAnePY.ipynb`: notebook con ejemplos y explicaciones.
- `PaqueteAnePY.html`: versión HTML del notebook.
- `setup.py`: configuración del paquete.
- `LICENSE`: licencia del proyecto.
- `CHANGELOG.md`: historial de cambios.

## Requisitos

- Python 3.
- Las bibliotecas adicionales que necesiten las funciones del paquete (matplotlib, numpy, pandas)

## Instalación

Clona este repositorio:

```bash
git clone https://github.com/anearregi04/PaqueteAnePY
```

Entra en la carpeta del proyecto:

```bash
cd PaqueteAnePY
```

Instala el paquete en modo editable:

```bash
python -m pip install -e .
```

## Uso

Una vez instalado, puedes importar las funciones del módulo desde Python.

Por ejemplo:

```python
from FuncionesPY import nombre_de_la_funcion
```

Sustituye `nombre_de_la_funcion` por el nombre de una función disponible en el módulo.

## Ejemplos y documentación

Consulta `PaqueteAnePY.ipynb` para ver el código y los ejemplos de uso.

También puedes abrir `PaqueteAnePY.html` directamente en un navegador web para leer el contenido sin necesidad de ejecutar el notebook.

## Licencia

Consulta el archivo `LICENSE` para conocer las condiciones de uso y distribución del proyecto.
