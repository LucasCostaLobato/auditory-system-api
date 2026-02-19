# Referências Bibliográficas do Modelo de Vibração da Membrana Basilar

## Referências Principais Utilizadas

### 1. Mapa Tonotópico (Implementação Direta)

**Greenwood, D. D. (1990)**
"A cochlear frequency-position function for several species - 29 years later"
*The Journal of the Acoustical Society of America*, 87(6), 2592-2605.
DOI: 10.1121/1.399052

**Uso no modelo**: A fórmula de Greenwood foi implementada exatamente como publicada:
```
CF(x) = A * (10^(a*(1-x/L)) - k)
```
Onde para humanos: A = 165.4 Hz, a = 2.1, k = 0.88

### 2. Modelo de Osciladores (Base Conceitual)

**Lesser, M. B., & Berkley, D. A. (1972)**
"Fluid mechanics of the cochlea. Part 1"
*Journal of Fluid Mechanics*, 51(3), 497-512.
DOI: 10.1017/S0022112072002320

**Uso no modelo**: Conceito de modelar cada seção da membrana basilar como um oscilador massa-mola-amortecedor com parâmetros variáveis:
- m(x) = massa por unidade de área
- k(x) = rigidez
- c(x) = amortecimento

Equação fundamental:
```
m(x) * d²η/dt² + c(x) * dη/dt + k(x) * η = F(t)
```

### 3. Fundamentos da Onda Viajante (Conceitual)

**von Békésy, G. (1960)**
*Experiments in Hearing*
McGraw-Hill, New York.

**Uso no modelo**: 
- Princípio da onda viajante
- Padrão de excitação com pico localizado
- Conceito de análise de frequência espacial

### 4. Parâmetros Mecânicos (Referência Indireta)

**Neely, S. T. (1981)**
"Finite difference solution of a two-dimensional mathematical model of the cochlea"
*The Journal of the Acoustical Society of America*, 69(5), 1386-1393.

**Uso no modelo**: Valores típicos de parâmetros mecânicos foram baseados em trabalhos de modelagem numérica similar.

---

## Outras Referências de Suporte

### Modelos Computacionais de Cóclea

**Allen, J. B. (1977)**
"Two-dimensional cochlear fluid model: New results"
*The Journal of the Acoustical Society of America*, 61(1), 110-119.

**Sondhi, M. M. (1978)**
"Method for computing motion in a two-dimensional cochlear model"
*The Journal of the Acoustical Society of America*, 63(5), 1468-1477.

### Dados Fisiológicos

**Rhode, W. S. (1971)**
"Observations of the vibration of the basilar membrane in squirrel monkeys using the Mössbauer technique"
*The Journal of the Acoustical Society of America*, 49(4B), 1218-1231.

Fornece dados experimentais de deslocamentos da membrana basilar (escala de nanômetros).

**Ruggero, M. A., Rich, N. C., Recio, A., Narayan, S. S., & Robles, L. (1997)**
"Basilar-membrane responses to tones at the base of the chinchilla cochlea"
*The Journal of the Acoustical Society of America*, 101(4), 2151-2163.

Dados sobre não-linearidades e ganho coclear.

---

## Simplificações e Adaptações

### O que o modelo implementa DIRETAMENTE:

1. **Mapa de Greenwood (1990)**: Implementação exata da fórmula
2. **Conceito de osciladores de Lesser & Berkley (1972)**: Estrutura conceitual
3. **Filtros passa-banda**: Implementação prática usando filtros digitais (scipy.signal)

### O que foi SIMPLIFICADO:

1. **Acoplamento fluido**: O modelo original de Lesser & Berkley usa acoplamento completo via mecânica de fluidos. Nosso modelo simplifica usando filtros passa-banda independentes.

2. **Não-linearidades**: Modelos modernos incluem amplificação coclear ativa (células ciliadas externas). Nosso modelo é LINEAR e PASSIVO.

3. **Geometria**: O modelo original é 2D/3D. Nosso modelo é essencialmente 1D (variação apenas ao longo do comprimento).

---

## Nota Importante sobre a Implementação

Este modelo é uma **versão didática simplificada** que:

- ✅ Reproduz o comportamento qualitativo correto da membrana basilar
- ✅ Usa parâmetros fisiologicamente plausíveis
- ✅ Gera deslocamentos na escala correta (nanômetros)
- ✅ Demonstra a onda viajante e análise de frequência

Porém:

- ❌ NÃO é um modelo biofísico completo
- ❌ NÃO inclui amplificação coclear ativa
- ❌ NÃO modela células ciliadas ou transdução
- ❌ NÃO resolve as equações completas de mecânica de fluidos

Para modelos mais completos e validados experimentalmente, consulte:
- **Biblioteca cochlea** (Zilany et al., 2014; Holmberg, 2007)
- **CoNNear** (Verhulst et al., 2021)
- **Modelos de elementos finitos** (vários autores)

---

## Referências Adicionais Consultadas

**Viergever, M. A. (1980)**
*Mechanics of the Inner Ear*
Delft University Press.

**Steele, C. R., & Lim, K. M. (1999)**
"Cochlear model with three-dimensional fluid, inner sulcus and feed-forward mechanism"
*Auditory and Vestibular Research*, 8, 152-165.

**Rudnicki, M., Schoppe, O., Isik, M., Völk, F., & Hemmert, W. (2015)**
"Modeling auditory coding: from sound to spikes"
*Cell and Tissue Research*, 361(1), 159-175.

**Baby, D., Van Den Broucke, A., & Verhulst, S. (2021)**
"A convolutional neural-network model of human cochlear mechanics and filter tuning for real-time applications"
*Nature Machine Intelligence*, 3(2), 134-143.

---

## Citação Sugerida para Este Modelo

Se você usar este modelo em trabalhos acadêmicos, sugerimos citar as referências principais:

```
Este modelo simplificado da membrana basilar foi desenvolvido com base no 
mapa tonotópico de Greenwood (1990) e na abordagem de osciladores proposta 
por Lesser & Berkley (1972), implementado em Python usando filtros digitais 
para eficiência computacional.
```

---

**Última atualização**: Janeiro 2026
