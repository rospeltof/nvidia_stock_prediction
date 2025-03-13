import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import yfinance as yf
import ta  
import mlflow
import mlflow.sklearn

class DataProcessor(object):
    def __init__(self):
        self.keep_cols = ['Date', 'Close_NVDA', 'High_NVDA', 'Low_NVDA', 'Open_NVDA', 'Volume_NVDA',
                          'Close_SMH', 'Close_^GSPC', 'Volume_SMH', 'Volume_^GSPC', 
                          'rsi', 'macd', 'macd_diff', 'stoch_k', 'stoch_d', 'Month', 'Dayofweek', 'Year']
        self.skewed_cols = ['Volume_NVDA', 'Volume_SMH', 'Volume_^GSPC', 'Close_SMH']
        
    def preprocess_data(self, df):
        df = df.copy()
        if 'Date' not in df.columns:
            df['Date'] = df.index
        df = df[self.keep_cols]
        df.dropna(inplace=True)
        # Transformación logarítmica en columnas con alta asimetría
        for col in self.skewed_cols:
            df[col] = np.log1p(df[col])
        # Transformación logarítmica con signo en 'macd'
        df['macd'] = np.sign(df['macd']) * np.log1p(np.abs(df['macd']))
        return df

def download_and_prepare_data(tickers, start_date, end_date):
    # Descarga de datos desde yfinance
    data = yf.download(tickers, start=start_date, end=end_date)
    # Aplanar las columnas (MultiIndex)
    data.columns = data.columns.map(lambda x: f"{x[0]}_{x[1]}")
    
    # Calcular indicadores técnicos para NVDA
    data['rsi'] = ta.momentum.RSIIndicator(close=data['Close_NVDA'], window=14).rsi()
    
    macd = ta.trend.MACD(close=data['Close_NVDA'])
    data['macd'] = macd.macd()
    data['macd_signal'] = macd.macd_signal()
    data['macd_diff'] = macd.macd_diff()
    
    bb = ta.volatility.BollingerBands(close=data['Close_NVDA'], window=20, window_dev=2)
    data['bb_mavg'] = bb.bollinger_mavg()    
    data['bb_high'] = bb.bollinger_hband()     
    data['bb_low'] = bb.bollinger_lband()
    
    stoch = ta.momentum.StochasticOscillator(
        high=data['High_NVDA'],
        low=data['Low_NVDA'],
        close=data['Close_NVDA'],
        window=14,
        smooth_window=3
    )
    data['stoch_k'] = stoch.stoch()
    data['stoch_d'] = stoch.stoch_signal()
    
    # Agregar columnas temporales basadas en la fecha
    data['Year'] = data.index.year
    data['Month'] = data.index.month
    data['Dayofweek'] = data.index.day_of_week
    
    return data

def main():
    # Fijamos manualmente la fecha de fin para pruebas
    end_date = "2025-03-12"  
    start_date = (datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=60)).strftime("%Y-%m-%d")
    
    tickers = ['NVDA', '^GSPC', 'SMH']
    data = download_and_prepare_data(tickers, start_date, end_date)
    
    processor = DataProcessor()
    data_processed = processor.preprocess_data(data)
    
    # En inferencia, usamos todas las columnas preprocesadas que se utilizaron en el entrenamiento.
    # Si entrenaste con un subconjunto, asegúrate de seleccionar las mismas.
    # Por ejemplo, si tu modelo se entrenó usando todas las columnas en self.keep_cols:
    features = processor.keep_cols.copy()
    # Elimina la columna 'Date' si no fue usada en entrenamiento:
    if 'Date' in features:
        features.remove('Date')
    
    X_new = data_processed[features].copy()
    
    # Cargar el modelo final registrado en MLflow. 
    # Reemplaza <RUN_ID> con el identificador real del run donde se guardó el modelo.
    model_uri = "runs:/<926805478441575022>/model"
    model = mlflow.sklearn.load_model(model_uri)
    
    # Realizar la predicción
    predictions = model.predict(X_new)
    print("Predicciones:")
    print(predictions)
    
    # Guardar las predicciones en un CSV
    output_path = os.path.join('..', 'data', 'predicciones', f"predicciones_{end_date}.csv")
    X_new['Predicted'] = predictions
    X_new.to_csv(output_path, index=False)
    print("Predicciones guardadas en:", output_path)

if __name__ == "__main__":
    main()