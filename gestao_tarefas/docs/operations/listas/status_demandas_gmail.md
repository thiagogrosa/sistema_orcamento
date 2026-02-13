# Status das Demandas - Pesquisa Gmail

> Atualizado em: 07/02/2026
> Total: 31 demandas | 2 completas | 27 precisam pesquisa

---

## Resumo

| Status | Qtd | Descrição |
|--------|-----|-----------|
| Dados suficientes | 2 | Não precisam pesquisa urgente |
| Parciais | 3 | Alguns dados encontrados, faltam campos |
| Dry-run (simulado) | 9 | Pesquisa nunca executada de fato |
| Sem resultado | 16 | Nenhuma busca realizada |
| **Precisam pesquisa** | **27** | **87% do total** |

---

## PRIORIDADE ALTA (10 demandas - TODAS precisam pesquisa)

| Asana ID | Cliente | Status | Campos Encontrados | Campos Faltando |
|----------|---------|--------|-------------------|-----------------|
| 26_038 | Semapi RS | dry_run | nenhum | TODOS |
| 26_041 | Zanon Advogados | dry_run | nenhum | TODOS |
| 26_049 | Porto Seguro Vitória/ES | parcial | cnpj, tel, valor | contato, email, endereco, local, tipo, prazo, porte, origem |
| 26_023 | Easy Planning CAU/SC | dry_run | nenhum | TODOS |
| 26_055 | Santana da Boa Vista (Portilho) | dry_run | nenhum | TODOS |
| 26_047 | Banrisul - Morrinhos do Sul | dry_run | nenhum | TODOS |
| 26_043 | Banrisul - Faxinal do Soturno | dry_run | nenhum | TODOS |
| 25_837 | Clínica Bertol Marques | dry_run | nenhum | TODOS |
| 26_053 | Edifício Mondrian Boldinc | dry_run | nenhum | TODOS |
| 26_044 | LFDA | dry_run | nenhum | TODOS |

**Nota:** "Portilho" = Matheus Portilho (funcionário Banrisul, NÃO é cliente)

### Comando para processar:
```bash
source venv/bin/activate
python scripts/ops/processar_demandas.py --prioridade alta
```

---

## PRIORIDADE MÉDIA (17 demandas - 16 precisam pesquisa)

| Asana ID | Cliente | Status | Campos Encontrados | Campos Faltando |
|----------|---------|--------|-------------------|-----------------|
| 26_018 | Cyrela Duo Concept | **OK** | cnpj, contato, email, endereco, local, tipo, detalhes, porte, origem | tel, prazo |
| 26_040 | Almeida Junior - Balneário Shopping | sem resultado | nenhum | TODOS |
| 26_054 | Dilermando de Aguiar - Laudo | sem resultado | nenhum | TODOS |
| 26_036 | Cassi - POA Norte | sem resultado | nenhum | TODOS |
| 26_056 | Pacaembu - Filtros | sem resultado | nenhum | TODOS |
| 26_058 | MSC - Turbina | sem resultado | nenhum | TODOS |
| 26_010 | Neo BPO - PMOC | sem resultado | nenhum | TODOS |
| 25_784 | Melnick Even PDV | sem resultado | nenhum | TODOS |
| 26_008 | BRDE - PMOC | sem resultado | nenhum | TODOS |
| 26_011 | Arezzo - Reserva Caxias/RJ | sem resultado | nenhum | TODOS |
| 26_014 | Expansão Imóveis | sem resultado | nenhum | TODOS |
| 26_027 | FIERGS - Bento Gonçalves | sem resultado | nenhum | TODOS |
| 26_031 | Ambaar POA - PMOC | sem resultado | nenhum | TODOS |
| 26_033 | Senac Penha - Condensadoras | sem resultado | nenhum | TODOS |
| 26_006 | Krystal PROEE Mariland | sem resultado | nenhum | TODOS |
| 25_860 | BB Abelardo Luz - SC | sem resultado | nenhum | TODOS |
| 26_048 | CEO Instituto Olhos Marcon | sem resultado | nenhum | TODOS |

### Comando para processar:
```bash
python scripts/ops/processar_demandas.py --prioridade media
```

---

## PRIORIDADE BAIXA (4 demandas - 1 precisa pesquisa)

| Asana ID | Cliente | Status | Campos Encontrados | Campos Faltando |
|----------|---------|--------|-------------------|-----------------|
| Vários | Banrisul - Várias Agências | parcial | local (8 agências), tipo, detalhes | cnpj, prazo |
| 26_029 | TRE - Pedro Osório | **OK** | contato, email, local, tipo, origem, licitacao | cnpj, endereco |
| 26_060 | Porto Seguro - PMOC | parcial | tipo, detalhes, porte | cnpj, endereco, contato |
| 26_062 | Colombo Park Shopping | **OK** | cnpj, endereco, local, tipo, detalhes, porte | contato |

### Comando para processar:
```bash
python scripts/ops/processar_demandas.py --prioridade baixa
```

---

## Próximos Passos

1. [ ] Executar pesquisa real para as 10 demandas de alta prioridade
2. [ ] Executar pesquisa para as 16 demandas de média prioridade
3. [ ] Complementar dados parciais (26_049, 26_060)
4. [ ] Gerar plano de atualização: `python scripts/ops/atualizar_asana.py`
5. [ ] Executar atualizações no Asana via MCP

---

## Como usar

```bash
# Ativar ambiente
source venv/bin/activate

# Processar todas as pendentes
python scripts/ops/processar_demandas.py

# Por prioridade
python scripts/ops/processar_demandas.py --prioridade alta

# Uma específica
python scripts/ops/processar_demandas.py --id 26_038

# Simular sem executar
python scripts/ops/processar_demandas.py --dry-run

# Gerar plano de atualização para Asana (após processar)
python scripts/ops/atualizar_asana.py
```
