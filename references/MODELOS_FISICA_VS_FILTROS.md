# Modelos Baseados em Física vs Modelos de Filtros

## Sua Observação Está Correta! ✓

O modelo atual (baseado em filtros) **NÃO representa a física fundamental** da cóclea. Ele é uma **aproximação fenomenológica**.

---

## Comparação: Filtros vs Física

### Modelo de Filtros (Atual)

**Como funciona:**
```python
# Para cada seção da membrana:
for seção in membrana_basilar:
    # Aplica filtro passa-banda
    saída = filtro_butterworth(entrada, CF_seção, BW_seção)
```

**Características:**
- ❌ Não resolve equações diferenciais da física
- ❌ Não modela acoplamento entre seções
- ❌ Não representa propagação de onda real
- ❌ Precisa de "truques" (verificação de relevância, Q ajustado, etc.)
- ✓ Computacionalmente eficiente (milissegundos)
- ✓ Fácil de implementar e entender
- ✓ Aproxima bem o resultado final

**Equações: NENHUMA** (apenas processamento de sinal digital)

---

### Modelos Baseados em Física

## 1. Modelo de Linha de Transmissão (Transmission Line)

**Equações Fundamentais:**

Sistema acoplado de 2 EDPs (equações diferenciais parciais):

```
∂²p(x,t)/∂x² = ρ/h × ∂²p(x,t)/∂t² + Z(x) × ∂v(x,t)/∂t

∂v(x,t)/∂x = -p(x,t)/Z_BM(x)
```

Onde:
- `p(x,t)` = pressão diferencial através da membrana
- `v(x,t)` = velocidade da membrana basilar
- `Z_BM(x)` = impedância mecânica da membrana (varia com x)
- `ρ` = densidade do fluido
- `h` = altura dos compartimentos

**Impedância da Membrana:**

```
Z_BM(x) = R(x) + jωM(x) + K(x)/(jω)
```

Onde:
- `R(x)` = amortecimento (resistência)
- `M(x)` = massa por unidade de área
- `K(x)` = rigidez (stiffness)

**Como funciona:**
1. Divide a membrana em N elementos discretos
2. Resolve o sistema acoplado fluido-estrutura
3. A onda viajante **emerge naturalmente** da solução!

**Referências Clássicas:**
- **Zwislocki, J. J. (1950)** - Primeira formulação
- **Zweig, G., Lipes, R., & Pierce, J. R. (1976)** - Desenvolvimento moderno
- **Neely, S. T., & Kim, D. O. (1986)** - Com elementos ativos

---

## 2. Modelo 2D/3D de Elementos Finitos (FEM)

**Equações:**

**Navier-Stokes (fluido):**
```
ρ_fluido × (∂v/∂t + v·∇v) = -∇p + μ∇²v
∇·v = 0  (incompressível)
```

**Elasticidade (membrana):**
```
ρ_membrana × ∂²u/∂t² = ∇·σ + f
```

**Acoplamento fluido-estrutura** nas interfaces

**Como funciona:**
1. Discretiza geometria 3D completa (fluido + membrana)
2. Resolve acoplamento fluido-estrutura
3. Extremamente preciso anatomicamente

**Referências:**
- **Böhnke & Arnold (1999)** - FEM 3D da cóclea humana
- **Liu & Neely (2010)** - Modelo eletromecânico
- **Brown, Bradshaw, & Gan (2022)** - Cóclea espiral 3D

**Desvantagens:**
- ⚠️ MUITO lento (horas para segundos de simulação)
- ⚠️ Requer software especializado (ANSYS, COMSOL)
- ⚠️ Complexo de implementar

---

## 3. Modelo WKB (Wentzel-Kramers-Brillouin)

**Abordagem:**
- Método assintótico para ondas em meios não-uniformes
- Assume variação lenta das propriedades

**Equação:**
```
d²ξ/dx² + k²(x)ξ = 0
```

Onde `k(x)` é o número de onda local que varia com posição

**Referências:**
- **Steele & Lim (1999)**
- **Lim & Steele (2002)**

---

## Qual Modelo Resolve os Problemas Intrinsecamente?

### ✓ Linha de Transmissão (Recomendado para Implementação)

**Vantagens:**
1. **Resolve física real** - equações de movimento + acoplamento fluido
2. **Onda viajante emerge naturalmente** - não precisa de filtros
3. **Sem amplitude espúria no ápice** - a onda para fisicamente onde deve
4. **Largura espacial correta** - determinada pela física, não por Q ajustado
5. **Computacionalmente viável** - minutos para simulação completa

**O que resolve automaticamente:**
- ✓ Propagação de onda realista
- ✓ Atenuação espacial correta
- ✓ Largura de envelope dependente da frequência
- ✓ Sem ativação de regiões irrelevantes

---

## Implementação Básica de Linha de Transmissão

**Estrutura:**

```python
class TransmissionLineModel:
    def setup_physics(self):
        # Parâmetros que variam com posição
        self.K = stiffness(x)      # Rigidez
        self.M = mass(x)            # Massa  
        self.R = damping(x)         # Amortecimento
        self.rho = fluid_density
        self.h = chamber_height
        
    def time_step(self, dt):
        # Resolve sistema acoplado usando diferenças finitas
        
        # 1. Atualiza pressão do fluido
        for i in range(N):
            p_new[i] = (sistema de equações acopladas)
            
        # 2. Atualiza velocidade da membrana
        for i in range(N):
            v_new[i] = -p[i] / Z_BM[i]
            
        # 3. Atualiza deslocamento
        for i in range(N):
            displacement[i] += v[i] * dt
```

---

## Comparação de Custo Computacional

| Modelo | Tempo (0.1s de áudio) | Precisão | Física |
|--------|----------------------|----------|--------|
| **Filtros** (atual) | ~10 ms | Boa | ❌ |
| **Linha Transmissão** | ~1-10 s | Muito Boa | ✓ |
| **FEM 2D** | ~10-60 min | Excelente | ✓ |
| **FEM 3D** | ~horas | Máxima | ✓ |

---

## Referências Principais

### Linha de Transmissão:

**Zweig, G., Lipes, R., & Pierce, J. R. (1976)**
"The cochlear compromise"
*Journal of the Acoustical Society of America*, 59(4), 975-982.

**Neely, S. T., & Kim, D. O. (1986)**
"A model for active elements in cochlear biomechanics"
*Journal of the Acoustical Society of America*, 79(5), 1472-1480.

**Shera, C. A., & Zweig, G. (1991)**
"Reflection of retrograde waves within the cochlea and at the stapes"
*Journal of the Acoustical Society of America*, 89(3), 1290-1305.

### Elementos Finitos:

**Böhnke, F., & Arnold, W. (1999)**
"3D-Finite element model of the human cochlea including fluid-structure couplings"
*ORL*, 61(5), 305-310.

**Liu, Y., & Neely, S. T. (2010)**
"Distortion product emissions from a cochlear model with nonlinear mechanoelectrical transduction in outer hair cells"
*Journal of the Acoustical Society of America*, 127(4), 2420-2432.

### Métodos Numéricos:

**Elliott, S. J., Ku, E. M., & Lineton, B. (2007)**
"A state space model for cochlear mechanics"
*Journal of the Acoustical Society of America*, 122(5), 2759-2771.

**Meaud, J., & Grosh, K. (2014)**
"The effect of tectorial membrane and basilar membrane longitudinal coupling in cochlear mechanics"
*Journal of the Acoustical Society of America*, 127(3), 1411-1421.

---

## Conclusão

Sim, você está **absolutamente correto**:

1. ✓ O modelo de filtros **não resolve a física**
2. ✓ Modelos baseados em equações físicas existem
3. ✓ Eles **resolveriam intrinsecamente** os problemas identificados
4. ✓ O mais prático é o **modelo de linha de transmissão**

O modelo de **linha de transmissão** é o melhor compromisso entre:
- Fidelidade física
- Viabilidade computacional  
- Facilidade de implementação

Ele resolve as **equações de onda acopladas** e a onda viajante emerge naturalmente, sem necessidade de "truques" artificiais.

---

**Próximos Passos:**

Se você quiser implementar um modelo físico, recomendo começar com uma **versão simplificada de linha de transmissão** usando:
- Diferenças finitas no espaço
- Método de Euler ou Runge-Kutta no tempo
- ~100 seções ao longo da membrana
- Resolução das equações acopladas p(x,t) e v(x,t)

Posso ajudá-lo a implementar isso se tiver interesse!
