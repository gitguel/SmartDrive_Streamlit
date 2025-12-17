import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from itertools import cycle
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import os

# Configuração da página
st.set_page_config(
    page_title="Análise t-SNE - SmartDrive",
    page_icon="🚛",
    layout="wide"
)

# Título e descrição
st.title("🚛 Análise t-SNE - SmartDrive")
st.markdown("""
Esta aplicação permite visualizar análises t-SNE de dados de telemetria veicular com filtros dinâmicos.
Explore padrões de comportamento por **tipo de veículo**, **eficiência de combustível** e **período**.
""")

# Mapeamento de placas para porte de veículo e consumo esperado
plate_to_vehicle_info = {
    # BRF Primaria
    'TFT7I29': {'porte': 'Extra Pesado', 'consumo_esperado': 3.0},
    'MJZ4J84': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    'MLP7A90': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    'SWC0A01': {'porte': 'Extra Pesado', 'consumo_esperado': 3.5},
    'TPO8G44': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    'SWS3A91': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    'TBR7C11': {'porte': 'Extra Pesado', 'consumo_esperado': 3.0},
    'RLM1C02': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    'RYK9E76': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    'RYC6E77': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    # BRF Secundaria
    'TUU1B96': {'porte': 'Médio', 'consumo_esperado': 6.0},
    'TDU2E15': {'porte': 'Médio', 'consumo_esperado': 6.0},
    'TUB1C36': {'porte': 'Médio', 'consumo_esperado': 7.0},
    'TJT9F17': {'porte': 'Médio', 'consumo_esperado': 6.0},
    'TTJ2J57': {'porte': 'Médio', 'consumo_esperado': 7.0},
    'O-222401': {'porte': 'Desconhecido', 'consumo_esperado': None},
    'TMF9E93': {'porte': 'Médio', 'consumo_esperado': 6.0},
    'STK6E75': {'porte': 'Leve', 'consumo_esperado': 8.0},
    'TJM6J93': {'porte': 'Médio', 'consumo_esperado': 6.0},
    'TLM3A45': {'porte': 'Médio', 'consumo_esperado': 6.0},
    # BRF Agro
    'SXA6B49': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    'SXR6E75': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    '6922SBS': {'porte': 'Desconhecido', 'consumo_esperado': None},
    'RMR4H06': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    'SXA6A99': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    'SXP4G15': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    '6568SBS': {'porte': 'Desconhecido', 'consumo_esperado': None},
    'SXU0G93': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    'RCB9G35': {'porte': 'Extra Pesado', 'consumo_esperado': 3.5},
    'RHH4H13': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    # Ecoforest
    'ECO4D74': {'porte': 'Extra Pesado', 'consumo_esperado': 3.0},
    'ECO4H11': {'porte': 'Extra Pesado', 'consumo_esperado': 3.0},
    'ECO4F91': {'porte': 'Extra Pesado', 'consumo_esperado': 3.0},
    'ECO4C71': {'porte': 'Extra Pesado', 'consumo_esperado': 3.0},
    'ECO5J81': {'porte': 'Extra Pesado', 'consumo_esperado': 3.0},
    'ECO4D13': {'porte': 'Extra Pesado', 'consumo_esperado': 3.0},
    'ECO4F6': {'porte': 'Extra Pesado', 'consumo_esperado': 3.0},
    'ECO4D23': {'porte': 'Extra Pesado', 'consumo_esperado': 3.0},
    'ECO6D31': {'porte': 'Extra Pesado', 'consumo_esperado': 3.0},
    'ECO5H03': {'porte': 'Extra Pesado', 'consumo_esperado': 3.0},
    # Framento
    'SSE0G99': {'porte': 'Médio', 'consumo_esperado': 6.0},
    '5570SCS': {'porte': 'Leve', 'consumo_esperado': 11.0},
    'SSE0H01': {'porte': 'Médio', 'consumo_esperado': 6.0},
    '5570SDS': {'porte': 'Leve', 'consumo_esperado': 14.0},
    'SSE0F46': {'porte': 'Médio', 'consumo_esperado': 6.0},
    'O-171816': {'porte': 'Desconhecido', 'consumo_esperado': None},
    'SSE7D54': {'porte': 'Médio', 'consumo_esperado': 6.0},
    'SSE0H10': {'porte': 'Médio', 'consumo_esperado': 6.0},
    '5566SIS': {'porte': 'Leve', 'consumo_esperado': 15.0},
    'O-145224': {'porte': 'Desconhecido', 'consumo_esperado': None},
    # Reiter
    'JBH8I68': {'porte': 'Extra Pesado', 'consumo_esperado': 3.5},
    'JCI6G83': {'porte': 'Extra Pesado', 'consumo_esperado': 3.0},
    'JBV2I73': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    'JBI7E87': {'porte': 'Extra Pesado', 'consumo_esperado': 3.5},
    'JBS5G57': {'porte': 'Extra Pesado', 'consumo_esperado': 3.5},
    '5891SHS': {'porte': 'Leve', 'consumo_esperado': 10.0},
    'JDM1I75': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    'RKI4B73': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    'JBU1I67': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5},
    'JBI1F97': {'porte': 'Extra Pesado', 'consumo_esperado': 2.5}
}

# Função para classificar veículos por tipo baseado na placa
def classify_vehicle_type(plate):
    """Classifica o tipo de veículo baseado na placa"""
    if pd.isna(plate):
        return 'Desconhecido'
    
    info = plate_to_vehicle_info.get(plate, {'porte': 'Desconhecido'})
    return info['porte']


def get_expected_consumption(plate):
    """Retorna o consumo esperado para a placa"""
    if pd.isna(plate):
        return None
    
    info = plate_to_vehicle_info.get(plate, {'consumo_esperado': None})
    return info['consumo_esperado']


# Função para classificar eficiência de combustível
def classify_fuel_efficiency(efficiency, expected_consumption):
    """Classifica a eficiência de combustível baseado no consumo esperado"""
    if pd.isna(efficiency) or efficiency <= 0:
        return 'Inválido'
    
    if pd.isna(expected_consumption) or expected_consumption is None:
        return 'Desconhecido'
    
    # Calcular % em relação ao esperado
    # Baixa: < 80% do esperado
    # Média: 80% a 100% do esperado
    # Alta: > 100% do esperado
    percentage = (efficiency / expected_consumption) * 100
    
    if percentage < 80:
        return 'Baixa Eficiência'
    elif percentage < 100:
        return 'Média Eficiência'
    else:
        return 'Alta Eficiência'


def identify_dominant_event(row):
    """Identifica o evento dominante baseado nos tempos de viagem"""
    times = {
        'Movimento': row.get('movementTime', 0),
        'Parado': row.get('stoppedTime', 0),
        'Subida': row.get('ascendingTime', 0),
        'Descida': row.get('descendingTime', 0),
        'Plano': row.get('flatTime', 0)
    }
    
    # Remover valores nulos ou negativos
    times = {k: v for k, v in times.items() if v and v > 0}
    
    if not times:
        return 'Desconhecido'
    
    # Retornar o evento com maior tempo
    return max(times, key=times.get)


def identify_dominant_event_from_columns(row):
    """Identifica o evento de direção mais frequente baseado nas colunas agregadas de eventos"""
    # Primeiro, tentar usar os tempos de viagem
    dominant_time = identify_dominant_event(row)
    
    # Depois, verificar se há eventos críticos de direção
    event_counts = {}
    
    # Lista de eventos críticos para verificar
    critical_events = [
        'event_FREADA BRUSCA',
        'event_ARRANCADA BRUSCA',
        'event_EXCESSO DE ROTAÇÃO',
        'event_FORÇA G LATERAL FORTE',
        'event_FORÇA G LATERAL MÉDIA',
        'event_FORÇA G LATERAL FRACA'
    ]
    
    for event_col in critical_events:
        if event_col in row.index and row[event_col] > 0:
            event_name = event_col.replace('event_', '')
            event_counts[event_name] = row[event_col]
    
    if event_counts:
        return max(event_counts, key=event_counts.get)
    
    return dominant_time


# Mapeamento de placas para modelos por operação (TOP 10 de cada)
plate_to_model_by_operation = {
    'BRF Primaria': {
        'TFT7I29': 'SCANIA/R560 A6X4',
        'MJZ4J84': 'STRALIS 600S44T',
        'MLP7A90': 'STRALIS 600S44T',
        'SWC0A01': 'SCANIA/G370 A6X2',
        'TPO8G44': 'S-WAY 480-6X2',
        'SWS3A91': 'R450 A6X2',
        'TBR7C11': 'XF FTS 480 SSC',
        'RLM1C02': 'STRALIS 600S44T',
        'RYK9E76': '28.480 MTM 6X2',
        'RYC6E77': 'STRALIS 600S44T'
    },
    'BRF Secundaria': {
        'TUU1B96': 'ACCELO 1017',
        'TDU2E15': 'DELIVERY 11.180',
        'TUB1C36': 'EXPRESS DRF 4X2',
        'TJT9F17': 'DELIVERY 11.180',
        'TTJ2J57': 'EXPRESS DRF 4X2',
        'O-222401': 'SEM INFORMAÇÃO',
        'TMF9E93': 'DELIVERY 11.180',
        'STK6E75': 'IVECO/DAILY',
        'TJM6J93': 'DELIVERY 11.180',
        'TLM3A45': 'DELIVERY 11.180'
    },
    'BRF Agro': {
        'SXA6B49': '30.320 CRM 8X2',
        'SXR6E75': '26.260 CRM 6X2',
        '6922SBS': 'SEM INFORMAÇÃO',
        'RMR4H06': '30.280 CRM 8X2',
        'SXA6A99': '30.320 CRM 8X2',
        'SXP4G15': '26.260 CRM 6X2',
        '6568SBS': 'SEM INFORMAÇÃO',
        'SXU0G93': '26.320 CRM 6X2',
        'RCB9G35': '24.330 CRC 6X2',
        'RHH4H13': '30.280 CRM 8X2'
    },
    'Ecoforest': {
        'ECO4D74': 'SCANIA/R560 A6X4',
        'ECO4H11': 'SCANIA/R560 A6X4',
        'ECO4F91': 'SCANIA/R560 A6X5',
        'ECO4C71': 'SCANIA/R560 A6X6',
        'ECO5J81': 'SCANIA/R560 A6X7',
        'ECO4D13': 'SCANIA/R560 A6X8',
        'ECO4F6': 'SCANIA/R560 A6X9',
        'ECO4D23': 'SCANIA/R560 A6X10',
        'ECO6D31': 'SCANIA/R560 A6X11',
        'ECO5H03': 'SCANIA/R560 A6X12'
    },
    'Framento': {
        'SSE0G99': 'VW/DELIVERY 11.180',
        '5570SCS': 'BMW/X1 S20I M SPORT',
        'SSE0H01': 'VW/DELIVERY 11.180',
        '5570SDS': 'FIAT/MOBI LIKE',
        'SSE0F46': 'VW/DELIVERY 11.180',
        'O-171816': 'SEM INFORMAÇÃO',
        'SSE7D54': 'VW/DELIVERY 11.180',
        'SSE0H10': 'VW/DELIVERY 11.180',
        '5566SIS': 'CHEV/ONIX PLUS 10TAT LTZ',
        'O-145224': 'SEM INFORMAÇÃO'
    },
    'Reiter': {
        'JBH8I68': 'SCANIA/R410 A4X2C',
        'JCI6G83': 'SCANIA/R410 A6X2C',
        'JBV2I73': 'SCANIA/G410 A6X4C XT',
        'JBI7E87': 'SCANIA/R410 A4X2C',
        'JBS5G57': 'SCANIA/R410 A4X2C',
        '5891SHS': 'FIAT/TORO FREED T270 AT6',
        'JDM1I75': 'VW/26.320 CRM 6X2',
        'RKI4B73': 'VW/25.420 CTC 6X2',
        'JBU1I67': 'SCANIA/G410 A6X4C XT',
        'JBI1F97': 'SCANIA/G410 A6X4C XT'
    }
}

# Mapeamento de arquivos para operações
file_to_operation = {
    "Delta 1 (BRF Primaria)": "BRF Primaria",
    "Delta 2 (BRF Secundaria)": "BRF Secundaria",
    "Delta 3 (BRF Agro)": "BRF Agro",
    "Ecoforest": "Ecoforest",
    "Framento": "Framento",
    "Reiter": "Reiter"
}

# Sidebar para seleção de dados
st.sidebar.header("⚙️ Configurações")

# # Caminho base dos dados
# data_base_path = "/home/carnot.filho/projetos/smartdrive/dados/stream"

# # Opções de arquivos disponíveis
# file_options = {
#     "Delta 1 (BRF Primaria)": "Delta_Events_BRF_Primaria.txt",
#     "Delta 2 (BRF Secundaria)": "Delta_Events_BRF_Secundaria.txt",
#     "Delta 3 (BRF Agro)": "Delta_Events_BRF_Agro.txt",
#     "Ecoforest": "Delta_Events_Ecoforest.txt",
#     "Framento": "Delta_Events_Framento.txt",
#     "Reiter": "Delta_Events_Reiter.txt"
# }

# Caminho base onde os parquets estão salvos
DATA_PATH = "data/processed"

# Mapeamento: Nome Exibido -> Nome da Pasta do Dataset
file_options = {
    "Delta 1 (BRF Primaria)": "delta_1_brf_primaria",
    "Delta 2 (BRF Secundaria)": "delta_2_brf_secundaria",
    "Delta 3 (BRF Agro)": "delta_3_brf_agro",
    "Ecoforest": "ecoforest",
    "Framento": "framento",
    "Reiter": "reiter"
}

selected_dataset = st.sidebar.selectbox(
    "📂 Selecione a base de dados:",
    options=list(file_options.keys()),
    index=1  # Delta 2 (BRF Secundaria) como padrão
)

# Obter o mapeamento correto de placas para a operação selecionada
operation = file_to_operation[selected_dataset]
plate_to_model = plate_to_model_by_operation[operation]
top_10_plates = list(plate_to_model.keys())

# Filtros dinâmicos
st.sidebar.subheader("🔍 Filtros")

# Filtro de tipo de veículo (agora multiselect)
vehicle_types = ['Extra Pesado', 'Médio', 'Leve', 'Desconhecido']
selected_vehicle_types = st.sidebar.multiselect(
    "🚛 Tipo de Veículo (Formato):",
    options=vehicle_types,
    default=vehicle_types,
    help="Selecione um ou mais tipos de veículos para filtrar"
)

# Filtro de eficiência
efficiency_classes = ['Todos', 'Alta Eficiência', 'Média Eficiência', 'Baixa Eficiência']
selected_efficiency = st.sidebar.selectbox(
    "⚡ Classe de Eficiência:",
    options=efficiency_classes,
    index=0
)

# Filtro de distância
st.sidebar.subheader("📏 Filtro de Distância")
dist_min = st.sidebar.number_input("Distância mínima (km)", min_value=0, max_value=500, value=0, step=5)
dist_max = st.sidebar.number_input("Distância máxima (km)", min_value=0, max_value=500, value=100, step=5)

# Filtro de período (dias do mês)
st.sidebar.subheader("📅 Filtro de Período")
day_min = st.sidebar.number_input("Dia inicial", min_value=1, max_value=31, value=1, step=1)
day_max = st.sidebar.number_input("Dia final", min_value=1, max_value=31, value=31, step=1)

# Parâmetros de configuração
st.sidebar.subheader("🎛️ Parâmetros do t-SNE")
sample_size = st.sidebar.slider(
    "Tamanho da amostra",
    min_value=1000,
    max_value=20000,
    value=5000,
    step=500,
    help="Número de amostras para o t-SNE"
)

random_state = st.sidebar.number_input(
    "Random State",
    min_value=0,
    max_value=100,
    value=42,
    help="Semente para reprodutibilidade"
)

# Opções de visualização
st.sidebar.subheader("👁️ Visualização")
color_by = st.sidebar.selectbox(
    "Colorir por:",
    options=['Eficiência de Combustível (km/L)', 'Evento Dominante', 'Distância Total (km)'],
    index=0
)

show_distributions = st.sidebar.checkbox("📊 Mostrar distribuições", value=True)
show_outliers = st.sidebar.checkbox("🎯 Destacar outliers", value=False)

# Informações sobre as top 10 placas da operação selecionada
with st.sidebar.expander(f"📋 Top 10 Placas - {operation}"):
    for plate, model in plate_to_model.items():
        st.markdown(f"**{plate}**: {model}")


@st.cache_data(show_spinner=False)
def load_and_process_data(dataset_folder_name, top_plates, plate_model_map):
    """Lê os arquivos Parquet locais e processa os dados"""
    try:
        # Monta o caminho completo: data/processed/nome_da_pasta
        folder_path = os.path.join(DATA_PATH, dataset_folder_name)
        
        # O Pandas é inteligente: se passarmos uma pasta para read_parquet,
        # ele lê todos os arquivos (part_0, part_1...) e une automaticamente.
        df_bruto = pd.read_parquet(folder_path)
        
        # --- FILTRAGEM E MAPEAMENTO (Mantido igual) ---
        
        # Filtrar apenas as top 10 placas
        df_filtered = df_bruto[df_bruto['plate'].isin(top_plates)].copy()
        
        # Adicionar coluna de modelo
        df_filtered['vehicle_model'] = df_filtered['plate'].map(plate_model_map)
        
        # Adicionar tipo de veículo
        df_filtered['vehicle_type'] = df_filtered['plate'].apply(classify_vehicle_type)
        
        # Adicionar consumo esperado
        df_filtered['expected_consumption'] = df_filtered['plate'].apply(get_expected_consumption)
        
        # Lógica de eficiência (Mantida)
        if 'km_litro' in df_filtered.columns:
            df_filtered['fuel_efficiency'] = df_filtered['km_litro']
        else:
            df_filtered['fuel_efficiency'] = np.where(
                df_filtered['fuelConsumption'] > 0,
                df_filtered['totalDistance'] / df_filtered['fuelConsumption'],
                np.nan
            )
        
        # Adicionar classe de eficiência
        df_filtered['efficiency_class'] = df_filtered.apply(
            lambda row: classify_fuel_efficiency(row['fuel_efficiency'], row['expected_consumption']),
            axis=1
        )
        
        # Adicionar dia do mês (Ajustado para datetime já convertido no parquet)
        if 'endTime' in df_filtered.columns:
            # Como salvamos em parquet, as datas já devem estar como datetime.
            # Mas por segurança, garantimos a conversão se necessário.
            if not pd.api.types.is_datetime64_any_dtype(df_filtered['endTime']):
                df_filtered['endTime'] = pd.to_datetime(df_filtered['endTime'], errors='coerce')
            df_filtered['day_of_month'] = df_filtered['endTime'].dt.day
        elif 'positionDate' in df_filtered.columns:
             if not pd.api.types.is_datetime64_any_dtype(df_filtered['positionDate']):
                df_filtered['positionDate'] = pd.to_datetime(df_filtered['positionDate'], errors='coerce')
             df_filtered['day_of_month'] = df_filtered['positionDate'].dt.day
        else:
            df_filtered['day_of_month'] = 1 
        
        # Adicionar evento dominante
        df_filtered['dominant_event'] = df_filtered.apply(identify_dominant_event_from_columns, axis=1)
        
        # Adicionar flag percurso
        if 'percurso_com_evento' not in df_filtered.columns:
            event_columns = [col for col in df_filtered.columns if col.startswith('event_')]
            df_filtered['percurso_com_evento'] = (df_filtered[event_columns].sum(axis=1) > 0).astype(int)
        
        return df_filtered, df_bruto

    except Exception as e:
        st.error(f"Erro ao ler os dados locais: {e}")
        return None, None


def apply_filters(df, vehicle_types, efficiency_class, dist_min, dist_max, day_min, day_max):
    """Aplica filtros dinâmicos ao dataframe"""
    df_filtered = df.copy()
    
    # Filtro de tipo de veículo (agora aceita lista)
    if vehicle_types and len(vehicle_types) > 0:
        df_filtered = df_filtered[df_filtered['vehicle_type'].isin(vehicle_types)]
    
    # Filtro de eficiência
    if efficiency_class != 'Todos':
        df_filtered = df_filtered[df_filtered['efficiency_class'] == efficiency_class]
    
    # Filtro de distância
    df_filtered = df_filtered[
        (df_filtered['totalDistance'] >= dist_min) & 
        (df_filtered['totalDistance'] <= dist_max)
    ]
    
    # Filtro de período
    df_filtered = df_filtered[
        (df_filtered['day_of_month'] >= day_min) & 
        (df_filtered['day_of_month'] <= day_max)
    ]
    
    return df_filtered


def create_distribution_plots(df):
    """Cria gráficos de distribuição (histograma com média das top-10 e boxplot)"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Distribuição de Eficiência - Top 10 Placas',
            'Boxplot por Tipo de Veículo',
            'Distribuição de Distância Total',
            'Boxplot de Eficiência por Tipo'
        ),
        specs=[[{"type": "histogram"}, {"type": "box"}],
               [{"type": "histogram"}, {"type": "box"}]]
    )
    
    # Histograma de eficiência com média das top-10
    fuel_eff_data = df['fuel_efficiency'].dropna()
    mean_efficiency = fuel_eff_data.mean()
    
    fig.add_trace(
        go.Histogram(
            x=fuel_eff_data,
            nbinsx=50,
            name='Eficiência',
            marker_color='skyblue',
            opacity=0.7
        ),
        row=1, col=1
    )
    
    # Adicionar linha vertical com a média das top-10
    fig.add_vline(
        x=mean_efficiency,
        line_dash="dash",
        line_color="red",
        line_width=2,
        annotation_text=f"Média: {mean_efficiency:.2f} km/L",
        annotation_position="top",
        row=1, col=1
    )
    
    # Boxplot de eficiência por tipo de veículo
    for vtype in df['vehicle_type'].unique():
        if vtype != 'Desconhecido':
            data_subset = df[df['vehicle_type'] == vtype]['fuel_efficiency'].dropna()
            fig.add_trace(
                go.Box(y=data_subset, name=vtype),
                row=1, col=2
            )
    
    # Histograma de distância
    fig.add_trace(
        go.Histogram(
            x=df['totalDistance'].dropna(),
            nbinsx=50,
            name='Distância',
            marker_color='lightgreen'
        ),
        row=2, col=1
    )
    
    # Boxplot de eficiência detalhado por tipo
    for vtype in df['vehicle_type'].unique():
        if vtype != 'Desconhecido':
            data_subset = df[df['vehicle_type'] == vtype]['fuel_efficiency'].dropna()
            fig.add_trace(
                go.Box(
                    y=data_subset,
                    name=vtype,
                    boxmean='sd'
                ),
                row=2, col=2
            )
    
    fig.update_layout(
        height=800,
        showlegend=False,
        template='plotly_white'
    )
    
    fig.update_xaxes(title_text="Eficiência (km/L)", row=1, col=1)
    fig.update_xaxes(title_text="Tipo de Veículo", row=1, col=2)
    fig.update_xaxes(title_text="Distância (km)", row=2, col=1)
    fig.update_xaxes(title_text="Tipo de Veículo", row=2, col=2)
    
    fig.update_yaxes(title_text="Frequência", row=1, col=1)
    fig.update_yaxes(title_text="Eficiência (km/L)", row=1, col=2)
    fig.update_yaxes(title_text="Frequência", row=2, col=1)
    fig.update_yaxes(title_text="Eficiência (km/L)", row=2, col=2)
    
    return fig


def run_tsne(df, sample_size=5000, random_state=42):
    """Executa o t-SNE nos dados"""
    if df is None or df.empty:
        return None, None

    working_df = df.copy()

    # Amostragem se necessário
    if len(working_df) > sample_size:
        working_df = working_df.sample(sample_size, random_state=random_state)

    # Selecionar features relevantes
    candidate_features = [
        'totalDistance', 'fuelConsumption', 'averageSpeed', 'maxSpeed',
        'movementTime', 'stoppedTime', 'ascendingTime', 'descendingTime',
        'flatTime', 'maxRPM', 'averageRPM', 'clutchPedalUsageKM',
        'brakePedalUsageKM', 'greenRangeAscendingDistance',
        'yellowRangeAscendingDistance', 'slowGearRangeAscendingDistance',
        'greenRangeDescendingDistance', 'yellowRangeFlatDistance',
        'greenRangeFlatDistance', 'slowGearRangeFlatDistance',
        'ascendingDistance', 'descendingDistance', 'flatDistance',
        'greenRangeAscendingTime', 'greenRangeDescendingTime', 'greenRangeFlatTime',
        'yellowRangeAscendingTime', 'yellowRangeDescendingTime', 'yellowRangeFlatTime',
        'slowGearRangeAscendingTime', 'slowGearRangeDescendingTime', 'slowGearRangeFlatTime',
        'motorBreakTime', 'engineRotationTime', 'totalTime',
        'event_FREADA BRUSCA', 'event_ARRANCADA BRUSCA', 'event_EXCESSO DE ROTAÇÃO',
        'event_FORÇA G LATERAL FORTE', 'event_FORÇA G LATERAL MÉDIA',
        'percurso_com_evento', 'L_por_100km', 'km_litro'
    ]
    feature_columns = [col for col in candidate_features if col in working_df.columns]
    
    if not feature_columns:
        feature_columns = working_df.select_dtypes(include=[np.number]).columns.tolist()

    # Preparar dados
    feature_frame = working_df[feature_columns].replace([np.inf, -np.inf], np.nan)
    valid_rows = feature_frame.notna().all(axis=1)
    feature_frame = feature_frame.loc[valid_rows]

    if feature_frame.empty:
        return None, None

    working_df = working_df.loc[feature_frame.index]

    # Remover colunas constantes
    non_constant_columns = [
        col for col in feature_frame.columns
        if feature_frame[col].nunique(dropna=True) > 1
    ]

    if not non_constant_columns:
        return None, None

    feature_frame = feature_frame[non_constant_columns]
    n_samples = feature_frame.shape[0]

    if n_samples < 3:
        return None, None

    # Normalizar
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(feature_frame.to_numpy(dtype=float))

    # Calcular perplexidade apropriada
    perplexity = min(30, max(5, n_samples // 3))
    perplexity = min(perplexity, n_samples - 1)
    perplexity = max(perplexity, 1)

    # Executar t-SNE
    tsne = TSNE(
        n_components=2,
        perplexity=perplexity,
        learning_rate='auto',
        init='pca',
        random_state=random_state
    )
    embedding = tsne.fit_transform(scaled_features)

    tsne_df = working_df.copy()
    tsne_df['tsne_1'] = embedding[:, 0]
    tsne_df['tsne_2'] = embedding[:, 1]

    metadata = {
        'features': non_constant_columns,
        'perplexity': perplexity,
        'sample_size': n_samples
    }

    return tsne_df, metadata


def detect_outliers(df, column='fuel_efficiency'):
    """Detecta outliers usando IQR"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    df['is_outlier'] = (df[column] < lower_bound) | (df[column] > upper_bound)
    return df


def create_tsne_plot(tsne_df, color_by='Eficiência de Combustível (km/L)', show_outliers=False):
    """Cria o gráfico t-SNE único e geral"""
    if tsne_df is None or tsne_df.empty:
        st.warning("Não há dados suficientes para gerar o t-SNE com os filtros aplicados.")
        return None
    
    # Preparar dados de coloração
    if color_by == 'Eficiência de Combustível (km/L)':
        color_data = tsne_df['fuel_efficiency']
        color_title = 'Eficiência (km/L)'
        colorscale = 'Viridis'
    elif color_by == 'Evento Dominante':
        event_map = {'Movimento': 0, 'Parado': 1, 'Subida': 2, 'Descida': 3, 'Plano': 4, 'Desconhecido': 5}
        color_data = tsne_df['dominant_event'].map(event_map)
        color_title = 'Evento Dominante'
        colorscale = 'Plotly3'
    elif color_by == 'Distância Total (km)':
        color_data = tsne_df['totalDistance']
        color_title = 'Distância (km)'
        colorscale = 'Plasma'
    else:
        # Fallback para eficiência
        color_data = tsne_df['fuel_efficiency']
        color_title = 'Eficiência (km/L)'
        colorscale = 'Viridis'
    
    # Preparar hover data
    hover_data = {
        'Placa': tsne_df['plate'],
        'Modelo': tsne_df['vehicle_model'],
        'Tipo': tsne_df['vehicle_type'],
        'Eficiência (km/L)': tsne_df['fuel_efficiency'].round(2),
        'Consumo Esperado (km/L)': tsne_df['expected_consumption'].fillna(0).round(2),
        'Evento Dominante': tsne_df['dominant_event'],
        'Distância (km)': tsne_df['totalDistance'].round(2),
        'Velocidade Média': tsne_df['averageSpeed'].round(2),
        'Dia do Mês': tsne_df['day_of_month']
    }
    
    # Adicionar informações de eventos se disponíveis
    if 'percurso_com_evento' in tsne_df.columns:
        hover_data['Tem Eventos'] = tsne_df['percurso_com_evento'].map({0: 'Não', 1: 'Sim'})
    
    if 'event_FREADA BRUSCA' in tsne_df.columns:
        hover_data['Freadas Bruscas'] = tsne_df['event_FREADA BRUSCA'].fillna(0).astype(int)
    
    if 'event_ARRANCADA BRUSCA' in tsne_df.columns:
        hover_data['Arrancadas Bruscas'] = tsne_df['event_ARRANCADA BRUSCA'].fillna(0).astype(int)
    
    customdata = np.column_stack([hover_data[key] for key in hover_data.keys()])
    
    hovertemplate = '<br>'.join([
        f'{key}: %{{customdata[{idx}]}}'
        for idx, key in enumerate(hover_data.keys())
    ]) + '<extra></extra>'
    
    # Criar figura
    fig = go.Figure()
    
    # Adicionar pontos principais
    if show_outliers:
        tsne_df = detect_outliers(tsne_df, 'fuel_efficiency')
        
        # Pontos normais
        normal_mask = ~tsne_df['is_outlier']
        fig.add_trace(go.Scattergl(
            x=tsne_df.loc[normal_mask, 'tsne_1'],
            y=tsne_df.loc[normal_mask, 'tsne_2'],
            mode='markers',
            marker=dict(
                size=6,
                opacity=0.7,
                color=color_data[normal_mask],
                colorscale=colorscale,
                colorbar=dict(title=color_title),
                line=dict(width=0)
            ),
            customdata=customdata[normal_mask],
            hovertemplate=hovertemplate,
            name='Normal'
        ))
        
        # Outliers
        outlier_mask = tsne_df['is_outlier']
        if outlier_mask.any():
            fig.add_trace(go.Scattergl(
                x=tsne_df.loc[outlier_mask, 'tsne_1'],
                y=tsne_df.loc[outlier_mask, 'tsne_2'],
                mode='markers',
                marker=dict(
                    size=10,
                    opacity=1.0,
                    color=color_data[outlier_mask],
                    colorscale=colorscale,
                    line=dict(width=2, color='red'),
                    symbol='diamond'
                ),
                customdata=customdata[outlier_mask],
                hovertemplate=hovertemplate,
                name='Outlier'
            ))
    else:
        fig.add_trace(go.Scattergl(
            x=tsne_df['tsne_1'],
            y=tsne_df['tsne_2'],
            mode='markers',
            marker=dict(
                size=6,
                opacity=0.7,
                color=color_data,
                colorscale=colorscale,
                colorbar=dict(title=color_title),
                line=dict(width=0)
            ),
            customdata=customdata,
            hovertemplate=hovertemplate,
            showlegend=False
        ))
    
    fig.update_layout(
        title=f't-SNE - Colorido por {color_by}',
        xaxis_title='t-SNE Dimensão 1',
        yaxis_title='t-SNE Dimensão 2',
        height=700,
        template='plotly_white',
        hovermode='closest'
    )
    
    return fig


# Funções antigas removidas - agora usamos create_tsne_plot() simplificada


# # Carregar dados
# file_path = os.path.join(data_base_path, file_options[selected_dataset])

# with st.spinner('Carregando dados...'):
#     df_all, df_bruto = load_and_process_data(file_path, top_10_plates, plate_to_model)

# Recupera o nome da pasta
selected_dataset_folder = file_options[selected_dataset]

# Carrega os dados (agora a mensagem é diferente)
with st.spinner('Carregando dados otimizados...'):
    df_all, df_bruto = load_and_process_data(selected_dataset_folder, top_10_plates, plate_to_model)

if df_all is not None:
    # Aplicar filtros
    df_filtered = apply_filters(
        df_all,
        selected_vehicle_types,
        selected_efficiency,
        dist_min,
        dist_max,
        day_min,
        day_max
    )
    
    # Badge da operação selecionada
    vehicle_types_str = ', '.join(selected_vehicle_types) if selected_vehicle_types else 'Nenhum'
    st.info(f"🔍 **Operação:** {operation} | **Formato:** {vehicle_types_str} | **Período:** Dias {day_min}-{day_max} | **Distância:** {dist_min}-{dist_max} km")
    
    # Estatísticas gerais
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📊 Total Original", len(df_bruto))
    
    with col2:
        st.metric("🎯 Após Filtros", len(df_filtered))
    
    with col3:
        st.metric("🚛 Placas", df_filtered['plate'].nunique())
    
    with col4:
        st.metric("👨‍✈️ Motoristas", df_filtered['driverId'].nunique())
    
    with col5:
        avg_eff = df_filtered['fuel_efficiency'].mean()
        st.metric("⚡ Efic. Média", f"{avg_eff:.2f} km/L" if not np.isnan(avg_eff) else "N/A")
    
    # Tabela de distribuição por tipo de veículo
    with st.expander("📊 Distribuição por Tipo de Veículo e Eficiência"):
        type_dist = df_all.groupby(['vehicle_type', 'efficiency_class']).agg({
            'plate': 'count',
            'fuel_efficiency': 'mean'
        }).round(2)
        type_dist.columns = ['Quantidade', 'Eficiência Média (km/L)']
        st.dataframe(type_dist, use_container_width=True)
    
    # Tabela de consumo esperado vs real por placa
    with st.expander("📊 Consumo Esperado vs Real - Top 10 Placas"):
        consumption_comparison = df_filtered.groupby(['plate', 'vehicle_type', 'expected_consumption']).agg({
            'fuel_efficiency': 'mean'
        }).reset_index().round(2)
        consumption_comparison.columns = ['Placa', 'Tipo', 'Consumo Esperado (km/L)', 'Consumo Real Médio (km/L)']
        consumption_comparison['% do Esperado'] = (
            (consumption_comparison['Consumo Real Médio (km/L)'] / consumption_comparison['Consumo Esperado (km/L)']) * 100
        ).round(1)
        consumption_comparison = consumption_comparison.sort_values('% do Esperado', ascending=False)
        st.dataframe(consumption_comparison, use_container_width=True)
    
    # Gráficos de distribuição
    if show_distributions:
        st.subheader("📈 Distribuições e Outliers")
        with st.spinner('Gerando gráficos de distribuição...'):
            dist_fig = create_distribution_plots(df_filtered)
            st.plotly_chart(dist_fig, use_container_width=True)
    
    # Análise de veículos altamente eficientes
    st.subheader("🎯 Análise de Veículos Altamente Eficientes")
    high_eff_df = df_filtered[df_filtered['efficiency_class'] == 'Alta Eficiência'].copy()
    
    if not high_eff_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top 10 Placas Mais Eficientes:**")
            top_efficient = high_eff_df.groupby(['plate', 'vehicle_model', 'vehicle_type'])['fuel_efficiency'].mean().sort_values(ascending=False).head(10)
            for (plate, model, vtype), eff in top_efficient.items():
                st.markdown(f"- **{plate}** ({vtype}): {eff:.2f} km/L  \n  _{model}_")
        
        with col2:
            st.markdown("**Distribuição por Tipo:**")
            eff_by_type = high_eff_df.groupby('vehicle_type')['fuel_efficiency'].agg(['count', 'mean']).round(2)
            eff_by_type.columns = ['Quantidade', 'Eficiência Média']
            st.dataframe(eff_by_type, use_container_width=True)
    else:
        st.info("Nenhum veículo com alta eficiência encontrado nos filtros atuais.")
    
    # Análise de Eventos Críticos de Direção
    st.subheader("⚠️ Análise de Eventos Críticos de Direção")
    
    event_columns = [col for col in df_filtered.columns if col.startswith('event_')]
    
    if event_columns and 'percurso_com_evento' in df_filtered.columns:
        # Estatísticas gerais de eventos
        total_percursos = len(df_filtered)
        percursos_com_evento = df_filtered['percurso_com_evento'].sum()
        percent_com_evento = (percursos_com_evento / total_percursos * 100) if total_percursos > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total de Percursos", total_percursos)
        with col2:
            st.metric("⚠️ Percursos com Eventos", int(percursos_com_evento))
        with col3:
            st.metric("📈 % com Eventos", f"{percent_com_evento:.1f}%")
        
        # Top eventos mais frequentes
        event_totals = {}
        for col in event_columns:
            event_name = col.replace('event_', '')
            total = df_filtered[col].sum()
            if total > 0:
                event_totals[event_name] = total
        
        if event_totals:
            st.markdown("**Top 10 Eventos Mais Frequentes:**")
            event_df = pd.DataFrame(list(event_totals.items()), columns=['Evento', 'Total'])
            event_df = event_df.sort_values('Total', ascending=False).head(10)
            st.dataframe(event_df, use_container_width=True)
            
            # Placas com mais eventos críticos
            critical_events = ['event_FREADA BRUSCA', 'event_ARRANCADA BRUSCA', 'event_EXCESSO DE ROTAÇÃO']
            available_critical = [e for e in critical_events if e in df_filtered.columns]
            
            if available_critical:
                st.markdown("**Top 10 Placas com Mais Eventos Críticos:**")
                df_filtered['total_critical_events'] = df_filtered[available_critical].sum(axis=1)
                top_critical = df_filtered.groupby('plate')['total_critical_events'].sum().sort_values(ascending=False).head(10)
                
                for plate, count in top_critical.items():
                    st.markdown(f"- **{plate}**: {int(count)} eventos críticos")
    else:
        st.info("Dados de eventos não disponíveis nesta base.")
    
    # Criar e exibir o gráfico t-SNE
    st.subheader("📊 Visualização t-SNE")
    
    if len(df_filtered) < 10:
        st.warning("⚠️ Dados insuficientes para gerar o t-SNE. Ajuste os filtros para incluir mais dados.")
    else:
        with st.spinner('Gerando gráfico t-SNE... Isso pode levar alguns minutos.'):
            try:
                # Executar t-SNE
                tsne_df, metadata = run_tsne(df_filtered, sample_size, random_state)
                
                if tsne_df is not None:
                    # Criar gráfico
                    tsne_fig = create_tsne_plot(tsne_df, color_by, show_outliers)
                    
                    if tsne_fig is not None:
                        st.plotly_chart(tsne_fig, use_container_width=True)
                        
                        # Informações sobre o t-SNE
                        with st.expander("ℹ️ Informações Técnicas do t-SNE"):
                            st.markdown(f"""
                            - **Amostras utilizadas:** {metadata['sample_size']}
                            - **Perplexidade:** {metadata['perplexity']}
                            - **Features utilizadas:** {len(metadata['features'])}
                            - **Random state:** {random_state}
                            
                            **Features principais:**
                            {', '.join(metadata['features'][:10])}
                            """)
                        
                        st.success("✅ Gráfico t-SNE gerado com sucesso!")
                else:
                    st.warning("Não foi possível gerar o t-SNE com os dados filtrados.")
                
            except Exception as e:
                st.error(f"❌ Erro ao gerar o gráfico: {e}")
                st.exception(e)
    
    # Informações adicionais
    st.markdown("---")
    st.markdown(f"""
    ### 📖 Sobre a Visualização
    
    Este gráfico utiliza **t-SNE** (t-Distributed Stochastic Neighbor Embedding) para reduzir a dimensionalidade
    dos dados de telemetria veicular para 2 dimensões, permitindo visualizar padrões e clusters de comportamento.
    
    **Classificação de Eficiência (baseada no consumo esperado de cada veículo):**
    - 🔴 **Baixa Eficiência**: < 80% do consumo esperado
    - 🟡 **Média Eficiência**: 80% a 100% do consumo esperado
    - 🟢 **Alta Eficiência**: > 100% do consumo esperado
    
    Cada veículo tem seu consumo esperado específico baseado no modelo e operação.
    
    **Como interpretar o t-SNE:**
    - Pontos próximos indicam comportamentos de direção similares
    - A cor pode representar eficiência, tipo de veículo, classe de eficiência ou placa
    - Outliers (quando habilitados) são destacados com borda vermelha e forma de diamante
    - Use os filtros laterais para explorar diferentes segmentos de dados
    - Use zoom e pan para explorar áreas específicas do gráfico
    
    **Tipos de Veículos:**
    - 🚛 **Extra Pesado**: Caminhões pesados (consumo esperado: 2.5-3.5 km/L)
      - Ex: SCANIA R560, STRALIS 600, VW 26.320, etc
    - 🚐 **Médio**: Veículos de distribuição (consumo esperado: 6-7 km/L)
      - Ex: DELIVERY 11.180, ACCELO 1017, EXPRESS DRF
    - 🚗 **Leve**: Carros de passeio e vans leves (consumo esperado: 8-15 km/L)
      - Ex: BMW X1, FIAT MOBI, ONIX, TORO, IVECO DAILY
    """)
else:
    st.error("❌ Não foi possível carregar os dados. Verifique o caminho do arquivo.")
