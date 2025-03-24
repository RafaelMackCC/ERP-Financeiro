import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Criar conexão com o banco de dados
def get_connection():
    return sqlite3.connect("erp_finance.db", detect_types=sqlite3.PARSE_DECLTYPES)

# Função para obter fluxo de caixa por mês
def get_fluxo_caixa():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT strftime('%Y-%m', data) as mes, tipo, SUM(valor) as total 
        FROM lancamentos 
        GROUP BY mes, tipo
    """, conn)
    conn.close()
    return df

# Função para obter distribuição das contas a pagar por fornecedor
def get_contas_por_fornecedor():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT fornecedor, SUM(valor) as total 
        FROM contas_pagar 
        GROUP BY fornecedor
    """, conn)
    conn.close()
    return df

# Função para obter comparação Receita vs Despesa do mês atual
def get_receita_vs_despesa():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT tipo, SUM(valor) as total 
        FROM lancamentos 
        WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
        GROUP BY tipo
    """, conn)
    conn.close()
    return df

# Interface Streamlit
def main():
    st.title("ERP Financeiro - Dashboard")
    menu = ["Fluxo de Caixa", "Contas por Fornecedor", "Receita vs Despesa"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)
    
    if choice == "Fluxo de Caixa":
        st.subheader("Fluxo de Caixa por Mês")
        df = get_fluxo_caixa()
        if not df.empty:
            fig = px.bar(df, x='mes', y='total', color='tipo', barmode='group', 
                         labels={'total': 'Valor', 'mes': 'Mês', 'tipo': 'Tipo'},
                         title="Fluxo de Caixa Mensal")
            st.plotly_chart(fig)
        else:
            st.info("Nenhum dado disponível.")
    
    elif choice == "Contas por Fornecedor":
        st.subheader("Distribuição das Contas a Pagar por Fornecedor")
        df = get_contas_por_fornecedor()
        if not df.empty:
            fig = px.pie(df, names='fornecedor', values='total', title="Distribuição das Contas a Pagar")
            st.plotly_chart(fig)
        else:
            st.info("Nenhum dado disponível.")
    
    elif choice == "Receita vs Despesa":
        st.subheader("Comparação Receita vs Despesa")
        df = get_receita_vs_despesa()
        if not df.empty:
            fig = px.bar(df, x='tipo', y='total', color='tipo', 
                         labels={'total': 'Valor', 'tipo': 'Categoria'},
                         title="Receita vs Despesa do Mês Atual")
            st.plotly_chart(fig)
        else:
            st.info("Nenhum dado disponível.")

if __name__ == "__main__":
    main()
