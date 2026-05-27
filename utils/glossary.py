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
**Cálculo:**  Diff = corr(PTAX, DTWEXBGS) − corr(PTAX, DXY)

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

    "COMMODITIES_EXPORT": {
        "title": "Commodities Brasileiras de Exportação",
        "short": "Brasil é exportador líquido de petróleo, soja, minério de ferro e café. Quando esses preços sobem, geram fluxo de USD para o país e tendem a fortalecer o BRL.",
        "detail": """
**As 4 principais commodities exportadas pelo Brasil (2025):**

| Commodity | Valor exportado | Ranking |
|---|---|---|
| **Petróleo Bruto** (Brent) | US$ 44 bi | #1 |
| **Soja em grão** | US$ 43 bi | #2 |
| **Minério de Ferro** | US$ 26 bi | #3 |
| **Café Arábica** | US$ 15 bi | #4 |

**Como afetam o BRL:**

Quando os preços sobem:
1. Exportadores recebem mais USD por unidade exportada
2. Maior fluxo de USD entrando no país
3. Pressão de oferta sobre o USD → BRL aprecia
4. Termos de troca melhoram → confiança no real aumenta

**Defasagem típica:** O canal preço-câmbio opera com defasagem de 5-15 dias úteis. Movimentos súbitos de commodities são geralmente seguidos por movimento do BRL na mesma semana.

**Limitações como indicador:**
- Não captura volumes exportados (só preços)
- Petróleo e soja têm canais financeiros (futuros) que se movem antes do canal físico
- Eventos climáticos podem mover preços sem afetar Brasil específico
        """,
        "why": "Commodities de exportação são o pilar fundamental da balança comercial brasileira. Quando sobem em uníssono, o BRL ganha fluxo estrutural e tende a se fortalecer mesmo contra dólar global forte.",
        "source": "Yahoo Finance · BZ=F, ZS=F, TIO=F, KC=F · Diária",
    },

    "COMMODITIES_IMPORT": {
        "title": "Commodities Brasileiras de Importação",
        "short": "Brasil é importador líquido de derivados de petróleo (gasolina, diesel) e gás natural. Quando esses preços sobem, aumentam custos internos e pressionam o BRL para depreciar.",
        "detail": """
**As 3 principais commodities importadas pelo Brasil:**

| Commodity | % das importações | Por quê |
|---|---|---|
| **Gasolina refinada** | ~3% | Refinarias BR não processam todo cru pesado |
| **Diesel** | ~3% | Maior consumo do transporte rodoviário |
| **Gás Natural (GNL)** | ~1.5% | Demanda industrial e térmicas |

**Paradoxo brasileiro:**
O Brasil **exporta petróleo bruto** (pesado, das jazidas do pré-sal) e **importa derivados refinados** (mais leves, de refinarias internacionais). Isso porque o parque refinador brasileiro foi historicamente desenhado para processar petróleo médio do Oriente Médio, não o cru pesado nacional.

**Como afetam o BRL:**

Quando os preços de derivados sobem:
1. Importadores precisam comprar mais USD para pagar combustíveis
2. Pressão de demanda sobre o USD → BRL deprecia
3. Aumento de custos internos → inflação pressionada (gasolina, transportes)
4. BC pode precisar subir Selic → impacto secundário

**Sinal contrário ao das exportações:** quando preços de exportação E importação sobem juntos (ex: 2022 com guerra), o efeito líquido depende dos **termos de troca**.
        """,
        "why": "Custos de importação afetam balança comercial e inflação interna. Quando derivados sobem mas exportações não acompanham, BRL deprecia por dois canais: comercial e inflacionário.",
        "source": "Yahoo Finance · RB=F, HO=F, NG=F · Diária",
    },

    "TERMS_OF_TRADE": {
        "title": "Termos de Troca",
        "short": "Razão entre o preço médio das exportações e o preço médio das importações brasileiras. Quando sobe, Brasil 'ganha' no fluxo comercial; quando cai, 'perde'. É o indicador macro mais limpo de fundamentals do BRL.",
        "detail": """
**Conceito clássico de macroeconomia:**

Termos de Troca = Preço médio das Exportações / Preço médio das Importações

**Por que é o indicador macro mais limpo:**

Se o Brasil exporta a US$100 e importa a US$80, está "ganhando" — pode importar mais com cada unidade exportada. Se exporta a US$100 e importa a US$120, está "perdendo" — precisa exportar mais para importar o mesmo.

**Metodologia neste monitor:**

1. **Cesta de Exportação** (média de 4 commodities normalizadas):
   - Brent, Soja, Minério de Ferro, Café Arábica
2. **Cesta de Importação** (média de 3 commodities normalizadas):
   - Gasolina, Diesel, Gás Natural
3. **Cada série normalizada para base 100 = 1 ano atrás**
   - Necessário porque commodities têm unidades diferentes (US$/barril, cents/bushel, etc)
4. **Índice de TT = (Cesta Exp / Cesta Imp) × 100**

**Interpretação:**
- **TT > 100:** termos de troca melhoraram desde a base — Brasil ganhando
- **TT < 100:** termos de troca pioraram — Brasil perdendo
- **TT estável:** equilíbrio entre os dois lados

**Relação com BRL:**

Historicamente, TT e PTAX têm correlação **negativa forte** (-0.5 a -0.7):
- TT sobe → BRL aprecia (cai)
- TT cai → BRL deprecia (sobe)

Quando TT e BRL **divergem** (ambos sobem ou ambos caem juntos), é sinal de que outro fator está dominando o BRL (fiscal, monetário, fluxo de capital).

**Limitações:**
- Não inclui preços de volume — assume volumes constantes
- Cesta simplificada (apenas commodities líquidas com futures)
- Não captura serviços, manufaturados, etc.
        """,
        "why": "É o fundamento estrutural mais robusto do BRL no curto-médio prazo. Quando você quer saber se o real 'merece' estar onde está, olhar TT vs PTAX é o primeiro reality check.",
        "source": "Cálculo interno · cestas normalizadas base 100 anual",
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


