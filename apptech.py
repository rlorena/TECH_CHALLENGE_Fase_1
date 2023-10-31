#Importações
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
   page_title="Exportações Vinhos",layout="wide",
   initial_sidebar_state="auto")


# Título
st.write('# Exportações brasileiras de vinhos')

tab0, tab1, tab2, tab3 = st.tabs(['###### Tabela','###### Gráficos','###### Conclusão','###### Códigos'])
# Subindo e tratandos os dados
df_vinhos=pd.read_csv('ExpVinho.csv',sep=";")
#df_vinhos.head()

##TRATAMENTOS FEITOS NO NOTEBOOK

##seleção das colunas que serão trabalhadas
df_vinhos_colunas=df_vinhos[
        ['Id','País','2008', '2008.1', '2009', '2009.1', '2010', '2010.1', '2011', '2011.1',
       '2012', '2012.1', '2013', '2013.1', '2014', '2014.1', '2015', '2015.1',
       '2016', '2016.1', '2017', '2017.1', '2018', '2018.1', '2019', '2019.1',
       '2020', '2020.1', '2021', '2021.1', '2022', '2022.1']
       ]
#df_vinhos_colunas.head()


##Transformação da coluna "Id" em índice
#df_vinhos_colunas.reset_index()
df_vinhos_indice=df_vinhos_colunas.set_index('Id')


#tabela separada por quantidade
df_vinhos_qtd=df_vinhos_indice[
        ['País','2008', '2009', '2010', '2011', '2012','2013', '2014', '2015', 
      '2016', '2017', '2018', '2019', '2020', '2021', '2022']
      ]
#df_vinhos_qtd.head()

#tabela separada por valor
df_vinhos_valor=df_vinhos_indice[
        ['País','2008.1','2009.1','2010.1','2011.1','2012.1','2013.1','2014.1','2015.1',
     '2016.1','2017.1','2018.1','2019.1','2020.1','2021.1','2022.1']
     ]                                                                                       
#df_vinhos_valor.head()

##Criando a coluna "Qtd Total"
df_vinhos_qtd ['Qtd Total']=df_vinhos_qtd ['2008']+df_vinhos_qtd ['2009']\
+df_vinhos_qtd ['2010']+df_vinhos_qtd ['2011']+df_vinhos_qtd ['2012']\
+df_vinhos_qtd ['2013']+df_vinhos_qtd ['2014']+df_vinhos_qtd ['2015']\
+df_vinhos_qtd ['2016']+df_vinhos_qtd ['2017']+df_vinhos_qtd ['2018']\
+df_vinhos_qtd ['2019']+df_vinhos_qtd ['2020']+df_vinhos_qtd ['2021']\
+df_vinhos_qtd ['2022']
#df_vinhos_qtd.head()

#Criação da coluna "Total Valor"
#acredito que essa não é a melhor forma de se fazer em um Data Frame grande.
df_vinhos_valor['Total Valor']=df_vinhos_valor['2008.1']+df_vinhos_valor['2009.1']\
+df_vinhos_valor['2010.1']+df_vinhos_valor['2011.1']+df_vinhos_valor['2012.1']\
+df_vinhos_valor['2013.1']+df_vinhos_valor['2014.1']+df_vinhos_valor['2015.1']\
+df_vinhos_valor['2016.1']+df_vinhos_valor['2017.1']+df_vinhos_valor['2018.1']\
+df_vinhos_valor['2019.1']+df_vinhos_valor['2020.1']+df_vinhos_valor['2021.1']\
+df_vinhos_valor['2022.1']
#df_vinhos_valor.head()

#Excluindo linhas com Qtd Total ==0
df_vinhos_qtd.drop(df_vinhos_qtd.loc[df_vinhos_qtd['Qtd Total']==0].index, inplace=True)
#ordenando valores
df_vinhos_qtd=df_vinhos_qtd.sort_values(by='Qtd Total', ascending=False)
#df_vinhos_qtd.head(10)

#Excluindo linhas com Total Valor ==0
df_vinhos_valor.drop(df_vinhos_valor.loc[df_vinhos_valor['Total Valor']==0].index, inplace=True)
#ordenando valores
df_vinhos_valor=df_vinhos_valor.sort_values(by='Total Valor', ascending=False)
#df_vinhos_valor.head(10)

#unificação dos data frames com 'merge'.
df_vinhos_unificado=pd.merge(df_vinhos_qtd, df_vinhos_valor, on='País', how='left')
#df_vinhos_unificado.head()

df_vinhos_totais=df_vinhos_unificado[['País','Qtd Total', 'Total Valor']]
#df_vinhos_totais.head()

#Ciação da coluna 'País de Origem'
df_vinhos_totais['País de origem']=df_vinhos_totais.index
#df_vinhos_totais.head()      

#Substituindo os nomes dos país na coluna "País de origem" por 'Brasil'
df_vinhos_totais =df_vinhos_totais [['País de origem','País','Qtd Total','Total Valor']]
df_vinhos_totais ['País de origem']=df_vinhos_totais ['País de origem'].apply(lambda x: 'Brasil' if x=='sim'else 'Brasil')
#df_vinhos_totais.head()

#Renomeando as colunas e ordenando
df_vinhos_totais.rename(columns={'País': 'País de destino'}, inplace=True)
df_vinhos_totais.rename(columns={'Qtd Total': 'Qtd Total (L)'}, inplace=True)
df_vinhos_totais.rename(columns={'Total Valor': 'Valor Total (US$)'}, inplace=True)
df_vinhos_totais=df_vinhos_totais.sort_values(by='Valor Total (US$)', ascending=False)
#df_vinhos_totais

#Manipulação para fazer o gráfico de linha
df_grafico_linhas_valor=df_vinhos_valor.set_index('País')
df_grafico_linhas_valor=df_grafico_linhas_valor.drop('Total Valor', axis=1)
#df_grafico_linhas_valor.head()

#Alterando o nome das colunas para que o eixo x seja representado de forma correta.
df_grafico_linhas_valor.rename(columns={'2008.1': '2008'}, inplace=True)
df_grafico_linhas_valor.rename(columns={'2009.1': '2009'}, inplace=True)
df_grafico_linhas_valor.rename(columns={'2010.1': '2010'}, inplace=True)
df_grafico_linhas_valor.rename(columns={'2011.1': '2011'}, inplace=True)
df_grafico_linhas_valor.rename(columns={'2012.1': '2012'}, inplace=True)
df_grafico_linhas_valor.rename(columns={'2013.1': '2013'}, inplace=True)
df_grafico_linhas_valor.rename(columns={'2014.1': '2014'}, inplace=True)
df_grafico_linhas_valor.rename(columns={'2015.1': '2015'}, inplace=True)
df_grafico_linhas_valor.rename(columns={'2016.1': '2016'}, inplace=True)
df_grafico_linhas_valor.rename(columns={'2017.1': '2017'}, inplace=True)
df_grafico_linhas_valor.rename(columns={'2018.1': '2018'}, inplace=True)
df_grafico_linhas_valor.rename(columns={'2019.1': '2019'}, inplace=True)
df_grafico_linhas_valor.rename(columns={'2020.1': '2020'}, inplace=True)
df_grafico_linhas_valor.rename(columns={'2021.1': '2021'}, inplace=True)
df_grafico_linhas_valor.rename(columns={'2022.1': '2022'}, inplace=True)
#df_grafico_linhas_valor


#Manipulação para fazer os gráficos
df_valor=df_grafico_linhas_valor.head()
df_valor=df_valor.T
#df_valor.head()

#Manipulação para fazer o gráfico de linha
df_grafico_linhas_qtd=df_vinhos_qtd.set_index('País')
df_grafico_linhas_qtd=df_grafico_linhas_qtd.drop('Qtd Total', axis=1)
#df_grafico_linhas_qtd.head()

#Manipulação para fazer os gráficos
df_quantidade=df_grafico_linhas_qtd.head()
df_quantidade=df_quantidade.T
#df_quantidade.head()

#Tratando os dados para montar o gráfico de linhas com as quantidades e valores no período
df_qtd_total_ano=df_grafico_linhas_qtd.sum()
df_qtd_total_ano=pd.DataFrame(df_qtd_total_ano)
df_qtd_total_ano.head()
df1=df_qtd_total_ano.reset_index()
df1.index.rename('novo', inplace=True)
#df1.head()

#Tratando os dados para montar o gráfico de linhas com as quantidades e valores no período
df_valor_total_ano=df_grafico_linhas_valor.sum()
df_valor_total_ano=pd.DataFrame(df_valor_total_ano)
df_valor_total_ano.head()
df2=df_valor_total_ano.reset_index()
df2.index.rename('novo', inplace=True)
#df2.head()

#Tratando os dados para montar o gráfico de linhas com as quantidades e valores no período
df3=pd.merge(df1,df2, on='novo', how='left')
df3=df3.drop('index_y', axis=1)
#df3.head()

#Tratando os dados para montar o gráfico de linhas com as quantidades e valores no período
df3.rename(columns={'index_x':'Ano'}, inplace=True)
df3.rename(columns={'0_x':'Quantidade'}, inplace=True)
df3.rename(columns={'0_y':'Valor'}, inplace=True)
df3=df3
df3=df3.set_index('Ano')
#df3.head()


#######################################################################

##TAB2 CONCLUSÃO 

with tab2:
        
                    
        st.subheader('Considerações finais')
        st.write('#### Segundo a ApexBrasil, o Brasil é um grande produtor de vinhos, mas exporta pouco, porém o cenário vem demonstrando aumento a cada ano nos volumes exportados.')
        st.write('#### Fato que pode ajudar a explicar esse crescimento é o projeto “Wines of Brasil”, criado e mantido pela União Brasileira de Vinicultura (Uvibra) e Apex Brasil com objetivo de promover os vinhos brasileiros no mercado internacional, através de ações especiais de promoção comercial.')
        st.write('#### Vale considerarmos que apesar do crescimento apresentado, fatores externos podem influenciar no resultado futuro, como:')
        st.write('#### • Guerra na Rússia')
        st.write('#### • Guerra em Israel') 
        st.write('#### O conflito no Leste Europeu, por exemplo, segundo reportagem do Jornal Nacional da rede Globo("Guerra na Ucrânia afeta as exportações brasileiras | Jornal Nacional | G1 (globo.com)") desde seu início já vem afetando as exportações brasileiras devido a grandes transportadores marítimos terem suspendido as rotas para a Rússia, país que é nosso segundo maior importados de vinhos.')
        st.write('#### Já no Oriente médio, caso o conflito se espalhe a tendência é de alta no preço do barril de petróleo, que por consequência vai elevar ainda mais o custo de transporte e produção.')
        st.write('#### Todos esses fatores devem ser considerados, precisamos ter ciência da possibilidade de redução da margem de lucro ou até mesmo a inviabilidade comercial da exportação para determinadas regiões do globo em caso de agravamento dessa crise e na confirmação das condições adversas apresentadas.')
        st.write('####  Apesar das considerações e dos pontos de atenção levantados, recomendamos o investimentos nas exportações de vinhos, tendo um vista que, o atual cenário ainda é favorável e o histórico demonstra crescimento contínuo no comércio de vinhos brasileiro.')
        st.write(
                'Nota. foi constatado que o Brasil aparece na base de exportação de vinhos, não ficando claro o motivo de aparecer em sua própria lista, \
                        já que não é possível exportar para si mesmo, no entanto esses valores foram considerados, mas não representam volume significativo capaz\
                        alterar ou prejudicar a análise.'
                         )

#######################################################################

##TAB1 GRÁFICOS

with tab1:    
       
#Gráfico de barras demonstrando a quantidade e o valor exportado do período
        fig = px.bar(df3, x=df3.index, y=df3.columns, barmode="group",template='plotly_white')
        fig.update_layout(title='Quantidade e valor total exportado.(2008 a 2022)', width = 1200)
        fig.update_xaxes(title_text="Ano")
        fig.update_yaxes(title_text="Valor")
        fig.show()
        st.plotly_chart(fig)

        st.write(
                '###### Nos primeiros anos desta série temporal percebemos que o valor agregado do produto "vinho" era reduzido,\
                        passando a partir de 2010 ter maior agregação de valor, que pode ser comprovado através do crescimento da barra\
                        laranja(valor) em relação a barra azul(quantidade).'
                        ) 
        st.divider()
        
with tab1:
        col1, col2=st.columns(2)

        with col1:

#Gráfico de linha Valor 5 maiores
                fig =px.line(df_valor,  x=df_valor.index, y=df_valor.columns,markers=True,template='plotly_white',
                title='Totais em US$ de vinhos exportados aos 5 maiores importadores.',width = 700)
                fig.update_xaxes(title='Ano')
                fig.update_yaxes(title='Valor (US$)')
                fig.show()
                st.plotly_chart(fig)

                st.write(
                        '###### Entre os 5 maiores importadores podemos destacar Rússia e Paraguai, este primeiro apresentou\
                            números expressivos nos anos de 2009 e 2013, mas retraindo consideravelmente em 2014, passando de 14M para 61K (em US$),\
                            já o Paraguai vem aumentando seu volume de importações desde 2012 praticamente.'
                            )                            
                st.divider()

        with col2:

#Gráfico de linhas demonstrando a quantidade e o valor exportado do período
                fig =px.line(df3, x=df3.index ,y=df3.columns,markers=True,template='plotly_white',
                title='Exportações brasileiras por período.',width = 700)
                fig.update_xaxes(title='Ano')
                fig.update_yaxes(title='Valor (US$)')
                fig.show()
                st.plotly_chart(fig)

                st.write(
                        '###### Identificamos possível tendência de afastamento das linhas que representam a quantidade e valor, sendo que o valor\
                        das exportações tendem a continuar o movimento de alta, acompanhando o histórico do período, vale ressaltar que,\
                            o histórico passado não significa garantia de desempenho futuro. '
                            ) 
                st.divider()

with tab1:

#Gráfico de scatter
        fig=px.scatter(df_vinhos_totais,  x='Qtd Total (L)', y='Valor Total (US$)', 
                log_x=True, log_y=True,width = 1200, opacity=0.8, template='plotly_white')
        fig.update_traces(marker = dict(size = 10, line=dict(width = 1)), selector = dict(mode = 'markers'))
        fig.update_layout(title='Dispersão das exportações no período.')
        fig.update_xaxes(title='Quantidade(L)')
        fig.update_yaxes(title='Valor (US$)')
        fig.show()
        st.plotly_chart(fig)

        st.markdown('###### Distribuição das exportações no período, demonstra maior concentração entre 10 e 260 mil US$. ') 

############################################################

#TAB0 TABELA 

with tab0:
        col1, col2=st.columns(2)
        with col1:
#Formatação da coluna "Valor Total (US$)"

                df_vinhos_exportados=df_vinhos_totais

                st.subheader('Tabelas das exportações brasileiras (2008-2022)', divider='rainbow' )
                st.dataframe(df_vinhos_exportados, width=900, height=600)
                

        with col2:
                #Não consegui configurar de forma satisfatória o texto com o Streamlit, então neste caso usei o word e plotei a imagem. 
                st.image('Números_Totais.png')


#######################################################################

##TAB3 CÓDIGOS (INCLUSÃO CO CÓDIGO NO STREAMLIT)

with tab3:
        st.subheader('Códigos utilizados neste app')
        codigo_python ="""
                        #Importações
                        import pandas as pd
                        import plotly.express as px
                        import streamlit as st

                        st.set_page_config(
                        page_title="Exportações Vinhos",layout="wide",
                        initial_sidebar_state="auto")


                        # Título
                        st.write('# Exportações brasileiras de vinhos')

                        tab0, tab1, tab2, tab3 = st.tabs(['###### Tabela','###### Gráficos','###### Conclusão','###### Códigos'])
                        # Subindo e tratandos os dados
                        df_vinhos=pd.read_csv('ExpVinho.csv',sep=";")
                        #df_vinhos.head()

                        ##TRATAMENTOS FEITOS NO NOTEBOOK

                        ##seleção das colunas que serão trabalhadas
                        df_vinhos_colunas=df_vinhos[
                                ['Id','País','2008', '2008.1', '2009', '2009.1', '2010', '2010.1', '2011', '2011.1',
                        '2012', '2012.1', '2013', '2013.1', '2014', '2014.1', '2015', '2015.1',
                        '2016', '2016.1', '2017', '2017.1', '2018', '2018.1', '2019', '2019.1',
                        '2020', '2020.1', '2021', '2021.1', '2022', '2022.1']
                        ]
                        #df_vinhos_colunas.head()


                        ##Transformação da coluna "Id" em índice
                        #df_vinhos_colunas.reset_index()
                        df_vinhos_indice=df_vinhos_colunas.set_index('Id')


                        #tabela separada por quantidade
                        df_vinhos_qtd=df_vinhos_indice[
                                ['País','2008', '2009', '2010', '2011', '2012','2013', '2014', '2015', 
                        '2016', '2017', '2018', '2019', '2020', '2021', '2022']
                        ]
                        #df_vinhos_qtd.head()

                        #tabela separada por valor
                        df_vinhos_valor=df_vinhos_indice[
                                ['País','2008.1','2009.1','2010.1','2011.1','2012.1','2013.1','2014.1','2015.1',
                        '2016.1','2017.1','2018.1','2019.1','2020.1','2021.1','2022.1']
                        ]                                                                                       
                        #df_vinhos_valor.head()

                        ##Criando a coluna "Qtd Total"
                        df_vinhos_qtd ['Qtd Total']=df_vinhos_qtd ['2008']+df_vinhos_qtd ['2009']\
                        +df_vinhos_qtd ['2010']+df_vinhos_qtd ['2011']+df_vinhos_qtd ['2012']\
                        +df_vinhos_qtd ['2013']+df_vinhos_qtd ['2014']+df_vinhos_qtd ['2015']\
                        +df_vinhos_qtd ['2016']+df_vinhos_qtd ['2017']+df_vinhos_qtd ['2018']\
                        +df_vinhos_qtd ['2019']+df_vinhos_qtd ['2020']+df_vinhos_qtd ['2021']\
                        +df_vinhos_qtd ['2022']
                        #df_vinhos_qtd.head()

                        #Criação da coluna "Total Valor"
                        #acredito que essa não é a melhor forma de se fazer em um Data Frame grande.
                        df_vinhos_valor['Total Valor']=df_vinhos_valor['2008.1']+df_vinhos_valor['2009.1']\
                        +df_vinhos_valor['2010.1']+df_vinhos_valor['2011.1']+df_vinhos_valor['2012.1']\
                        +df_vinhos_valor['2013.1']+df_vinhos_valor['2014.1']+df_vinhos_valor['2015.1']\
                        +df_vinhos_valor['2016.1']+df_vinhos_valor['2017.1']+df_vinhos_valor['2018.1']\
                        +df_vinhos_valor['2019.1']+df_vinhos_valor['2020.1']+df_vinhos_valor['2021.1']\
                        +df_vinhos_valor['2022.1']
                        #df_vinhos_valor.head()

                        #Excluindo linhas com Qtd Total ==0
                        df_vinhos_qtd.drop(df_vinhos_qtd.loc[df_vinhos_qtd['Qtd Total']==0].index, inplace=True)
                        #ordenando valores
                        df_vinhos_qtd=df_vinhos_qtd.sort_values(by='Qtd Total', ascending=False)
                        #df_vinhos_qtd.head(10)

                        #Excluindo linhas com Total Valor ==0
                        df_vinhos_valor.drop(df_vinhos_valor.loc[df_vinhos_valor['Total Valor']==0].index, inplace=True)
                        #ordenando valores
                        df_vinhos_valor=df_vinhos_valor.sort_values(by='Total Valor', ascending=False)
                        #df_vinhos_valor.head(10)

                        #unificação dos data frames com 'merge'.
                        df_vinhos_unificado=pd.merge(df_vinhos_qtd, df_vinhos_valor, on='País', how='left')
                        #df_vinhos_unificado.head()

                        df_vinhos_totais=df_vinhos_unificado[['País','Qtd Total', 'Total Valor']]
                        #df_vinhos_totais.head()

                        #Ciação da coluna 'País de Origem'
                        df_vinhos_totais['País de origem']=df_vinhos_totais.index
                        #df_vinhos_totais.head()      

                        #Substituindo os nomes dos país na coluna "País de origem" por 'Brasil'
                        df_vinhos_totais =df_vinhos_totais [['País de origem','País','Qtd Total','Total Valor']]
                        df_vinhos_totais ['País de origem']=df_vinhos_totais ['País de origem'].apply(lambda x: 'Brasil' if x=='sim'else 'Brasil')
                        #df_vinhos_totais.head()

                        #Renomeando as colunas e ordenando
                        df_vinhos_totais.rename(columns={'País': 'País de destino'}, inplace=True)
                        df_vinhos_totais.rename(columns={'Qtd Total': 'Qtd Total (L)'}, inplace=True)
                        df_vinhos_totais.rename(columns={'Total Valor': 'Valor Total (US$)'}, inplace=True)
                        df_vinhos_totais=df_vinhos_totais.sort_values(by='Valor Total (US$)', ascending=False)
                        #df_vinhos_totais

                        #Manipulação para fazer o gráfico de linha
                        df_grafico_linhas_valor=df_vinhos_valor.set_index('País')
                        df_grafico_linhas_valor=df_grafico_linhas_valor.drop('Total Valor', axis=1)
                        #df_grafico_linhas_valor.head()

                        #Alterando o nome das colunas para que o eixo x seja representado de forma correta.
                        df_grafico_linhas_valor.rename(columns={'2008.1': '2008'}, inplace=True)
                        df_grafico_linhas_valor.rename(columns={'2009.1': '2009'}, inplace=True)
                        df_grafico_linhas_valor.rename(columns={'2010.1': '2010'}, inplace=True)
                        df_grafico_linhas_valor.rename(columns={'2011.1': '2011'}, inplace=True)
                        df_grafico_linhas_valor.rename(columns={'2012.1': '2012'}, inplace=True)
                        df_grafico_linhas_valor.rename(columns={'2013.1': '2013'}, inplace=True)
                        df_grafico_linhas_valor.rename(columns={'2014.1': '2014'}, inplace=True)
                        df_grafico_linhas_valor.rename(columns={'2015.1': '2015'}, inplace=True)
                        df_grafico_linhas_valor.rename(columns={'2016.1': '2016'}, inplace=True)
                        df_grafico_linhas_valor.rename(columns={'2017.1': '2017'}, inplace=True)
                        df_grafico_linhas_valor.rename(columns={'2018.1': '2018'}, inplace=True)
                        df_grafico_linhas_valor.rename(columns={'2019.1': '2019'}, inplace=True)
                        df_grafico_linhas_valor.rename(columns={'2020.1': '2020'}, inplace=True)
                        df_grafico_linhas_valor.rename(columns={'2021.1': '2021'}, inplace=True)
                        df_grafico_linhas_valor.rename(columns={'2022.1': '2022'}, inplace=True)
                        #df_grafico_linhas_valor


                        #Manipulação para fazer os gráficos
                        df_valor=df_grafico_linhas_valor.head()
                        df_valor=df_valor.T
                        #df_valor.head()

                        #Manipulação para fazer o gráfico de linha
                        df_grafico_linhas_qtd=df_vinhos_qtd.set_index('País')
                        df_grafico_linhas_qtd=df_grafico_linhas_qtd.drop('Qtd Total', axis=1)
                        #df_grafico_linhas_qtd.head()

                        #Manipulação para fazer os gráficos
                        df_quantidade=df_grafico_linhas_qtd.head()
                        df_quantidade=df_quantidade.T
                        #df_quantidade.head()

                        #Tratando os dados para montar o gráfico de linhas com as quantidades e valores no período
                        df_qtd_total_ano=df_grafico_linhas_qtd.sum()
                        df_qtd_total_ano=pd.DataFrame(df_qtd_total_ano)
                        df_qtd_total_ano.head()
                        df1=df_qtd_total_ano.reset_index()
                        df1.index.rename('novo', inplace=True)
                        #df1.head()

                        #Tratando os dados para montar o gráfico de linhas com as quantidades e valores no período
                        df_valor_total_ano=df_grafico_linhas_valor.sum()
                        df_valor_total_ano=pd.DataFrame(df_valor_total_ano)
                        df_valor_total_ano.head()
                        df2=df_valor_total_ano.reset_index()
                        df2.index.rename('novo', inplace=True)
                        #df2.head()

                        #Tratando os dados para montar o gráfico de linhas com as quantidades e valores no período
                        df3=pd.merge(df1,df2, on='novo', how='left')
                        df3=df3.drop('index_y', axis=1)
                        #df3.head()

                        #Tratando os dados para montar o gráfico de linhas com as quantidades e valores no período
                        df3.rename(columns={'index_x':'Ano'}, inplace=True)
                        df3.rename(columns={'0_x':'Quantidade'}, inplace=True)
                        df3.rename(columns={'0_y':'Valor'}, inplace=True)
                        df3=df3
                        df3=df3.set_index('Ano')
                        #df3.head()


                        #######################################################################

                        ##TAB2 CONCLUSÃO 

                        with tab2:
                                
                                        
                                st.subheader('Considerações finais')
                                st.write('#### Segundo a ApexBrasil, o Brasil é um grande produtor de vinhos, mas exporta pouco, porém o cenário vem demonstrando aumento a cada ano nos volumes exportados.')
                                st.write('#### Fato que pode ajudar a explicar esse crescimento é o projeto “Wines of Brasil”, criado e mantido pela União Brasileira de Vinicultura (Uvibra) e Apex Brasil com objetivo de promover os vinhos brasileiros no mercado internacional, através de ações especiais de promoção comercial.')
                                st.write('#### Vale considerarmos que apesar do crescimento apresentado, fatores externos podem influenciar no resultado futuro, como:')
                                st.write('#### • Guerra na Rússia')
                                st.write('#### • Guerra em Israel') 
                                st.write('#### O conflito no Leste Europeu, por exemplo, segundo reportagem do Jornal Nacional da rede Globo("Guerra na Ucrânia afeta as exportações brasileiras | Jornal Nacional | G1 (globo.com)") desde seu início já vem afetando as exportações brasileiras devido a grandes transportadores marítimos terem suspendido as rotas para a Rússia, país que é nosso segundo maior importados de vinhos.')
                                st.write('#### Já no Oriente médio, caso o conflito se espalhe a tendência é de alta no preço do barril de petróleo, que por consequência vai elevar ainda mais o custo de transporte e produção.')
                                st.write('#### Todos esses fatores devem ser considerados, precisamos ter ciência da possibilidade de redução da margem de lucro ou até mesmo a inviabilidade comercial da exportação para determinadas regiões do globo em caso de agravamento dessa crise e na confirmação das condições adversas apresentadas.')
                                st.write('####  Apesar das considerações e dos pontos de atenção levantados, recomendamos o investimentos nas exportações de vinhos, tendo um vista que, o atual cenário ainda é favorável e o histórico demonstra crescimento contínuo no comércio de vinhos brasileiro.')
                                st.write(
                                        'Nota. foi constatado que o Brasil aparece na base de exportação de vinhos, não ficando claro o motivo de aparecer em sua própria lista, \
                                                já que não é possível exportar para si mesmo, no entanto esses valores foram considerados, mas não representam volume significativo capaz\
                                                alterar ou prejudicar a análise.'
                                                )

                        #######################################################################

                        ##TAB1 GRÁFICOS

                        with tab1:    
                        
                        #Gráfico de barras demonstrando a quantidade e o valor exportado do período
                                fig = px.bar(df3, x=df3.index, y=df3.columns, barmode="group",template='plotly_white')
                                fig.update_layout(title='Quantidade e valor total exportado.(2008 a 2022)', width = 1600)
                                fig.update_xaxes(title_text="Ano")
                                fig.update_yaxes(title_text="Valor")
                                fig.show()
                                st.plotly_chart(fig)

                                st.write(
                                        '###### Nos primeiros anos desta série temporal percebemos que o valor agregado do produto "vinho" era reduzido,\
                                                passando a partir de 2010 ter maior agregação de valor, que pode ser comprovado através do crescimento da barra\
                                                laranja(valor) em relação a barra azul(quantidade).'
                                                ) 
                                st.divider()
                                
                        with tab1:
                                col1, col2=st.columns(2)

                                with col1:

                        #Gráfico de linha Valor 5 maiores
                                        fig =px.line(df_valor,  x=df_valor.index, y=df_valor.columns,markers=True,template='plotly_white',
                                        title='Totais em US$ de vinhos exportados aos 5 maiores importadores.',width = 800)
                                        fig.update_xaxes(title='Ano')
                                        fig.update_yaxes(title='Valor (US$)')
                                        fig.show()
                                        st.plotly_chart(fig)

                                        st.write(
                                                '###### Entre os 5 maiores importadores podemos destacar Rússia e Paraguai, este primeiro apresentou\
                                                números expressivos nos anos de 2009 e 2013, mas retraindo consideravelmente em 2014, passando de 14M para 61K (em US$),\
                                                já o Paraguai vem aumentando seu volume de importações desde 2012 praticamente.'
                                                )                            
                                        st.divider()

                                with col2:

                        #Gráfico de linhas demonstrando a quantidade e o valor exportado do período
                                        fig =px.line(df3, x=df3.index ,y=df3.columns,markers=True,template='plotly_white',
                                        title='Exportações brasileiras por período.',width = 800)
                                        fig.update_xaxes(title='Ano')
                                        fig.update_yaxes(title='Valor (US$)')
                                        fig.show()
                                        st.plotly_chart(fig)

                                        st.write(
                                                '###### Identificamos possível tendência de afastamento das linhas que representam a quantidade e valor, sendo que o valor\
                                                das exportações tendem a continuar o movimento de alta, acompanhando o histórico do período, vale ressaltar que,\
                                                o histórico passado não significa garantia de desempenho futuro. '
                                                ) 
                                        st.divider()

                        with tab1:

                        #Gráfico de scatter
                                fig=px.scatter(df_vinhos_totais,  x='Qtd Total (L)', y='Valor Total (US$)', 
                                        log_x=True, log_y=True,width = 1600, opacity=0.8, template='plotly_white')
                                fig.update_traces(marker = dict(size = 10, line=dict(width = 1)), selector = dict(mode = 'markers'))
                                fig.update_layout(title='Dispersão das exportações no período.')
                                fig.update_xaxes(title='Quantidade(L)')
                                fig.update_yaxes(title='Valor (US$)')
                                fig.show()
                                st.plotly_chart(fig)

                                st.markdown('###### Distribuição das exportações no período, demonstra maior concentração entre 10 e 260 mil US$. ') 

                        ############################################################

                        #TAB0 TABELA 

                        with tab0:
                                col1, col2=st.columns(2)
                                with col1:
                        #Formatação da coluna "Valor Total (US$)"

                                        df_vinhos_exportados=df_vinhos_totais

                                        st.subheader('Tabelas das exportações brasileiras (2008-2022)', divider='rainbow' )
                                        st.dataframe(df_vinhos_exportados, width=900, height=600)
                                        

                                with col2:
                                        #Não consegui configurar de forma satisfatória o texto com o Streamlit, então neste caso usei o word e plotei a imagem. 
                                        st.image('Números_Totais.png')
                        """
        st.code(codigo_python, language='python')
