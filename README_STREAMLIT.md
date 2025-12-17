# 🚛 Aplicação Streamlit - Análise t-SNE SmartDrive

## 📋 Descrição

Esta aplicação Streamlit permite visualizar análises t-SNE de dados de telemetria veicular, focando nas **top 10 placas** com informações detalhadas sobre modelos de veículos.

## 🎯 Funcionalidades

- ✅ Seleção interativa de diferentes bases de dados
- ✅ Visualização de gráficos t-SNE interativos com Plotly
- ✅ Filtros por faixas de distância (5-20 km e 20-50 km)
- ✅ Análise semanal (4 semanas)
- ✅ Informações sobre top placas e top motoristas
- ✅ Mapeamento de placas para modelos de veículos
- ✅ Métricas e estatísticas em tempo real

## 🚀 Instalação e Execução

Este projeto utiliza **Poetry** para gerenciamento de dependências e ambientes virtuais.

### 1. Clonar o repositório

Abra o terminal e clone o repositório para sua máquina local:

```bash
git clone git@github.com:gitguel/SmartDrive_Streamlit.git
cd SmartDrive_Streamlit
```

### 2. Configurar o ambiente

Certifique-se de ter o [Poetry](https://python-poetry.org/docs/#installation) instalado. Em seguida, instale as dependências do projeto (isso criará o ambiente virtual automaticamente):

```bash
poetry install
```

### 3. Executar a aplicação

Para iniciar o servidor do Streamlit utilizando o ambiente configurado, execute:

```bash
poetry run streamlit run src/streamlit_tsne_app.py
```

A aplicação será aberta automaticamente no navegador em:
```
http://localhost:8501
```

## ⚙️ Configurações Disponíveis

### Sidebar (Barra Lateral)

1. **📂 Seleção de Base de Dados**
   - Delta 1 (BRF)
   - Delta 2 (BRF) - *padrão*
   - Delta 3 (BRF)
   - Ecoforest
   - Framento
   - Reiter

2. **🎛️ Parâmetros do t-SNE**
   - **Tamanho da amostra**: 1.000 - 10.000 (padrão: 5.000)
   - **Random State**: 0 - 100 (padrão: 42)

3. **📋 Top 10 Placas e Modelos**
   - TUU1B96: ACCELO 1017
   - TDU2E15: DELIVERY 11.180
   - TUB1C36: EXPRESS DRF 4X2
   - TJT9F17: DELIVERY 11.180
   - TTJ2J57: EXPRESS DRF 4X2
   - O-222401: SEM INFORMAÇÃO
   - TMF9E93: DELIVERY 11.180
   - STK6E75: IVECO/DAILY
   - TJM6J93: DELIVERY 11.180
   - TLM3A45: DELIVERY 11.180

## 📊 Estrutura do Gráfico

O gráfico é composto por:

- **2 linhas**: Uma para cada faixa de distância (5-20 km e 20-50 km)
- **6 colunas**:
  1. Top placa (forma = motorista)
  2. Top motorista (forma = placa)
  3. Semana 1
  4. Semana 2
  5. Semana 3
  6. Semana 4

### Legenda de Cores

- 🎨 **Escala de cores Viridis**: Representa a eficiência de combustível (km/L)
  - 🟣 Roxo: Menor eficiência
  - 🟢 Verde: Eficiência média
  - 🟡 Amarelo: Maior eficiência

### Formas dos Marcadores

Diferentes formas representam diferentes entidades (placas ou motoristas), permitindo distinguir visualmente os grupos.

## 📖 Como Interpretar

1. **Proximidade dos pontos**: Pontos próximos indicam comportamentos de direção similares
2. **Cores**: Indicam a eficiência de combustível (hover para ver valores exatos)
3. **Formas**: Diferenciam entre diferentes placas ou motoristas
4. **Clusters**: Agrupamentos podem indicar padrões de comportamento comuns

## 🔍 Informações no Hover

Ao passar o mouse sobre qualquer ponto, você verá:
- Placa do veículo
- Modelo do veículo
- ID do motorista
- Data da posição
- Distância total
- Consumo de combustível
- Eficiência de combustível
- Velocidade média e máxima
- Tempo de movimento e parado
- Distâncias em subida, descida e plano
- E muito mais...

## 🛠️ Requisitos Técnicos

- Python 3.10+ (Gerenciado pelo Poetry)
- Poetry (Gerenciador de pacotes)
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Plotly

## 📂 Estrutura de Arquivos Esperada

```
SmartDrive_Streamlit/
├── data/
│   └── deltas/
│       ├── delta_1_*.txt
│       └── ...
│   └── deltas_events/
│       ├── delta_event_1_*.txt
│       └── ...
├── src/
│   └── streamlit_tsne_app.py
├── pyproject.toml
├── poetry.lock
└── README.md
```

## 💡 Dicas de Uso

1. **Performance**: Para conjuntos de dados muito grandes, reduza o tamanho da amostra
2. **Reprodutibilidade**: Use o mesmo Random State para comparar diferentes bases de dados
3. **Cache**: A aplicação usa cache do Streamlit para acelerar recarregamentos
4. **Interatividade**: Use zoom e pan nos gráficos Plotly para explorar detalhes

## 🐛 Solução de Problemas

### Erro "Module not found"
- Certifique-se de ter rodado `poetry install` antes de executar.
- Verifique se está rodando o comando com o prefixo `poetry run ...`.

### Erro ao carregar arquivo
- Verifique se o caminho dos dados está correto
- Certifique-se de que os arquivos existem na pasta `data/deltas/` (atenção para a mudança de `dados` para `data` se tiver alterado a estrutura).

### Gráfico não aparece
- Aguarde o processamento (pode levar alguns minutos)
- Verifique se há dados suficientes após o filtro das top 10 placas

### Aplicação lenta
- Reduza o tamanho da amostra nos parâmetros
- Use um conjunto de dados menor