"""
Glossário centralizado.
"""

GLOSSARY = {
    "PTAX": {
        "title": "PTAX (BRL/USD)",
        "short": "Taxa oficial de câmbio USD/BRL divulgada pelo Banco Central. É a referência para liquidação de contratos cambiais e indexação de derivativos no Brasil.",
        "detail": """
A **PTAX** é a média ponderada das cotações de compra e venda do dólar praticadas no mercado interbancário brasileiro, calculada e divulgada pelo Banco Central do Brasil em 4 boletins ao longo do dia (10h, 11h, 12h, 13h) mais o fechamento.

A PTAX usada como referência neste monitor é a **PTAX venda** (série 1 do BCB SGS), valor padrão para liquidação de NDFs, contratos cambiais e operações estruturadas no Brasil.

**Características técnicas:**
- Calculada apenas em dias úteis (calendário B3)
- Não inclui movimentos intradiários após o último boletim
- Pode divergir do "dólar comercial" cotado pelas mesas no fim do dia
        """,
        "why": "É o preço de referência para qualquer hedge cambial estruturado no Brasil.",
        "source": "BCB SGS · Série 1 · Diária (D+0)",
    },

    "DXY": {
        "title": "DXY — US Dollar Index",
        "short": "Índice que mede o dólar contra 6 moedas de economias desenvolvidas (EUR, JPY, GBP, CAD, SEK, CHF). É 57% EUR/USD invertido.",
        "detail": """
O **DXY** (ICE U.S. Dollar Index) é o índice mais antigo e popular de força do dólar, criado em 1973 pelo Fed.

**Composição:**
- EUR: 57,6% · JPY: 13,6% · GBP: 11,9% · CAD: 9,1% · SEK: 4,2% · CHF: 3,6%

**Limitação para emergentes:** Não inclui CNY, INR, MXN, BRL. Para análise de BRL, é indicador parcial.
        """,
        "why": "Termômetro de força global do dólar. Quando DXY sobe, emergentes em geral apanham — mas o BRL pode se descolar se houver fator local dominante.",
        "source": "Yahoo Finance · DX-Y.NYB · Diária",
    },

    "DTWEXBGS": {
        "title": "DTWEXBGS — Trade-Weighted Broad Dollar",
        "short": "Índice do Fed que mede o dólar contra 26 moedas, ponderado por volume de comércio. Inclui CNY e outras emergentes — mais relevante para o BRL que o DXY.",
        "detail": """
O **DTWEXBGS** é mantido pelo Federal Reserve e oferece uma medida muito mais completa da força do dólar que o DXY tradicional.

**Vantagens sobre DXY:**
- 26 moedas (vs 6 do DXY)
- Inclui CNY, ausente no DXY
- Inclui MXN, KRW, INR, BRL
- Pesos ajustados anualmente conforme fluxo comercial

**Limitação:** atualização semanal (sextas-feiras).
        """,
        "why": "Para análise de emergentes, especialmente BRL, é estruturalmente mais informativo que o DXY clássico — captura a perna asiática/emergente do dólar.",
        "source": "FRED · DTWEXBGS · Semanal",
    },

    "CNH": {
        "title": "CNH — Yuan Offshore (Hong Kong)",
        "short": "Yuan negociado fora da China continental. Flutua livremente (CNY tem banda controlada). É o principal driver China-side do BRL.",
        "detail": """
O **CNH** é o yuan chinês negociado em mercados offshore (Hong Kong). Diferente do **CNY** onshore, que tem banda de flutuação de ±2% controlada pelo PBoC.

**Por que importa pro BRL:**
China é o maior comprador de commodities brasileiras. Quando o yuan enfraquece:
1. Commodities em USD ficam mais caras pra China
2. China reduz importações ou pressiona por preços menores
3. Termos de troca do Brasil pioram → BRL deprecia

Defasagem BRL→CNH histórica: poucos dias durante stress.
        """,
        "why": "Indicador antecedente útil para movimentos de moedas emergentes commodity-exporters.",
        "source": "Yahoo Finance · CNH=X · Diária",
    },

    "VIX": {
        "title": "VIX — Volatilidade Implícita S&P 500",
        "short": "Mede volatilidade implícita das opções do S&P 500. Termômetro global de apetite por risco — sobe em stress, cai em períodos calmos.",
        "detail": """
**Faixas de referência:**
- VIX < 15: mercado calmo, risk-on — bom pra carry trade EM
- VIX 15-20: normal
- VIX 20-30: stress moderado — EMs começam a apanhar
- VIX > 30: crise — fuga pra dólar
- VIX > 50: pânico (COVID, Lehman)

**Limitação:** mede vol implícita americana. Choques idiossincráticos brasileiros não aparecem aqui.
        """,
        "why": "Quando VIX sobe, capital flui pra dólar — EMs incluindo BRL apanham sem evento local. Contexto essencial pra distinguir movimento global vs idiossincrático.",
        "source": "Yahoo Finance · ^VIX · 15min delay",
    },

    "MXN": {
        "title": "MXN/USD — Peso Mexicano",
        "short": "Peso mexicano vs dólar. Moeda emergente latino-americana mais líquida, frequentemente comparada com BRL como par 'irmão'.",
        "detail": """
**Por que comparar com BRL:**
- Ambos commodity-exporters
- Ambos bancos centrais independentes com metas de inflação
- Compartilham faixa de risco em portfólios globais

**Diferenças:**
- MXN mais ligado ao ciclo dos EUA (NAFTA/USMCA)
- BRL mais ligado à China (commodities)
- Quando MXN apanha mas BRL não: stress idiossincrático mexicano
- Quando BRL apanha mas MXN não: stress idiossincrático brasileiro

Movimento conjunto = fator EM/LatAm global. Divergente = idiossincrático.
        """,
        "why": "Quando MXN e BRL se movem juntos, é fator EM regional; quando divergem, é fator idiossincrático local.",
        "source": "Yahoo Finance · MXN=X · Diária",
    },

    "ZAR": {
        "title": "ZAR/USD — Rand Sul-Africano",
        "short": "Rand sul-africano. Tem correlação histórica alta com BRL — ambos commodity-exporters emergentes com fragilidades fiscais.",
        "detail": """
**Por que tão correlacionado com BRL:**
- Ambos commodity-exporters (ZA: ouro, platina, minério; BR: minério, soja)
- Ambos têm China como maior parceiro comercial
- Ambos com histórico de fragilidade fiscal
- Frequentemente no mesmo "bucket" de risco emergente

**Como traders globais usam:**
Pra expor risco emergente "high-beta" sem decidir entre BR e ZA, montam cesta BRL+ZAR.

Correlação BRL-ZAR fica frequentemente acima de 0,6 em 30-90 dias.
        """,
        "why": "Peer emergente com correlação histórica mais alta com BRL. Termômetro útil pra separar 'beta de emergente' de 'risco Brasil'.",
        "source": "Yahoo Finance · ZAR=X · Diária",
    },

    "TRY": {
        "title": "TRY/USD — Lira Turca",
        "short": "Lira turca. Moeda emergente mais volátil e politicamente instável — 'canário na mina' pra stress em EMs.",
        "detail": """
A **TRY** é conhecida como uma das moedas emergentes mais voláteis:
- Inflação alta histórica (50%+ em 2022-2024)
- Política monetária controversa
- Intervenções cambiais frequentes
- Fragilidade externa

**Como early warning:**
- TRY caindo + outros EMs estáveis = idiossincrático Turquia
- TRY caindo + MXN/ZAR também caindo = stress EM generalizado, BRL provavelmente apanha em breve
        """,
        "why": "Termômetro de stress emergente. Use em conjunto com MXN e ZAR.",
        "source": "Yahoo Finance · TRY=X · Diária",
    },

    "USDT_PREMIUM": {
        "title": "USDT/BRL Premium",
        "short": "Diferença percentual entre o preço de USDT em BRL nas exchanges crypto e a PTAX oficial. Mede demanda por dólar via cripto vs câmbio tradicional.",
        "detail": """
**Cálculo:**
premium = (preço_USDT_BRL / PTAX) - 1
**Interpretação:**
- **Positivo (>0%):** USDT mais caro que dólar oficial — demanda represada por dólar via cripto
- **Negativo (<0%):** USDT mais barato — excesso de oferta de USDT
- **Próximo de zero:** mercado em equilíbrio

**Faixas típicas no Brasil:**
- < 0,5%: mercado calmo
- 0,5% - 1,5%: normal (cobre custos de on/off-ramp)
- 1,5% - 3%: demanda elevada
- > 3%: stress significativo, arbitragem clara
- > 5%: pânico ou restrição cambial

**Aplicação operacional:**
Quando o premium abre, há demanda represada — sinal antecedente de pressão no PTAX. Para mesa OTC, é também medida direta de oportunidade de arbitragem.

**Dispersão entre exchanges:**
Diferenças refletem (a) liquidez, (b) custos operacionais, (c) base de clientes (varejo vs institucional).
        """,
        "why": "Indicador antecedente de pressão no BRL e medida direta de oportunidade de arbitragem.",
        "source": "APIs públicas: Binance, Mercado Bitcoin, Foxbit, Bitso · PTAX: BCB SGS",
    },

    "P2P_VS_SPOT": {
        "title": "P2P vs Spot — Por que o premium difere",
        "short": "P2P é onde pessoas físicas trocam USDT direto entre si. Spot é o livro de ofertas profissional. P2P geralmente tem premium maior por refletir demanda de varejo.",
        "detail": """
**Spot (livro tradicional):**
- Exchange casa ordens automaticamente
- Market makers profissionais
- Spread bid-ask apertado (0,01-0,1%)

**P2P (peer-to-peer):**
- Pessoas físicas anunciam direto
- Pagamento por PIX, transferência
- Spread bid-ask largo (1-3%)
- Reflete demanda de varejo

**Por que P2P tem premium maior:**
1. PIX é instantâneo, exchange tradicional pode ter delay
2. Anonimato relativo
3. Volumes pequenos (varejo puro)
4. Captura stress cambial primeiro

**Diferencial P2P-Spot como indicador:**
Em regimes normais, diferença é 0,3-0,8%. Quando passa de 1,5%, é sinal de demanda represada por dólar.

**Metodologia neste monitor:**
Mediana das 5 melhores ofertas (em vez da #1 ou média), porque:
- Ignora outliers e spam
- Reflete preço executável com volume
- Mais estável
        """,
        "why": "Quando diverge muito do spot institucional, indica stress cambial que ainda não foi precificado no câmbio oficial.",
        "source": "Binance P2P API (não-oficial) · top 5 mediana",
    },

    "CORR_ROLLING": {
        "title": "Correlação Rolling",
        "short": "Correlação entre retornos do BRL e do índice em janela móvel (padrão: 30 dias). Próxima de zero ou negativa sinaliza descolamento do driver normal.",
        "detail": """
Calculada sobre **retornos percentuais** em janela móvel de N dias.

**Por que retornos e não preços:**
Séries de preço são não-estacionárias. Correlação em nível dá resultados espúrios.

**Interpretação:**
- Forte (>0,5): BRL se move como esperado
- Fraca (-0,2 a 0,2): outros fatores dominam — regime atípico
- Negativa: algo idiossincrático move o BRL contra o fluxo global

**Janela:**
- 10d: muito ruidosa
- 30d: padrão de mesa, equilíbrio
- 90d: estrutural, suaviza eventos pontuais
        """,
        "why": "Identifica quando o BRL está em regime atípico — momentos em que fatores locais dominam sobre driver global.",
        "source": "Cálculo interno · janela ajustável",
    },

    "CORR_DIFFERENTIAL": {
        "title": "Diferencial de Correlação",
        "short": "Indica se o BRL está mais correlacionado com dólar contra emergentes (DTWEXBGS) ou contra G10 (DXY). Identifica o 'regime' em que o real está operando.",
        "detail": """
**Cálculo:**
Diff = corr(PTAX, DTWEXBGS) − corr(PTAX, DXY)
**Interpretação:**
- **Positivo (>0):** BRL como emergente típico — regime "EM-driven"
- **Negativo (<0):** BRL como G10 — carry-trade ou idiossincrático
- **Mudanças bruscas:** transição de regime — momento pra reavaliar posições

**Aplicação:**
- Regime EM → hedge via cesta de emergentes ou DTWEXBGS
- Regime G10 → hedge via DXY ou par específico
- Transição → prêmio adicional em derivativos
        """,
        "why": "Trader que entende regime cobra spread diferente que trader que opera correlação estática.",
        "source": "Cálculo interno",
    },
}


def get_term(key):
    return GLOSSARY.get(key)


def render_inline_description(key, layout="side"):
    term = get_term(key)
    if not term:
        return ""

    return f"""
    <div style="
        background-color: #0A0A0A;
        border: 1px solid #2D2D2D;
        border-left: 3px solid #FFA500;
        padding: 0.8rem 1rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        color: #B0B0B0;
        line-height: 1.6;
        margin: 0.5rem 0;
    ">
        <div style="color: #FFA500; font-weight: 600; margin-bottom: 0.4rem; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.05em;">
            ℹ {term['title']}
        </div>
        <div>{term['short']}</div>
    </div>
    """


def render_detail_expander(key, st):
    term = get_term(key)
    if not term:
        return

    with st.expander(f"📖 Saiba mais sobre {term['title']}"):
        st.markdown(term['detail'])
        st.markdown(f"**Por que importa para o BRL:** {term['why']}")
        st.caption(f"📊 {term['source']}")
