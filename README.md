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

