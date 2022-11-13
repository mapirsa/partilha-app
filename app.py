# Import required packages

from dash import Dash, dcc, html, Input, Output

import os 

# Títulos e sub-títulos

title = 'Cálculo de Divisão de Bens e Herança por Modalidade de Regime de Bens'

esc_evento = "Selecione o evento desejado"

esc_reg = 'Selecione a modalidade do regime de bens'

tit_divorcio = 'Como fica a divisão de bens'

tit_sucessao = 'Como fica a divisão da herança'

questoes = ['Há cônjuge sobrevivente ?',
            'Existem herdeiros necessários ?',
            'Qual percentual testou da herança disponível ?',
            'Deixou testamento ?',
            'Quem foram os beneficiários do testamento ?',
            "Qual percentual dos bens foram adquiridos na constância do casamento ?"]
respostas = ['Sim',
            'Não']


# Menus dos dropdowns
eventos = [
    {'label': 'Divórcio', 'value': 1},
    {'label': 'Sucessão', 'value': 2}
]
esc_reg = 'Selecione a modalidade do regime de bens'

regimes = [
    {'label': 'Comunhão Parcial de Bens', 'value': 0},
    {'label': 'Comunhão Universal de Bens', 'value': 1},
    {'label': 'Separação Total de Bens', 'value': 2},
    {'label': 'Separação Obrigatória de Bens', 'value': 3}
]
herdeiros = [
    {'label': 'Sem herdeiros', 'value': 0},
    {'label': '1 herdeiro', 'value': 1},
    {'label': '2 herdeiros', 'value': 2},
    {'label': '3 herdeiros', 'value': 3},
    {'label': '4 herdeiros', 'value': 4},
    {'label': '5 herdeiros', 'value': 5}]

beneficiarios = [
    {'label': 'Somente o cônjuge sobrevivente', 'value': 0},
    {'label': 'Herdeiros necessários igualitariamente', 'value': 1},
    {'label': 'Cônjuge sobrevivente e herdeiros necessários, igualitariamente', 'value': 2},
    {'label': 'Outros', 'value': 3}]


# Respostas

divorcio_respostas = [
    [''' * Bens adquiridos antes do casamento não se comunicam.''',
    '''* Bens adquiridos durante o casamento são divididos na proporção de 50% para cada cônjuge.'''],

    [''' * O patrimônio adquirido antes ou durante o casamento pertence a ambos os côniuges e serão divididos na proporção de 50% para cada um.''',
    '''* Apenas não farão parte do patrimônio comum as herancas e doações recebidas com cláusula de incomunicabilidade.'''],

    [''' * Os bens não se comunicam. ''', '''* Não há divisão de bens.'''],
    [''' * Os bens não se comunicam. ''', '''* Não há divisão de bens.''']]

# Aviso Final

aviso = [ "Aviso",
        "* Podem haver interpretações alternativas da legislação.",
          "* Consulte um advogado especializado para um aconselhamento mais detalhado.",
        "Fonte: Código Civil - Art.1.829",
        "Fonte: Código Civil - Art. 1.658 e seguintes"]


# Estilos das mensagens

style_msg = {'textAlign':'left', 'color': '#F57241','font-size': 30}
style_resposta = {'textAlign':'left', 'color': '#503D36','font-size': 25}
style_title = {'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
style_regime = {'width': '80%', 'padding':'3px','font-size': '20px','text-align-last':'left'}

# Create a dash application
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server



# Get the layout of the application and adjust it.
app.layout = html.Div(children = [html.H1(title,style=style_title),
                        html.P(esc_evento,style = style_msg),
                        dcc.Dropdown(id='evento',
                                    options=eventos,
                                    placeholder = "Selecione",
                                    style=style_regime),
                        html.Div(id='layout-div')]
                     )



@app.callback(Output('layout-div', 'children'), Input('evento', 'value'))

def ver_evento(evento_sl):

    x = ""
    
    # Evento divorcio
    if ( evento_sl == 1):
        x = html.Div(children = [html.P(esc_reg,style = style_msg),
                dcc.Dropdown(id='regime_casamento',
                options=regimes,placeholder = 'Selecione',
                style=style_regime),
                html.Div(id='divorcio-div')])


    if ( evento_sl == 2):

        x = html.Div(children = [html.Br(),
                html.Label(questoes[0],style=style_msg),
                html.Br(),
                dcc.RadioItems(respostas,respostas[0], style={'padding': 10, 'flex': 1},id='conjuge'),
                html.Label(questoes[3],style=style_msg),
                dcc.RadioItems(respostas,respostas[0], style={'padding': 10, 'flex': 1},id='testamento'),
                html.Label(questoes[1],style=style_msg),
                dcc.Dropdown(id='herdeiro',
                        options=herdeiros,value = 0,
                        style=style_regime),
                html.Br(),
                html.Label(questoes[5],style=style_msg),
                html.Br(),html.Br(),
                dcc.RangeSlider(id='bens-adquiridos-slider',
                                    min= 0,
                                    max = 100,
                                    step = 20,
                                    marks = { 0: '0%', 10: '10%', 20: '20%', 30: '30%',
                                              40: '40%', 50: '50%', 60: '60%', 70: '70%', 80: '80%', 90: '90%', 100:'100%'},
                                    value = [100]
                                ),
                html.Br(), html.Br(),
                html.Label(esc_reg,style=style_msg),
                dcc.Dropdown(id='modalidade',
                        options=regimes,placeholder = esc_reg ,
                        style=style_regime),
                html.Div(id='sucessao-div')])


    return x



# Trata o evento divórcio
@app.callback(Output('divorcio-div', 'children'),Input('regime_casamento','value'), prevent_initial_call=True)

def calc_div(regime_sl):


    if (regime_sl != None):
        x = html.Div([html.P(tit_divorcio,style = style_msg),
                dcc.Markdown(divorcio_respostas[regime_sl][0], style = style_resposta),
                dcc.Markdown(divorcio_respostas[regime_sl][1], style = style_resposta),
                html.Br(), html.Br(),html.Br(),
                html.Label(aviso[0],style=style_msg),
                dcc.Markdown(aviso[1], style = style_resposta),
                dcc.Markdown(aviso[2], style = style_resposta),
                dcc.Markdown(aviso[4], style = style_resposta),
                ])
    else:
                x = html.Div([html.P(" ")])

    return x



def calcula_parte_disponivel(modalidade,adq_casamento=100):
    
# Modalidades
# Comunhão Parcial de Bens - 0
# Comunhão Universal de Bens -  1
# Separação Total de Bens -  2
# Separação Obrigatória de Bens -  3


# Parte disponível é sempre 50% do valor disponível

    meacao_modalidade = [0.50,0.50,0,0]

    meacao = meacao_modalidade[modalidade]
    
    if (modalidade != 0):
    
        parte_disponivel = 0.50 * ( 1 - meacao)

    else:

        parte_disponivel = 0.25 * adq_casamento/100 + 0.50 * (1 - adq_casamento/100)


    r = str(int(parte_disponivel * 100))

    return r , parte_disponivel


def calcula_heranca(modalidade,conjuge,herdeiro,atestado):
    
# Modalidades
# Comunhão Parcial de Bens - 0
# Comunhão Universal de Bens -  1
# Separação Total de Bens -  2
# Separação Obrigatória de Bens -  3
# Legitima é sempre 50% do valor disponível
# Parte disponível é sempre 50% do valor disponível
# Se for testada, a disponível vira legítima


# Na Comunhão Parcial
# - Bens adquiridos na constância do casamento
#     - Há meação dos bens adquiridos na constância do casamento
#     - Legítima de 25% fica para os herdeiros necessários
#     - Disponível não atestada é dividida igualmente entre os herdeiros necessários
# - Bens adquiridos antes do casamento
#     - Não há meação
#     - Legítima e Disponível não atestada são divididas igualmente entre os herdeiros necessários e cônjuge sobrevivente


# Na Comunhão Universal de bens 
# - Há meação
# - Legítima fica para os herdeiros necessários
# - Disponível não atestada é dividida igualmente entre os herdeiros necessários e cônjuge sobrevivente


# Na Separação Total 
# - Não há meação
# - Legítima e Disponível não atestada são divididas igualmente entre os herdeiros necessários e cônjuge sobrevivente

# Na Separação Total 
# - Não há meação
# - Legítima e Disponível não atestada são divididas igualmente entre os herdeiros necessários
# - Conjuge não recebe nada


    meacao_modalidade = [0.50,0.50,0,0]

    meacao = meacao_modalidade[modalidade]
    parte_disponivel = 0.50 * ( 1 - meacao)
    legitima = parte_disponivel
    disponivel_div = (1 - meacao - legitima) * (1 - atestado/100)

    if (conjuge == 'Sim'):

        if (meacao != 0):

            perc_conjuge  = meacao

            if (herdeiro > 0):
            
                perc_herdeiro = (legitima + disponivel_div)/herdeiro
        
            else:

                perc_herdeiro = 0
                perc_conjuge = perc_conjuge + legitima + disponivel_div 
        else:

            if (modalidade == 2):
                if (herdeiro > 0):

                    perc_todos = (legitima + disponivel_div)/(herdeiro + 1)
                    perc_conjuge = perc_todos
                    perc_herdeiro = perc_todos

                else:

                    perc_herdeiro = 0
                    perc_conjuge = legitima + disponivel_div

            else:

                perc_conjuge = 0
                if (herdeiro > 0):

                    perc_herdeiro = (legitima + disponivel_div)/(herdeiro)

                else:

                    perc_herdeiro = 0
                    perc_conjuge = legitima + disponivel_div
    else:

        perc_conjuge = 0

        if (herdeiro > 0):

            perc_herdeiro = (meacao + legitima + disponivel_div)/ herdeiro
        else:
            perc_herdeiro = 0

    
    return perc_conjuge, perc_herdeiro



# Trata o evento sucessão
@app.callback(Output('sucessao-div', 'children'),
                    Input('conjuge','value'),
                    Input('herdeiro','value'),
                    Input('testamento','value'),
                    Input('modalidade','value'), 
                    Input('bens-adquiridos-slider','value')
                    ,prevent_initial_call=True
                    )

def calc_div(conjuge,herdeiro,testamento,regime_sl,slider):
    
    if (conjuge != 'Sim' ) and ( herdeiro == 0):
        a = "* Não há cônjuge sobrevivente."
        b = "* Não há herdeiros necessários."
        x = html.Div([html.P(tit_sucessao,style = style_msg),
                        dcc.Markdown(a, style = style_resposta),
                        dcc.Markdown(b, style = style_resposta),
                        html.Br(), html.Br(),html.Br(),
                        html.Label(aviso[0],style=style_msg),
                        dcc.Markdown(aviso[1], style = style_resposta),
                        dcc.Markdown(aviso[2], style = style_resposta),
                        dcc.Markdown(aviso[4], style = style_resposta)    
                    ])

        return x

    # Se não houve testamento
    if (testamento != 'Sim'):
        # Se rebime não é de separação parcial
        if (regime_sl != 0):

            y = calcula_heranca(regime_sl,conjuge,herdeiro,0)
            a = str(int(y[0]*1000)/10)
            b = str(int(y[1]*1000)/10)

            if (conjuge == 'Sim'):

                a = "* O cônjuge sobrevivente fica com " + a + " % do montante."

                if (herdeiro > 0):

                    b = "* Cada herdeiro fica com " + b + " % do montante."

                else:

                    b = ""
                
            else:

                if (herdeiro > 0):
                    a = "* Não há cônjuge sobrevivente."
                    b = "* Cada herdeiro fica com " + b + " % do montante."

            alerta = "* Podem haver interpretações alternativas da legislação."
            consulta = "* Consulte um advogado especializado para um aconselhamento mais detalhado."
            fonte = "Fonte: Código Civil - Art.1.829"

            # Resposta final para regimes diferente de comunhão parcial e sem inventário
            x = html.Div([html.P(tit_sucessao,style = style_msg),
                        dcc.Markdown(a, style = style_resposta),
                        dcc.Markdown(b, style = style_resposta),
                        html.Br(),html.Br(),html.Br(),
                        html.Label(aviso[0],style=style_msg),
                        dcc.Markdown(aviso[1], style = style_resposta),
                        dcc.Markdown(aviso[2], style = style_resposta),
                        dcc.Markdown(aviso[4], style = style_resposta)
                        ])
            
            return x
    
        # Se é separação parcial
        if (regime_sl == 0):

    
            # No regime da comunhão parcial de bens:
            # - Os bens adquiridos na constância do casamento são tratados como uma comunhão parcial
            # - Os bens adquiridos antes da constância são tratados como um separação total de bens
            y = calcula_heranca(regime_sl,conjuge,herdeiro,0)
            bens_casamento = slider[0]/100
            bens_conjuge = y[0] * bens_casamento
            bens_herdeiro = y[1] * bens_casamento
    
            # - Os bens adquiridos antes da constância são tratados como um separação total de bens
            y = calcula_heranca(2,conjuge,herdeiro,0)
            bens_fora_casamento = 1 - bens_casamento
            bens_conjuge = bens_conjuge + bens_fora_casamento * y[0]
            bens_herdeiro = bens_herdeiro + y[1] * bens_fora_casamento 

            a = str(int(bens_conjuge * 1000)/10)
            b = str(int(bens_herdeiro * 1000)/10)

            if (conjuge == 'Sim'):

                if (herdeiro > 0):

                    a = "* O cônjuge sobrevivente fica com " + a + " % do montante."
                    b = "* Cada herdeiro fica com " + b + " % do montante."

            else:

                a = "* O cônjuge sobrevivente fica com " + a + " % do montante."
                b = ""
                
        else:

            if (herdeiro > 0):
                a = "* Não há cônjuge sobrevivente."
                b = "* Cada herdeiro fica com " + b + " % do montante."
   

        x = html.Div([html.Label(tit_sucessao,style = style_msg),
                        dcc.Markdown(a, style = style_resposta),
                        dcc.Markdown(b, style = style_resposta),
                        html.Br(), html.Br(),html.Br(),
                        html.Label(aviso[0],style=style_msg),
                        dcc.Markdown(aviso[1], style = style_resposta),
                        dcc.Markdown(aviso[2], style = style_resposta),
                        dcc.Markdown(aviso[4], style = style_resposta)
                        ])

        return x




    # Se houve testamento
    if (testamento == 'Sim'):

        m = "A herança disponível é " + calcula_parte_disponivel(regime_sl,slider[0])[0] + " % do montante. Qual percentual do montante que o falecido testou ?"
        
        # Se não é comunhão parcial
        if(regime_sl != 0):

                x = html.Div(children = [html.Br(),
                html.Label(m,style=style_msg),
                html.Br(), html.Br(),
                dcc.RangeSlider(id='heranca-slider',
                                    min= 0,
                                    max = 100,
                                    step = 20,
                                    marks = { 0: '0%', 20: '20%', 
                                              40: '40%', 60: '60%', 80: '80%',100:'100%'},
                                    value = [100]
                                ),html.Br(),
                html.Label(questoes[4],style=style_msg),html.Br(),
                dcc.Dropdown(id='beneficiario',
                        options=beneficiarios,value = 0,
                        style=style_regime),
                html.Div(id='testamento-div')])
                return x

        # Se é separação parcial
        else:

            x = html.Div(children = [html.Br(),
                html.Label(m,style=style_msg),
                html.Br(), html.Br(),
                dcc.RangeSlider(id='heranca-parcial-slider',
                                    min= 0,
                                    max = 100,
                                    step = 20,
                                    marks = { 0: '0%', 20: '20%', 
                                              40: '40%', 60: '60%', 80: '80%',100:'100%'},
                                    value = [100]
                                ),
                html.Br(),
                html.Label(questoes[4],style=style_msg),html.Br(),
                dcc.Dropdown(id='beneficiario_parcial',
                        options=beneficiarios,value = 0,
                        style=style_regime),
                html.Div(id='comunhao-parcial-testamento-div')])
            return x


# Trata o evento sucessão, houve testamento e é comunhão parcial de bens
@app.callback(Output('comunhao-parcial-testamento-div', 'children'),
                    Input('conjuge','value'),
                    Input('herdeiro','value'),
                    Input('heranca-parcial-slider','value'),
                    Input('beneficiario_parcial','value'),
                    Input('bens-adquiridos-slider','value'),
                    Input('modalidade','value'))

def calc_div_parcial(conjuge,herdeiro,slider,beneficiario,slider2,regime_sl):

    print ( ">>>>> Houve testamento e comunhão parcial ")
    
    print ("Regine = ", regime_sl)    
    # No regime da comunhão parcial de bens:
    # - Os bens adquiridos na constância do casamento são tratados como uma comunhão parcial
    # - Os bens adquiridos antes da constância são tratados como um separação total de bens
    y = calcula_heranca(regime_sl,conjuge,herdeiro,slider[0])
    bens_casamento = slider2[0]/100
    bens_conjuge = y[0] * bens_casamento
    bens_herdeiro = y[1] * bens_casamento
    
    print ( "Bens conjuge na constancia do casamento = ", bens_conjuge)

    # - Os bens adquiridos antes da constância são tratados como um separação total de bens
    y = calcula_heranca(2,conjuge,herdeiro,slider[0])
    bens_fora_casamento = 1 - bens_casamento
    perc_conj = bens_conjuge + bens_fora_casamento * y[0]
    perc_herdeiro = bens_herdeiro + y[1] * bens_fora_casamento 

    print ( "Bens conjuge fora do casamento + dentro = ", perc_conj)

    print ( "% bens adquiridos no casamento = ", slider2[0])

    z = calcula_parte_disponivel(regime_sl)[1] * slider[0]/100
        
    
    print (z)

    if (beneficiario == 0 ):

        perc_conj = perc_conj + z

    else:

        if (beneficiario == 1 and herdeiro > 0):

                perc_herdeiro = perc_herdeiro + z/herdeiro

        else:

            if (beneficiario == 2):

                perc_conj = perc_conj + z/(herdeiro + 1)
                perc_herdeiro = perc_herdeiro + z/(herdeiro + 1)


    a = str(int(perc_conj * 10000)/100)
    b = str(int(perc_herdeiro * 10000)/100)

    if (conjuge == 'Sim'):

        if (herdeiro > 0):

            a = "* O cônjuge sobrevivente fica com " + a + " % do montante."
            b = "* Cada herdeiro fica com " + b + " % do montante."

        else:

            a = "* O cônjuge sobrevivente fica com " + a + " % do montante."
            b = ""
                
    else:

        if (herdeiro > 0):
            a = "* Não há cônjuge sobrevivente."
            b = "* Cada herdeiro fica com " + b + " % do montante."

    x = html.Div([html.P(tit_sucessao,style = style_msg),
                        dcc.Markdown(a, style = style_resposta),
                        dcc.Markdown(b, style = style_resposta),
                        html.Br(), html.Br(),html.Br(),
                        html.Label(aviso[0],style=style_msg),
                        dcc.Markdown(aviso[1], style = style_resposta),
                        dcc.Markdown(aviso[2], style = style_resposta),
                        dcc.Markdown(aviso[4], style = style_resposta)    
                    ])
            
    return x


# Trata o evento sucessão, houve testamento e não é comunhão parcial de bens
@app.callback(Output('testamento-div', 'children'),
                    Input('conjuge','value'),
                    Input('herdeiro','value'),
                    Input('heranca-slider','value'),
                    Input('beneficiario','value'),
                    Input('modalidade','value'))

def calc_div(conjuge,herdeiro,slider,beneficiario,regime_sl):
    
        print ( ">>>>> Houve testamento e outros ")
    

        y = calcula_heranca(regime_sl,conjuge,herdeiro,slider[0])

        perc_conj = y[0]
        perc_herdeiro = y[1]

        z = calcula_parte_disponivel(regime_sl)[1] * slider[0]/100
        

        if (beneficiario == 0 ):

            perc_conj = perc_conj + z

        else:

            if (beneficiario == 1 and herdeiro > 0):

                perc_herdeiro = perc_herdeiro + z/herdeiro

            else:

                if (beneficiario == 2):

                    perc_conj = perc_conj + z/(herdeiro + 1)
                    perc_herdeiro = perc_herdeiro + z/(herdeiro + 1)

        
        a = str(int(perc_conj*10000)/100)
        b = str(int(perc_herdeiro*10000)/100)
        
        if (conjuge == 'Sim'):

            a = "* O cônjuge sobrevivente fica com " + a + " % do montante."

            if (herdeiro > 0):

                b = "* Cada herdeiro fica com " + b + " % do montante."

            else:

                b = ""
                
        else:
        
            a = "* Não há cônjuge sobrevivente."
            b = "* Cada herdeiro fica com " + y[1] + " % do montante."

        x = html.Div([html.P(tit_sucessao,style = style_msg),
                        dcc.Markdown(a, style = style_resposta),
                        dcc.Markdown(b, style = style_resposta),
                        html.Br(), html.Br(),html.Br(),
                        html.Label(aviso[0],style=style_msg),
                        dcc.Markdown(aviso[1], style = style_resposta),
                        dcc.Markdown(aviso[2], style = style_resposta),
                        dcc.Markdown(aviso[4], style = style_resposta)
                        ])
            
        return x
    



# Trata o evento sucessão, comunhão parcial de bens sem testamento
@app.callback(Output('comunhao-parcial-div', 'children'),
                    Input('conjuge','value'),
                    Input('herdeiro','value'),
                    Input('bens-adquiridos-slider','value'))

def calc_div(conjuge,herdeiro,slider2):

    print ( ">>>>> comunhao parcial de bens")
    
    # Regime de comunhão parcial de bens
    regime_sl = 0
    
    # No regime da comunhão parcial de bens:
    # - Os bens adquiridos na constância do casamento são tratados como uma comunhão parcial
    # - Os bens adquiridos antes da constância são tratados como um separação total de bens
    y = calcula_heranca(0,conjuge,herdeiro,0)
    bens_casamento = slider2[0]/100
    bens_conjuge = y[0] * bens_casamento
    bens_herdeiro = y[1] * bens_casamento
    
    # - Os bens adquiridos antes da constância são tratados como um separação total de bens
    y = calcula_heranca(2,conjuge,herdeiro,0)
    bens_fora_casamento = 1 - bens_casamento
    bens_conjuge = bens_conjuge + bens_fora_casamento * y[0]
    bens_herdeiro = bens_herdeiro + y[1] * bens_fora_casamento 

    a = str(int(bens_conjuge * 1000)/10)
    b = str(int(bens_herdeiro * 1000)/10)

    if (conjuge == 'Sim'):

        if (herdeiro > 0):

            a = "* O cônjuge sobrevivente fica com " + a + " % do montante."
            b = "* Cada herdeiro fica com " + b + " % do montante."

        else:

            a = "* O cônjuge sobrevivente fica com " + a + " % do montante."
            b = ""
                
    else:

        if (herdeiro > 0):
            a = "* Não há cônjuge sobrevivente."
            b = "* Cada herdeiro fica com " + b + " % do montante."
   

    x = html.Div([html.P(tit_sucessao,style = style_msg),
                        dcc.Markdown(a, style = style_resposta),
                        dcc.Markdown(b, style = style_resposta),
                        html.Br(), html.Br(),html.Br(),
                        html.Label(aviso[0],style=style_msg),
                        dcc.Markdown(aviso[1], style = style_resposta),
                        dcc.Markdown(aviso[2], style = style_resposta),
                        dcc.Markdown(aviso[4], style = style_resposta)
                        ])

    return x


# Run the application                   
if __name__ == '__main__':
    app.run_server(debug=True)
