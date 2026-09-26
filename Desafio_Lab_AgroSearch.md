**INSTITUIÇÃO: UNIPÊ** DISCIPLINA: TÔPICOS AVANÇADOS - Recuperação de Informação / PLN  
ATIVIDADE: Laboratório Prático 04 - Desafio Integrador  
PROFESSOR: Me. Ricardo Roberto de Lima *PÚBLICO-ALVO: Grupos de 2 a 3 alunos – valor: 0.5 pontos extras na AV1.*

## 🎯 Título do Desafio: AgroSearch - Motor de Busca Inteligente

### 1. Estudo de Caso (Contexto)

A startup AgroTech Solutions possui uma base interna com dezenas de manuais técnicos sobre agricultura sustentável, controle de pragas e irrigação. Atualmente, os técnicos de campo perdem muito tempo procurando informações específicas. A diretoria contratou sua equipe para desenvolver o AgroSearch, um prototype de motor de busca textual. O sistema deve permitir que o técnico digite uma consulta e o sistema retorne os trechos mais relevantes, ranqueados por relevância.

### 2. Objetivos de Aprendizagem

- Consolidar o pipeline de pré-processamento de texto (Tokenização, Normalização, Stopwords, Stemming).
- Compreender a construção e a utilidade do Índice Invertido em memória.
- Aplicar a métrica TF-IDF para ranqueamento de documentos.
- Desenvolver uma interface interativa e unificada utilizando Streamlit.

### 3. Regras e Entregáveis

- Equipes: Grupos de 2 ou 3 alunos.
- Entrega: Um único arquivo .py (Streamlit) e um breve relatório em PDF (máx. 2 páginas).
- Restrição Técnica: **É PROIBIDO o uso de bibliotecas de alto nível (ex: scikit-learn, TfidfVectorizer). O índice invertido e o cálculo do TF-IDF devem ser implementados 'do zero' (from scratch).**

### 4. Especificações Técnicas

A aplicação Streamlit deve integrar os 3 pilares:

#### Fase 1: O Pipeline de Pré-processamento

Implementar as 4 etapas. A UI deve permitir ligar/desligar Stemming e Stopwords via checkboxes para ver o vocabulário mudar dinamicamente.

#### Fase 2: O Índice Invertido

Construir o Índice Invertido (Termo -&gt; [IDs de Docs]) usando os tokens pré-processados. Exibir via st.json ou st.dataframe.

#### Fase 3: Busca e Ranqueamento TF-IDF

O usuário digita uma Query. O sistema calcula TF, IDF e TF-IDF. Exibir uma tabela ordenada do maior para o menor TF-IDF acumulado, destacando o documento vencedor.

### 5. Base de Documentos (Hardcode sugerido)

1. Doc 1: A soja requer irrigação constante durante o período de floração para garantir a produtividade.
2. Doc 2: O controle biológico de lagartas na soja pode ser feito com a vespa Trichogramma.
3. Doc 3: A adubação verde com leguminosas melhora o nitrogênio no solo para o milho.
4. Doc 4: Lagartas desfolhadoras causam grande prejuízo na cultura da soja e do algodão.
5. Doc 5: A irrigação por gotejamento economiza água e é ideal para o cultivo orgânico.

### 6. Critérios de Avaliação

| Critério              | Peso   | Descrição                                                                   |
|-----------------------|--------|-----------------------------------------------------------------------------|
| Correção do Pipeline  | 20%    | Pré-processamento remove acentos, lowercases e aplica stemming/stopwords.   |
| Índice Invertido      | 20%    | Estrutura reflete corretamente a relação Termo-Documento com tokens limpos. |
| Cálculo TF-IDF        | 30%    | Fórmulas de TF, IDF e ranqueamento final estão matematicamente corretos.    |
| Interface (Streamlit) | 20%    | UI intuitiva, permite interação e exibe dados de forma clara.               |
| Trabalho em Equipe    | 10%    | Divisão clara de tarefas no relatório e qualidade do código.                |

### 7. Desafio Bônus (Nota Extra)

Implementar a Similaridade de Cosseno entre o vetor da Query e o vetor TF-IDF dos documentos para lidar melhor com consultas de múltiplas palavras.