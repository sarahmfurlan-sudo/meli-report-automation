"""
generate_report.py
==================
Consolida as bases mensais de cada área e gera o resumo executivo do Report Meli.

Como usar com dados reais:
    Substitua pd.read_csv('data/sample_data.csv') por pd.read_excel()
    apontando para os arquivos no SharePoint da sua organização.

Uso:
    python src/generate_report.py
"""

import pandas as pd
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# ──────────────────────────────────────────────
# 1. CARREGAR BASE
# ──────────────────────────────────────────────

def load_data():
    path = os.path.join(DATA_DIR, 'sample_data.csv')
    df = pd.read_csv(path)
    return df

# ──────────────────────────────────────────────
# 2. VALIDAÇÕES
# ──────────────────────────────────────────────

def validar(df):
    issues = []
    if df.isnull().any().any():
        cols = df.columns[df.isnull().any()].tolist()
        issues.append(f"  ⚠️  Campos vazios em: {', '.join(cols)}")
    if 'mes_referencia' in df.columns:
        meses = df['mes_referencia'].unique()
        if len(meses) > 1:
            issues.append(f"  ⚠️  Múltiplos meses: {meses}")
    if issues:
        print("\n[Validação] Alertas:")
        for i in issues: print(i)
    else:
        print("✅ Base validada sem problemas")

# ──────────────────────────────────────────────
# 3. CONSOLIDAÇÃO POR ÁREA
# ──────────────────────────────────────────────

def consolidar(df):
    resumo = {}
    for area, grupo in df.groupby('area'):
        resumo[area] = {
            'analistas': len(grupo),
            'projetos_ativos': grupo[grupo['status_projeto'] == 'Em andamento'].shape[0],
            'tickets_total': grupo['tickets_backlog'].sum() if 'tickets_backlog' in grupo else 0,
        }
    return resumo

# ──────────────────────────────────────────────
# 4. RELATÓRIO EXECUTIVO
# ──────────────────────────────────────────────

def print_report(resumo, mes='YYYY-MM'):
    print("\n" + "=" * 55)
    print(f"  REPORT MELI MENSAL — {mes}")
    print(f"  Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 55)
    for area, dados in resumo.items():
        print(f"\n📌 {area} ({dados['analistas']} analistas)")
        print(f"   Projetos em andamento: {dados['projetos_ativos']}")
        print(f"   Tickets backlog:       {dados['tickets_total']}")
    print("\n" + "=" * 55)
    print("✅ Consolidação concluída.")
    print("   Próximo passo: gerar PowerPoint com python-pptx")
    print("=" * 55)

# ──────────────────────────────────────────────
# 5. MAIN
# ──────────────────────────────────────────────

if __name__ == '__main__':
    print("🔄 Carregando base de dados...")
    df = load_data()

    print("🔍 Validando...")
    validar(df)

    resumo = consolidar(df)
    mes = df['mes_referencia'].iloc[0] if 'mes_referencia' in df.columns else 'N/A'
    print_report(resumo, mes)
