# Plano de Expansão de Composições (v1)

## Objetivo
Expandir e validar a base de composições para que ela dite corretamente as necessidades das bases de materiais, mão de obra, ferramentas e equipamentos.

## Critério de Prioridade
- **Alta:** alta recorrência comercial e alto impacto em precificação
- **Média:** serviços recorrentes, mas com menor volume
- **Baixa:** casos específicos/esporádicos

---

## Prioridade Alta (Sprint 1)

### 1) Instalações Hi-Wall faltantes
- Instalação Split Hi-Wall 9.000 BTUs (já padronizada)
- **Adicionar:** Instalação Split Hi-Wall 36.000 BTUs
- **Adicionar:** Instalação Split Hi-Wall 48.000 BTUs
- **Adicionar:** Instalação Split Hi-Wall 60.000 BTUs

### 2) Elétrica por capacidade (substituir genérico com o tempo)
- **Adicionar:** Alimentação elétrica 220V 9–12K
- **Adicionar:** Alimentação elétrica 220V 18–24K
- **Adicionar:** Alimentação elétrica 220V 30–36K
- **Adicionar:** Alimentação elétrica 220V 48–60K
- **Manter atual:** Alimentação elétrica 220V monofásica (legado)

### 3) Dreno por cenário real
- **Adicionar:** Dreno com bomba (linha dedicada)
- **Adicionar:** Dreno com elevação > 2m
- **Adicionar:** Dreno para múltiplas evaporadoras

### 4) Serviços críticos de instalação
- **Adicionar:** Start-up e comissionamento
- **Adicionar:** Vácuo profundo + teste de estanqueidade estendido
- **Adicionar:** Adequação elétrica de quadro (QDC) com proteção completa

---

## Prioridade Média (Sprint 2)

### 5) Manutenção corretiva estruturada
- **Adicionar:** Correção de vazamento em linha frigorígena
- **Adicionar:** Reparo de linha com troca de trecho
- **Adicionar:** Limpeza química de serpentina (evaporadora)
- **Adicionar:** Limpeza química de serpentina (condensadora)

### 6) Peças com variação por faixa
- **Adicionar:** Troca de placa por faixa (9–18K / 24–36K / 48–60K)
- **Adicionar:** Troca de motor por faixa (P/M/G)
- **Adicionar:** Troca de sensor por tipo (ambiente/evap/cond/pres)

### 7) Serviços de visita
- **Adicionar:** Visita técnica sem execução
- **Adicionar:** Visita técnica com laudo
- **Adicionar:** Visita técnica com deslocamento estendido

---

## Prioridade Baixa (Sprint 3)

### 8) Casos especiais
- **Adicionar:** Instalação em fachada com rapel/plataforma
- **Adicionar:** Instalação em ambiente crítico (CPD/laboratório)
- **Adicionar:** Reinstalação com mudança de posição (obra civil leve)

### 9) Linhas avançadas
- **Adicionar:** Built-in acima de 36K
- **Adicionar:** Cassete com múltiplas insuflações especiais

---

## Regras de Validação (gate obrigatório)

### A) Integridade de referências
- Todo `codigo` de item da composição deve existir na base correspondente (MAT/MO/FER/EQP)
- Não permitir código órfão

### B) Coerência de unidade
- Item variável deve ter unidade compatível com cenário (`metro`, `kg`, `h`, `un`)
- Não misturar unidade fixa/variável sem justificativa

### C) Faixa técnica
- Quantidades por metro e base devem ter faixa mínima/máxima plausível
- Alertar outliers (ex.: consumo exagerado de solda/fita)

### D) Cobertura comercial
- Toda composição “vendável” precisa ter variante de elétrica + dreno + acabamento ou regra explícita de exclusão

---

## Entregáveis sugeridos por sprint

### Sprint 1 (imediato)
1. Lista final das novas composições de alta prioridade
2. Inclusão das composições no `dados/composicoes.py`
3. Script de validação automática de integridade (composição x bases)
4. Relatório de inconsistências

### Sprint 2
1. Expansão de corretivas e peças por faixa
2. Ajuste fino de coeficientes
3. Testes automatizados adicionais

### Sprint 3
1. Casos especiais
2. Revisão de nomenclatura final
3. Congelamento de versão de catálogo (baseline)

---

## Próxima ação recomendada
Começar agora pela **Sprint 1 / item 1 e 2** (Hi-Wall faltantes + elétrica por capacidade), porque isso destrava rápido validação e uso comercial.
