Attribute VB_Name = "modMacros"
Option Explicit

' =============================================================================
' MODULO: modMacros
' Macros para a Planilha de Custos HVAC Split
'
' Estrutura de colunas COMPOSICOES (A-R):
'   A: Codigo, B: Descricao, C: Tipo, D: Cod.Item, E: Un (SPILL)
'   F: Qtd Base, G: Qtd Var, H: Preco Unit. (SPILL), I: Sub.Base (SPILL), J: Sub.Var (SPILL)
'   K: Mult. (SPILL), L: Base c/Margem (SPILL), M: Var c/Margem (SPILL), N: Selecao
'   O: Desc.Pre, P: Desc.Pos, Q: Unid.Sing, R: Unid.Plur
'
' IMPORTANTE: Colunas E, H, I, J, K, L, M sao preenchidas por formulas de spill
' no template.xlsm. As formulas de spill calculam valores para itens E somam
' automaticamente nas linhas de header.
' Este modulo so insere DADOS nas colunas A, B, C, D, F, G, N, O, P, Q, R.
'
' Linhas de multiplicadores na aba NEGOCIO:
'   B42: MAT, B43: MO, B44: FER, B45: EQP
' =============================================================================

' Constantes de cores por tipo
Private Const COR_MO As Long = 15461593   ' RGB(234,250,241) - verde claro
Private Const COR_FER As Long = 15202814  ' RGB(254,249,231) - amarelo claro
Private Const COR_EQP As Long = 16511467  ' RGB(235,245,251) - azul claro
Private Const COR_HEADER As Long = 11240238 ' RGB(46,134,171) - azul cabecalho

' Linhas de multiplicadores na aba NEGOCIO (ajustar se necessario)
Private Const MULT_MAT_ROW As Long = 42
Private Const MULT_MO_ROW As Long = 43
Private Const MULT_FER_ROW As Long = 44
Private Const MULT_EQP_ROW As Long = 45

' =============================================================================
' AtualizarSelecao - Atualiza formulas da coluna Selecao na aba ativa
' =============================================================================
Public Sub AtualizarSelecao()
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim selCol As Integer
    Dim formulaPattern As String
    Dim i As Long
    Dim startRow As Long

    Set ws = ActiveSheet

    Select Case ws.Name
        Case "MATERIAIS"
            selCol = 6  ' Coluna F
            formulaPattern = "=A{ROW}&"" - ""&C{ROW}"
            startRow = 2
            lastRow = FindLastDataRow(ws, 1)

        Case "MAO_DE_OBRA"
            selCol = 6
            formulaPattern = "=A{ROW}&"" - ""&C{ROW}"
            startRow = 2
            lastRow = FindLastDataRow(ws, 1)

        Case "FERRAMENTAS"
            selCol = 7  ' Coluna G
            formulaPattern = "=A{ROW}&"" - ""&C{ROW}"
            startRow = 2
            lastRow = FindLastDataRow(ws, 1)

        Case "EQUIPAMENTOS"
            selCol = 7
            formulaPattern = "=A{ROW}&"" - ""&C{ROW}"
            startRow = 2
            lastRow = FindLastDataRow(ws, 1)

        Case "COMPOSICOES"
            ' Selecao agora na coluna N (14)
            Call AtualizarSelecaoComposicoes(ws)
            Exit Sub

        Case Else
            MsgBox "Esta funcao so funciona nas abas:" & vbCrLf & _
                   "- MATERIAIS" & vbCrLf & _
                   "- MAO_DE_OBRA" & vbCrLf & _
                   "- FERRAMENTAS" & vbCrLf & _
                   "- EQUIPAMENTOS" & vbCrLf & _
                   "- COMPOSICOES", vbExclamation, "Aba Invalida"
            Exit Sub
    End Select

    If lastRow >= startRow Then
        For i = startRow To lastRow
            ws.Cells(i, selCol).Formula = Replace(formulaPattern, "{ROW}", CStr(i))
        Next i

        Call AtualizarIntervaloNomeado(ws.Name, selCol, lastRow)

        MsgBox "Selecao atualizada!" & vbCrLf & _
               "Linhas processadas: " & (lastRow - startRow + 1), _
               vbInformation, "Concluido"
    Else
        MsgBox "Nenhum dado encontrado na aba.", vbExclamation, "Aviso"
    End If
End Sub

' =============================================================================
' Funcao auxiliar para encontrar ultima linha com dados
' =============================================================================
Private Function FindLastDataRow(ws As Worksheet, col As Integer) As Long
    Dim lastRow As Long
    lastRow = ws.Cells(ws.Rows.Count, col).End(xlUp).Row
    If lastRow < 2 Then lastRow = 1
    FindLastDataRow = lastRow
End Function

' =============================================================================
' Atualiza Selecao para COMPOSICOES (coluna O = 15)
' =============================================================================
Private Sub AtualizarSelecaoComposicoes(ws As Worksheet)
    Dim lastRow As Long
    Dim i As Long
    Dim countUpdated As Long

    lastRow = FindLastDataRow(ws, 1)
    countUpdated = 0

    For i = 2 To lastRow
        If ws.Cells(i, 1).Value <> "" And _
           Left(ws.Cells(i, 1).Value, 5) = "COMP_" And _
           ws.Cells(i, 2).Value <> "" Then

            ' Coluna N (14) = Selecao
            ws.Cells(i, 14).Formula = "=A" & i & "&"" - ""&B" & i
            countUpdated = countUpdated + 1
        End If
    Next i

    Call AtualizarIntervaloNomeado("COMPOSICOES", 14, lastRow)

    MsgBox "Selecao atualizada!" & vbCrLf & _
           "Composicoes processadas: " & countUpdated, _
           vbInformation, "Concluido"
End Sub

' =============================================================================
' Atualiza intervalo nomeado para dropdown
' =============================================================================
Private Sub AtualizarIntervaloNomeado(sheetName As String, selCol As Integer, lastRow As Long)
    Dim nm As Name
    Dim nmName As String
    Dim colLetter As String
    Dim refText As String

    Select Case sheetName
        Case "MATERIAIS": nmName = "LISTA_MAT"
        Case "MAO_DE_OBRA": nmName = "LISTA_MO"
        Case "FERRAMENTAS": nmName = "LISTA_FER"
        Case "EQUIPAMENTOS": nmName = "LISTA_EQP"
        Case "COMPOSICOES": nmName = "LISTA_COMP"
        Case Else: Exit Sub
    End Select

    colLetter = Split(Cells(1, selCol).Address, "$")(1)
    refText = "=" & sheetName & "!$" & colLetter & "$2:$" & colLetter & "$" & lastRow

    On Error Resume Next
    ThisWorkbook.Names(nmName).Delete
    On Error GoTo 0

    ThisWorkbook.Names.Add Name:=nmName, RefersTo:=refText
End Sub

' =============================================================================
' NovaComposicao - Abre wizard para criar nova composicao
' =============================================================================
Public Sub NovaComposicao()
    If ActiveSheet.Name <> "COMPOSICOES" Then
        If MsgBox("Voce nao esta na aba COMPOSICOES." & vbCrLf & _
                  "Deseja ir para la agora?", vbQuestion + vbYesNo) = vbYes Then
            ThisWorkbook.Sheets("COMPOSICOES").Activate
        Else
            Exit Sub
        End If
    End If

    frmNovaComposicao.Show
End Sub

' =============================================================================
' CriarComposicaoCompleta - Cria composicao com 4 linhas de tipo
' Chamado pelo UserForm
' =============================================================================
Public Sub CriarComposicaoCompleta(codigo As String, descricao As String, _
                                    descPre As String, descPos As String, _
                                    unidSing As String, unidPlur As String, _
                                    Optional copiarDe As String = "")
    Dim ws As Worksheet
    Dim insertRow As Long
    Dim lastRow As Long
    Dim tipos As Variant
    Dim i As Integer
    Dim firstItemRow As Long
    Dim lastItemRow As Long

    tipos = Array("MAT", "MO", "FER", "EQP")

    On Error Resume Next
    Set ws = ThisWorkbook.Sheets("COMPOSICOES")
    On Error GoTo 0

    If ws Is Nothing Then
        MsgBox "Aba COMPOSICOES nao encontrada!", vbCritical
        Exit Sub
    End If

    ' Encontra ultima linha com dados (verifica colunas A, C e D pois itens nao tem valor em A)
    Dim lastRowA As Long, lastRowC As Long, lastRowD As Long
    lastRowA = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row  ' Coluna Codigo
    lastRowC = ws.Cells(ws.Rows.Count, 3).End(xlUp).Row  ' Coluna Tipo
    lastRowD = ws.Cells(ws.Rows.Count, 4).End(xlUp).Row  ' Coluna Cod.Item

    ' Usa a maior das tres
    lastRow = lastRowA
    If lastRowC > lastRow Then lastRow = lastRowC
    If lastRowD > lastRow Then lastRow = lastRowD

    ' Nova composicao vai 2 linhas abaixo da ultima (1 linha de espaco)
    If lastRow > 1 Then
        insertRow = lastRow + 2
    Else
        insertRow = 2
    End If

    ' Cabecalho da composicao
    Call FormatarCabecalhoComposicao(ws, insertRow, codigo, descricao, descPre, descPos, unidSing, unidPlur)

    firstItemRow = insertRow + 1

    ' Se copiarDe especificado, copiar itens da composicao existente
    If copiarDe <> "" Then
        Call CopiarItensComposicao(ws, copiarDe, insertRow)
    Else
        ' Criar 4 linhas vazias (uma por tipo)
        For i = 0 To 3
            Call FormatarLinhaItem(ws, insertRow + 1 + i, CStr(tipos(i)))
        Next i
    End If

    ' Encontra ultima linha de itens criada
    lastItemRow = FindUltimaLinhaItens(ws, insertRow)
    If lastItemRow < firstItemRow Then lastItemRow = firstItemRow + 19

    ' NOTA: Os totais nas linhas de cabecalho (J, K, M, N) sao calculados
    ' automaticamente pelas formulas de spill. Cada formula detecta se a linha
    ' e um cabecalho (coluna A preenchida) e calcula a soma dos itens abaixo.

    ' Seleciona a celula da nova composicao
    ws.Activate
    ws.Cells(insertRow, 1).Select

    MsgBox "Composicao criada na linha " & insertRow & "!" & vbCrLf & vbCrLf & _
           "Estrutura criada:" & vbCrLf & _
           "- Cabecalho formatado" & vbCrLf & _
           "- 4 linhas de itens (MAT, MO, FER, EQP)" & vbCrLf & vbCrLf & _
           "NOTA: As formulas de spill preencherao automaticamente" & vbCrLf & _
           "as colunas E, F, I-N apos voce preencher os dados." & vbCrLf & vbCrLf & _
           "Preencha os codigos dos itens na coluna D.", _
           vbInformation, "Composicao Criada"
End Sub

' =============================================================================
' FormatarCabecalhoComposicao - Formata linha de cabecalho (colunas A-R)
' =============================================================================
Private Sub FormatarCabecalhoComposicao(ws As Worksheet, row As Long, _
                                         codigo As String, descricao As String, _
                                         descPre As String, descPos As String, _
                                         unidSing As String, unidPlur As String)
    Dim col As Integer

    ' Coluna A: Codigo
    With ws.Cells(row, 1)
        .Value = codigo
        .Font.Bold = True
        .Font.Color = vbWhite
        .Font.Name = "Consolas"
        .Interior.Color = COR_HEADER
        .HorizontalAlignment = xlLeft
        .VerticalAlignment = xlCenter
        .Borders.LineStyle = xlContinuous
    End With

    ' Coluna B: Descricao
    With ws.Cells(row, 2)
        .Value = descricao
        .Font.Bold = True
        .Font.Color = vbWhite
        .Interior.Color = COR_HEADER
        .HorizontalAlignment = xlLeft
        .VerticalAlignment = xlCenter
        .Borders.LineStyle = xlContinuous
    End With

    ' Colunas C-M: Vazias com preenchimento azul (SPILL preenchera totais)
    For col = 3 To 13
        With ws.Cells(row, col)
            .Interior.Color = COR_HEADER
            .Borders.LineStyle = xlContinuous
        End With
    Next col

    ' Coluna N: Selecao (formula)
    With ws.Cells(row, 14)
        .Formula = "=A" & row & "&"" - ""&B" & row
        .Interior.Color = COR_HEADER
        .Borders.LineStyle = xlContinuous
    End With

    ' Coluna O: Desc. Pre
    With ws.Cells(row, 15)
        .Value = descPre
        .Font.Color = vbWhite
        .Interior.Color = COR_HEADER
        .Borders.LineStyle = xlContinuous
    End With

    ' Coluna P: Desc. Pos
    With ws.Cells(row, 16)
        .Value = descPos
        .Font.Color = vbWhite
        .Interior.Color = COR_HEADER
        .Borders.LineStyle = xlContinuous
    End With

    ' Coluna Q: Unid. Sing
    With ws.Cells(row, 17)
        .Value = unidSing
        .Font.Color = vbWhite
        .Interior.Color = COR_HEADER
        .Borders.LineStyle = xlContinuous
    End With

    ' Coluna R: Unid. Plur
    With ws.Cells(row, 18)
        .Value = unidPlur
        .Font.Color = vbWhite
        .Interior.Color = COR_HEADER
        .Borders.LineStyle = xlContinuous
    End With
End Sub

' =============================================================================
' FormatarLinhaItem - Formata linha de item com tipo pre-preenchido
' NOTA: Colunas E, H, I, J, K, L, M sao preenchidas por formulas de spill
' =============================================================================
Private Sub FormatarLinhaItem(ws As Worksheet, row As Long, tipo As String)
    Dim col As Integer

    ' Colunas A-B: Vazias
    ws.Cells(row, 1).Value = ""
    ws.Cells(row, 1).Borders.LineStyle = xlContinuous
    ws.Cells(row, 2).Value = ""
    ws.Cells(row, 2).Borders.LineStyle = xlContinuous

    ' Coluna C: Tipo (DADO)
    With ws.Cells(row, 3)
        .Value = tipo
        .HorizontalAlignment = xlCenter
        .Borders.LineStyle = xlContinuous
    End With

    ' Coluna D: Vazia (usuario preenche - DADO)
    With ws.Cells(row, 4)
        .Value = ""
        .Font.Name = "Consolas"
        .Borders.LineStyle = xlContinuous
    End With

    ' Coluna E: Vazia (SPILL preenchera Un)
    ws.Cells(row, 5).HorizontalAlignment = xlCenter
    ws.Cells(row, 5).Borders.LineStyle = xlContinuous

    ' Colunas F-G: Vazias (input - DADO)
    ws.Cells(row, 6).Value = ""
    ws.Cells(row, 6).NumberFormat = "0.00"
    ws.Cells(row, 6).HorizontalAlignment = xlCenter
    ws.Cells(row, 6).Borders.LineStyle = xlContinuous

    ws.Cells(row, 7).Value = ""
    ws.Cells(row, 7).NumberFormat = "0.00"
    ws.Cells(row, 7).HorizontalAlignment = xlCenter
    ws.Cells(row, 7).Borders.LineStyle = xlContinuous

    ' Colunas H-M: Vazias (SPILL preenchera)
    For col = 8 To 13
        ws.Cells(row, col).Borders.LineStyle = xlContinuous
        If col = 11 Then  ' Mult.
            ws.Cells(row, col).NumberFormat = "0.0000"
            ws.Cells(row, col).HorizontalAlignment = xlCenter
        Else
            ws.Cells(row, col).NumberFormat = """R$ ""#,##0.00"
        End If
    Next col

    ' Colunas N, O, P, Q, R: Vazias
    For col = 14 To 18
        ws.Cells(row, col).Value = ""
        ws.Cells(row, col).Borders.LineStyle = xlContinuous
    Next col

    ' Aplicar cor por tipo (18 colunas A-R)
    Call AplicarCorPorTipo(ws, row, tipo)
End Sub

' =============================================================================
' Funcoes auxiliares para construir formulas
' =============================================================================
Private Function BuildFormulaDescricao(row As Long, extractCode As String) As String
    BuildFormulaDescricao = "=IF(C" & row & "="""",""""," & _
        "IF(C" & row & "=""MAT"",VLOOKUP(" & extractCode & ",MATERIAIS!$A:$E,3,FALSE)," & _
        "IF(C" & row & "=""MO"",VLOOKUP(" & extractCode & ",MAO_DE_OBRA!$A:$E,3,FALSE)," & _
        "IF(C" & row & "=""FER"",VLOOKUP(" & extractCode & ",FERRAMENTAS!$A:$F,3,FALSE)," & _
        "IF(C" & row & "=""EQP"",VLOOKUP(" & extractCode & ",EQUIPAMENTOS!$A:$F,3,FALSE),"""")))))"
End Function

Private Function BuildFormulaUnidade(row As Long, extractCode As String) As String
    BuildFormulaUnidade = "=IF(C" & row & "="""",""""," & _
        "IF(C" & row & "=""MAT"",VLOOKUP(" & extractCode & ",MATERIAIS!$A:$E,4,FALSE)," & _
        "IF(C" & row & "=""MO"",VLOOKUP(" & extractCode & ",MAO_DE_OBRA!$A:$E,4,FALSE)," & _
        "IF(C" & row & "=""FER"",""H""," & _
        "IF(C" & row & "=""EQP"",VLOOKUP(" & extractCode & ",EQUIPAMENTOS!$A:$F,5,FALSE),"""")))))"
End Function

Private Function BuildFormulaPreco(row As Long, extractCode As String) As String
    BuildFormulaPreco = "=IF(C" & row & "="""",""""," & _
        "IF(C" & row & "=""MAT"",VLOOKUP(" & extractCode & ",MATERIAIS!$A:$E,5,FALSE)," & _
        "IF(C" & row & "=""MO"",VLOOKUP(" & extractCode & ",MAO_DE_OBRA!$A:$E,5,FALSE)," & _
        "IF(C" & row & "=""FER"",VLOOKUP(" & extractCode & ",FERRAMENTAS!$A:$F,6,FALSE)," & _
        "IF(C" & row & "=""EQP"",VLOOKUP(" & extractCode & ",EQUIPAMENTOS!$A:$F,6,FALSE),"""")))))"
End Function

Private Function BuildFormulaMultiplicador(row As Long) As String
    BuildFormulaMultiplicador = "=IF(C" & row & "="""",""""," & _
        "IF(C" & row & "=""MAT"",NEGOCIO!$B$" & MULT_MAT_ROW & "," & _
        "IF(C" & row & "=""MO"",NEGOCIO!$B$" & MULT_MO_ROW & "," & _
        "IF(C" & row & "=""FER"",NEGOCIO!$B$" & MULT_FER_ROW & "," & _
        "IF(C" & row & "=""EQP"",NEGOCIO!$B$" & MULT_EQP_ROW & ",1)))))"
End Function

' =============================================================================
' AplicarCorPorTipo - Aplica cor de fundo baseada no tipo (colunas A-R)
' =============================================================================
Private Sub AplicarCorPorTipo(ws As Worksheet, row As Long, tipo As String)
    Dim corFill As Long
    Dim col As Integer

    Select Case tipo
        Case "MO"
            corFill = COR_MO
        Case "FER"
            corFill = COR_FER
        Case "EQP"
            corFill = COR_EQP
        Case Else
            Exit Sub  ' MAT usa cor padrao
    End Select

    For col = 1 To 18  ' Colunas A-R
        ws.Cells(row, col).Interior.Color = corFill
    Next col
End Sub

' =============================================================================
' CopiarItensComposicao - Copia itens de uma composicao existente
' =============================================================================
Private Sub CopiarItensComposicao(ws As Worksheet, codigoOrigem As String, insertRow As Long)
    Dim origemRow As Long
    Dim firstItemOrigem As Long
    Dim lastItemOrigem As Long
    Dim i As Long
    Dim destRow As Long
    Dim tipo As String

    ' Encontra a composicao de origem
    origemRow = 0
    For i = 2 To ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
        If ws.Cells(i, 1).Value = codigoOrigem Then
            origemRow = i
            Exit For
        End If
    Next i

    If origemRow = 0 Then
        ' Composicao nao encontrada, cria estrutura padrao
        Call FormatarLinhaItem(ws, insertRow + 1, "MAT")
        Call FormatarLinhaItem(ws, insertRow + 2, "MO")
        Call FormatarLinhaItem(ws, insertRow + 3, "FER")
        Call FormatarLinhaItem(ws, insertRow + 4, "EQP")
        Exit Sub
    End If

    ' Encontra primeira e ultima linha de itens da composicao de origem
    firstItemOrigem = origemRow + 1
    lastItemOrigem = firstItemOrigem

    i = firstItemOrigem
    Do While i <= ws.Cells(ws.Rows.Count, 3).End(xlUp).Row + 1
        If ws.Cells(i, 1).Value <> "" And Left(ws.Cells(i, 1).Value, 5) = "COMP_" Then
            lastItemOrigem = i - 1
            Exit Do
        ElseIf ws.Cells(i, 3).Value = "" And ws.Cells(i, 4).Value = "" Then
            If i > firstItemOrigem Then lastItemOrigem = i - 1
            Exit Do
        End If
        lastItemOrigem = i
        i = i + 1
    Loop

    ' Copia cada linha de item
    destRow = insertRow + 1
    For i = firstItemOrigem To lastItemOrigem
        tipo = ws.Cells(i, 3).Value
        If tipo <> "" Then
            ' Formata linha com o mesmo tipo
            Call FormatarLinhaItem(ws, destRow, tipo)

            ' Copia valores de quantidade (F e G)
            If ws.Cells(i, 6).Value <> "" Then ws.Cells(destRow, 6).Value = ws.Cells(i, 6).Value
            If ws.Cells(i, 7).Value <> "" Then ws.Cells(destRow, 7).Value = ws.Cells(i, 7).Value

            ' Copia codigo do item (D) - apenas o codigo, nao a selecao completa
            Dim codItem As String
            codItem = ws.Cells(i, 4).Value
            If InStr(codItem, " - ") > 0 Then
                codItem = Left(codItem, InStr(codItem, " - ") - 1)
            End If
            ws.Cells(destRow, 4).Value = codItem

            destRow = destRow + 1
        End If
    Next i
End Sub

' =============================================================================
' FindUltimaLinhaItens - Encontra ultima linha de itens de uma composicao
' =============================================================================
Private Function FindUltimaLinhaItens(ws As Worksheet, headerRow As Long) As Long
    Dim i As Long
    Dim lastItem As Long

    lastItem = headerRow
    i = headerRow + 1

    Do While i <= ws.Cells(ws.Rows.Count, 3).End(xlUp).Row + 1
        If ws.Cells(i, 1).Value <> "" And Left(ws.Cells(i, 1).Value, 5) = "COMP_" Then
            Exit Do
        ElseIf ws.Cells(i, 3).Value <> "" Then
            lastItem = i
        ElseIf ws.Cells(i, 3).Value = "" And ws.Cells(i, 4).Value = "" Then
            Exit Do
        End If
        i = i + 1
    Loop

    FindUltimaLinhaItens = lastItem
End Function

' =============================================================================
' AtualizarTotaisComposicao - Informativo sobre formulas de spill
' NOTA: Os totais sao calculados automaticamente pelas formulas de spill.
' As colunas J, K, M, N detectam linhas de cabecalho (coluna A preenchida)
' e calculam a soma dos itens abaixo automaticamente.
' =============================================================================
Public Sub AtualizarTotaisComposicao()
    MsgBox "Os totais das composicoes sao calculados automaticamente" & vbCrLf & _
           "pelas formulas de spill nas colunas J, K, M, N." & vbCrLf & vbCrLf & _
           "Nas linhas de cabecalho (com codigo na coluna A)," & vbCrLf & _
           "os valores mostram a soma dos itens abaixo." & vbCrLf & vbCrLf & _
           "Pressione F9 para recalcular se necessario.", _
           vbInformation, "Totais Automaticos"
End Sub

' =============================================================================
' VerificarCodigoExiste - Verifica se codigo ja existe (usada pelo form)
' =============================================================================
Public Function VerificarCodigoExiste(codigo As String) As Boolean
    Dim ws As Worksheet
    Dim rng As Range

    On Error Resume Next
    Set ws = ThisWorkbook.Sheets("COMPOSICOES")
    On Error GoTo 0

    If ws Is Nothing Then
        VerificarCodigoExiste = False
        Exit Function
    End If

    Set rng = ws.Columns(1).Find(What:=codigo, LookIn:=xlValues, LookAt:=xlWhole)
    VerificarCodigoExiste = Not rng Is Nothing
End Function

' =============================================================================
' ListarComposicoes - Retorna array com todas as composicoes existentes
' Usada pelo form para preencher o ComboBox
' =============================================================================
Public Function ListarComposicoes() As Variant
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim lista() As String
    Dim count As Long

    On Error Resume Next
    Set ws = ThisWorkbook.Sheets("COMPOSICOES")
    On Error GoTo 0

    If ws Is Nothing Then
        ListarComposicoes = Array()
        Exit Function
    End If

    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    count = 0

    ' Primeiro, conta quantas composicoes existem
    For i = 2 To lastRow
        If Left(ws.Cells(i, 1).Value, 5) = "COMP_" Then
            count = count + 1
        End If
    Next i

    If count = 0 Then
        ListarComposicoes = Array()
        Exit Function
    End If

    ReDim lista(1 To count)
    count = 0

    ' Agora preenche o array (Descricao - Codigo para facilitar busca)
    For i = 2 To lastRow
        If Left(ws.Cells(i, 1).Value, 5) = "COMP_" Then
            count = count + 1
            lista(count) = ws.Cells(i, 2).Value & " - " & ws.Cells(i, 1).Value
        End If
    Next i

    ListarComposicoes = lista
End Function

' =============================================================================
' ObterDadosComposicao - Retorna Descricao, DescPre, DescPos, UnidSing, UnidPlur
' Usada pelo form para preencher campos ao copiar
' =============================================================================
Public Function ObterDadosComposicao(codigo As String) As Variant
    Dim ws As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim resultado(1 To 5) As String  ' 1=Descricao, 2=DescPre, 3=DescPos, 4=UnidSing, 5=UnidPlur

    resultado(1) = ""
    resultado(2) = ""
    resultado(3) = ""
    resultado(4) = ""
    resultado(5) = ""

    On Error Resume Next
    Set ws = ThisWorkbook.Sheets("COMPOSICOES")
    On Error GoTo 0

    If ws Is Nothing Then
        ObterDadosComposicao = resultado
        Exit Function
    End If

    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row

    For i = 2 To lastRow
        If ws.Cells(i, 1).Value = codigo Then
            resultado(1) = ws.Cells(i, 2).Value   ' Coluna B: Descricao
            resultado(2) = ws.Cells(i, 15).Value  ' Coluna O: Desc.Pre
            resultado(3) = ws.Cells(i, 16).Value  ' Coluna P: Desc.Pos
            resultado(4) = ws.Cells(i, 17).Value  ' Coluna Q: Unid.Sing
            resultado(5) = ws.Cells(i, 18).Value  ' Coluna R: Unid.Plur
            Exit For
        End If
    Next i

    ObterDadosComposicao = resultado
End Function
