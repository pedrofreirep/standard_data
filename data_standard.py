import streamlit as st
import numpy as np
import pandas as pd
import openpyxl
from openpyxl import Workbook
from io import BytesIO
# import xlrd


st.title('🗂️ Transformando diferentes bases em um mesmo padrão de dados')
st.caption('Feito com 🧠 por [Blue AI](https://blueai.com.br/)')
st.info('Este app transforma diferentes bases salvas em CSV ou Excel em um mesmo padrão de dados. **Os arquivos aqui carregados não são salvos, copiados ou armezados pela Blue AI** em nenhum momento. Esta aplicação é gratuita, **você pode usar quando e o quanto quiser**. O código desta aplicação em breve estará aberto e será público.')

st.markdown('\n\n')
st.write('#### 1) Comece escolhendo o seu arquivo, CSV ou Excel, para ser transformado')
col1, col2 = st.columns([1.5, 2.5])

with col1:
    file_type = st.radio(
        "1.1) Selecione o tipo de arquivo: 👉",
        options=["CSV (.csv)", "Excel (.xlsx)", "Excel (.xls)"],
    )

with col2:
    if file_type == "CSV (.csv)":
        input_dataframe = st.file_uploader(label = "1.2) Carregue o seu arquivo aqui: 👇", type = 'csv')
    elif file_type == "Excel (.xlsx)":
        input_dataframe = st.file_uploader(label = "1.2) Carregue o seu arquivo aqui: 👇", type = 'xlsx')
    elif file_type == "Excel (.xls)":
        input_dataframe = st.file_uploader(label = "1.2) Carregue o seu arquivo aqui: 👇", type = 'xls')
    else:
        pass

if file_type == "CSV (.csv)":
    if input_dataframe:
        file_details = {
            "Filename":input_dataframe.name,
            "FileType":input_dataframe.type,
            "FileSize":input_dataframe.size}

        # wb = openpyxl.load_workbook(input_dataframe)

        ## Select sheet
        # sheet_selector = st.selectbox("Select sheet:",wb.sheetnames)
        header_line = st.number_input('1.3) Selecione em qual linha está os nomes das colunas da sua base:', step=1)
        new_df = pd.read_csv(input_dataframe, header=header_line)
        st.markdown('\n')
        st.markdown("----")
        st.caption(":blue[1.4) Confira a base selecionada:")
        st.write(new_df)
        st.markdown("----")
else:
    if input_dataframe:
        file_details = {
            "Filename":input_dataframe.name,
            "FileType":input_dataframe.type,
            "FileSize":input_dataframe.size}

        wb = openpyxl.load_workbook(input_dataframe)

        ## Show Excel file
        # st.subheader("File details:")
        # st.json(file_details,expanded=False)
        # st.markdown("----")

        ## Select sheet
        sheet_selector = st.selectbox("1.3) Seleciona a aba do seu arquivo:",wb.sheetnames)
        header_line = st.number_input('1.4) Selecione em qual linha está os nomes das colunas da sua base:', step=1)
        new_df = pd.read_excel(input_dataframe, sheet_selector, header=header_line)
        st.caption(f":blue[1.5) Confira a base seleciona na aba `{sheet_selector}`:]")
        st.write(new_df)
        st.markdown("----")

if input_dataframe:
    st.markdown('\n\n')
    st.write('#### 2) Para cada coluna desejada selecione o formato padrão que melhor a representa')
    df_payment = new_df
    df_claims = new_df
    df_advanced = new_df
    Payment_Tab, Claims_Tab, Advanced_Tab = st.tabs(["Template de faturamento", "Template de sinistralidade", "Configuração avançada"])

    with Payment_Tab:
        st.markdown('O template de padronização de bases de faturamento organiza informações mínimas necessárias, e comuns entre arquivos de diferentes operadoras, para registro de mensalidades por beneficiário. Identifique na sua base as colunas que representam cada informação abaixo:')
        header_list = df_payment.columns
        options_list = ['Nome do beneficiário', 'Código do beneficiário', 'Idade do beneficiário', 'Data de inclusão no plano', 'Data de exclusão no plano', 'Código de matrícula', 'Categoria do plano de saúde', 'Co-participação', 'Valor da mensalidade', 'Valor total da família do beneficiário', 'Titular ou dependente', 'Tipo de dependência']
        # selected_options = []
        for i in range(len(options_list)):
            try:
                option = st.selectbox(
                f"Qual formato melhor define a coluna **`{options_list[i]}`**?",
                (header_list), key=f"payment_option_`{[i]}`")

                df_payment = df_payment.rename(columns={option:options_list[i]})
                with st.expander("Clique para visualizar:"):
                    new_df = df_payment
                    new_df
                    # selected_options.append(options_list[i])
                    selected_options = options_list
            except ValueError:
                st.error('A coluna selecionada já foi usada, tente uma opção diferente.', icon="🤖")
            # option = st.selectbox(
            # f"Qual formato melhor define a coluna **`{header_selected[i]}`**?",
            # (options_list))

            # new_df = new_df.rename(columns={header_selected[i]:option})
            # new_df
            # header_list = options_list.remove(option)
        
        if st.button('Padronizar', key="payment_standard"):
            try:
                st.markdown("----")
                st.markdown('\n\n')
                st.write('#### 3) Confira o resultado e baixe a sua base padronizada')
                # st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                # st.radio()

                # col3, col4 = st.columns([2, 2])

                # with col3:
                #     standard_only = st.checkbox('Somente colunas padronizadas')
                # with col4:
                #     entire_df = st.checkbox('Todas as colunas')

                # if standard_only:
                st.markdown('\n')
                new_df = new_df[selected_options]
                st.write(new_df)
                # if entire_df:
                #     st.markdown('\n')
                #     st.write(new_df)
                
                def to_excel(df):
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    new_df.to_excel(writer, index=False, sheet_name='Sheet1')
                    workbook = writer.book
                    worksheet = writer.sheets['Sheet1']
                    format1 = workbook.add_format({'num_format': '0.00'}) 
                    worksheet.set_column('A:A', None, format1)  
                    writer.save()
                    processed_data = output.getvalue()
                    return processed_data

                df_xlsx = to_excel(new_df)
                st.markdown('\n\n')
                st.download_button(label='📥 Baixar Planilha',
                                                data=df_xlsx ,
                                                file_name= 'base_faturamento_padronizada.xlsx')
            except ValueError:
                pass


    with Claims_Tab:
        st.markdown('O template de padronização de bases de sinistros organiza informações mínimas necessárias, e comuns entre arquivos de diferentes operadoras, para registro de procedimentos realizados pelo plano de saúde de cada beneficiário. Identifique na sua base as colunas que representam cada informação abaixo:')
        header_list = df_claims.columns
        options_list = ['Código do beneficiário', 'Sexo do beneficiário', 'Data de nascimento do beneficiário', 'Código tuss do procedimento', 'Valor pago pelo procedimento', 'Data de realização do procedimento', 'Data de pagamento do procedimento', 'Código do prestador de saúde']
        # selected_options = []
        for i in range(len(options_list)):
            try:
                option = st.selectbox(
                f"Qual formato melhor define a coluna **`{options_list[i]}`**?",
                (header_list), key=f"claims_option_`{[i]}`")

                df_claims = df_claims.rename(columns={option:options_list[i]})
                with st.expander("Clique para visualizar:"):
                    new_df = df_claims
                    new_df
                    # selected_options.append(options_list[i])
                    selected_options = options_list
            except ValueError:
                st.error('A coluna selecionada já foi usada, tente uma opção diferente.', icon="🤖")
            # option = st.selectbox(
            # f"Qual formato melhor define a coluna **`{header_selected[i]}`**?",
            # (options_list))

            # new_df = new_df.rename(columns={header_selected[i]:option})
            # new_df
            # header_list = options_list.remove(option)
        
        if st.button('Padronizar', key="claims_standard"):
            try:
                st.markdown("----")
                st.markdown('\n\n')
                st.write('#### 3) Confira o resultado e baixe a sua base padronizada')
                # st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                # st.radio()

                # col3, col4 = st.columns([2, 2])

                # with col3:
                #     standard_only = st.checkbox('Somente colunas padronizadas')
                # with col4:
                #     entire_df = st.checkbox('Todas as colunas')

                # if standard_only:
                st.markdown('\n')
                new_df = new_df[selected_options]
                st.write(new_df)
                # if entire_df:
                #     st.markdown('\n')
                #     st.write(new_df)
                
                def to_excel(df):
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    new_df.to_excel(writer, index=False, sheet_name='Sheet1')
                    workbook = writer.book
                    worksheet = writer.sheets['Sheet1']
                    format1 = workbook.add_format({'num_format': '0.00'}) 
                    worksheet.set_column('A:A', None, format1)  
                    writer.save()
                    processed_data = output.getvalue()
                    return processed_data

                df_xlsx = to_excel(new_df)
                st.markdown('\n\n')
                st.download_button(label='📥 Baixar Planilha',
                                                data=df_xlsx ,
                                                file_name= 'base_sinistros_padronizada.xlsx')
            except ValueError:
                pass

    with Advanced_Tab:
        st.markdown('O modo de configuração avançada te permite selecionar as colunas que você desejar da sua base de gestão de saúde, e para cada coluna encontrar o melhor padrão que a defina. Identifique na sua base as colunas que gostaria de padronizar e, em seguida, selecione a definição que a represente melhor:')
        header_list = df_advanced.columns
        header_selected = st.multiselect('Selecione as colunas desejadas para serem padronizadas, você pode escolher quantas quiser:', header_list)
        options_list = ['Nome do beneficiário', 'Código do beneficiário', 'Sexo do beneficiário', 'Data de nascimento do beneficiário', 'Idade do beneficiário', 'Data de inclusão no plano', 'Data de exclusão no plano', 'Código de matrícula',  'Operadora do plano de saúde', 'Categoria do plano de saúde', 'Empresa do beneficiário', 'Co-participação', 'Valor da mensalidade', 'Valor total da família do beneficiário', 'Titular ou dependente', 'Tipo de dependência', 'Código tuss do procedimento', 'Valor pago pelo procedimento', 'Data de realização do procedimento', 'Data de pagamento do procedimento', 'Código do prestador de saúde', 'UF do prestador de saúde']
        selected_options = []
        for i in range(len(header_selected)):
            try:
                option = st.selectbox(
                f"Qual formato melhor define a coluna **`{header_selected[i]}`**?",
                (options_list))

                df_advanced = df_advanced.rename(columns={header_selected[i]:option})
                with st.expander("Clique para visualizar:"):
                    new_df = df_advanced
                    new_df
                    selected_options.append(option)
            except ValueError:
                st.error('A coluna selecionada já foi usada, tente uma opção diferente.', icon="🤖")
            # option = st.selectbox(
            # f"Qual formato melhor define a coluna **`{header_selected[i]}`**?",
            # (options_list))

            # new_df = new_df.rename(columns={header_selected[i]:option})
            # new_df
            # header_list = options_list.remove(option)

        if st.button('Padronizar', key="Advanced"):
            try:
                st.markdown("----")
                st.markdown('\n\n')
                st.write('#### 3) Confira o resultado e baixe a sua base padronizada')
                # st.write('<style>div.Widget.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
                # st.radio()

                # col3, col4 = st.columns([2, 2])

                # with col3:
                #     standard_only = st.checkbox('Somente colunas padronizadas')
                # with col4:
                #     entire_df = st.checkbox('Todas as colunas')

                # if standard_only:
                st.markdown('\n')
                new_df = new_df[selected_options]
                st.write(new_df)
                # if entire_df:
                #     st.markdown('\n')
                #     st.write(new_df)
                
                def to_excel(df):
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    new_df.to_excel(writer, index=False, sheet_name='Sheet1')
                    workbook = writer.book
                    worksheet = writer.sheets['Sheet1']
                    format1 = workbook.add_format({'num_format': '0.00'}) 
                    worksheet.set_column('A:A', None, format1)  
                    writer.save()
                    processed_data = output.getvalue()
                    return processed_data

                df_xlsx = to_excel(new_df)
                st.markdown('\n\n')
                st.download_button(label='📥 Baixar Planilha',
                                                data=df_xlsx ,
                                                file_name= 'base_padronizada.xlsx')
            except ValueError:
                pass


    
        

