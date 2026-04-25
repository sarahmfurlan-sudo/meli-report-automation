# Arquitetura do Fluxo

## Visão geral

```
Analista preenche o Forms
        ↓
Power Automate dispara (trigger: nova resposta)
        ↓
Obter detalhes da resposta (Forms)
        ↓
Condição: qual setor?
   ├── Shipping  → Adicionar linha em Base_Shipping.xlsx (SharePoint)
   ├── DEV       → Adicionar linha em Base_DEV.xlsx
   ├── Oficinas  → Adicionar linha em Base_Oficinas.xlsx
   ├── Estoque   → Condição por nome → Base_Estoque_{analista}.xlsx
   └── Gestão    → Adicionar linha em Base_Gestao.xlsx
        ↓
Python lê as bases consolidadas
        ↓
python-pptx gera o deck mensal automaticamente
```

## Regras de validação no Forms

- Nome do analista: **dropdown obrigatório** (nunca texto livre)
- Mês de referência: **date picker** (nunca texto)
- Campos numéricos: tipo **Número** (evita "nd", "—", texto)
- Todos os campos críticos: **obrigatórios**

## Lição aprendida

O conector Excel do Power Automate exige que os dados estejam 
formatados como **Tabela do Excel** (Inserir → Tabela), não apenas
com cabeçalhos. Sem isso, o flow retorna erro ao tentar adicionar linhas.
