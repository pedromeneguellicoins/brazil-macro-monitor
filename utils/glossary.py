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
        "source": "APIs públicas: Mercado Bitcoin, Foxbit, Bitso, NovaDAX, OKX · PTAX: BCB SGS",
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

    "SELIC": {
        "title": "Selic — Taxa Básica de Juros do Brasil",
        "short": "Taxa básica de juros decidida pelo Copom a cada 45 dias. Define o custo do dinheiro na economia brasileira e é o âncora de todo o sistema de juros do país.",
        "detail": """
A **Selic** (Sistema Especial de Liquidação e Custódia) é a taxa básica de juros da economia brasileira, definida pelo Comitê de Política Monetária do BCB (Copom).

**Dois conceitos importantes:**
- **Selic Meta:** decisão de política monetária do Copom (8 reuniões por ano)
- **Selic Efetiva:** taxa praticada no mercado interbancário (segue a meta, mas pode ter pequenas variações intradiárias)

**Como afeta o BRL:**

Selic alta:
1. Atrai capital estrangeiro buscando carry trade
2. Pressiona BRL pra apreciar
3. Mas se subir por motivo errado (fiscal descontrolado), pode deprecar mesmo assim

Selic baixa:
1. Reduz atratividade do carry trade
2. Pressiona BRL pra depreciar
3. Mas pode favorecer crescimento econômico → BRL via canal de fundamento

**Histórico relevante:**
- 2003: Selic em 26,5% (combate à inflação Lula 1)
- 2013: Selic em 7,25% (mínima histórica até então)
- 2020: Selic em 2,00% (mínima histórica absoluta, pandemia)
- 2022-2023: Selic em 13,75% (combate à inflação pós-pandemia)

**Diferença para o CDI:**
CDI segue a Selic com diferencial mínimo (~10 bps abaixo geralmente). É a referência operacional de fundos e CDBs.
        """,
        "why": "Selic é o principal motor do carry trade brasileiro. Diferencial Selic-Fed é o pilar fundamental que sustenta o BRL em períodos sem stress idiossincrático.",
        "source": "BCB SGS · Séries 432 (meta) e 4189 (efetiva) · Diária",
    },

    "FED_FUNDS": {
        "title": "Fed Funds Rate — Taxa Básica de Juros dos EUA",
        "short": "Taxa básica de juros decidida pelo FOMC (Fed) a cada 6 semanas. É a referência global de juros em dólar e ancora todo o mercado financeiro mundial.",
        "detail": """
A **Federal Funds Rate** é a taxa básica de juros dos EUA, decidida pelo Federal Open Market Committee (FOMC, comitê do Federal Reserve) em 8 reuniões anuais.

**Por que é o juro mais importante do mundo:**

1. **USD é a moeda de reserva global** — Fed Funds afeta custo de capital globalmente
2. **Treasuries são o ativo livre de risco mundial** — Fed Funds ancora curva
3. **Carry trade global** depende do diferencial Fed Funds vs juros de outros países

**Como afeta o BRL:**

Fed alto:
1. Capital migra pra EUA buscando juros mais altos
2. Emergentes incluindo Brasil perdem fluxo
3. BRL deprecia mesmo se Selic estiver alta também (carry trade encolhe)

Fed baixo:
1. Capital busca yield em emergentes
2. BRL favorecido pelo "search for yield"
3. Carry trade Brasil-US vira atrativo

**Histórico relevante:**
- 2008-2015: 0-0,25% (pós-crise Lehman, ZIRP)
- 2018-2019: 2,25-2,50% (ciclo de alta Powell I)
- 2020-2022: 0-0,25% (pandemia)
- 2022-2023: subiu de 0,25% para 5,50% (combate inflação pós-pandemia, mais agressivo da história)
- 2024-2025: gradual descida

**Indicador a observar:**
Dot Plot (projeções dos membros do FOMC) e expectativa de cortes via FedWatch CME.
        """,
        "why": "Fed Funds define o regime de capital global. Quando Fed corta, é geralmente vento favorável pro BRL. Quando sobe, é vento contra — mesmo com Selic alta.",
        "source": "FRED · DFF · Diária",
    },

    "RATE_SPREAD": {
        "title": "Spread Brasil-EUA (Selic - Fed Funds)",
        "short": "Diferencial nominal entre Selic e Fed Funds. É o motor do carry trade BRL — quando alto, atrai capital pra Brasil; quando baixo ou negativo, capital sai.",
        "detail": """
**Cálculo:**
Spread BR-US = Selic (Brasil) - Fed Funds (EUA)

**Interpretação:**

O spread representa quanto mais um investidor recebe ao colocar dinheiro no Brasil vs nos EUA, em **termos nominais** (sem ajustar pra inflação).

**Faixas históricas:**
- Spread > 10 pp: muito atrativo, BRL deveria estar muito forte
- Spread 5-10 pp: atrativo, regime normal de carry
- Spread 2-5 pp: marginal, BRL precisa de outros fundamentos
- Spread < 2 pp: carry trade morto, BRL vulnerável

**Por que "deveria" mas nem sempre é:**

O spread nominal alto **deveria** sustentar o BRL. Mas existem **3 razões** pelas quais nem sempre funciona:

1. **Risco cambial:** se o mercado precifica que o BRL vai depreciar 15% no ano, um spread de 10% não compensa
2. **Risco fiscal:** se Brasil está com fiscal deteriorando, investidores exigem prêmio maior — mesmo com Selic alta
3. **Risco político:** eleições, ruptura institucional → investidores fogem mesmo com carry alto

**Histórico de divergências famosas:**

- **2015:** Selic alta (14,25%), Fed baixo (0,25%) — spread de 14 pp. BRL apanhou mesmo assim (Lava Jato, recessão, Dilma).
- **2024:** Selic 10,75%, Fed 5,5% — spread 5,25 pp. BRL desabou pra R$ 6,20 (crise fiscal).

**Carry real vs carry nominal:**
Mais importante que o spread nominal é o **spread real** (ajustado pela inflação dos dois países). Esse está em outra entrada do glossário.
        """,
        "why": "É o fundamento mais clássico do BRL. Quando o spread está alto e o BRL não aprecia, sinal de stress idiossincrático Brasil. Quando o spread cai e BRL não deprecia, sinal de que outro fator (commodity, fluxo) está sustentando.",
        "source": "Cálculo interno · BCB SGS + FRED",
    },

    "CARRY_REAL": {
        "title": "Carry Real (Spread Real Brasil-EUA)",
        "short": "Spread entre juros reais (descontados da inflação) do Brasil e dos EUA. É o indicador mais limpo de atratividade do BRL para capital externo de longo prazo.",
        "detail": """
**Cálculo:**

Carry Real = (Selic - IPCA 12m) - (Fed Funds - CPI 12m)

Onde:
- IPCA 12m: inflação acumulada Brasil últimos 12 meses
- CPI 12m: inflação acumulada EUA últimos 12 meses

**Por que real é melhor que nominal:**

Investidor estrangeiro raciocina em termos de **poder de compra**. Se Brasil tem Selic 14% mas inflação 10%, o juro real é só 4%. Se EUA tem Fed 5% mas inflação 3%, o juro real é 2%. O spread real é 4% - 2% = 2%, muito menor que o spread nominal (9%).

**Faixas históricas:**

- Carry real > 6 pp: excelente, BRL muito atrativo
- Carry real 3-6 pp: atrativo, regime normal
- Carry real 1-3 pp: marginal
- Carry real < 1 pp: pouco atrativo
- Carry real negativo: estruturalmente ruim pra BRL

**Exemplos práticos:**

**2023:**
- Selic 13,75%, IPCA 4,5% → Real BR = 9,25%
- Fed 5,25%, CPI 3,2% → Real US = 2,05%
- **Carry real = 7,2 pp** — muito atrativo
- BRL apreciou de 5,30 pra 4,80 no ano

**2020:**
- Selic 2%, IPCA 4,5% → Real BR = -2,5%
- Fed 0,25%, CPI 1,4% → Real US = -1,15%
- **Carry real = -1,35 pp** — negativo
- BRL apanhou (5,90)

**Limitações:**

1. Inflação é backward-looking (últimos 12 meses, não próximos 12)
2. Expectativas de inflação podem ser diferentes da realizada
3. Ignora prêmio de risco (CDS, fiscal, etc)
        """,
        "why": "É a métrica mais robusta para o BRL no longo prazo. Quando carry real está alto e BRL não aprecia, é sinal claro de stress idiossincrático. Quando carry real cai, geralmente precede depreciação estrutural.",
        "source": "Cálculo interno · BCB SGS (IPCA) + FRED (CPI)",
    },

    "UST_CURVE": {
        "title": "Curva Americana (UST 2Y, 10Y)",
        "short": "Yields dos Treasuries americanos. O spread 10Y-2Y é o indicador mais clássico de recessão dos EUA — quando inverte (negativo), recessão geralmente segue em 12-18 meses.",
        "detail": """
**Componentes:**

- **UST 2Y:** Treasury de 2 anos. Reflete expectativa de Fed Funds nos próximos 2 anos
- **UST 10Y:** Treasury de 10 anos. Reflete expectativa de crescimento de longo prazo + prêmio de risco
- **Spread 10Y-2Y:** diferencial entre os dois

**Por que o spread 10Y-2Y é importante:**

Em condições normais, a curva é **ascendente** (10Y > 2Y) porque investidores exigem prêmio pra prazos mais longos.

Quando a curva **inverte** (10Y < 2Y, spread negativo):
- Mercado precifica que Fed vai cortar juros em breve
- Geralmente porque vê desaceleração/recessão à frente
- **Indicador antecedente de recessão:** todas as recessões americanas dos últimos 50 anos foram precedidas por inversão da curva 10Y-2Y

**Como afeta o BRL:**

Curva inclinada (spread positivo, normal):
- EUA crescendo, risco-on global
- Capital flui pra emergentes incluindo BRL

Curva invertida (spread negativo):
- Mercado precifica recessão US
- Geralmente Fed corta juros → bom pra emergentes via canal de juros
- Mas se recessão for severa, risk-off domina e BRL apanha

**Histórico:**

- 2006-2007: curva invertida — recessão 2008
- 2019: brevemente invertida — recessão 2020 (acelerada por COVID)
- 2022-2024: curva profundamente invertida (-100 bps em pico)
        """,
        "why": "Sinal antecedente mais robusto de recessão americana. Quando inverte, mercado precifica corte do Fed — vento favorável pra carry trade emergente nos meses seguintes.",
        "source": "FRED · DGS2, DGS10 · Diária",
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

