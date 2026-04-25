# 📊 meli-report-automation

> Automação de coleta e consolidação de dados mensais para geração de relatórios executivos — desenvolvido para o time de CX/Cyber da Stefanini.

---

## 🧩 O problema

O relatório mensal do time Mercado Livre envolvia **5 áreas** (Shipping, DEV, Oficinas, Estoque, Gestão) com **~15 analistas** respondendo em formatos diferentes, por e-mail ou mensagem. A consolidação era feita manualmente, levando horas todo mês.

---

## ✅ A solução

Um pipeline completo de automação:

```
Microsoft Forms  →  Power Automate  →  Excel/SharePoint  →  Python  →  PowerPoint
```

| Etapa | Ferramenta | O que faz |
|---|---|---|
| Coleta | Microsoft Forms | Formulário único por área com campos tipados e validados |
| Roteamento | Power Automate (Flow Meli_Main) | Detecta o setor e escreve na base correta |
| Armazenamento | Excel + SharePoint | Uma base por área, formatada como tabela |
| Geração | Python (python-pptx) | Lê as bases e monta o deck automaticamente |

---

## 🗂️ Estrutura do repositório

```
meli-report-automation/
├── data/
│   └── sample_data.csv         ← Estrutura esperada dos dados (sem dados reais)
├── src/
│   └── generate_report.py      ← Script de consolidação e geração do relatório
├── docs/
│   └── architecture.md         ← Diagrama da arquitetura do fluxo
├── requirements.txt
└── README.md
```

> ⚠️ **Os dados reais são confidenciais e não estão incluídos neste repositório.**
> Use `data/sample_data.csv` como referência da estrutura esperada.
> Em produção, os arquivos Excel ficam no SharePoint corporativo e são lidos via `openpyxl` ou Microsoft Graph API.

---

## 🔄 Arquitetura do Flow (Power Automate)

```
[Analista preenche Forms]
        ↓
[Gatilho: "Quando nova resposta enviada"]
        ↓
[Ação: "Obter detalhes da resposta"]
        ↓
[Condição: qual setor?]
   ├── Shipping  → escreve em Base_Shipping.xlsx
   ├── DEV       → escreve em Base_DEV.xlsx
   ├── Oficinas  → escreve em Base_Oficinas.xlsx
   ├── Estoque   → condição por analista → Base_Estoque_{nome}.xlsx
   └── Gestão    → escreve em Base_Gestao.xlsx
```

---

## 📋 Campos coletados por área

### Shipping
`Analista · Mês · Tickets Backlog · KM Rodados · Projeto Ativo · Status · Destaque · Desafio · Próximo Passo`

### DEV
`Analista · Mês · Projeto 1 · Status · Entregas · Projeto 2 · Status · Trilhas em andamento`

### Oficinas
`Analista · Mês · Tickets Totais · Tickets Encerrados · Backlog · MTTR · Destaque · Próximo Passo`

### Estoque (personalizado por analista)
- **Adriano** — descarte por tipo, inventário local, CAD chamados
- **Alessandro** — recebidos/enviados, inventário, CAD
- **Guilherme** — câmeras, CCTV, controle de acesso, periféricos
- **João Felipe** — handheld, notebook, impressora, descarte total

---

## 🚀 Como rodar

```bash
# Clone o repositório
git clone https://github.com/sarahmfurlan-sudo/meli-report-automation
cd meli-report-automation

# Instale as dependências
pip install -r requirements.txt

# Gere o relatório consolidado com dados simulados
python src/generate_report.py
```

O script lê os CSVs de `/data`, consolida tudo e imprime o resumo executivo no terminal.

> **Nota:** Os dados são simulados. Em produção, os CSVs são substituídos pelas bases Excel do SharePoint, lidas via `openpyxl`.

---

## 💡 Principais aprendizados técnicos

- **Tipagem no Forms é crítica** — campos numéricos como número, datas como date picker; texto livre gera dados sujos
- **Dropdown obrigatório para nome do analista** — evita variações ("Adriano", "adriano", "Adri") que quebram o roteamento
- **Tabela formatada no Excel é obrigatória** — o conector do Power Automate exige tabela nomeada, não apenas cabeçalhos
- **BackgroundTasks para não travar o fluxo** — operações de escrita em paralelo sem bloquear o trigger

---

## 🛠️ Stack

![Power Automate](https://img.shields.io/badge/Power%20Automate-0066FF?logo=microsoft)
![Microsoft Forms](https://img.shields.io/badge/Microsoft%20Forms-217346?logo=microsoft)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![SharePoint](https://img.shields.io/badge/SharePoint-0078D4?logo=microsoft)
![Excel](https://img.shields.io/badge/Excel-217346?logo=microsoft-excel)

---

## 👩‍💻 Autora

**Sarah Marangoni Furlan**  
Automação · Dados · Marketing Digital com IA  
[linkedin.com/in/sarah-mfurlan](https://linkedin.com/in/sarah-mfurlan) · [github.com/sarahmfurlan-sudo](https://github.com/sarahmfurlan-sudo)
