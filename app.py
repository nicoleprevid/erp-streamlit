import streamlit as st
import pandas as pd
import sqlite3

# Função para exibir a distribuição das contas a pagar por fornecedor
def distribuicao_contas_por_fornecedor(conn):
    st.subheader("Distribuição das Contas a Pagar por Fornecedor")
    query = """
        SELECT fornecedor, SUM(valor) AS total
        FROM contas_pagar
        GROUP BY fornecedor
        ORDER BY total DESC
    """
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)

    if not df.empty:
        st.bar_chart(df.set_index("fornecedor"), use_container_width=True)

# Função para exibir a comparação Receita vs Despesa
def comparacao_receita_vs_despesa(conn):
    st.subheader("Comparação Receita vs Despesa (Mês Atual)")
    query = """
        SELECT tipo, SUM(valor) AS total
        FROM lancamentos
        WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
        GROUP BY tipo
    """
    df = pd.read_sql_query(query, conn)
    st.dataframe(df)

    if not df.empty:
        st.bar_chart(df.set_index("tipo"), use_container_width=True)

# Função para exibir o status das contas a pagar e receber
def status_contas_pagar_receber(conn):
    st.subheader("Status das Contas a Pagar e Receber")
    query_pagar = """
        SELECT status, SUM(valor) AS total
        FROM contas_pagar
        GROUP BY status
    """
    query_receber = """
        SELECT status, SUM(valor) AS total
        FROM contas_receber
        GROUP BY status
    """
    df_pagar = pd.read_sql_query(query_pagar, conn)
    df_receber = pd.read_sql_query(query_receber, conn)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Contas a Pagar - Status")
        st.dataframe(df_pagar)
        if not df_pagar.empty:
            st.bar_chart(df_pagar.set_index("status"), use_container_width=True)
    
    with col2:
        st.write("Contas a Receber - Status")
        st.dataframe(df_receber)
        if not df_receber.empty:
            st.bar_chart(df_receber.set_index("status"), use_container_width=True)

# Interface Streamlit
def main():
    st.title("ERP Financeiro com Streamlit")
    
    menu = ["Clientes", "Contas a Pagar", "Contas a Receber", "Lançamentos", "Relatórios"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    conn = sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)
    
    if choice == "Clientes":
        st.subheader("Cadastro de Clientes")
        df = pd.read_sql_query("SELECT * FROM clientes", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Pagar":
        st.subheader("Contas a Pagar")
        df = pd.read_sql_query("SELECT * FROM contas_pagar", conn)
        st.dataframe(df)
        
    elif choice == "Contas a Receber":
        st.subheader("Contas a Receber")
        df = pd.read_sql_query("SELECT * FROM contas_receber", conn)
        st.dataframe(df)
        
    elif choice == "Lançamentos":
        st.subheader("Lançamentos Financeiros")
        df = pd.read_sql_query("SELECT * FROM lancamentos", conn)
        st.dataframe(df)
        
    elif choice == "Relatórios":
        relatorio_menu = [
            "Fluxo de Caixa",
            "Distribuição Contas a Pagar por Fornecedor",
            "Comparação Receita vs Despesa",
            "Status Contas a Pagar e Receber"
        ]
        relatorio_choice = st.radio("Escolha um relatório", relatorio_menu)
        
        if relatorio_choice == "Fluxo de Caixa":
            st.subheader("Relatório de Fluxo de Caixa")
            df = pd.read_sql_query("SELECT tipo, SUM(valor) as total FROM lancamentos GROUP BY tipo", conn)
            st.dataframe(df)
        elif relatorio_choice == "Distribuição Contas a Pagar por Fornecedor":
            distribuicao_contas_por_fornecedor(conn)
        elif relatorio_choice == "Comparação Receita vs Despesa":
            comparacao_receita_vs_despesa(conn)
        elif relatorio_choice == "Status Contas a Pagar e Receber":
            status_contas_pagar_receber(conn)
    
    conn.close()
    
if __name__ == "__main__":
    main()
