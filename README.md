# House Price Prediction

Projeto de machine learning para estimar preco de imoveis com base em caracteristicas como area util, numero de quartos, numero de banheiros, idade da casa e distancia ao centro urbano.

O repositorio inclui:
- pipeline de treinamento com geracao de dados sinteticos, EDA e avaliacao de modelos
- API Flask para previsao
- CLI interativa para inferencia local
- frontend estatico com visualizacao de resultado, metricas e importancias

## Estrutura

- `train.py`: gera dados, treina os modelos, avalia e salva artefatos
- `predict.py`: executa previsao via terminal
- `app.py`: expoe `POST /predict` e `GET /model_info`
- `frontend/`: interface web do dashboard
- `dataset.csv`: dataset sintetico gerado pelo treinamento
- `house_price_model.pkl`: modelo treinado
- `model_metadata.json`: metricas e feature importances
- `plots/`: graficos gerados no treinamento
- `tests/`: testes automatizados da API

## Features

- `sqft_living`
- `bedrooms`
- `bathrooms`
- `age_years`
- `distance_to_center_km`

## Como rodar

### 1. Clonar o repositorio

```bash
git clone https://github.com/JoaoVictorAAbreu-Dev/project-house-price-prediction.git
cd project-house-price-prediction
```

### 2. Criar ambiente virtual e instalar dependencias

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Treinar o modelo

```powershell
python train.py
```

Esse comando gera:
- `dataset.csv`
- `house_price_model.pkl`
- `model_metadata.json`
- arquivos em `plots/`

### 4. Rodar a API e o frontend

```powershell
python app.py
```

Abra:
- http://127.0.0.1:5000

### 5. Rodar previsao pela CLI

Modo interativo:

```powershell
python predict.py
```

Modo com argumentos:

```powershell
python predict.py --sqft 2200 --bedrooms 3 --bathrooms 2.5 --age 8 --distance 4.2
```

### 6. Rodar os testes

```powershell
pytest
```

## API

### `POST /predict`

Payload:

```json
{
  "sqft_living": 2200,
  "bedrooms": 3,
  "bathrooms": 2.5,
  "age_years": 8,
  "distance_to_center_km": 4.2
}
```

Resposta:

```json
{
  "price": 445267.35,
  "breakdown": {
    "base_value": 100000,
    "size_contribution": 264000,
    "rooms_contribution": 107500,
    "age_depreciation": -6400,
    "location_effect": -12600
  }
}
```

### `GET /model_info`

Retorna:
- melhores hiperparametros do Random Forest
- metricas dos modelos
- feature importances

## Configuracao

Variaveis opcionais definidas em `.env.example`:

- `HOST`
- `PORT`
- `FLASK_DEBUG`

## Tecnologias

- Python 3.8+
- Flask
- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn
- pytest

## Observacao

Os dados sao sinteticos e o melhor desempenho neste conjunto tende a ser do modelo linear, porque a regra de geracao e majoritariamente aditiva.
