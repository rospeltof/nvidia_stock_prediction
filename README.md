# Predicción del Precio de Acciones de Nvidia con Regresión Lineal (Baseline)

Este proyecto tiene como objetivo predecir el precio de cierre del día siguiente para las acciones de Nvidia utilizando un modelo de regresión lineal (baseline). Se ha implementado un pipeline de inferencia dockerizado para facilitar el despliegue y garantizar la reproducibilidad del entorno, permitiendo que otros usuarios puedan ejecutar el proceso end-to-end sin configuración adicional.

---

## Tabla de Contenidos

- [Visión General](#visión-general)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requerimientos](#requerimientos)
- [Pipeline de Preprocesamiento e Inferencia](#pipeline-de-preprocesamiento-e-inferencia)
- [Entrenamiento del Modelo](#entrenamiento-del-modelo)
- [Ejecución de Predicciones](#ejecución-de-predicciones)
- [Uso de Docker](#uso-de-docker)
- [Notas Adicionales](#notas-adicionales)

---

## Visión General

El proyecto se desarrolla para predecir el precio de cierre de Nvidia para el día siguiente utilizando datos diarios descargados desde Yahoo Finance. Se calculan diversos indicadores técnicos (RSI, MACD, Bollinger Bands, entre otros) que se usan para entrenar y evaluar un modelo baseline de regresión lineal.

El pipeline completo está dockerizado para asegurar que cualquier usuario pueda reproducir el entorno fácilmente.

---

## Estructura del Proyecto

```bash
nvidia_stock_prediction/
├── Dockerfile
├── README.md
├── requirements.txt
├── mlruns/            # Experimentos MLflow (generado automáticamente)
├── models/            # Modelos guardados
├── notebooks/         # Notebooks de exploración
├── data/
│   ├── ABTs/          # ABT generados en preprocesamiento
│   └── predicciones/  # Resultados de las predicciones
└── src/
    └── run_pipeline.py    # Pipeline completo (descarga, TA, predicción)
```

## Requerimientos

Las principales dependencias del proyecto son:

- Python 3.9 (u otra versión compatible)
- numpy
- pandas
- yfinance
- ta
- scikit-learn
- mlflow
- catboost (*opcional*)

Todas las dependencias se encuentran especificadas en `requirements.txt`:

```bash
numpy>=1.21.0
pandas>=1.3.0
yfinance>=0.2.20
ta>=0.10.2
scikit-learn>=1.0.2
mlflow>=2.3.0
```
## Crear en docker y hacer inferencia
1. Crear el contenedor
   
```bash
docker build -t nvidia_stock_prediction .
```
2. Correr el archivo de inferencia
   
```bash
docker run -v $(pwd)/mlruns:/app/mlruns nvidia_stock_prediction python src/run_pipeline.py
```

