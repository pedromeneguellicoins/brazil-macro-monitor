"""
Glossário centralizado — definições e contexto de cada indicador.
Quando adicionar nova métrica ao app, registra aqui.

Estrutura de cada entrada:
- short: 1-2 linhas pra caixa lateral ao gráfico
- detail: explicação completa pro expander "Saiba mais"
- why: por que esse indicador importa pra o BRL
- source: fonte e periodicidade
"""

GLOSSARY = {
    # ============================================================
    # FX & MOEDAS
    # ============================================================
    "PTAX": {
        "title": "PTAX (BRL/USD)",
        "short": "Taxa oficial de câmbio USD/BRL divulgada pelo Banco Central. É a referência para liquidação de contratos cambiais e indexação de derivativos no Brasil.",
        "detail": """
A **PTAX** é a média ponderada das cotações de compra e venda do dólar praticadas no mercado interbancário brasileiro, calculada e divulgada pelo Banco Central do Brasil em 4 boletins ao longo do dia (10h, 11h, 12h, 13h) mais o fechamento.

A PTAX usada como referência neste monitor é a **PTAX venda** (série 1 do BCB SGS), que é o valor padrão para liquidação de NDFs (Non-Deliverable Forwards), contratos cambiais e operações estruturadas no Brasil.

**Características técnicas:**
- Calculada apenas em dias úteis (calendário B3)
- Não inclui movimentos intradiários após o último boletim
- Pode divergir do "dólar comercial" cotado pelas mesas no fim do dia
        """,
        "why": "É o preço de referência para qualquer hedge cambial estruturado no Brasil. Toda análise de regime do real começa aqui.",
        "source": "BCB SGS · Série 1 · Diária (D+0)",
    },

    "DXY": {
        "title": "DXY — US Dollar Index",
        "short": "Índice que mede o dólar contra 6 moedas de economias desenvolvidas (EUR, JPY, GBP, CAD, SEK, CHF). É 57% EUR/USD invertido.",
        "detail": """
O **DXY** (ICE U.S. Dollar Index) é o índice mais antigo e popular de força do dólar americano. Foi criado em 1973 pelo Fed após o fim do Bretton Woods.

**Composição (pesos fixos):**
- EUR: 57,6%
- JPY: 13,6%
- GBP: 11,9%
- CAD: 9,1%
- SEK: 4,2%
- CHF: 3,6%

**Limitação para análise de emergentes:** O DXY foi desenhado em 1973 e não inclui nenhuma moeda asiática emergente (sem CNY, sem INR, sem MXN, sem BRL). Para BRL, é apenas um indicador parcial — útil pra capturar movimento "macro global do dólar", mas insuficiente sozinho.

**Quando subir:** geralmente reflete Fed mais hawkish, fuga pra dólar (safe haven), ou crise no G10 (Europa/Japão).
        """,
        "why": "Termômetro de força do dólar globalmente. Quando DXY sobe, emergentes em geral apanham — mas o BRL pode se descolar se houver fator local dominante.",
        "source": "Yahoo Finance · DX-Y.NYB · Diária",
    },

    "DTWEXBGS": {
        "title": "DTWEXBGS — Trade-Weighted Broad Dollar Index",
        "short": "Índice do Fed que mede o dólar contra 26 moedas, ponderado por volume de comércio dos EUA. Inclui CNY e outras moedas emergentes — mais relevante para o BRL que o DXY.",
        "detail": """
O **DTWEXBGS** (Trade-We
