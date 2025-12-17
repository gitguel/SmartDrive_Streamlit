import pandas as pd
import numpy as np
import gdown
import os
import shutil

# --- CONFIGURAÇÃO ---
# Seus IDs do Drive
DATASETS = {
    "delta_1_brf_primaria": "1R8ttOebc3qjDtdf47jE8pXCLPMLOln2U",
    "delta_2_brf_secundaria": "1qvUvWQK0ECqRie6o7UPw8Vul8Nzagwrd",
    "delta_3_brf_agro": "147gGDOYZ-mBpbB1-NONg20aNmHw7Ttg8",
    "ecoforest": "1aY3G5QdnifprCRI3t7MgVYlBGWUvPUOu",
    "framento": "1STnQCcrBSswSyUM5HL9z3MqczEn83e1k",
    "reiter": "1-en9yLpksaEqQTl0YAjqIAnyBIc2iDNG"
}

OUTPUT_DIR = "data/processed"
TEMP_DIR = "temp_raw_data"

def optimize_dataframe(df):
    """
    Reduz o uso de memória convertendo tipos de dados.
    """
    # 1. Converter Floats de 64 bits para 32 bits
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = df[col].astype('float32')
    
    # 2. Converter Ints de 64 bits para 32 bits (se couber)
    for col in df.select_dtypes(include=['int64']).columns:
        if df[col].max() < 2147483647 and df[col].min() > -2147483648:
            df[col] = df[col].astype('int32')

    # 3. Converter Strings repetitivas em Categorias
    # Se uma coluna de texto tem menos de 50% de valores únicos, vale a pena virar Categoria
    for col in df.select_dtypes(include=['object']).columns:
        num_unique_values = len(df[col].unique())
        num_total_values = len(df[col])
        if num_unique_values / num_total_values < 0.5:
            df[col] = df[col].astype('category')
            
    return df

def process_datasets():
    # Cria diretórios necessários
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)

    print(f"🚀 Iniciando processamento de {len(DATASETS)} datasets...")

    for name, file_id in DATASETS.items():
        print(f"\n--- Processando: {name} ---")
        
        # 1. Download
        raw_path = os.path.join(TEMP_DIR, f"{name}.json")
        if not os.path.exists(raw_path):
            print(f"📥 Baixando do Drive (ID: {file_id})...")
            url = f'https://drive.google.com/uc?id={file_id}'
            gdown.download(url, raw_path, quiet=False, fuzzy=True)
        else:
            print(f"📂 Arquivo já existe em cache: {raw_path}")

        # 2. Leitura
        print("📖 Lendo JSON...")
        try:
            df = pd.read_json(raw_path, lines=True)
        except ValueError as e:
            print(f"❌ Erro ao ler {name}: {e}")
            continue

        # 3. Otimização
        mem_before = df.memory_usage(deep=True).sum() / 1024**2
        print(f"💾 Memória antes: {mem_before:.2f} MB")
        
        df = optimize_dataframe(df)
        
        mem_after = df.memory_usage(deep=True).sum() / 1024**2
        print(f"📉 Memória depois: {mem_after:.2f} MB (Redução de {100-(mem_after/mem_before*100):.1f}%)")

        # 4. Salvamento Particionado (Safety Split)
        # Vamos dividir em 4 partes para garantir que nada passe de 100MB no GitHub
        dataset_folder = os.path.join(OUTPUT_DIR, name)
        if os.path.exists(dataset_folder):
            shutil.rmtree(dataset_folder) # Limpa versão anterior
        os.makedirs(dataset_folder)

        print(f"💾 Salvando em Parquet particionado em: {dataset_folder}/")
        
        # Divide o dataframe em 4 pedaços iguais
        chunks = np.array_split(df, 4)
        
        for i, chunk in enumerate(chunks):
            save_path = os.path.join(dataset_folder, f"part_{i}.parquet")
            # engine='pyarrow' e compression='zstd' (ótimo equilíbrio de tamanho/velocidade)
            chunk.to_parquet(save_path, engine='pyarrow', compression='zstd')
            
            # Check de tamanho
            size_mb = os.path.getsize(save_path) / (1024*1024)
            print(f"   -> Parte {i}: {size_mb:.2f} MB")
            if size_mb > 95:
                print("   ⚠️ ALERTA: Parte próxima do limite de 100MB do GitHub!")

    # Limpeza final
    print("\n🧹 Limpando arquivos temporários...")
    shutil.rmtree(TEMP_DIR)
    print("✅ Processamento concluído com sucesso!")

if __name__ == "__main__":
    process_datasets()