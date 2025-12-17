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

## 🚀 Como executar

### 1. Instalar dependências

Certifique-se de ter as seguintes bibliotecas instaladas:

```bash
pip install streamlit pandas numpy scikit-learn plotly
```

### 2. Executar a aplicação

No terminal, navegue até a pasta `src` e execute:

```bash
streamlit run streamlit_tsne_app.py
```

### 3. Acessar a aplicação

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

- Python 3.8+
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Plotly

## 📂 Estrutura de Arquivos Esperada

```
smartdrive/
├── dados/
│   └── deltas/
│       ├── delta_1_2025-08-01_00-00-00-03-00_2025-08-31_23-59-59-03-00.txt
│       ├── delta_2_2025-08-01_00-00-00-03-00_2025-08-31_23-59-59-03-00.txt
│       ├── delta_3_2025-08-01_00-00-00-03-00_2025-08-31_23-59-59-03-00.txt
│       ├── delta_ecoforest_2025-08-01_00-00-00-03-00_2025-08-31_23-59-59-03-00.txt
│       ├── delta_framento_2025-08-01_00-00-00-03-00_2025-08-31_23-59-59-03-00.txt
│       └── delta_reiter_2025-08-01_00-00-00-03-00_2025-08-31_23-59-59-03-00.txt
└── src/
    └── streamlit_tsne_app.py
```

## 💡 Dicas de Uso

1. **Performance**: Para conjuntos de dados muito grandes, reduza o tamanho da amostra
2. **Reprodutibilidade**: Use o mesmo Random State para comparar diferentes bases de dados
3. **Cache**: A aplicação usa cache do Streamlit para acelerar recarregamentos
4. **Interatividade**: Use zoom e pan nos gráficos Plotly para explorar detalhes

## 🐛 Solução de Problemas

### Erro ao carregar arquivo
- Verifique se o caminho dos dados está correto
- Certifique-se de que os arquivos existem na pasta `dados/deltas/`

### Gráfico não aparece
- Aguarde o processamento (pode levar alguns minutos)
- Verifique se há dados suficientes após o filtro das top 10 placas

### Aplicação lenta
- Reduza o tamanho da amostra nos parâmetros
- Use um conjunto de dados menor

## 📝 Notas

- O processamento pode levar alguns minutos dependendo do tamanho dos dados
- A aplicação filtra automaticamente apenas as top 10 placas
- Os dados são cacheados para melhor performance
