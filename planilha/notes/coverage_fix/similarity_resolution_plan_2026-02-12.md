# Similarity Resolution Plan — 2026-02-12

## Summary
- Remaining DESCRIPTION_HIGH_SIMILARITY warnings: **5**
- Accepted capacity variants moved to info: **15**

## Remaining warnings (actionable)
- `COMP_INST_9K` ↔ `COMP_INST_HW_12K` | sim=0.96 | jaccard=1.00 | **Ação sugerida:** revisar descrição para diferenciar escopo técnico real
- `COMP_INST_9K` ↔ `COMP_INST_HW_18K` | sim=0.96 | jaccard=0.83 | **Ação sugerida:** revisar descrição para diferenciar escopo técnico real
- `COMP_INST_CS4_18K` ↔ `COMP_INST_CS1_18K` | sim=0.96 | jaccard=0.86 | **Ação sugerida:** revisar descrição para diferenciar escopo técnico real
- `COMP_INST_CS4_24K` ↔ `COMP_INST_CS1_24K` | sim=0.96 | jaccard=0.86 | **Ação sugerida:** revisar descrição para diferenciar escopo técnico real
- `COMP_INST_CS4_36K` ↔ `COMP_INST_CS1_36K` | sim=0.96 | jaccard=0.86 | **Ação sugerida:** revisar descrição para diferenciar escopo técnico real

## Naming normalization rule adopted
- If same family and different BTU capacity, treat as acceptable variant (info).
- Keep warning only when high description similarity is not explained by capacity variant.

