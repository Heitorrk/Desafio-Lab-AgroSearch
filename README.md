<div align="center">

# 🌱 AgroSearch — Motor de Busca Inteligente

**Recuperação de Informação Textual e Mineração de Manuais Agrícolas (PLN)**  
*Laboratório Prático 04 — Desafio Integrador (AV1)*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/Status-100%25%20Concluído-success.svg)](#)
[![Restrição](https://img.shields.io/badge/Algoritmos-100%25%20From%20Scratch-darkgreen.svg)](#)
[![Bônus](https://img.shields.io/badge/Desafio%20Bônus-Similaridade%20de%20Cosseno-gold.svg)](#)

</div>

---

## 🏛️ Contexto Acadêmico

- **Instituição:** Centro Universitário de João Pessoa — **UNIPÊ**
- **Curso:** Ciência da Computação / Engenharia de Software
- **Disciplina:** Tópicos Avançados — Recuperação de Informação e PLN
- **Docente:** Prof. Me. Ricardo Roberto de Lima
- **Atividade:** Laboratório Prático 04 — Desafio Integrador (AV1)

### 👥 Equipe de Desenvolvimento
- **Mateus Ieno Ramalho**
- **Heitor de Oliveira Mamede**
- **Júlio César Carvalho Santos**

---

## 🎯 1. Estudo de Caso (Contexto)

A startup **AgroTech Solutions** possui uma base interna de manuais técnicos sobre agricultura sustentável, manejo integrado de pragas e sistemas de irrigação. No dia a dia de campo, os técnicos perdem tempo precioso procurando informações pontuais em documentos extensos.

O **AgroSearch** foi concebido como um motor de busca textual inteligente desenvolvido em **arquivo único Streamlit (`app.py`)**, permitindo que o técnico insira consultas em linguagem natural e receba os trechos mais relevantes ranqueados instantaneamente.

> [!IMPORTANT]
> **RESTRIÇÃO TÉCNICA RIGOROSA:** É proibido o uso de bibliotecas de alto nível (ex: `scikit-learn`, `TfidfVectorizer`). O pipeline textual, o índice invertido em memória, o cálculo das métricas TF-IDF e o modelo vetorial foram implementados estritamente **do zero (*from scratch*)** utilizando apenas estruturas nativas do Python e o módulo matemático `math`.

---

## ⚙️ 2. Arquitetura em Fases

A aplicação organiza o fluxo em abas sequenciais que espelham exatamente os pilares técnicos exigidos na especificação:

```mermaid
flowchart LR
    A[Texto Bruto dos Manuais] --> B[Fase 1: Pipeline de PLN]
    B --> C[Fase 2: Índice Invertido em Memória]
    C --> D[Fase 3: Motor TF-IDF & Cosseno]
    D --> E[Interface Streamlit & Ranqueamento]
```

### 🔹 Fase 1: O Pipeline de Pré-processamento
Implementado em 4 etapas canônicas:
1. **Normalização:** Conversão para minúsculas (`lower()`) e remoção de acentos via decomposição canônica (`NFKD` do módulo nativo `unicodedata`).
2. **Tokenização:** Segmentação léxica com expressões regulares (`re.findall(r'[a-zA-Z0-9]+', text)`), isolando palavras alfanuméricas e removendo pontuações.
3. **Filtro de Stopwords:** Remoção de termos gramaticais sem carga discriminativa (artigos, preposições, conjunções, pronomes), empregando uma curadoria nativa com mais de 160 stopwords do português brasileiro.
4. **Stemming Morfológico (Radicalização):** Algoritmo próprio baseado em regras morfológicas de sufixos verbais, nominais e plurais, reduzindo palavras flexionadas (*"irrigação"*, *"irrigar"*) ao radical comum (*"irrig"*), preservando raiz mínima de 3 caracteres.
- **Dinamismo da UI:** Checkboxes interativas permitem ligar/desligar Stopwords e Stemming na hora, permitindo visualizar a mutação dinâmica do vocabulário (de **26 termos limpos** para **47 termos brutos**).

### 🔹 Fase 2: O Índice Invertido em Memória
- Constrói o mapeamento:
  $$\text{ÍndiceInvertido}[t] = [Doc_1, Doc_2, \dots, Doc_k] \quad \text{onde } t \in Doc_i$$
- Mapeia cada token limpo aos documentos onde ocorre, calculando a frequência local do termo ($f_{t, d}$) e a frequência documental ($DF$).
- Exibição dupla: **Tabela interativa (`st.dataframe`)** com busca filtrável por prefixo e **visualização hierárquica nativa em JSON (`st.json`)**.

### 🔹 Fase 3: Busca e Ranqueamento TF-IDF
- **TF Relativo (Term Frequency):**
  $$TF(t, d) = \frac{f(t, d)}{\sum_{t' \in d} f(t', d)}$$
  *Normaliza a frequência pelo tamanho do documento, eliminando o viés de textos longos.*
- **IDF Suavizado (Inverse Document Frequency):**
  $$IDF(t) = \log_{10}\left(\frac{N}{DF(t)}\right) + 1.0$$
  *Pondera a raridade do termo na coleção com garantia de valores estritamente positivos.*
- **Peso do Documento:** $TF\text{-}IDF(t, d) = TF(t, d) \times IDF(t)$
- **Ranqueamento por TF-IDF Acumulado:**
  $$\text{Score}_{\text{soma}}(q, d) = \sum_{t \in q \cap d} TF\text{-}IDF(t, d)$$
- **Destaque do Vencedor:** Exibe card estilizado com o **Documento Vencedor (#1)** e os termos pesquisados grifados em `<mark>`.

### ⭐ Desafio Bônus: Similaridade de Cosseno (Nota Extra)
Para lidar com consultas compostas de múltiplos termos com máxima precisão geométrica, foi implementado o Modelo Vetorial no qual o vetor da query $\vec{q}$ e os documentos $\vec{d}$ têm seus ângulos comparados:
$$\text{CosineSim}(\vec{q}, \vec{d}) = \frac{\vec{q} \cdot \vec{d}}{\|\vec{q}\| \times \|\vec{d}\|} = \frac{\sum_t w_{t, q} \cdot w_{t, d}}{\sqrt{\sum_t w_{t, q}^2} \times \sqrt{\sum_t w_{t, d}^2}}$$

---

## 🧪 3. Validação Experimental dos Casos de Teste

Testes executados sobre a base técnica oficial recomendada pelo professor:

| ID | Conteúdo do Manual Agrícola |
| :---: | :--- |
| **Doc 1** | *A soja requer irrigação constante durante o período de floração para garantir a produtividade.* |
| **Doc 2** | *O controle biológico de lagartas na soja pode ser feito com a vespa Trichogramma.* |
| **Doc 3** | *A adubação verde com leguminosas melhora o nitrogênio no solo para o milho.* |
| **Doc 4** | *Lagartas desfolhadoras causam grande prejuízo na cultura da soja e do algodão.* |
| **Doc 5** | *A irrigação por gotejamento economiza água e é ideal para o cultivo orgânico.* |

### Resultados Obtidos nas Consultas:
| Consulta | Tokens ($\vec{q}$) | Doc Vencedor | Score Cosseno | Score TF-IDF | Análise de Relevância |
| :--- | :--- | :---: | :---: | :---: | :--- |
| `"irrigação na soja"` | `[irrig, soja]` | **Doc 1** | **0.4074** | **0.3275** | Doc 1 contém ambos os conceitos simultaneamente. |
| `"controle biológico lagartas"` | `[control, biolog, lagart]` | **Doc 2** | **0.6019** | **0.5284** | Doc 2 contempla 100% dos 3 termos pesquisados. |
| `"adubação nitrogênio milho"` | `[adub, nitrogen, milh]` | **Doc 3** | **0.6547** | **0.5143** | Doc 3 recupera com precisão todos os termos agronômicos. |
| `"cultivo orgânico gotejamento"` | `[cultiv, organ, gotej]` | **Doc 5** | **0.6547** | **0.5298** | Doc 5 lidera para práticas sustentáveis de irrigação. |

---

## 💻 4. Como Executar o Projeto

### Pré-requisitos
- Python 3.10 ou superior
- Pip instalado

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/Heitorrk/agrosearch.git
cd agrosearch
```

2. **Instale as dependências mínimas:**
```bash
pip install streamlit pandas fpdf2
```

3. **Inicie o servidor do AgroSearch:**
```bash
streamlit run app.py
```
*(ou execute diretamente `python -m streamlit run app.py`)*

4. **Acesse no seu navegador:**
```
http://localhost:8501
```

---

## 📁 5. Estrutura do Repositório

```text
├── app.py                      # Aplicação Streamlit unificada (100% From Scratch)
├── relatorio.pdf               # Relatório Técnico oficial de 1 página (A4 Executivo)
├── relatorio.md                # Fonte do relatório técnico em Markdown
├── Desafio_Lab_AgroSearch.md   # Especificação oficial do Laboratório Prático 04
└── README.md                   # Documentação completa do projeto
```

---

## 📊 6. Matriz de Conformidade com a Avaliação

| Critério Avaliado | Peso | Status | Implementação |
| :--- | :---: | :---: | :--- |
| **Correção do Pipeline** | 20% | ✅ Cumprido | Normalização Unicode, tokenização regex, stopwords PT e Stemming morfológico próprio. |
| **Índice Invertido** | 20% | ✅ Cumprido | Mapeamento Termo $\rightarrow$ [Doc IDs] em memória com visualização em `st.dataframe` e `st.json`. |
| **Cálculo TF-IDF** | 30% | ✅ Cumprido | Fórmulas matematicamente exatas sem libs externas; tabela de ranqueamento e vencedor destacados. |
| **Interface (Streamlit)** | 20% | ✅ Cumprido | UI moderna, cards estilizados, navegação por abas sequenciais e auditoria matemática. |
| **Trabalho em Equipe** | 10% | ✅ Cumprido | Divisão clara no relatório e código modularizado de alta legibilidade. |
| **Desafio Bônus** | Nota Extra | ⭐ Cumprido | Modelo Vetorial completo com Similaridade de Cosseno para consultas compostas. |

---

<div align="center">
Desenvolvido com excelência técnica para a disciplina de <strong>Tópicos Avançados (Recuperação de Informação / PLN)</strong> &bull; <strong>UNIPÊ</strong>
</div>
