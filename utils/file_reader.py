"""
utils/file_reader.py — Leitura de Arquivos (PDF, CSV, Excel)
"""

import io
import hashlib
import pdfplumber
import pandas as pd
from pathlib import Path


def read_file(uploaded_file):
    """
    Lê arquivo enviado pelo Streamlit e retorna conteúdo estruturado.
    
    Args:
        uploaded_file: streamlit UploadedFile object
    
    Returns:
        dict: {
            'type': 'pdf' | 'csv' | 'excel',
            'filename': str,
            'content': str | DataFrame,
            'raw_bytes': bytes,
            'hash': str (MD5),
        }
    """
    
    filename = uploaded_file.name
    ext = Path(filename).suffix.lower()
    
    # Lê bytes completos
    uploaded_file.seek(0)
    raw_bytes = uploaded_file.read()
    
    # Calcula hash
    file_hash = hashlib.md5(raw_bytes).hexdigest()
    
    # Lê conteúdo baseado no tipo
    if ext == '.pdf':
        content = _read_pdf(io.BytesIO(raw_bytes))
        file_type = 'pdf'
    
    elif ext == '.csv':
        content = _read_csv(io.BytesIO(raw_bytes))
        file_type = 'csv'
    
    elif ext in ['.xlsx', '.xls']:
        content = _read_excel(io.BytesIO(raw_bytes))
        file_type = 'excel'
    
    else:
        raise ValueError(f"Tipo de arquivo não suportado: {ext}")
    
    return {
        'type': file_type,
        'filename': filename,
        'content': content,
        'raw_bytes': raw_bytes,
        'hash': file_hash,
    }


def _read_pdf(file_buffer):
    """
    Lê PDF e retorna texto completo.
    
    Returns:
        str: texto extraído do PDF
    """
    text = ""
    
    with pdfplumber.open(file_buffer) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    return text


def _read_csv(file_buffer):
    """
    Lê CSV com detecção automática de encoding e delimitador.
    
    Returns:
        DataFrame
    """
    # Tenta encoding padrão primeiro
    try:
        df = pd.read_csv(file_buffer, encoding='utf-8')
        return df
    except:
        pass
    
    # Tenta outros encodings
    for encoding in ['latin1', 'iso-8859-1', 'cp1252']:
        try:
            file_buffer.seek(0)
            df = pd.read_csv(file_buffer, encoding=encoding)
            return df
        except:
            continue
    
    raise ValueError("Não foi possível ler o CSV. Encoding não suportado.")


def _read_excel(file_buffer):
    """
    Lê Excel (todas as sheets concatenadas).
    
    Returns:
        DataFrame
    """
    # Lê todas as sheets
    excel_file = pd.ExcelFile(file_buffer)
    
    dfs = []
    for sheet_name in excel_file.sheet_names:
        df = pd.read_excel(file_buffer, sheet_name=sheet_name)
        df['_sheet'] = sheet_name
        dfs.append(df)
    
    # Concatena todas as sheets
    if len(dfs) == 1:
        return dfs[0]
    else:
        return pd.concat(dfs, ignore_index=True)
