import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io

# ====================== CONFIGURACIÓN ======================
st.set_page_config(page_title="Sistema Escolar", page_icon="school", layout="wide")

# ====================== DATOS ======================
data = [
    ["Alejandro Vargas", 13579246, "Matemáticas", 4.5, 8], ["Alejandro Vargas", 13579246, "Español", 7.2, 9],
    ["Alejandro Vargas", 13579246, "Inglés", 6.8, 7], ["Alejandro Vargas", 13579246, "Ciencias", 5.9, 8],
    ["Beatriz Morales", 24681357, "Matemáticas", 8.1, 10], ["Beatriz Morales", 24681357, "Español", 9.0, 10],
    ["Beatriz Morales", 24681357, "Inglés", 7.5, 9], ["Beatriz Morales", 24681357, "Ciencias", 8.8, 10],
    ["Carlos Mendoza", 35792468, "Matemáticas", 6.4, 7], ["Carlos Mendoza", 35792468, "Español", 5.8, 6],
    ["Carlos Mendoza", 35792468, "Inglés", 8.2, 9], ["Carlos Mendoza", 35792468, "Ciencias", 7.0, 8],
    ["Daniela Ortiz", 46813579, "Matemáticas", 3.8, 5], ["Daniela Ortiz", 46813579, "Español", 6.5, 8],
    ["Daniela Ortiz", 46813579, "Inglés", 5.0, 6], ["Daniela Ortiz", 46813579, "Ciencias", 4.2, 4],
    ["Eduardo Navarro", 57924680, "Matemáticas", 9.2, 10], ["Eduardo Navarro", 57924680, "Español", 8.7, 9],
    ["Eduardo Navarro", 57924680, "Inglés", 9.5, 10], ["Eduardo Navarro", 57924680, "Ciencias", 8.9, 10],
    ["Fernanda Pérez", 68035791, "Matemáticas", 7.9, 9], ["Fernanda Pérez", 68035791, "Español", 8.8, 10],
    ["Fernanda Pérez", 68035791, "Inglés", 9.0, 10], ["Fernanda Pérez", 68035791, "Ciencias", 8.5, 9],
    ["Gabriel Quintana", 79146802, "Matemáticas", 5.3, 7], ["Gabriel Quintana", 79146802, "Español", 7.6, 9],
    ["Gabriel Quintana", 79146802, "Inglés", 6.1, 8], ["Gabriel Quintana", 79146802, "Ciencias", 6.8, 7],
    ["Helena Ruiz", 80257913, "Matemáticas", 8.5, 10], ["Helena Ruiz", 80257913, "Español", 7.3, 8],
    ["Helena Ruiz", 80257913, "Inglés", 8.9, 10], ["Helena Ruiz", 80257913, "Ciencias", 7.7, 9],
    ["Ignacio Salazar", 91368024, "Matemáticas", 6.7, 8], ["Ignacio Salazar", 91368024, "Español", 5.5, 6],
    ["Ignacio Salazar", 91368024, "Inglés", 7.4, 9], ["Ignacio Salazar", 91368024, "Ciencias", 6.9, 8],
    ["Juliana Torres", 2479135, "Matemáticas", 9.0, 10], ["Juliana Torres", 2479135, "Español", 8.6, 9],
    ["Juliana Torres", 2479135, "Inglés", 9.3, 10], ["Juliana Torres", 2479135, "Ciencias", 8.8, 10],
]

df = pd.DataFrame(data, columns=["Nombre", "Cédula", "Materia", "Nota_Final", "Horas_Asistidas"])

# ====================== FUNCIÓN PARA GENERAR PDF ======================
def generar_certificado_pdf(nombre, cedula, colegio, promedio, notas_df):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1*inch, bottomMargin=1*inch)
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    titulo = ParagraphStyle('Titulo', parent=styles['Heading1'], fontSize=24, alignment=TA_CENTER, spaceAfter=30, textColor=colors.HexColor("#1a5276"))
    subtitulo = ParagraphStyle('Subtitulo', parent=styles['Heading2'], fontSize=16, alignment=TA_CENTER, spaceAfter=40)
    normal_centro = ParagraphStyle('NormalCentro', parent=styles['Normal'], alignment=TA_CENTER, fontSize=12)
    
    story = []
    
    # Encabezado
    story.append(Paragraph("CERTIFICADO DE ESTUDIOS", titulo))
    story.append(Paragraph(f"{colegio}", subtitulo))
    story.append(Spacer(1, 20))
    
    # Contenido principal
    texto = f"""
    La dirección del {colegio} hace constar que:<br/><br/>
    <b>{nombre}</b><br/>
    Identificado(a) con cédula de ciudadanía N° <b>{cedula:,}</b><br/><br/>
    Es estudiante regular de la institución en el período académico 2025,<br/>
    con un promedio general de <b>{promedio:.2f}</b> sobre 10.0
    """
    story.append(Paragraph(texto, normal_centro))
    story.append(Spacer(1, 30))
    
    # Tabla de notas
    data_table = [["Materia", "Nota Final", "Horas Asistidas"]]
    for _, row in notas_df.iterrows():
        data_table.append([row["Materia"], f"{row['Nota_Final']:.1f}", str(row["Horas_Asistidas"])])
    
    table = Table(data_table, colWidths=[200, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1a5276")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#f0f0f0")),
        ('GRID', (0,0), (-1,-1), 1, colors.grey),
    ]))
    story.append(table)
    
    story.append(Spacer(1, 60))
    story.append(Paragraph(f"Valledupar, {datetime.now().strftime('%d de %B de %Y')}", normal_centro))
    story.append(Spacer(1, 40))
    story.append(Paragraph("_________________________________", normal_centro))
    story.append(Paragraph("Rector(a)", normal_centro))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# ====================== INTERFAZ (igual que antes pero con PDF real) ======================
if "colegio" not in st.session_state:
    st.session_state.colegio = None
    st.session_state.rol = None
    st.session_state.cedula = None

if st.session_state.colegio is None:
    st.title("Bienvenido al Sistema Escolar")
    st.markdown("### Selecciona tu institución educativa:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("**Colegio Departamental Carlos Giraldo**", use_container_width=True):
            st.session_state.colegio = "Colegio Departamental Carlos Giraldo"
            st.rerun()
    with col2:
        if st.button("**Instituto Olga Santa María**", use_container_width=True):
            st.session_state.colegio = "Instituto Olga Santa María"
            st.rerun()
else:
    st.sidebar.success(f"{st.session_state.colegio}")

    if st.session_state.rol is None:
        st.sidebar.header("Iniciar sesión")
        rol = st.sidebar.radio("Selecciona tu rol:", ["Estudiante", "Profesor", "Padre"])
        cedula_input = st.sidebar.text_input("Cédula (solo estudiantes)")
        if st.sidebar.button("Ingresar"):
            if rol == "Estudiante" and cedula_input and int(cedula_input) in df["Cédula"].values:
                st.session_state.rol = rol
                st.session_state.cedula = int(cedula_input)
                nombre = df[df['Cédula'] == int(cedula_input)]['Nombre'].iloc[0]
                st.success(f"¡Bienvenido(a), {nombre.split()[0]}!")
                st.rerun()
            elif rol in ["Profesor", "Padre"]:
                st.session_state.rol = rol
                st.success(f"¡Bienvenido, {rol}!")
                st.rerun()
            else:
                st.error("Cédula no encontrada")

    else:
        st.sidebar.write(f"**Rol:** {st.session_state.rol}")
        if st.sidebar.button("Cerrar sesión"):
            st.session_state.clear()
            st.rerun()

        # ====================== CHATBOT ======================
        st.header("Asistente Virtual")
        faq = {
            "calendario": "El calendario inicia el 20 de enero y termina el 5 de diciembre de 2025.",
            "matrícula": "Matrículas abiertas hasta el 20 de diciembre. Valor: $380.000.",
            "ruta": "Tenemos 4 rutas escolares. Consulta horarios en secretaría.",
            "actividade": "Fútbol, danza, robótica, inglés y banda musical.",
            "refuerzo": "Aquí tienes el video de refuerzo:",
            "tutoria": "Aquí tienes el video de tutoría:",
        }

        if prompt := st.chat_input("¿En qué te puedo ayudar hoy?"):
            prompt_lower = prompt.lower()
            respuesta = "Lo siento, no entendí. Pregúntame sobre calendario, matrícula, rutas, refuerzo..."
            for clave, valor in faq.items():
                if clave in prompt_lower:
                    respuesta = valor
                    if any(p in prompt_lower for p in ["refuerzo", "tutoria", "tutoría"]):
                        respuesta += f"\n\nhttps://www.youtube.com/watch?v=AXpNTCccjZA"
                    break
            st.chat_message("user").write(prompt)
            st.chat_message("assistant").write(respuesta)

        # ====================== CERTIFICADO CON PDF REAL ======================
        if st.session_state.rol in ["Estudiante", "Padre", "Profesor"]:
            st.markdown("---")
            st.subheader("Generar Certificado de Estudios")
            cedula_cert = st.text_input("Número de cédula del estudiante", value=str(st.session_state.cedula) if st.session_state.cedula else "")
            
            if st.button("Generar Certificado PDF", type="primary") and cedula_cert:
                try:
                    ced = int(cedula_cert)
                    if ced in df["Cédula"].values:
                        estudiante = df[df["Cédula"] == ced].iloc[0]
                        notas_est = df[df["Cédula"] == ced]
                        promedio = notas_est["Nota_Final"].mean()
                        
                        # Generar PDF
                        pdf_buffer = generar_certificado_pdf(
                            nombre=estudiante["Nombre"],
                            cedula=ced,
                            colegio=st.session_state.colegio,
                            promedio=promedio,
                            notas_df=notas_est[["Materia", "Nota_Final", "Horas_Asistidas"]]
                        )
                        
                        st.success(f"¡Certificado generado para {estudiante['Nombre']}!")
                        
                        st.download_button(
                            label="Descargar Certificado en PDF",
                            data=pdf_buffer,
                            file_name=f"Certificado_{estudiante['Nombre'].replace(' ', '_')}_{ced}.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error("Estudiante no encontrado")
                except:
                    st.error("Error al generar el certificado")

        # ====================== DASHBOARD (mismo que antes) ======================
        st.markdown("---")
        st.subheader("Dashboard General")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Estudiantes", len(df["Cédula"].unique()))
        with col2: st.metric("Promedio General", f"{df['Nota_Final'].mean():.2f}")
        with col3: st.metric("Mejor promedio", f"{df.groupby('Nombre')['Nota_Final'].mean().max():.2f}")

        fig = px.bar(df.groupby("Nombre")["Nota_Final"].mean().sort_values(ascending=False).round(2),
                     title="Promedio por Estudiante")
        st.plotly_chart(fig, use_container_width=True)

# Aviso de privacidad
with st.expander("Aviso de Privacidad"):
    st.markdown("Tus datos son tratados conforme a la Ley 1581 de 2012 de Protección de Datos Personales (Habeas Data).")

st.sidebar.markdown("---")
st.sidebar.caption("Sistema Escolar 2025 - Todos los derechos reservados")