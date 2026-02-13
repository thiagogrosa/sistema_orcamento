# Escopos da Gmail API - Referência Rápida

## 🎯 Escopo Recomendado para Este Projeto

```
https://www.googleapis.com/auth/gmail.modify
```

**Por quê?** Permite todas as operações necessárias SEM permitir exclusão permanente de emails.

---

## 📋 Todos os Escopos Disponíveis

### 1. Acesso Completo (NÃO RECOMENDADO)

```
https://mail.google.com/
```

**Permissões:**
- ✅ Ler mensagens e configurações
- ✅ Criar, modificar e deletar mensagens
- ✅ Enviar mensagens
- ✅ Gerenciar labels
- ⚠️ **EXCLUIR PERMANENTEMENTE mensagens**

**Quando usar:** Nunca (exceto se realmente precisar excluir emails)

---

### 2. Modificar (RECOMENDADO) ✅

```
https://www.googleapis.com/auth/gmail.modify
```

**Permissões:**
- ✅ Ler mensagens
- ✅ Criar e modificar mensagens
- ✅ Enviar mensagens
- ✅ Gerenciar labels
- ✅ Marcar como lido/não lido
- ✅ Arquivar/mover mensagens
- ❌ Excluir permanentemente

**Quando usar:** Sistema de orçamentos, CRM, automação de email (sem exclusão)

---

### 3. Somente Leitura

```
https://www.googleapis.com/auth/gmail.readonly
```

**Permissões:**
- ✅ Ler mensagens
- ✅ Ler configurações
- ❌ Modificar mensagens
- ❌ Enviar mensagens
- ❌ Deletar mensagens

**Quando usar:** Análise, backup, monitoramento

---

### 4. Composição

```
https://www.googleapis.com/auth/gmail.compose
```

**Permissões:**
- ✅ Criar e enviar rascunhos
- ✅ Enviar mensagens
- ❌ Ler mensagens existentes
- ❌ Modificar mensagens existentes

**Quando usar:** Apenas envio de email (sem leitura)

---

### 5. Somente Envio

```
https://www.googleapis.com/auth/gmail.send
```

**Permissões:**
- ✅ Enviar mensagens
- ❌ Ler mensagens
- ❌ Modificar mensagens
- ❌ Criar rascunhos

**Quando usar:** Notificações automáticas (sem leitura)

---

### 6. Inserir

```
https://www.googleapis.com/auth/gmail.insert
```

**Permissões:**
- ✅ Inserir mensagens na caixa de entrada
- ❌ Ler mensagens
- ❌ Modificar mensagens existentes

**Quando usar:** Importação de emails de outro sistema

---

### 7. Labels

```
https://www.googleapis.com/auth/gmail.labels
```

**Permissões:**
- ✅ Criar, modificar e deletar labels
- ❌ Ler ou modificar mensagens

**Quando usar:** Gerenciamento de labels apenas

---

### 8. Metadados

```
https://www.googleapis.com/auth/gmail.metadata
```

**Permissões:**
- ✅ Ler metadados de mensagens (remetente, assunto, data)
- ❌ Ler corpo das mensagens
- ❌ Modificar mensagens

**Quando usar:** Estatísticas, contagem, indexação

---

### 9. Configurações Básicas

```
https://www.googleapis.com/auth/gmail.settings.basic
```

**Permissões:**
- ✅ Ler/modificar configurações básicas
- ❌ Acesso a mensagens

**Quando usar:** Gerenciamento de configurações da conta

---

### 10. Configurações de Compartilhamento

```
https://www.googleapis.com/auth/gmail.settings.sharing
```

**Permissões:**
- ✅ Gerenciar delegação de caixa de entrada
- ❌ Acesso a mensagens

**Quando usar:** Configurar acesso de outros usuários

---

## 🔄 Comparação: O Que Cada Escopo Permite

| Ação | mail.google.com | gmail.modify | gmail.readonly | gmail.send |
|------|-----------------|--------------|----------------|------------|
| **Ler emails** | ✅ | ✅ | ✅ | ❌ |
| **Buscar emails** | ✅ | ✅ | ✅ | ❌ |
| **Marcar como lido** | ✅ | ✅ | ❌ | ❌ |
| **Adicionar labels** | ✅ | ✅ | ❌ | ❌ |
| **Arquivar** | ✅ | ✅ | ❌ | ❌ |
| **Enviar email** | ✅ | ✅ | ❌ | ✅ |
| **Mover para lixeira** | ✅ | ✅ | ❌ | ❌ |
| **Excluir permanentemente** | ✅ | ❌ | ❌ | ❌ |

---

## 🎯 Recomendações por Caso de Uso

### Sistema de Orçamentos (nosso caso)
```
✅ gmail.modify
```
**Justificativa:** Precisa ler, buscar e organizar emails, mas não deve excluir.

### Bot de Notificações (só envio)
```
✅ gmail.send
```
**Justificativa:** Apenas envia, não precisa ler nada.

### Backup de Emails
```
✅ gmail.readonly
```
**Justificativa:** Apenas leitura, sem modificações.

### Cliente de Email Completo
```
⚠️ mail.google.com
```
**Justificativa:** Precisa de todas as funcionalidades, incluindo exclusão.

### Análise de Metadados (estatísticas)
```
✅ gmail.metadata
```
**Justificativa:** Apenas metadados, mais rápido e privado.

---

## 🔒 Princípio de Menor Privilégio

**Regra de Ouro:** Sempre use o escopo mais restritivo que atende suas necessidades.

**Benefícios:**
1. ✅ **Segurança:** Limita danos em caso de bug ou ataque
2. ✅ **Privacidade:** Acesso mínimo necessário aos dados
3. ✅ **Auditoria:** Mais fácil de rastrear e entender ações
4. ✅ **Confiança:** Usuários se sentem mais seguros
5. ✅ **Compliance:** Atende regulações de proteção de dados

---

## 📚 Referências

- [Gmail API Scopes - Documentação Oficial](https://developers.google.com/gmail/api/auth/scopes)
- [OAuth 2.0 Scopes](https://developers.google.com/identity/protocols/oauth2/scopes)
- [Best Practices for OAuth 2.0](https://developers.google.com/identity/protocols/oauth2/best-practices)

---

## ✅ Checklist de Configuração

- [ ] Escolhido escopo apropriado (`gmail.modify` para orçamentos)
- [ ] Adicionado escopo no OAuth consent screen
- [ ] Incluídos escopos de identificação (openid, profile, email)
- [ ] Testado após configuração
- [ ] Documentado escolha de escopo no projeto
- [ ] Revisado periodicamente (cada 6 meses)

---

**Última atualização:** 2026-02-06
**Escopo recomendado atual:** `gmail.modify`
