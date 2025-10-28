import streamlit as st
import pandas as pd
import plotly.express as px

# Inicializar el estado de sesión para almacenar los gastos
if 'gastos' not in st.session_state:
    st.session_state.gastos = pd.DataFrame(columns=['Fecha', 'Categoría', 'Descripción', 'Monto'])

st.title("Administrador de Gastos Personales")

# Formulario para agregar un nuevo gasto
with st.form("Agregar gasto"):
    fecha = st.date_input("Fecha")
    categoria = st.selectbox("Categoría", ['Alimentación', 'Transporte', 'Entretenimiento', 'Servicios', 'Ahorro', 'Otros'])
    descripcion = st.text_input("Descripción")
    monto = st.number_input("Monto", min_value=0.0, format="%.2f")
    agregar = st.form_submit_button("Agregar gasto")

    if agregar:
        nuevo_gasto = pd.DataFrame([[fecha, categoria, descripcion, monto]], columns=['Fecha', 'Categoría', 'Descripción', 'Monto'])
        st.session_state.gastos = pd.concat([st.session_state.gastos, nuevo_gasto], ignore_index=True)
        st.success("Gasto agregado correctamente")

# Mostrar tabla de gastos
st.subheader("Gastos registrados")
if not st.session_state.gastos.empty:
    st.dataframe(st.session_state.gastos)

    # Selección de gasto para eliminar
    st.subheader("Eliminar gasto")
    indices = list(range(len(st.session_state.gastos)))
    index_to_delete = st.selectbox("Selecciona el índice del gasto a eliminar", indices)
    if st.button("Eliminar gasto"):
        st.session_state.gastos.drop(index_to_delete, inplace=True)
        st.session_state.gastos.reset_index(drop=True, inplace=True)
        st.success("Gasto eliminado correctamente")

    # Visualización de gráficos
    st.subheader("Visualización de gastos")
    fig_pie = px.pie(st.session_state.gastos, names='Categoría', values='Monto', title='Distribución de gastos por categoría')
    st.plotly_chart(fig_pie)

    fig_bar = px.bar(st.session_state.gastos, x='Categoría', y='Monto', color='Categoría', title='Gastos por categoría')
    st.plotly_chart(fig_bar)
else:
    st.info("No hay gastos registrados aún.")
    