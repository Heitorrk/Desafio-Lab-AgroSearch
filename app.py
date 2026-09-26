# -*- coding: utf-8 -*-
"""
=============================================================================
INSTITUIÇÃO: UNIPÊ - Centro Universitário de João Pessoa
CURSO: Ciência da Computação / Engenharia de Software
DISCIPLINA: Tópicos Avançados - Recuperação de Informação / PLN
PROFESSOR: Me. Ricardo Roberto de Lima
ATIVIDADE: Laboratório Prático 04 - Desafio Integrador
PROJETO: AgroSearch - Motor de Busca Inteligente
EQUIPE:
- Mateus Ieno Ramalho
- Heitor de Oliveira Mamede
- Júlio César Carvalho Santos
=============================================================================
RESTRIÇÃO TÉCNICA CUMPRIDA RIGOROSAMENTE:
- Implementação 100% "from scratch" (do zero), sem o uso de bibliotecas
  de alto nível (como scikit-learn, TfidfVectorizer ou dependências de NLP).
- Fases 1, 2, 3 e Desafio Bônus (Similaridade de Cosseno) construídos
  puramente em Python com estruturas nativas e módulo math.
=============================================================================
"""

import math
import re
import unicodedata
import streamlit as st
import pandas as pd

# =============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS VISUAIS (DESIGN AESTHETICS)
# =============================================================================
st.set_page_config(
    page_title="AgroSearch | Motor de Busca Inteligente",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada para estética premium e profissional
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Hero Header */
    .hero-container {
        background: linear-gradient(135deg, #1b4332 0%, #2d6a4f 50%, #40916c 100%);
        padding: 24px 30px;
        border-radius: 14px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(27, 67, 50, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .hero-title {
        font-size: 2.1rem;
        font-weight: 700;
        margin: 0;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .hero-subtitle {
        font-size: 0.98rem;
        color: #d8f3dc;
        margin-top: 6px;
        margin-bottom: 12px;
        font-weight: 400;
    }
    
    .hero-badges {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    
    .hero-badge {
        background: rgba(255, 255, 255, 0.16);
        backdrop-filter: blur(8px);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Card de Destaque - Documento Vencedor */
    .winner-card {
        background: linear-gradient(145deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid #86efac;
        border-radius: 12px;
        padding: 20px 24px;
        margin: 16px 0;
        box-shadow: 0 4px 16px rgba(34, 197, 94, 0.12);
    }
    
    .winner-badge {
        background: #15803d;
        color: white;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        display: inline-block;
        margin-bottom: 8px;
    }
    
    .winner-doc-id {
        font-size: 1.25rem;
        font-weight: 700;
        color: #14532d;
        margin-bottom: 6px;
    }
    
    .winner-text {
        font-size: 1.02rem;
        color: #1f2937;
        line-height: 1.5;
        background: white;
        padding: 14px 18px;
        border-radius: 8px;
        border-left: 4px solid #16a34a;
        margin-top: 8px;
    }
    
    mark.highlight {
        background-color: #fef08a;
        color: #854d0e;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
    }
    
    /* Métricas estilizadas */
    .metric-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
    }
    
    .metric-val {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1b4332;
    }
    
    .metric-label {
        font-size: 0.82rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Token Pills */
    .token-pill {
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1;
        padding: 3px 10px;
        border-radius: 16px;
        font-size: 0.85rem;
        font-family: monospace;
        font-weight: 600;
        margin: 2px 4px;
        border: 1px solid #bae6fd;
    }

    .phase-badge {
        display: inline-block;
        background: #2d6a4f;
        color: white;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# 2. BASE DE DADOS PADRÃO (HARDCODE SUGERIDO NO DESAFIO)
# =============================================================================
DOCUMENTS_DEFAULT = {
    1: "A soja requer irrigação constante durante o período de floração para garantir a produtividade.",
    2: "O controle biológico de lagartas na soja pode ser feito com a vespa Trichogramma.",
    3: "A adubação verde com leguminosas melhora o nitrogênio no solo para o milho.",
    4: "Lagartas desfolhadoras causam grande prejuízo na cultura da soja e do algodão.",
    5: "A irrigação por gotejamento economiza água e é ideal para o cultivo orgânico."
}

if "documents" not in st.session_state:
    st.session_state.documents = DOCUMENTS_DEFAULT.copy()

# Controle de estado das flags de pré-processamento
if "opt_stopwords" not in st.session_state:
    st.session_state.opt_stopwords = True

if "opt_stemming" not in st.session_state:
    st.session_state.opt_stemming = True


# =============================================================================
# 3. FASE 1: O PIPELINE DE PRÉ-PROCESSAMENTO (FROM SCRATCH)
# =============================================================================
# Lista enriquecida de Stopwords em Português (sem dependências externas)
STOPWORDS_PORTUGUESE = {
    "a", "ao", "aos", "aquela", "aquelas", "aquele", "aqueles", "aquilo", "as",
    "ate", "com", "como", "da", "das", "de", "dela", "delas", "dele", "deles",
    "depois", "do", "dos", "e", "ela", "elas", "ele", "eles", "em", "entre",
    "era", "eram", "eramos", "essa", "essas", "esse", "esses", "esta", "estamos",
    "estao", "estas", "estava", "estavam", "estavamos", "este", "esteja", "estejam",
    "estejamos", "estes", "esteve", "estive", "estivemos", "estiver", "estivera",
    "estiveram", "estiveramos", "estiverem", "estiveremos", "estiveres", "estivesse",
    "estivessem", "estivessemos", "estou", "eu", "foi", "fomos", "for", "fora",
    "foram", "foramos", "forem", "fores", "fosse", "fossem", "fossemos", "fui",
    "ha", "haja", "hajam", "hajamos", "havemos", "hei", "houve", "houvemos",
    "houver", "houvera", "houveram", "houveramos", "houverem", "houveremos",
    "houveres", "houvesse", "houvessem", "houvessemos", "isso", "isto", "ja",
    "lhe", "lhes", "mais", "mas", "me", "mesmo", "meu", "meus", "minha",
    "minhas", "muito", "na", "nao", "nas", "nem", "no", "nos", "nossa",
    "nossas", "nosso", "nossos", "num", "numa", "o", "os", "ou", "para",
    "pela", "pelas", "pelo", "pelos", "por", "qual", "quando", "que", "quem",
    "sao", "se", "seja", "sejam", "sejamos", "sem", "ser", "sera", "serao",
    "seriamos", "seria", "seriam", "so", "somos", "sou", "sua", "suas",
    "tambem", "te", "tem", "temos", "tenha", "tenham", "tenhamos", "tenho",
    "ter", "tera", "terao", "teriamos", "teria", "teriam", "teu", "teus",
    "teve", "tinha", "tinham", "tinhamos", "tive", "tivemos", "tiver", "tivera",
    "tiveram", "tiveramos", "tiverem", "tiveremos", "tiveres", "tivesse",
    "tivessem", "tivessemos", "tu", "tua", "tuas", "um", "uma", "uns", "umas",
    "voce", "voces", "vos", "durante", "pode", "podem", "grande", "feito",
    "sendo", "sido", "pra", "ante", "sob", "sobre", "tras"
}


def remove_accents(text: str) -> str:
    """Etapa de Normalização: remove diacríticos e acentos via decomposição Unicode."""
    normalized = unicodedata.normalize('NFKD', text)
    return "".join([c for c in normalized if not unicodedata.combining(c)])


def stem_portuguese(word: str) -> str:
    """
    Etapa de Stemming: Algoritmo de radicalização baseado em regras morfológicas
    de sufixos da língua portuguesa (inspirado no RSLP e Snowball).
    Preserva radicais com no mínimo 3 caracteres para evitar sub-radicalização.
    """
    w = word.lower()
    if len(w) <= 3:
        return w

    # 1. Sufixos Adverbiais
    suffixes_adverb = ["osamente", "icamente", "avelmente", "ivelmente", "mente"]
    for s in suffixes_adverb:
        if w.endswith(s) and len(w) - len(s) >= 3:
            w = w[:-len(s)]
            break

    # 2. Sufixos Nominais e Formadores de Substantivos/Adjetivos
    suffixes_noun = [
        "abilidade", "icidade", "edade", "idade", "ismo", "ista",
        "amento", "imento", "adora", "ador", "acao", "acoes", "coes",
        "avel", "ivel", "oso", "osa", "osos", "osas"
    ]
    for s in suffixes_noun:
        if w.endswith(s) and len(w) - len(s) >= 3:
            w = w[:-len(s)]
            break

    # 3. Sufixos Verbais
    suffixes_verb = [
        "ariamos", "eriamos", "iriamos", "assem", "essem", "issem",
        "avamos", "evamos", "ivamos", "aram", "eram", "iram",
        "ando", "endo", "indo", "adas", "ados", "idas", "idos",
        "asse", "esse", "isse", "aria", "eria", "iria",
        "ara", "era", "ira", "ava", "eva", "iva",
        "ou", "eu", "iu", "ar", "er", "ir"
    ]
    for s in suffixes_verb:
        if w.endswith(s) and len(w) - len(s) >= 3:
            w = w[:-len(s)]
            break

    # 4. Formas Plurais e Variações de Gênero
    if w.endswith("oes") and len(w) - 3 >= 3:
        w = w[:-3] + "ao"
    elif w.endswith("aes") and len(w) - 3 >= 3:
        w = w[:-3] + "ao"
    elif w.endswith("ais") and len(w) - 3 >= 3:
        w = w[:-3] + "al"
    elif w.endswith("eis") and len(w) - 3 >= 3:
        w = w[:-3] + "el"
    elif w.endswith("is") and len(w) - 2 >= 3:
        w = w[:-2] + "il"
    elif w.endswith("s") and len(w) - 1 >= 3:
        w = w[:-1]

    return w


def preprocess_text(text: str, remove_stopwords: bool = True, apply_stemming: bool = True) -> tuple[list[str], dict]:
    """
    Executa o pipeline completo de 4 etapas:
    1. Normalização (lower + remoção de acentos)
    2. Tokenização (divisão em palavras alfanuméricas)
    3. Remoção de Stopwords (se ativada via checkbox)
    4. Stemming / Radicalização (se ativada via checkbox)
    Retorna a lista final de tokens e um dicionário de auditoria de cada etapa.
    """
    # 1. Normalização
    norm_text = remove_accents(text.lower())
    
    # 2. Tokenização
    raw_tokens = re.findall(r'[a-zA-Z0-9]+', norm_text)
    
    # 3. Stopwords
    stopwords_removed = []
    if remove_stopwords:
        filtered_tokens = []
        for token in raw_tokens:
            if token in STOPWORDS_PORTUGUESE:
                stopwords_removed.append(token)
            else:
                filtered_tokens.append(token)
    else:
        filtered_tokens = raw_tokens
        
    # 4. Stemming
    stem_map = {}
    if apply_stemming:
        final_tokens = []
        for token in filtered_tokens:
            st_token = stem_portuguese(token)
            stem_map[token] = st_token
            final_tokens.append(st_token)
    else:
        final_tokens = filtered_tokens

    audit = {
        "original": text,
        "normalized": norm_text,
        "raw_tokens": raw_tokens,
        "stopwords_removed": stopwords_removed,
        "after_stopwords": filtered_tokens,
        "stem_map": stem_map,
        "final_tokens": final_tokens
    }
    return final_tokens, audit


# =============================================================================
# 4. FASE 2: O ÍNDICE INVERTIDO (FROM SCRATCH)
# =============================================================================
def build_inverted_index(documents: dict[int, str], remove_stopwords: bool, apply_stemming: bool):
    """
    Constrói o Índice Invertido:
    Mapeamento Termo -> [Lista de Doc IDs] e metadados de frequência.
    """
    inverted_index = {}        # Termo -> [doc_id1, doc_id2, ...]
    term_frequencies = {}      # Termo -> {doc_id: contagem_no_doc}
    doc_tokens_dict = {}       # doc_id -> list[tokens]
    doc_audits = {}            # doc_id -> audit pipeline dict

    for doc_id, text in documents.items():
        tokens, audit = preprocess_text(text, remove_stopwords, apply_stemming)
        doc_tokens_dict[doc_id] = tokens
        doc_audits[doc_id] = audit
        
        counts = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1
            
        for t, count in counts.items():
            if t not in inverted_index:
                inverted_index[t] = []
                term_frequencies[t] = {}
            inverted_index[t].append(doc_id)
            term_frequencies[t][doc_id] = count

    vocabulary = sorted(list(inverted_index.keys()))
    return inverted_index, term_frequencies, doc_tokens_dict, vocabulary, doc_audits


# =============================================================================
# 5. FASE 3: BUSCA E RANQUEAMENTO TF-IDF & DESAFIO BÔNUS (COSSENO)
# =============================================================================
def calculate_tf_idf_model(documents: dict[int, str], inverted_index: dict, term_frequencies: dict, doc_tokens_dict: dict):
    """
    Calcula matrizes e tabelas de TF, DF, IDF e TF-IDF para toda a coleção:
    - N: Total de documentos
    - DF(t): Document Frequency = número de documentos contendo t
    - IDF(t): log10(N / DF(t)) + 1.0 (com suavização)
    - TF(t, d): Frequência relativa = contagem(t, d) / total_tokens(d)
    - TF-IDF(t, d): TF(t, d) * IDF(t)
    """
    N = len(documents)
    df_dict = {t: len(docs) for t, docs in inverted_index.items()}
    
    idf_dict = {
        t: (math.log10(N / df_dict[t]) + 1.0) if df_dict[t] > 0 else 0.0
        for t in df_dict
    }
    
    tf_matrix = {}
    tfidf_matrix = {}
    
    for doc_id, tokens in doc_tokens_dict.items():
        tf_matrix[doc_id] = {}
        tfidf_matrix[doc_id] = {}
        total_tokens = len(tokens)
        
        for t in set(tokens):
            raw_count = term_frequencies[t][doc_id]
            tf_val = raw_count / total_tokens if total_tokens > 0 else 0.0
            tfidf_val = tf_val * idf_dict[t]
            
            tf_matrix[doc_id][t] = tf_val
            tfidf_matrix[doc_id][t] = tfidf_val

    return df_dict, idf_dict, tf_matrix, tfidf_matrix


def search_and_rank(
    query: str,
    documents: dict[int, str],
    inverted_index: dict,
    df_dict: dict,
    idf_dict: dict,
    tfidf_matrix: dict,
    remove_stopwords: bool,
    apply_stemming: bool
):
    """
    Executa a busca e o ranqueamento:
    1. Pré-processa os tokens da query
    2. Calcula TF-IDF Acumulado (soma dos pesos dos termos da query)
    3. Calcula Similaridade de Cosseno (Desafio Bônus) entre query e documento
    """
    query_tokens, query_audit = preprocess_text(query, remove_stopwords, apply_stemming)
    if not query_tokens:
        return [], query_tokens, query_audit, {}, []

    query_counts = {}
    for t in query_tokens:
        query_counts[t] = query_counts.get(t, 0) + 1
        
    query_len = len(query_tokens)
    query_tfidf = {}
    for t, count in query_counts.items():
        if t in idf_dict:
            t_tf = count / query_len
            t_idf = idf_dict[t]
            query_tfidf[t] = t_tf * t_idf

    norm_query = math.sqrt(sum(w ** 2 for w in query_tfidf.values()))

    results = []
    audit_table_rows = []

    for doc_id, text in documents.items():
        doc_weights = tfidf_matrix[doc_id]
        
        # 1. TF-IDF Acumulado
        accumulated_tfidf = 0.0
        matched_in_doc = []
        
        for t in set(query_tokens):
            if t in doc_weights:
                weight = doc_weights[t]
                accumulated_tfidf += weight
                matched_in_doc.append(t)
                
                audit_table_rows.append({
                    "Doc ID": f"Doc {doc_id}",
                    "Termo": t,
                    "DF": df_dict.get(t, 0),
                    "IDF": round(idf_dict.get(t, 0.0), 4),
                    "TF no Doc": round(weight / idf_dict.get(t, 1.0), 4),
                    "TF-IDF no Doc": round(weight, 4),
                    "Peso na Query": round(query_tfidf.get(t, 0.0), 4)
                })

        # 2. Similaridade de Cosseno (Desafio Bônus)
        dot_product = sum(query_tfidf.get(t, 0.0) * doc_weights.get(t, 0.0) for t in query_tokens if t in doc_weights)
        norm_doc = math.sqrt(sum(w ** 2 for w in doc_weights.values()))
        
        if norm_query > 0 and norm_doc > 0:
            cosine_similarity = dot_product / (norm_query * norm_doc)
        else:
            cosine_similarity = 0.0

        results.append({
            "doc_id": doc_id,
            "text": text,
            "accumulated_tfidf": accumulated_tfidf,
            "cosine_similarity": cosine_similarity,
            "matched_terms": matched_in_doc
        })

    return results, query_tokens, query_audit, query_tfidf, audit_table_rows


def highlight_matched_text(text: str, matched_stems: list[str], remove_stopwords: bool, apply_stemming: bool) -> str:
    """Gera visualização com tags <mark> destacando os termos relevantes encontrados."""
    words = re.findall(r'\S+', text)
    highlighted = []
    
    for word in words:
        clean_word = re.sub(r'[^a-zA-Z0-9áéíóúâêîôûãõçÁÉÍÓÚÂÊÎÔÛÃÕÇ]', '', word)
        tokens, _ = preprocess_text(clean_word, remove_stopwords=remove_stopwords, apply_stemming=apply_stemming)
        
        if any(t in matched_stems for t in tokens):
            highlighted.append(f"<mark class='highlight'>{word}</mark>")
        else:
            highlighted.append(word)
            
    return " ".join(highlighted)


# =============================================================================
# 6. BARRA LATERAL (CONTROLES E GERENCIAMENTO DO CORPUS)
# =============================================================================
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1574943320219-553eb213f72d?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.markdown("### ⚙️ Painel de Controle")
    st.caption("Ajuste as configurações globais do motor de busca.")
    
    st.markdown("#### 1. Flags do Pipeline (Fase 1)")
    sidebar_stopwords = st.checkbox(
        "Remover Stopwords",
        value=st.session_state.opt_stopwords,
        key="sb_stopwords",
        help="Ativa/desativa a exclusão de termos gramaticais."
    )
    sidebar_stemming = st.checkbox(
        "Aplicar Stemming",
        value=st.session_state.opt_stemming,
        key="sb_stemming",
        help="Ativa/desativa a redução morfológica ao radical comum."
    )
    
    # Sincroniza estado das flags
    st.session_state.opt_stopwords = sidebar_stopwords
    st.session_state.opt_stemming = sidebar_stemming

    st.divider()
    st.markdown("#### 2. Critério de Ranqueamento (Fase 3 & Bônus)")
    ranking_mode = st.radio(
        "Métrica de Ordenação Principal:",
        options=["Similaridade de Cosseno (Desafio Bônus)", "TF-IDF Acumulado (Soma Direta)"],
        index=0,
        help="Define o critério que determina a posição e o Documento Vencedor."
    )
    
    st.divider()
    st.markdown("#### 3. Base de Documentos (Hardcode 5 Docs)")
    with st.expander("📚 Ver / Gerenciar Manuais", expanded=False):
        for doc_id, doc_text in sorted(st.session_state.documents.items()):
            st.markdown(f"**Doc {doc_id}:** {doc_text}")
            
        st.markdown("---")
        st.markdown("**Adicionar Novo Manual:**")
        with st.form("form_add_doc"):
            new_text = st.text_area("Texto do manual agrícola:", placeholder="Ex: A rotação de culturas melhora a retenção hídrica do solo.")
            submitted = st.form_submit_button("➕ Adicionar à Base")
            if submitted and new_text.strip():
                next_id = max(st.session_state.documents.keys()) + 1 if st.session_state.documents else 1
                st.session_state.documents[next_id] = new_text.strip()
                st.success(f"Doc {next_id} adicionado!")
                st.rerun()
                
        if st.button("🔄 Restaurar 5 Documentos Padrão"):
            st.session_state.documents = DOCUMENTS_DEFAULT.copy()
            st.info("Base padrão restaurada com sucesso.")
            st.rerun()

    st.markdown("---")
    st.caption("🏛️ **UNIPÊ - Tópicos Avançados**<br>Prof. Me. Ricardo Roberto de Lima", unsafe_allow_html=True)


# =============================================================================
# 7. EXECUÇÃO DO PIPELINE E ÍNDICE EM MEMÓRIA
# =============================================================================
inv_index, term_freqs, doc_tokens, vocab, audits = build_inverted_index(
    st.session_state.documents,
    remove_stopwords=st.session_state.opt_stopwords,
    apply_stemming=st.session_state.opt_stemming
)

df_dict, idf_dict, tf_matrix, tfidf_matrix = calculate_tf_idf_model(
    st.session_state.documents,
    inv_index,
    term_freqs,
    doc_tokens
)


# =============================================================================
# 8. CABEÇALHO HERO DA APLICAÇÃO
# =============================================================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🌱 AgroSearch &mdash; Motor de Busca Inteligente</div>
    <div class="hero-subtitle">Recuperação de Informação Textual e Mineração de Manuais Agrícolas &bull; Implementação 100% From Scratch</div>
    <div class="hero-badges">
        <span class="hero-badge">🏛️ UNIPÊ</span>
        <span class="hero-badge">📚 Laboratório Prático 04 (Desafio Integrador)</span>
        <span class="hero-badge">👨‍🏫 Prof. Me. Ricardo Roberto de Lima</span>
        <span class="hero-badge">⭐ Desafio Bônus: Similaridade de Cosseno Ativa</span>
    </div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# 9. ABAS DE NAVEGAÇÃO SEGUINDO A RISCA AS FASES DA ESPECIFICAÇÃO
# =============================================================================
tab1_pipeline, tab2_indice, tab3_busca, tab4_auditoria = st.tabs([
    "⚙️ Fase 1: Pipeline de Pré-processamento",
    "🗂️ Fase 2: O Índice Invertido",
    "🔍 Fase 3: Busca e Ranqueamento TF-IDF & Bônus",
    "📐 Auditoria Matemática & Desafio Bônus"
])


# -----------------------------------------------------------------------------
# ABA 1: FASE 1 - O PIPELINE DE PRÉ-PROCESSAMENTO
# -----------------------------------------------------------------------------
with tab1_pipeline:
    st.markdown('<span class="phase-badge">FASE 1 DA ESPECIFICAÇÃO</span>', unsafe_allow_html=True)
    st.markdown("### ⚙️ Pipeline de Pré-processamento de Texto")
    st.caption("Implementação das 4 etapas fundamentais: Normalização, Tokenização, Stopwords e Stemming.")

    # Painel interativo exigido: "A UI deve permitir ligar/desligar Stemming e Stopwords via checkboxes para ver o vocabulário mudar dinamicamente"
    st.markdown("#### 🎛️ Controles Interativos da Fase 1")
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        tab_opt_stop = st.checkbox(
            "✅ Ativar Remoção de Stopwords",
            value=st.session_state.opt_stopwords,
            key="tab_opt_stop_key",
            help="Filtra palavras com baixa carga discriminativa."
        )
    with col_ctrl2:
        tab_opt_stem = st.checkbox(
            "✅ Ativar Stemming (Radicalização)",
            value=st.session_state.opt_stemming,
            key="tab_opt_stem_key",
            help="Reduz flexões ao seu radical comum em português."
        )

    # Se usuário mudou o checkbox dentro da aba, sincroniza e recarrega
    if tab_opt_stop != st.session_state.opt_stopwords or tab_opt_stem != st.session_state.opt_stemming:
        st.session_state.opt_stopwords = tab_opt_stop
        st.session_state.opt_stemming = tab_opt_stem
        st.rerun()

    # Métricas dinâmicas do vocabulário
    total_tokens_corpus = sum(len(tokens) for tokens in doc_tokens.values())
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val">{len(st.session_state.documents)}</div>
            <div class="metric-label">Documentos na Base</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val">{len(vocab)}</div>
            <div class="metric-label">Tamanho do Vocabulário</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val">{total_tokens_corpus}</div>
            <div class="metric-label">Total de Tokens no Corpus</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        status_prep = f"{'✅' if st.session_state.opt_stopwords else '❌'} Stop | {'✅' if st.session_state.opt_stemming else '❌'} Stem"
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val" style="font-size: 1.1rem; padding-top: 8px;">{status_prep}</div>
            <div class="metric-label">Filtros Ativos</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🔬 Inspeção Passo a Passo das 4 Etapas do Pipeline")
    selected_doc_id = st.selectbox(
        "Selecione um manual para analisar a transformação etapa a etapa:",
        options=sorted(st.session_state.documents.keys()),
        format_func=lambda x: f"Doc {x}: {st.session_state.documents[x][:65]}..."
    )
    
    audit_selected = audits[selected_doc_id]
    
    col_step1, col_step2 = st.columns(2)
    with col_step1:
        st.markdown("**1. Texto Original Bruto:**")
        st.info(audit_selected["original"])
        
        st.markdown("**2. Normalização (minúsculas + acentos removidos):**")
        st.code(audit_selected["normalized"], language="text")
        
    with col_step2:
        st.markdown(f"**3. Stopwords Filtradas ({len(audit_selected['stopwords_removed'])} termos descartados):**")
        if audit_selected["stopwords_removed"]:
            st.warning(", ".join(audit_selected["stopwords_removed"]))
        else:
            st.success("Nenhuma stopword descartada (filtro desativado ou ausente).")
            
        st.markdown(f"**4. Tokens Finais ({len(audit_selected['final_tokens'])} tokens indexados):**")
        st.markdown("".join([f"<span class='token-pill'>{t}</span>" for t in audit_selected["final_tokens"]]), unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📋 Visão Consolidada dos Manuais e Tokens")
    summary_prep = []
    for doc_id, text in sorted(st.session_state.documents.items()):
        summary_prep.append({
            "Doc ID": f"Doc {doc_id}",
            "Texto Original": text,
            "Tokens Pré-processados": ", ".join(doc_tokens[doc_id]),
            "Qtd Tokens": len(doc_tokens[doc_id])
        })
    st.dataframe(pd.DataFrame(summary_prep), use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# ABA 2: FASE 2 - O ÍNDICE INVERTIDO
# -----------------------------------------------------------------------------
with tab2_indice:
    st.markdown('<span class="phase-badge">FASE 2 DA ESPECIFICAÇÃO</span>', unsafe_allow_html=True)
    st.markdown("### 🗂️ O Índice Invertido em Memória")
    st.caption("Construção do mapeamento: Termo -> [IDs de Docs] utilizando os tokens pré-processados. Exibição via st.dataframe e st.json conforme exigência do enunciado.")
    
    filtro_termo = st.text_input("Filtrar termo no índice:", placeholder="Ex: soja, irrig, lagart, milh...", key="filtro_idx_tab2")
    
    index_table = []
    for term in vocab:
        if not filtro_termo or filtro_termo.lower() in term:
            posting = inv_index[term]
            postings_str = f"[{', '.join([f'Doc {d}' for d in posting])}]"
            freq_str = ", ".join([f"Doc {d}: {term_freqs[term][d]}x" for d in posting])
            
            index_table.append({
                "Termo (Token)": term,
                "DF (Frequência Documental)": len(posting),
                "Documentos Onde Ocorre (Posting List)": postings_str,
                "Frequência por Documento": freq_str
            })

    col_view1, col_view2 = st.columns([3, 2])
    with col_view1:
        st.markdown("#### 📑 Exibição via `st.dataframe`")
        st.dataframe(pd.DataFrame(index_table), use_container_width=True, hide_index=True)
        
    with col_view2:
        st.markdown("#### 📦 Exibição via `st.json`")
        json_display = {
            term: {
                "documentos": [f"Doc {d}" for d in inv_index[term]],
                "df": len(inv_index[term]),
                "frequencias": {f"Doc {d}": term_freqs[term][d] for d in inv_index[term]}
            }
            for term in (vocab if not filtro_termo else [t for t in vocab if filtro_termo.lower() in t])
        }
        st.json(json_display, expanded=True)


# -----------------------------------------------------------------------------
# ABA 3: FASE 3 - BUSCA E RANQUEAMENTO TF-IDF & BÔNUS
# -----------------------------------------------------------------------------
with tab3_busca:
    st.markdown('<span class="phase-badge">FASE 3 DA ESPECIFICAÇÃO & DESAFIO BÔNUS</span>', unsafe_allow_html=True)
    st.markdown("### 🔍 Busca e Ranqueamento TF-IDF")
    st.caption("Digite uma consulta técnica. O sistema calcula TF, IDF e TF-IDF acumulado e Similaridade de Cosseno, destacando o documento vencedor.")
    
    col_ex1, col_ex2, col_ex3, col_ex4 = st.columns(4)
    if "query_input" not in st.session_state:
        st.session_state.query_input = "irrigação na soja"
        
    if col_ex1.button("🌱 'irrigação na soja'"):
        st.session_state.query_input = "irrigação na soja"
    if col_ex2.button("🐛 'controle biológico lagartas'"):
        st.session_state.query_input = "controle biológico lagartas"
    if col_ex3.button("🌽 'adubação nitrogênio milho'"):
        st.session_state.query_input = "adubação verde nitrogênio milho"
    if col_ex4.button("💧 'irrigação gotejamento água'"):
        st.session_state.query_input = "irrigação gotejamento água orgânico"

    query_text = st.text_input(
        "Digite a sua pesquisa técnica nos manuais:",
        value=st.session_state.query_input,
        placeholder="Ex: irrigação na cultura da soja",
        key="main_search_box"
    )

    if query_text.strip():
        results, q_tokens, q_audit, q_tfidf, audit_rows = search_and_rank(
            query=query_text,
            documents=st.session_state.documents,
            inverted_index=inv_index,
            df_dict=df_dict,
            idf_dict=idf_dict,
            tfidf_matrix=tfidf_matrix,
            remove_stopwords=st.session_state.opt_stopwords,
            apply_stemming=st.session_state.opt_stemming
        )

        st.markdown("**Tokens gerados para a consulta:** " + "".join([f"<span class='token-pill'>{t}</span>" for t in q_tokens]), unsafe_allow_html=True)
        if q_audit["stopwords_removed"]:
            st.caption(f"ℹ️ Stopwords filtradas da consulta: {', '.join(q_audit['stopwords_removed'])}")

        sort_key = "cosine_similarity" if "Cosseno" in ranking_mode else "accumulated_tfidf"
        sorted_results = sorted(results, key=lambda x: x[sort_key], reverse=True)
        
        winner = sorted_results[0] if sorted_results and sorted_results[0][sort_key] > 0 else None

        if winner:
            score_win = winner[sort_key]
            highlighted_snippet = highlight_matched_text(
                winner["text"],
                winner["matched_terms"],
                remove_stopwords=st.session_state.opt_stopwords,
                apply_stemming=st.session_state.opt_stemming
            )
            
            st.markdown(f"""
            <div class="winner-card">
                <span class="winner-badge">🏆 DOCUMENTO VENCEDOR (#1 NO RANKING)</span>
                <div class="winner-doc-id">Documento {winner['doc_id']} &bull; Score: {score_win:.4f} ({'Cosseno (Bônus)' if 'Cosseno' in ranking_mode else 'TF-IDF Acumulado'})</div>
                <div class="winner-text">
                    {highlighted_snippet}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Nenhum documento da base contém os termos pesquisados com as configurações atuais.")

        st.markdown("#### 📊 Tabela Ordenada de Ranqueamento")
        st.caption("Ordenada do maior para o menor score acumulado, destacando o documento vencedor.")
        
        table_data = []
        for rank, r in enumerate(sorted_results, 1):
            is_win = "🏆 " if rank == 1 and r[sort_key] > 0 else ""
            table_data.append({
                "Posição": f"{is_win}#{rank}",
                "Doc ID": f"Doc {r['doc_id']}",
                "Texto do Manual": r["text"],
                "TF-IDF Acumulado": f"{r['accumulated_tfidf']:.4f}",
                "Similaridade Cosseno (Bônus)": f"{r['cosine_similarity']:.4f}",
                "Termos Coincidentes": ", ".join(r["matched_terms"]) if r["matched_terms"] else "Nenhum"
            })
            
        df_ranking = pd.DataFrame(table_data)
        st.dataframe(df_ranking, use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# ABA 4: AUDITORIA MATEMÁTICA & DESAFIO BÔNUS
# -----------------------------------------------------------------------------
with tab4_auditoria:
    st.markdown('<span class="phase-badge">AUDITORIA PEDAGÓGICA</span>', unsafe_allow_html=True)
    st.markdown("### 📐 Auditoria e Validação Matemática das Fórmulas")
    st.caption("Transparência acadêmica total para conferência dos cálculos de TF, IDF, TF-IDF e Similaridade de Cosseno implementados do zero.")
    
    with st.expander("📚 Formulação Matemática Teórica Aplicada", expanded=True):
        st.markdown(r"""
        - **Term Frequency (TF relativo):**
          $$TF(t, d) = \frac{\text{contagem}(t, d)}{\sum_{t' \in d} \text{contagem}(t', d)}$$
          *Normaliza a frequência do termo pelo tamanho do documento.*

        - **Inverse Document Frequency (IDF suavizado):**
          $$IDF(t) = \log_{10}\left(\frac{N}{DF(t)}\right) + 1.0$$
          *Onde $N$ é o total de documentos na base e $DF(t)$ é a quantidade de documentos contendo o termo $t$.*

        - **Peso TF-IDF do Documento:**
          $$TF\text{-}IDF(t, d) = TF(t, d) \times IDF(t)$$

        - **Ranqueamento por TF-IDF Acumulado:**
          $$\text{Score}_{\text{soma}}(q, d) = \sum_{t \in q \cap d} TF\text{-}IDF(t, d)$$

        - **Desafio Bônus &mdash; Similaridade de Cosseno:**
          $$\text{CosineSim}(\vec{q}, \vec{d}) = \frac{\vec{q} \cdot \vec{d}}{\|\vec{q}\| \times \|\vec{d}\|} = \frac{\sum_{t} w_{t, q} \cdot w_{t, d}}{\sqrt{\sum_{t} w_{t, q}^2} \times \sqrt{\sum_{t} w_{t, d}^2}}$$
        """)

    if query_text.strip() and audit_rows:
        st.markdown("#### 🔬 Decomposição dos Cálculos para a Consulta Atual")
        st.caption(f"Consulta: **'{query_text}'** &bull; Tokens analisados: {', '.join(q_tokens)}")
        st.dataframe(pd.DataFrame(audit_rows), use_container_width=True, hide_index=True)
    else:
        st.info("Digite uma consulta na Aba 3 para inspecionar os cálculos decompostos.")

    st.markdown("---")
    st.markdown("#### 📊 Matriz Completa TF-IDF (Documentos × Vocabulário)")
    matrix_data = []
    for doc_id in sorted(st.session_state.documents.keys()):
        row = {"Doc ID": f"Doc {doc_id}"}
        for term in vocab:
            row[term] = round(tfidf_matrix[doc_id].get(term, 0.0), 4)
        matrix_data.append(row)
    st.dataframe(pd.DataFrame(matrix_data), use_container_width=True, hide_index=True)


# =============================================================================
# 10. RODAPÉ ACADÊMICO
# =============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 12px 0;">
    <strong>AgroSearch &bull; Laboratório Prático 04 &bull; UNIPÊ</strong><br>
    Desenvolvido para a disciplina de Tópicos Avançados (Recuperação de Informação / PLN) &bull; Prof. Me. Ricardo Roberto de Lima
</div>
""", unsafe_allow_html=True)
