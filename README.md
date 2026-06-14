# Predição de Preços de Casas - Pipeline de Machine Learning & Web Dashboard

Este projeto de estudo implementa um pipeline completo de Data Science e Machine Learning para a predição de preços de imóveis com base em características como tamanho (m²/sqft), número de quartos/banheiros, idade da casa e distância até o centro da cidade.

Além do pipeline de modelagem, o projeto inclui uma ferramenta interativa de linha de comando (CLI) e um **Web Dashboard interativo premium** desenvolvido com Flask, HTML5, CSS3 (Glassmorphism) e Javascript.

---

## Estrutura do Projeto

O repositório está organizado da seguinte forma:

- **`train.py`**: Pipeline completo que gera o dataset sintético, realiza a análise exploratória (EDA), realiza a sintonia de hiperparâmetros com `GridSearchCV`, executa a validação cruzada (K-Fold) e salva o melhor modelo.
- **`predict.py`**: Script interativo de linha de comando para realizar predições rápidas fornecendo as características do imóvel.
- **`app.py`**: Backend em Flask que serve a API de inferência `/predict` e os arquivos estáticos do frontend.
- **`frontend/`**: Interface web do usuário (HTML, CSS customizado com tema escuro e efeitos de vidro fosco, e Javascript).
- **`exploration.ipynb`**: Notebook Jupyter interativo contendo toda a análise exploratória detalhada dos dados e comparação passo a passo dos modelos.
- **`dataset.csv`**: O conjunto de dados gerado sinteticamente.
- **`house_price_model.pkl`**: O modelo Random Forest Regressor treinado e serializado via `joblib`.
- **`plots/`**: Visualizações geradas automaticamente durante o treinamento:
  - `correlation_matrix.png`: Matriz de correlação de Pearson entre as variáveis.
  - `size_vs_price.png`: Gráfico de dispersão entre área habitável e preço.
  - `model_evaluation.png`: Comparação de previsões vs valores reais (Regressão Linear vs Random Forest).
  - `residuals_distribution.png`: Distribuição dos resíduos do Random Forest (análise de erro).
  - `feature_importance.png`: Importância relativa de cada variável no modelo Random Forest.
- **`requirements.txt`**: Lista de bibliotecas Python necessárias para executar o projeto.

---

## Dicionário de Variáveis (Features)

| Variável | Tipo | Descrição |
| :--- | :--- | :--- |
| **sqft_living** | Numérico | Área interna habitável em pés quadrados (sqft). |
| **bedrooms** | Inteiro | Número de quartos da residência (1 a 10). |
| **bathrooms** | Decimal | Número de banheiros da residência (1.0 a 6.0). |
| **age_years** | Inteiro | Idade do imóvel em anos (0 a 80). |
| **distance_to_center_km** | Decimal | Distância linear até o centro urbano mais próximo em quilômetros. |
| **price** (Target) | Inteiro | Preço estimado do imóvel em dólares americanos (USD). |

---

## Modelagem e Resultados

Duas abordagens de Machine Learning foram avaliadas e comparadas:

1. **Regressão Linear Múltipla** (Modelo de Baseline Linear)
2. **Random Forest Regressor** (Modelo Ensemble não linear sintonizado via Grid Search)

### Desempenho no Conjunto de Teste:

* **Regressão Linear**:
  - **R² Score**: `0.9165` (Explica 91.65% da variabilidade dos preços)
  - **Erro Médio Absoluto (MAE)**: `$17,368.44`
  - **Raiz do Erro Quadrático Médio (RMSE)**: `$22,646.50`
  - **Erro Percentual Absoluto Médio (MAPE)**: `5.46%`

* **Random Forest** (Hiperparâmetros: `n_estimators=150`, `max_depth=10`, `min_samples_split=2`):
  - **R² Score**: `0.8759`
  - **Erro Médio Absoluto (MAE)**: `$22,014.61`
  - **Raiz do Erro Quadrático Médio (RMSE)**: `$27,610.44`
  - **Erro Percentual Absoluto Médio (MAPE)**: `6.90%`

*Nota: Em nosso dataset sintético, o modelo de Regressão Linear obteve um desempenho ligeiramente superior devido à natureza estritamente aditiva usada na lógica de geração dos dados.*

### Importância das Variáveis (Random Forest):
1. **Tamanho do Imóvel (`sqft_living`)**: 60.0%
2. **Distância até o Centro (`distance_to_center_km`)**: 16.0%
3. **Número de Quartos (`bedrooms`)**: 8.4%
4. **Número de Banheiros (`bathrooms`)**: 7.8%
5. **Idade do Imóvel (`age_years`)**: 7.8%

---

## 🛠️ Como Executar o Projeto

### Pré-requisitos
Certifique-se de ter o **Python 3.8+** instalado no seu sistema.

### 1. Clonar e Acessar o Repositório
```bash
git clone https://github.com/JoaoVictorAAbreu-Dev/house-price-prediction.git
cd house-price-prediction
```

### 2. Configurar o Ambiente Virtual e Instalar Dependências
No Windows:
```powershell
# Criação do ambiente virtual
python -m venv .venv
# Ativação do ambiente
.venv\Scripts\activate
# Instalação das bibliotecas
pip install -r requirements.txt
```

No Linux/macOS:
```bash
# Criação do ambiente virtual
python3 -m venv .venv
# Ativação do ambiente
source .venv/bin/activate
# Instalação das bibliotecas
pip install -r requirements.txt
```

### 3. Executar o Treinamento do Modelo
Para regerar o dataset, rodar a análise exploratória básica e salvar as métricas e gráficos atualizados:
```bash
python train.py
```

### 4. Realizar Predições via Terminal (CLI)
Você pode usar o script de inferência de forma interativa:
```bash
python predict.py
```
O script solicitará as informações do imóvel passo a passo.

Ou você pode passar os argumentos diretamente no comando:
```bash
python predict.py --sqft 2200 --bedrooms 3 --bathrooms 2.5 --age 8 --distance 4.2
```

### 5. Iniciar o Web Dashboard Interativo
Para rodar a interface web sofisticada em sua máquina local:
```bash
python app.py
```
Após iniciar o servidor, abra o navegador e acesse:
 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## Tecnologias Empregadas

- **Linguagem Principal**: Python 3.11+
- **Machine Learning**: Scikit-Learn
- **Manipulação de Dados**: Pandas, NumPy
- **Visualização**: Matplotlib, Seaborn
- **Desenvolvimento Web (Backend)**: Flask (Python)
- **Interface Gráfica (Frontend)**: HTML5 semântico, Javascript (ES6 Fetch API), CSS3 Avançado (Glassmorphic dark design, micro-animações, layout fluido).
