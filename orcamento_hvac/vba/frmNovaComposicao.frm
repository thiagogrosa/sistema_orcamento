VERSION 5.00
Begin {C62A69F0-16DC-11CE-9E98-00AA00574A4F} frmNovaComposicao
   Caption         =   "Nova Composicao"
   ClientHeight    =   4200
   ClientLeft      =   120
   ClientTop       =   465
   ClientWidth     =   5400
   OleObjectBlob   =   "frmNovaComposicao.frx":0000
   StartUpPosition =   1  'CenterOwner
End
Attribute VB_Name = "frmNovaComposicao"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
' =============================================================================
' USERFORM: frmNovaComposicao
' Wizard para criar nova composicao na aba COMPOSICOES
'
' Controles necessarios (criar manualmente no VBA Editor):
'   - lblCodigo: Label "Codigo:"
'   - txtCodigo: TextBox para codigo (ex: COMP_NOVO)
'   - lblDescricao: Label "Descricao:"
'   - txtDescricao: TextBox para descricao curta
'   - lblDescPre: Label "Desc. Pre:"
'   - txtDescPre: TextBox para texto antes da variavel (opcional)
'   - lblDescPos: Label "Desc. Pos:"
'   - txtDescPos: TextBox para texto apos a variavel (opcional)
'   - lblUnidSing: Label "Unid. Sing:"
'   - txtUnidSing: TextBox para unidade singular (ex: "metro") - opcional
'   - lblUnidPlur: Label "Unid. Plur:"
'   - txtUnidPlur: TextBox para unidade plural (ex: "metros") - opcional
'   - lblCopiarDe: Label "Copiar de:"
'   - txtBusca: TextBox para buscar composicoes (digite para filtrar)
'   - lstComposicoes: ListBox para mostrar resultados da busca
'   - btnCriar: CommandButton "Criar"
'   - btnCancelar: CommandButton "Cancelar"
'
' Layout sugerido:
'   lblCodigo (12,18), txtCodigo (90,15) Width=280
'   lblDescricao (12,48), txtDescricao (90,45) Width=280
'   lblDescPre (12,78), txtDescPre (90,75) Width=280
'   lblDescPos (12,108), txtDescPos (90,105) Width=280
'   lblUnidSing (12,138), txtUnidSing (90,135) Width=130
'   lblUnidPlur (155,138), txtUnidPlur (240,135) Width=130
'   lblCopiarDe (12,168), txtBusca (90,165) Width=280
'   lstComposicoes (90,190) Width=280, Height=80
'   btnCriar (90,280) Width=100, btnCancelar (200,280) Width=100
'   Form Height: 340
' =============================================================================

Option Explicit

' Array para armazenar lista completa de composicoes (para filtro)
Private m_listaCompleta() As String

Private Sub UserForm_Initialize()
    Me.txtCodigo.Text = "COMP_"
    Me.txtDescricao.Text = ""
    Me.txtDescPre.Text = ""
    Me.txtDescPos.Text = ""
    Me.txtUnidSing.Text = ""
    Me.txtUnidPlur.Text = ""
    Me.txtBusca.Text = ""

    ' Carregar lista de composicoes
    Call CarregarListaCompleta
    Call FiltrarLista("")

    Me.txtCodigo.SetFocus
End Sub

Private Sub CarregarListaCompleta()
    ' Carrega todas as composicoes em array para filtro posterior
    Dim composicoes As Variant
    Dim i As Long
    Dim count As Long

    composicoes = ListarComposicoes()

    If IsArray(composicoes) Then
        count = 0
        For i = LBound(composicoes) To UBound(composicoes)
            If composicoes(i) <> "" Then count = count + 1
        Next i

        If count > 0 Then
            ReDim m_listaCompleta(1 To count)
            count = 0
            For i = LBound(composicoes) To UBound(composicoes)
                If composicoes(i) <> "" Then
                    count = count + 1
                    m_listaCompleta(count) = composicoes(i)
                End If
            Next i
        Else
            ReDim m_listaCompleta(0 To 0)
        End If
    Else
        ReDim m_listaCompleta(0 To 0)
    End If
End Sub

Private Sub FiltrarLista(filtro As String)
    ' Preenche ListBox com itens que contem o filtro (case insensitive)
    Dim i As Long
    Dim filtroUpper As String

    Me.lstComposicoes.Clear
    Me.lstComposicoes.AddItem "(Nao copiar - criar vazia)"

    filtroUpper = UCase(Trim(filtro))

    If UBound(m_listaCompleta) >= 1 Then
        For i = LBound(m_listaCompleta) To UBound(m_listaCompleta)
            If m_listaCompleta(i) <> "" Then
                If filtroUpper = "" Or InStr(1, UCase(m_listaCompleta(i)), filtroUpper, vbTextCompare) > 0 Then
                    Me.lstComposicoes.AddItem m_listaCompleta(i)
                End If
            End If
        Next i
    End If

    ' Seleciona primeiro item por padrao
    If Me.lstComposicoes.ListCount > 0 Then
        Me.lstComposicoes.ListIndex = 0
    End If
End Sub

Private Sub txtBusca_Change()
    ' Filtra a lista em tempo real enquanto digita
    Call FiltrarLista(Me.txtBusca.Text)
End Sub

Private Sub lstComposicoes_Click()
    ' Ao clicar em um item, preenche os campos
    Call PreencherCamposDaSelecao
End Sub

Private Sub lstComposicoes_DblClick(ByVal Cancel As MSForms.ReturnBoolean)
    ' Duplo clique seleciona e foca no proximo campo
    Call PreencherCamposDaSelecao
    Me.txtCodigo.SetFocus
End Sub

Private Sub PreencherCamposDaSelecao()
    ' Preenche campos baseado na selecao do ListBox
    If Me.lstComposicoes.ListIndex < 0 Then Exit Sub

    If Me.lstComposicoes.ListIndex = 0 Then
        ' "(Nao copiar - criar vazia)"
        Me.txtDescricao.Text = ""
        Me.txtDescPre.Text = ""
        Me.txtDescPos.Text = ""
        Me.txtUnidSing.Text = ""
        Me.txtUnidPlur.Text = ""
    Else
        Dim selText As String
        Dim lastSep As Long
        Dim codigoOrigem As String
        Dim dados As Variant

        selText = Me.lstComposicoes.Value
        lastSep = InStrRev(selText, " - ")

        If lastSep > 0 Then
            codigoOrigem = Mid(selText, lastSep + 3)
            dados = ObterDadosComposicao(codigoOrigem)

            Me.txtDescricao.Text = dados(1) & " (copia)"
            Me.txtDescPre.Text = dados(2)
            Me.txtDescPos.Text = dados(3)
            Me.txtUnidSing.Text = dados(4)
            Me.txtUnidPlur.Text = dados(5)
        End If
    End If
End Sub

Private Sub btnCriar_Click()
    Dim copiarDe As String

    ' Validacao do codigo
    If Trim(Me.txtCodigo.Text) = "" Or Trim(Me.txtCodigo.Text) = "COMP_" Then
        MsgBox "Informe o codigo da composicao (ex: COMP_NOVO)", vbExclamation, "Codigo Obrigatorio"
        Me.txtCodigo.SetFocus
        Exit Sub
    End If

    ' Valida formato do codigo
    If Left(UCase(Trim(Me.txtCodigo.Text)), 5) <> "COMP_" Then
        MsgBox "O codigo deve comecar com COMP_" & vbCrLf & _
               "Exemplo: COMP_INST_12K", vbExclamation, "Formato Invalido"
        Me.txtCodigo.SetFocus
        Exit Sub
    End If

    ' Validacao da descricao
    If Trim(Me.txtDescricao.Text) = "" Then
        MsgBox "Informe a descricao da composicao", vbExclamation, "Descricao Obrigatoria"
        Me.txtDescricao.SetFocus
        Exit Sub
    End If

    ' Verifica se codigo ja existe
    If VerificarCodigoExiste(Trim(Me.txtCodigo.Text)) Then
        MsgBox "Este codigo ja existe na planilha!" & vbCrLf & _
               "Escolha outro codigo.", vbExclamation, "Codigo Duplicado"
        Me.txtCodigo.SetFocus
        Exit Sub
    End If

    ' Extrai codigo da composicao a copiar (se selecionado no ListBox)
    copiarDe = ""
    If Me.lstComposicoes.ListIndex > 0 Then
        Dim selText As String
        Dim lastSep As Long
        selText = Me.lstComposicoes.Value
        lastSep = InStrRev(selText, " - ")
        If lastSep > 0 Then
            copiarDe = Mid(selText, lastSep + 3)
        End If
    End If

    ' Chama a sub que cria a composicao
    Call CriarComposicaoCompleta( _
        Trim(Me.txtCodigo.Text), _
        Trim(Me.txtDescricao.Text), _
        Trim(Me.txtDescPre.Text), _
        Trim(Me.txtDescPos.Text), _
        Trim(Me.txtUnidSing.Text), _
        Trim(Me.txtUnidPlur.Text), _
        copiarDe)

    Unload Me
End Sub

Private Sub btnCancelar_Click()
    Unload Me
End Sub

Private Sub txtCodigo_Change()
    ' Converte para maiusculas automaticamente
    Dim curPos As Long
    curPos = Me.txtCodigo.SelStart
    Me.txtCodigo.Text = UCase(Me.txtCodigo.Text)
    Me.txtCodigo.SelStart = curPos
End Sub
