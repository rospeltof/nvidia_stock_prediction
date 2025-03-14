Este proyecto tiene como objetivo predecir el precio de cierre del día siguiente para las acciones de Nvidia utilizando un modelo de regresión lineal (baseline). Además, se ha implementado un pipeline de preprocesamiento e inferencia que integra la descarga de datos, el cálculo de indicadores técnicos y la generación de predicciones. Se utilizan herramientas como MLflow para el seguimiento de experimentos y Docker para facilitar el despliegue reproducible del código.
Tabla de Contenidos

    Visión General
    Estructura del Proyecto
    Requerimientos
    Pipeline de Preprocesamiento e Inferencia
    Entrenamiento del Modelo
    Ejecución de Predicciones
    Uso de Docker
    Notas Adicionales

Visión General

El proyecto se desarrolla para predecir el precio de cierre de Nvidia para el día siguiente a partir de datos diarios descargados de Yahoo Finance. Se calculan diversos indicadores técnicos (RSI, MACD, Bollinger Bands, Stochastic Oscillator, etc.) y se aplican transformaciones a las variables para mejorar la calidad de las features. Se optó por un modelo de regresión lineal por su simplicidad, interpretabilidad y buen desempeño en comparación con modelos de boosting más complejos, que mostraban tendencia al sobreajuste.

El pipeline de inferencia se ha dockerizado para facilitar su despliegue y garantizar la reproducibilidad del entorno, permitiendo que otros usuarios puedan ejecutar el proceso end-to-end sin configuraciones adicionales.
Estructura del Proyecto

La estructura del repositorio es la siguiente:

nvidia_stock_prediction/
├── Dockerfile

├── README.md

├── requirements.txt

├── mlruns/      # Carpeta para experimentos MLflow (se genera y actualiza)

├── src/

│   ├── train_baseline.py  # Script de entrenamiento del modelo (regresión lineal)

│   └── run_pipeline.py    # Pipeline de inferencia end-to-end (descarga, TA, preprocesamiento, predicción)

├── notebooks/            # Notebooks de experimentación y desarrollo

└── data/

    ├── ABTs/            # Archivos de ABT generados durante el preprocesamiento
    
    └── predicciones/    # Resultados de las predicciones

Requerimientos

Las principales dependencias del proyecto son:

    Python 3.9 (u otra versión compatible)
    numpy
    pandas
    yfinance
    ta
    scikit-learn
    mlflow
    catboost (si se utiliza en otros experimentos, opcional)

Las dependencias estan en  requirements.txt.

numpy>=1.21.0
pandas>=1.3.0
yfinance>=0.2.20
ta>=0.10.2
scikit-learn>=1.0.2
mlflow>=2.3.0


## Pipeline de Preprocesamiento e Inferencia

El pipeline de inferencia está implementado en el archivo src/run_pipeline.py e incluye:

    Descarga de Datos:
    Se descargan datos de los tickers NVDA, ^GSPC y SMH de Yahoo Finance para los últimos 60 días (la fecha final se fija manualmente para pruebas).

    Cálculo de Indicadores Técnicos:
    Se calculan indicadores como RSI, MACD (y sus componentes), Bollinger Bands, Stochastic Oscillator, y se agregan variables temporales (Año, Mes, Día de la semana).

    Preprocesamiento:
    Se aplican transformaciones (por ejemplo, logaritmo en columnas con alta asimetría y transformación de 'macd') mediante la clase DataProcessor.

    Inferencia:
    Se carga el modelo previamente guardado (en formato pickle en la carpeta models) y se realizan predicciones. Se asume que el modelo está entrenado para predecir el precio de cierre del día siguiente. Además, se guarda un CSV con las predicciones y la fecha de cada registro.

Entrenamiento del Modelo

El modelo baseline (regresión lineal) se entrena a partir de un ABT generado previamente (archivo CSV en la carpeta data/ABTs). El script de entrenamiento se encuentra en src/train_baseline.py y registra los experimentos en MLflow. La elección del modelo de regresión lineal se justificó por su simplicidad y buen desempeño en comparación con modelos de boosting que presentaban sobreajuste.
Ejecución de Predicciones

Para realizar las predicciones (inferir el precio de cierre de mañana), sigue estos pasos:

    Actualiza la variable end_date en src/run_pipeline.py para fijar manualmente la fecha final (por ejemplo, "2025-03-12").
    Ejecuta el script de inferencia para que descargue y procese los datos, cargue el modelo y genere las predicciones.
    Desde la raíz del proyecto:

    python src/run_pipeline.py

    Revisa el archivo CSV generado en la carpeta data/predicciones/ para ver los resultados, que incluirán la fecha de predicción y el precio predicho para el día siguiente.


Construir y Ejecutar la Imagen Docker

Desde la raíz del proyecto, ejecuta los siguientes comandos:

    Construir la imagen:

docker build -t nvidia_stock_prediction .

Ejecutar el contenedor: Para ejecutar el script de inferencia (y montar la carpeta mlruns si es necesario):

docker run -v $(pwd)/mlruns:/app/mlruns nvidia_stock_prediction

Con esto, el contenedor usará la carpeta mlruns de tu host, y el script de inferencia cargará el modelo correctamente.
