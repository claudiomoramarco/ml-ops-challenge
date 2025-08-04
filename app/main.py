import joblib
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

#qui iris
from app.models.payload import IrisPayload
app = FastAPI(title="Iris API")
Instrumentator().instrument(app).expose(app)
model = joblib.load("app/model.joblib")

@app.get("/health", status_code=200)
def health_check():
    """Endpoint per lo stato del ."""
    return {"status": "ok"}

@app.post("/predict")
def predict(payload: IrisPayload):
    """Esegue la predizione sulla base delle caratteristiche feature ricevute."""
    predictions = model.predict(payload.features)
    #esempio tipo 
    iris_target_names = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
    prediction_labels = [iris_target_names[p] for p in predictions]
    
    return {"predictions": prediction_labels}