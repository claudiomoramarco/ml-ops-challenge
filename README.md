# MLOps Challenge - API di Classificazione Iris

Questo repository contiene la soluzione completa per la MLOps Challenge. Il progetto implementa un intero ciclo di vita MLOps: dall'addestramento e tracciamento di modelli di classificazione, fino al deployment come API REST containerizzata e gestita tramite una pipeline di CI/CD automatizzata.

## Indice

- [Architettura della Soluzione](#architettura-della-soluzione)
- [Come Eseguire il Progetto](#come-eseguire-il-progetto)
  - [Prerequisiti](#prerequisiti)
  - [1. Setup dell'Ambiente Locale](#1-setup-dellambiente-locale)
  - [2. Addestramento e Tracking dei Modelli](#2-addestramento-e-tracking-dei-modelli)
  - [3. Eseguire l'API Localmente](#3-eseguire-lapi-localmente)
  - [4. Eseguire i Test](#4-eseguire-i-test)
  - [5. Build e Run con Docker](#5-build-e-run-con-docker)
  - [6. Deploy su Kubernetes con Helm](#6-deploy-su-kubernetes-con-helm)
- [Pipeline di CI/CD (GitHub Actions)](#pipeline-di-cicd-github-actions)
- [Scelte Progettuali e Giustificazioni](#scelte-progettuali-e-giustificazioni)

---

## Architettura della Soluzione

- **Addestramento Modello**: Uno script Python (`src/train.py`) addestra due modelli (`LogisticRegression`, `RandomForestClassifier`) e traccia esperimenti, parametri e metriche (incluse quelle di cross-validation) con **MLflow**.
- **API Server**: Un'applicazione **FastAPI** carica il modello scelto e lo espone tramite un endpoint `POST /predict`. Un endpoint `GET /health` fornisce uno status check e `GET /metrics` espone metriche in formato Prometheus.
- **Containerizzazione**: Un **Dockerfile** multi-stage ottimizzato per creare un'immagine di produzione leggera e sicura.
- **Deployment**: Una **chart Helm** parametrizzata (`charts/mlops-api`) per un deployment declarativo e ripetibile su Kubernetes.
- **Testing**:
  - **Test Funzionali**: `pytest` viene utilizzato per testare gli endpoint dell'API e validarne il comportamento.
  - **Stress Test**: `Locust` viene utilizzato per simulare il carico degli utenti e valutare la stabilità e le performance dell'API.
- **CI/CD**: Una pipeline **GitHub Actions** (`.github/workflows/ci.yml`) automatizza l'intero processo di validazione ad ogni push/pull request, includendo: linting, testing, build, scansione di sicurezza dell'immagine con Trivy e push su GitHub Container Registry.

---

## Come Eseguire il Progetto

### Prerequisiti

- Python 3.9+
- Docker
- Rancher Desktop (o un altro cluster Kubernetes locale)
- Helm
- Git

### 1. Setup dell'Ambiente Locale

```bash
# Clona il repository
git clone [https://github.com/claudiomoramarco/ml-ops-challenge.git](https://github.com/claudiomoramarco/ml-ops-challenge.git)
cd ml-ops-challenge

# Crea e attiva un ambiente virtuale
python3 -m venv venv
source venv/bin/activate

# Installa le dipendenze
pip install -r requirements.txt
```

### 2. Addestramento e Tracking dei Modelli

```bash
# In un terminale, avvia l'interfaccia di MLflow
mlflow ui

# In un secondo terminale, esegui lo script di addestramento
python src/train.py
```
Apri `http://127.0.0.1:5000` nel browser per visualizzare gli esperimenti.

### 3. Eseguire l'API Localmente

```bash
# Avvia il server FastAPI
uvicorn app.main:app --reload
```
L'API sarà disponibile all'indirizzo `http://127.0.0.1:8000`.

### 4. Eseguire i Test

```bash
# Esegui i test funzionali
pytest

# Per lo stress test, assicurati che l'API sia in esecuzione, poi:
locust -f locustfile.py --host http://localhost:8000
```
Apri `http://localhost:8089` nel browser per avviare lo stress test.

### 5. Build e Run con Docker

```bash
# Costruisci l'immagine Docker
docker build -t mlops-iris-api .

# Avvia il container
docker run -p 8080:80 mlops-iris-api
```
L'API sarà accessibile su `http://localhost:8080`.

### 6. Deploy su Kubernetes con Helm

Assicurati che il tuo cluster Kubernetes (Rancher Desktop) sia in esecuzione.

```bash
# Controlla la sintassi della chart
helm lint charts/mlops-api

# Installa l'applicazione sul cluster
# (Potrebbe richiedere --insecure-skip-tls-verify a seconda dell'ambiente)
helm install my-api-release charts/mlops-api

# Verifica che il pod sia in esecuzione
kubectl get pods

# Crea un tunnel per accedere all'API
kubectl port-forward svc/my-api-release-mlops-api 8080:80
```
L'API sarà accessibile su `http://localhost:8080`.

---

## Pipeline di CI/CD (GitHub Actions)

La pipeline è definita in `.github/workflows/ci.yml` e si attiva ad ogni `push` o `pull_request` sul branch `main`. Esegue i seguenti step in un job sequenziale:
1.  **Lint & Test**: Controlla lo stile del codice con `flake8` e `black` ed esegue i test con `pytest`.
2.  **Build, Scan & Push**: Costruisce l'immagine Docker, la scansiona per vulnerabilità `CRITICAL` e `HIGH` con `Trivy` e, solo sul branch `main`, la carica su GitHub Container Registry.
3.  **Helm Lint**: Controlla la sintassi della chart Helm.

---

## Scelte Progettuali e Giustificazioni

### Scelta del Modello

Per la selezione del modello, è stata utilizzata una **convalida incrociata a 5 fold** per ottenere una stima robusta delle performance. Sebbene entrambi i modelli fossero molto performanti, è stato scelto il modello **LogisticRegression**.

**Giustificazione**: Ha mostrato un'**accuratezza media (`cv_accuracy_mean`) leggermente superiore** (`0.973`) rispetto al RandomForest (`0.966`) e una stabilità comparabile. Data la sua maggiore semplicità e interpretabilità a fronte di performance migliori, è risultata la scelta ottimale per questo caso d'uso, seguendo il principio di preferire la soluzione più semplice ed efficace.


---

## Scelte Progettuali e Giustificazioni

### Scelta del Modello

Per la selezione del modello, è stata utilizzata una **convalida incrociata a 5 fold** per ottenere una stima robusta delle performance. Sebbene entrambi i modelli fossero molto performanti, è stato scelto il modello **LogisticRegression**.

**Giustificazione**: Ha mostrato un'**accuratezza media (`cv_accuracy_mean`) leggermente superiore** (`0.973`) rispetto al RandomForest (`0.966`) e una stabilità comparabile. Data la sua maggiore semplicità e interpretabilità a fronte di performance migliori, è risultata la scelta ottimale per questo caso d'uso, seguendo il principio di preferire la soluzione più semplice ed efficace.

### Strategia di Testing

- **Test Funzionali**: I test con `pytest` sono stati implementati per coprire il "happy path" dell'API, assicurando che gli endpoint `/health` e `/predict` funzionino correttamente con un payload valido. Per questa challenge, è stato testato un singolo caso di predizione per la classe "setosa" per validare il flusso end-to-end.
  - **Sviluppo Futuro**: In un ambiente di produzione reale, questi test verrebbero estesi utilizzando la parametrizzazione di `pytest` (`@pytest.mark.parametrize`) per coprire sistematicamente tutte le classi del modello, casi limite (es. payload vuoti o malformati) e scenari di errore.

- **Test di Carico**: Lo stress test con `Locust` ha confermato che l'API è stabile e performante sotto un carico simulato di 100 utenti concorrenti, senza registrare fallimenti e mantenendo tempi di risposta bassi.

### Versioning delle Dipendenze

- **Sviluppo Locale**: Durante lo sviluppo, il file `requirements.txt` è stato generato con `pip freeze` per garantire la riproducibilità dell'ambiente di training.
- **CI/CD**: Per la pipeline di CI/CD, il `requirements.txt` è stato semplificato per includere solo le dipendenze di primo livello. Questa scelta garantisce una maggiore flessibilità e compatibilità con l'ambiente pulito del runner di GitHub Actions, evitando errori di build dovuti a versioni di sotto-dipendenze troppo specifiche.

---