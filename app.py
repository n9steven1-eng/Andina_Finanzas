"""
app.py
======
Dashboard Financiero Ejecutivo - Distribuciones Andina Comercial S.A.S. (2021–2025)
Diseñado por: Analista Financiero Senior & Especialista en Visualización de Datos
Framework: Streamlit & Plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

from data_loader import load_financial_data, get_financial_summary
from financial_metrics import get_kpi_delta, generate_financial_verdict, calculate_eva

# Configuración de página
st.set_page_config(
    page_title="Andina | Financial Executive Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Paleta de colores corporativos de alta fidelidad
COLOR_PRIMARY = "#0F172A"      # Slate 900
COLOR_SECONDARY = "#1E3A8A"    # Blue 900
COLOR_ACCENT = "#2563EB"       # Blue 600
COLOR_CYAN = "#0284C7"         # Sky 600
COLOR_SUCCESS = "#10B981"      # Emerald 500
COLOR_WARNING = "#F59E0B"      # Amber 500
COLOR_DANGER = "#EF4444"       # Red 500
COLOR_PURPLE = "#8B5CF6"       # Violet 500
COLOR_BG_LIGHT = "#F8FAFC"     # Slate 50
COLOR_CARD_BORDER = "#E2E8F0"  # Slate 200

# Inyección de estilos CSS premium
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #0369A1 100%);
        padding: 24px 30px;
        border-radius: 14px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
    }
    
    .main-header h1 {
        color: #FFFFFF;
        font-weight: 800;
        font-size: 28px;
        margin: 0 0 6px 0;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        color: #94A3B8;
        font-size: 14px;
        margin: 0;
    }
    
    .summary-banner {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #2563EB;
        border-radius: 10px;
        padding: 14px 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    }
    
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 16px 16px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s, box-shadow 0.2s;
        margin-bottom: 12px;
        min-height: 142px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
        border-color: #CBD5E1;
    }
    
    .kpi-label {
        font-size: 11.5px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748B;
        margin-bottom: 4px;
    }
    
    .kpi-value {
        font-size: 23px;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.15;
    }
    
    /* BADGES RESALTADOS PARA PUNTOS PORCENTUALES (P.P.) Y VARIACIONES */
    .badge-pp-inc {
        background-color: #DCFCE7;
        color: #15803D;
        border: 1px solid #86EFAC;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11.5px;
        display: inline-block;
        margin-top: 5px;
        letter-spacing: -0.2px;
    }
    
    .badge-pp-dec {
        background-color: #FEE2E2;
        color: #B91C1C;
        border: 1px solid #FCA5A5;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11.5px;
        display: inline-block;
        margin-top: 5px;
        letter-spacing: -0.2px;
    }
    
    .badge-pp-neutral {
        background-color: #F1F5F9;
        color: #475569;
        border: 1px solid #CBD5E1;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 11.5px;
        display: inline-block;
        margin-top: 5px;
        letter-spacing: -0.2px;
    }
    
    .kpi-subtext {
        font-size: 11px;
        color: #94A3B8;
        margin-top: 5px;
    }
    
    .insight-box {
        background: #F0FDF4;
        border-left: 4px solid #10B981;
        border-radius: 8px;
        padding: 14px 18px;
        margin: 16px 0;
    }
    
    .insight-box.warning {
        background: #FFFBEB;
        border-left-color: #F59E0B;
    }
    
    .insight-box.info {
        background: #EFF6FF;
        border-left-color: #3B82F6;
    }
</style>
""", unsafe_allow_html=True)

# Cargar modelo financiero consolidado
@st.cache_data
def get_data():
    df_metrics = get_financial_summary()
    df_bg, df_er, df_ef = load_financial_data()
    return df_metrics, df_bg, df_er, df_ef

df_metrics, df_bg, df_er, df_ef = get_data()

# ----------------- FUNCIONES DE FORMATEO Y BADGES -----------------
def format_pp_badge(curr_val, prev_val, is_pct=True, lower_is_better=False, is_first_year=False, suffix_metric="%"):
    """
    Calcula la variación en puntos porcentuales (p.p.) o unidades métricas,
    y genera un badge HTML resaltado indicando si aumentó o disminuyó.
    """
    if is_first_year:
        return '<span class="badge-pp-neutral">Año Base (2021)</span>'
    
    diff = curr_val - prev_val
    if is_pct:
        abs_diff = abs(diff)
        if abs_diff < 0.005:
            return '<span class="badge-pp-neutral">= 0.00 p.p. (Sin cambio)</span>'
        elif diff > 0:
            badge_class = "badge-pp-dec" if lower_is_better else "badge-pp-inc"
            label = "Aumentó"
            return f'<span class="{badge_class}">▲ +{diff:.2f} p.p. ({label})</span>'
        else:
            badge_class = "badge-pp-inc" if lower_is_better else "badge-pp-dec"
            label = "Disminuyó"
            return f'<span class="{badge_class}">▼ {diff:.2f} p.p. ({label})</span>'
    else:
        abs_diff = abs(diff)
        if abs_diff < 0.005:
            return f'<span class="badge-pp-neutral">= 0.0 {suffix_metric} (Sin cambio)</span>'
        elif diff > 0:
            badge_class = "badge-pp-dec" if lower_is_better else "badge-pp-inc"
            label = "Aumentó"
            return f'<span class="{badge_class}">▲ +{diff:.2f} {suffix_metric} ({label})</span>'
        else:
            badge_class = "badge-pp-inc" if lower_is_better else "badge-pp-dec"
            label = "Disminuyó"
            return f'<span class="{badge_class}">▼ {diff:.2f} {suffix_metric} ({label})</span>'

def format_nominal_badge(curr_val, prev_val, factor=1.0, simbolo="$M", is_first_year=False, lower_is_better=False):
    """
    Genera badge resaltado para magnitudes nominales monetarias con variación porcentual interanual (YoY %).
    """
    if is_first_year:
        return '<span class="badge-pp-neutral">Año Base (2021)</span>'
    if prev_val != 0:
        pct_chg = ((curr_val - prev_val) / abs(prev_val)) * 100
    else:
        pct_chg = 0.0
    if abs(pct_chg) < 0.05:
        return '<span class="badge-pp-neutral">= 0.0% YoY (Sin cambio)</span>'
    elif pct_chg > 0:
        badge_class = "badge-pp-dec" if lower_is_better else "badge-pp-inc"
        return f'<span class="{badge_class}">▲ +{pct_chg:.1f}% YoY (Aumentó)</span>'
    else:
        badge_class = "badge-pp-inc" if lower_is_better else "badge-pp-dec"
        return f'<span class="{badge_class}">▼ {pct_chg:.1f}% YoY (Disminuyó)</span>'

def render_kpi_card_html(label, value_str, badge_html, subtext_str=""):
    """
    Genera la tarjeta visual KPI estandarizada con su badge resaltado.
    """
    return f"""
    <div class="kpi-card">
        <div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value_str}</div>
        </div>
        <div>
            <div>{badge_html}</div>
            <div class="kpi-subtext">{subtext_str}</div>
        </div>
    </div>
    """

# ----------------- BARRA LATERAL (SIDEBAR) -----------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=65)
    st.markdown("### **Distribuciones Andina Comercial S.A.S.**")
    st.markdown("<span style='font-size:12px; color:#64748B;'>NIT 900.842.155-8 | Sector: Mayorista B2B Tecnología & Redes</span>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("#### ⚙️ Parámetros Globales")
    year_selected = st.selectbox(
        "Año de Referencia para Diagnóstico:",
        options=[2025, 2024, 2023, 2022, 2021],
        index=0
    )
    
    moneda_label = st.radio(
        "Unidad Monetaria:",
        ["Millones de COP ($M)", "Miles de COP ($K)"],
        index=0
    )
    factor_moneda = 1.0 if moneda_label.startswith("Millones") else 1000.0
    simbolo_moneda = "$M" if factor_moneda == 1.0 else "$K"
    
    st.divider()
    st.markdown("#### 🎯 Metas & Benchmarks Corporativos")
    target_ebitda = st.slider("Meta Margen EBITDA (%):", min_value=8.0, max_value=14.0, value=10.0, step=0.5)
    target_cce = st.slider("Meta Ciclo de Caja (Días):", min_value=40, max_value=80, value=60, step=1)
    target_dso = st.slider("Meta Días de Cartera (DSO):", min_value=30, max_value=60, value=45, step=1)
    
    st.divider()
    st.markdown("""
    **💡 Contexto del Caso:**
    Empresa B2B colombiana de distribución de seguridad electrónica y redes. En **2021** sufrió estrés de liquidez por *'vender sin generar caja'*. Entre **2022 y 2025** implementó un riguroso plan de capital de trabajo, renegociación de proveedores y plataforma B2B digital.
    """)

# Obtener datos del año seleccionado y año anterior
idx_sel = list(df_metrics['Año']).index(year_selected)
row_sel = df_metrics.iloc[idx_sel]
is_first_year = (year_selected == 2021)
idx_prev = max(0, idx_sel - 1)
row_prev = df_metrics.iloc[idx_prev] if not is_first_year else row_sel
year_prev_str = "2021" if is_first_year else str(year_selected - 1)

# ENCABEZADO PRINCIPAL
st.markdown(f"""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
        <div>
            <h1>Distribuciones Andina Comercial S.A.S.</h1>
            <p>Tablero Integral de Diagnóstico Estratégico-Financiero | Período 2021 – 2025 | Análisis Corporativo</p>
        </div>
        <div style="text-align: right; background: rgba(255,255,255,0.12); padding: 10px 18px; border-radius: 8px;">
            <div style="font-size: 11px; text-transform: uppercase; color: #E2E8F0; font-weight: 600;">Año Visualizado</div>
            <div style="font-size: 24px; font-weight: 800; color: #FFFFFF;">{year_selected}</div>
            <div style="font-size: 11px; color: #CBD5E1;">vs. Base {year_prev_str}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# PESTAÑAS ANALÍTICAS
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏢 Resumen Ejecutivo (C-Suite)",
    "📈 Crecimiento y Rentabilidad (P&L)",
    "🔄 Capital de Trabajo y CCE",
    "⚖️ Estructura de Capital y Solvencia",
    "💎 Retorno DuPont, FCL & Creación de Valor",
    "📑 Estados Financieros Auditados"
])

# ==============================================================================
# TAB 1: RESUMEN EJECUTIVO (C-SUITE)
# ==============================================================================
with tab1:
    # Banner de presentación
    st.markdown(f"""
    <div class="summary-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="font-size: 16px; font-weight: 700; color: #1E3A8A;">
                    📌 Resumen Ejecutivo General del Año {year_selected}
                </span>
                <div style="font-size: 12.5px; color: #64748B;">
                    Indicadores clave de desempeño con variación resaltada en <b>puntos porcentuales (p.p.)</b> vs {year_prev_str}
                </div>
            </div>
            <span style="background: #EFF6FF; color: #1D4ED8; font-weight: 600; padding: 4px 12px; border-radius: 20px; font-size: 12px; border: 1px solid #BFDBFE;">
                Auditoría 2021–2025
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 6 KPIs Clave en 6 columnas con badges p.p. resaltados
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    
    # KPI 1: Ventas Netas
    v_curr = row_sel['Ventas'] * factor_moneda
    b_v = format_nominal_badge(row_sel['Ventas'], row_prev['Ventas'], is_first_year=is_first_year)
    kpi1.markdown(render_kpi_card_html("Ventas Netas", f"${v_curr:,.0f} {simbolo_moneda}", b_v, "CAGR 2021-25: 10.7%"), unsafe_allow_html=True)
    
    # KPI 2: EBITDA & Margen
    eb_curr = row_sel['EBITDA'] * factor_moneda
    eb_mg = row_sel['Margen_EBITDA_%']
    b_eb = format_pp_badge(eb_mg, row_prev['Margen_EBITDA_%'], is_pct=True, is_first_year=is_first_year)
    kpi2.markdown(render_kpi_card_html("Margen EBITDA", f"{eb_mg:.1f}%", b_eb, f"${eb_curr:,.0f} {simbolo_moneda} EBITDA"), unsafe_allow_html=True)
    
    # KPI 3: Utilidad Neta
    un_curr = row_sel['Utilidad_Neta'] * factor_moneda
    un_mg = row_sel['Margen_Neto_%']
    b_un = format_pp_badge(un_mg, row_prev['Margen_Neto_%'], is_pct=True, is_first_year=is_first_year)
    kpi3.markdown(render_kpi_card_html("Margen Neto", f"{un_mg:.2f}%", b_un, f"${un_curr:,.0f} {simbolo_moneda} Neta"), unsafe_allow_html=True)
    
    # KPI 4: Ciclo de Caja (CCE)
    cce_curr = row_sel['CCE_Dias']
    b_cce = format_pp_badge(cce_curr, row_prev['CCE_Dias'], is_pct=False, lower_is_better=True, is_first_year=is_first_year, suffix_metric="días")
    kpi4.markdown(render_kpi_card_html("Ciclo Efectivo", f"{cce_curr:.1f} días", b_cce, f"Meta: &le; {target_cce} días"), unsafe_allow_html=True)
    
    # KPI 5: Flujo de Caja Libre (FCL)
    fcl_curr = row_sel['FCL'] * factor_moneda
    b_fcl = format_nominal_badge(row_sel['FCL'], row_prev['FCL'], is_first_year=is_first_year)
    kpi5.markdown(render_kpi_card_html("Flujo Caja Libre", f"${fcl_curr:,.0f} {simbolo_moneda}", b_fcl, "CFO + CFI (CAPEX)"), unsafe_allow_html=True)
    
    # KPI 6: Deuda Neta / EBITDA
    dn_ebitda = row_sel['Deuda_Neta_EBITDA']
    b_dn = format_pp_badge(dn_ebitda, row_prev['Deuda_Neta_EBITDA'], is_pct=False, lower_is_better=True, is_first_year=is_first_year, suffix_metric="x")
    kpi6.markdown(render_kpi_card_html("Deuda Neta / EBITDA", f"{dn_ebitda:.2f}x", b_dn, "Apalancamiento neto"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # VEREDICTO DEL ANALISTA FINANCIERO
    verdict = generate_financial_verdict(df_metrics)
    st.markdown(f"""
    <div class="insight-box info">
        <h4 style="margin: 0 0 8px 0; color: #1E3A8A; font-weight: 700;">
            📊 Diagnóstico del Analista Senior: {verdict['headline']}
        </h4>
        <ul style="margin: 0; padding-left: 20px; font-size: 13.5px; color: #1E293B;">
            {"".join(f"<li style='margin-bottom: 4px;'>{item}</li>" for item in verdict['key_takeaways'])}
        </ul>
        <div style="margin-top: 10px; font-weight: 600; font-size: 13px; color: #0369A1;">
            🎯 Recomendación Estratégica: {verdict['recommendation']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # FILA DE GRÁFICOS EJECUTIVOS: PENTÁGONO DE SALUD FINANCIERA & TENDENCIA MAESTRA
    col_rad, col_trend = st.columns([1, 1.2])
    
    with col_rad:
        st.markdown("#### 🧭 Radar de Salud Financiera: 2021 vs 2025")
        
        r_categories = ['Margen EBIT', 'Retorno (ROE)', 'Liquidez Corriente', 'Eficiencia de Caja (CCE)', 'Cobertura de Deuda']
        
        r_2021 = [
            (df_metrics.loc[0, 'Margen_EBIT_%'] / 11) * 100,
            (df_metrics.loc[0, 'ROE_%'] / 25) * 100,
            (df_metrics.loc[0, 'Razon_Corriente'] / 2.5) * 100,
            max(20, 100 - (df_metrics.loc[0, 'CCE_Dias'] - 50) * 2),
            (df_metrics.loc[0, 'Cobertura_Intereses'] / 9) * 100
        ]
        
        r_2025 = [
            (df_metrics.loc[4, 'Margen_EBIT_%'] / 11) * 100,
            (df_metrics.loc[4, 'ROE_%'] / 25) * 100,
            (df_metrics.loc[4, 'Razon_Corriente'] / 2.5) * 100,
            max(20, 100 - (df_metrics.loc[4, 'CCE_Dias'] - 50) * 2),
            (df_metrics.loc[4, 'Cobertura_Intereses'] / 9) * 100
        ]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=r_2021,
            theta=r_categories,
            fill='toself',
            name='Año 2021 (Crisis de Caja)',
            line=dict(color=COLOR_DANGER, width=2),
            fillcolor='rgba(239, 68, 68, 0.2)'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=r_2025,
            theta=r_categories,
            fill='toself',
            name='Año 2025 (Madurez y Eficiencia)',
            line=dict(color=COLOR_SUCCESS, width=2),
            fillcolor='rgba(16, 185, 129, 0.25)'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            legend=dict(orientation="h", y=-0.15, x=0.1),
            margin=dict(l=30, r=30, t=20, b=30),
            height=370
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.caption("Nota: Ejes estandarizados a escala 0-100 para comparar el fortalecimiento integral de la empresa.")
        
    with col_trend:
        st.markdown("#### 📈 Evolución Histórica Maestra: Ventas, EBITDA y Flujo Libre")
        fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Barras de Ventas
        fig_trend.add_trace(
            go.Bar(
                x=df_metrics['Año'],
                y=df_metrics['Ventas'] * factor_moneda,
                name="Ventas Netas",
                marker_color="#94A3B8",
                opacity=0.6,
                hovertemplate="Ventas: $%{y:,.0f}<extra></extra>"
            ),
            secondary_y=False
        )
        # Línea de EBITDA
        fig_trend.add_trace(
            go.Scatter(
                x=df_metrics['Año'],
                y=df_metrics['EBITDA'] * factor_moneda,
                name="EBITDA",
                mode="lines+markers",
                line=dict(color=COLOR_SECONDARY, width=3),
                marker=dict(size=8),
                hovertemplate="EBITDA: $%{y:,.0f}<extra></extra>"
            ),
            secondary_y=False
        )
        # Línea de Flujo de Caja Libre
        fig_trend.add_trace(
            go.Scatter(
                x=df_metrics['Año'],
                y=df_metrics['FCL'] * factor_moneda,
                name="Flujo de Caja Libre (FCL)",
                mode="lines+markers",
                line=dict(color=COLOR_SUCCESS, width=3, dash='dash'),
                marker=dict(size=8, symbol='diamond'),
                hovertemplate="FCL: $%{y:,.0f}<extra></extra>"
            ),
            secondary_y=False
        )
        # Línea de Margen EBITDA (%)
        fig_trend.add_trace(
            go.Scatter(
                x=df_metrics['Año'],
                y=df_metrics['Margen_EBITDA_%'],
                name="Margen EBITDA (%)",
                mode="lines+markers",
                line=dict(color=COLOR_WARNING, width=2),
                marker=dict(size=6),
                hovertemplate="Margen EBITDA: %{y:.1f}%<extra></extra>"
            ),
            secondary_y=True
        )
        
        fig_trend.update_layout(
            height=370,
            margin=dict(l=30, r=30, t=20, b=30),
            legend=dict(orientation="h", y=-0.15, x=0.05),
            hovermode="x unified"
        )
        fig_trend.update_yaxes(title_text=f"Monto ({simbolo_moneda})", secondary_y=False)
        fig_trend.update_yaxes(title_text="Margen (%)", secondary_y=True, range=[5, 15])
        st.plotly_chart(fig_trend, use_container_width=True)
        st.caption("Se aprecia cómo el FCL superó su bache negativo de 2021 impulsado por la expansión de EBITDA y la recuperación de capital de trabajo.")

# ==============================================================================
# TAB 2: CRECIMIENTO Y RENTABILIDAD (P&L)
# ==============================================================================
with tab2:
    # Banner de presentación
    st.markdown(f"""
    <div class="summary-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="font-size: 16px; font-weight: 700; color: #1E3A8A;">
                    📌 Resumen de Desempeño Operativo y Márgenes del Año {year_selected}
                </span>
                <div style="font-size: 12.5px; color: #64748B;">
                    Evolución de ingresos y expansión/compresión de márgenes expresada en <b>puntos porcentuales (p.p.)</b> vs {year_prev_str}
                </div>
            </div>
            <span style="background: #F0FDF4; color: #15803D; font-weight: 600; padding: 4px 12px; border-radius: 20px; font-size: 12px; border: 1px solid #BBF7D0;">
                Estado de Resultados (P&L)
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 6 KPIs de P&L con resaltado en p.p.
    pl_c1, pl_c2, pl_c3, pl_c4, pl_c5, pl_c6 = st.columns(6)
    
    # 1. Ventas
    b_pl_v = format_nominal_badge(row_sel['Ventas'], row_prev['Ventas'], is_first_year=is_first_year)
    pl_c1.markdown(render_kpi_card_html("Ingresos (Ventas)", f"${row_sel['Ventas']*factor_moneda:,.0f} {simbolo_moneda}", b_pl_v, "Facturación neta"), unsafe_allow_html=True)
    
    # 2. Margen Bruto
    b_pl_mb = format_pp_badge(row_sel['Margen_Bruto_%'], row_prev['Margen_Bruto_%'], is_pct=True, is_first_year=is_first_year)
    pl_c2.markdown(render_kpi_card_html("Margen Bruto", f"{row_sel['Margen_Bruto_%']:.2f}%", b_pl_mb, f"${row_sel['Utilidad_Bruta']*factor_moneda:,.0f} {simbolo_moneda}"), unsafe_allow_html=True)
    
    # 3. Margen EBITDA
    b_pl_eb = format_pp_badge(row_sel['Margen_EBITDA_%'], row_prev['Margen_EBITDA_%'], is_pct=True, is_first_year=is_first_year)
    pl_c3.markdown(render_kpi_card_html("Margen EBITDA", f"{row_sel['Margen_EBITDA_%']:.2f}%", b_pl_eb, f"${row_sel['EBITDA']*factor_moneda:,.0f} {simbolo_moneda}"), unsafe_allow_html=True)
    
    # 4. Margen EBIT
    b_pl_ebit = format_pp_badge(row_sel['Margen_EBIT_%'], row_prev['Margen_EBIT_%'], is_pct=True, is_first_year=is_first_year)
    pl_c4.markdown(render_kpi_card_html("Margen EBIT", f"{row_sel['Margen_EBIT_%']:.2f}%", b_pl_ebit, f"${row_sel['EBIT']*factor_moneda:,.0f} {simbolo_moneda}"), unsafe_allow_html=True)
    
    # 5. Margen Neto
    b_pl_mn = format_pp_badge(row_sel['Margen_Neto_%'], row_prev['Margen_Neto_%'], is_pct=True, is_first_year=is_first_year)
    pl_c5.markdown(render_kpi_card_html("Margen Neto", f"{row_sel['Margen_Neto_%']:.2f}%", b_pl_mn, f"${row_sel['Utilidad_Neta']*factor_moneda:,.0f} {simbolo_moneda}"), unsafe_allow_html=True)
    
    # 6. Gastos SG&A (% Ventas)
    sga_curr = (row_sel['Gastos_Admin'] + row_sel['Gastos_Ventas']) / row_sel['Ventas'] * 100
    sga_prev = (row_prev['Gastos_Admin'] + row_prev['Gastos_Ventas']) / row_prev['Ventas'] * 100
    b_pl_sga = format_pp_badge(sga_curr, sga_prev, is_pct=True, lower_is_better=True, is_first_year=is_first_year)
    pl_c6.markdown(render_kpi_card_html("SG&A (% Ventas)", f"{sga_curr:.2f}%", b_pl_sga, "Admin + Ventas"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_waterfall, col_margins = st.columns([1.1, 1])
    
    with col_waterfall:
        st.markdown(f"#### 🌊 Cascada de Resultados {year_selected}: De Ingresos a Utilidad Neta")
        
        # Componentes del Waterfall para el año seleccionado
        v_val = row_sel['Ventas'] * factor_moneda
        cv_val = -row_sel['Costo_Ventas'] * factor_moneda
        adm_val = -row_sel['Gastos_Admin'] * factor_moneda
        vts_val = -row_sel['Gastos_Ventas'] * factor_moneda
        da_val = -row_sel['Depreciacion'] * factor_moneda
        gf_val = -row_sel['Gastos_Financieros'] * factor_moneda
        tax_val = -row_sel['Impuestos'] * factor_moneda
        un_val = row_sel['Utilidad_Neta'] * factor_moneda
        
        fig_wf = go.Figure(go.Waterfall(
            name="P&L",
            orientation="v",
            measure=["absolute", "relative", "relative", "relative", "relative", "relative", "relative", "total"],
            x=["Ventas Netas", "Costo Ventas", "G. Admin", "G. Ventas", "D&A", "G. Financieros", "Impuestos", "Utilidad Neta"],
            y=[v_val, cv_val, adm_val, vts_val, da_val, gf_val, tax_val, un_val],
            text=[f"${abs(x):,.0f}" for x in [v_val, cv_val, adm_val, vts_val, da_val, gf_val, tax_val, un_val]],
            textposition="outside",
            connector={"line": {"color": "#94A3B8"}},
            decreasing={"marker": {"color": COLOR_DANGER}},
            increasing={"marker": {"color": COLOR_SUCCESS}},
            totals={"marker": {"color": COLOR_SECONDARY}}
        ))
        fig_wf.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=30, b=30),
            yaxis_title=f"Monto ({simbolo_moneda})"
        )
        st.plotly_chart(fig_wf, use_container_width=True)
        st.caption(f"Estructura de absorción del ingreso en {year_selected}. Costo de ventas absorbe el 75%, dejando un margen bruto del 25%.")

    with col_margins:
        st.markdown("#### 📈 Evolución y Expansión de Márgenes (2021–2025)")
        fig_mg = go.Figure()
        
        fig_mg.add_trace(go.Scatter(
            x=df_metrics['Año'], y=df_metrics['Margen_Bruto_%'],
            name="Margen Bruto", mode="lines+markers",
            line=dict(color="#475569", width=2, dash='dot'),
            hovertemplate="Bruto: %{y:.1f}%<extra></extra>"
        ))
        fig_mg.add_trace(go.Scatter(
            x=df_metrics['Año'], y=df_metrics['Margen_EBITDA_%'],
            name="Margen EBITDA", mode="lines+markers",
            line=dict(color=COLOR_ACCENT, width=3),
            hovertemplate="EBITDA: %{y:.1f}%<extra></extra>"
        ))
        fig_mg.add_trace(go.Scatter(
            x=df_metrics['Año'], y=df_metrics['Margen_EBIT_%'],
            name="Margen Operacional (EBIT)", mode="lines+markers",
            line=dict(color=COLOR_SECONDARY, width=2.5),
            hovertemplate="EBIT: %{y:.2f}%<extra></extra>"
        ))
        fig_mg.add_trace(go.Scatter(
            x=df_metrics['Año'], y=df_metrics['Margen_Neto_%'],
            name="Margen Neto", mode="lines+markers",
            line=dict(color=COLOR_SUCCESS, width=3),
            hovertemplate="Neto: %{y:.2f}%<extra></extra>"
        ))
        
        fig_mg.update_layout(
            height=420,
            margin=dict(l=20, r=20, t=30, b=30),
            yaxis_title="Porcentaje de Ventas (%)",
            hovermode="x unified",
            legend=dict(orientation="h", y=-0.15, x=0.05)
        )
        st.plotly_chart(fig_mg, use_container_width=True)
        st.caption("Margen bruto estable al 25%. La expansión de los márgenes operativo y neto demuestra apalancamiento operativo.")

    # ANÁLISIS DE APALANCAMIENTO OPERATIVO (SG&A COMO % DE VENTAS)
    st.markdown("#### ⚙️ Eficiencia en Gastos Operativos (Apalancamiento Operativo)")
    col_ga1, col_ga2 = st.columns(2)
    
    with col_ga1:
        df_exp_pct = pd.DataFrame({
            'Año': df_metrics['Año'],
            'Gastos Admin (% Ventas)': df_metrics['Gastos_Admin'] / df_metrics['Ventas'] * 100,
            'Gastos Ventas (% Ventas)': df_metrics['Gastos_Ventas'] / df_metrics['Ventas'] * 100,
            'Total SG&A (% Ventas)': (df_metrics['Gastos_Admin'] + df_metrics['Gastos_Ventas']) / df_metrics['Ventas'] * 100
        })
        fig_exp = px.bar(
            df_exp_pct, x='Año', y=['Gastos Admin (% Ventas)', 'Gastos Ventas (% Ventas)'],
            barmode='stack',
            color_discrete_sequence=['#93C5FD', '#3B82F6'],
            title="Evolución de Gastos Operacionales (SG&A) como % de Ventas"
        )
        fig_exp.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20), yaxis_title="% de Ingresos")
        st.plotly_chart(fig_exp, use_container_width=True)
        
    with col_ga2:
        st.markdown(f"""
        <div class="insight-box">
            <h5 style="color: #065F46; margin: 0 0 6px 0; font-weight: 700;">💡 Hallazgo de Apalancamiento Operativo:</h5>
            <p style="font-size: 13px; color: #1E293B; margin-bottom: 8px;">
                Entre 2021 y 2025, la proporción total de <b>Gastos de Administración y Ventas (SG&A)</b> disminuyó del 
                <b>16.30% al 14.50% de las ventas</b> (una optimización neta de <b>-1.80 p.p.</b> o <b>180 bps</b>).
            </p>
            <p style="font-size: 13px; color: #1E293B; margin: 0;">
                En el año <b>{year_selected}</b>, los gastos SG&A representaron el <b>{sga_curr:.2f}%</b> de las ventas, 
                con una variación de {b_pl_sga} frente a {year_prev_str}.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 3: CAPITAL DE TRABAJO Y CCE
# ==============================================================================
with tab3:
    # Banner de presentación
    st.markdown(f"""
    <div class="summary-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="font-size: 16px; font-weight: 700; color: #1E3A8A;">
                    📌 Resumen de Capital de Trabajo y Ciclo Operativo del Año {year_selected}
                </span>
                <div style="font-size: 12.5px; color: #64748B;">
                    Eficiencia de caja, rotaciones en días y productividad de capital (PKT) con deltas en <b>puntos porcentuales (p.p.)</b> vs {year_prev_str}
                </div>
            </div>
            <span style="background: #EFF6FF; color: #1D4ED8; font-weight: 600; padding: 4px 12px; border-radius: 20px; font-size: 12px; border: 1px solid #BFDBFE;">
                Gestión de Liquidez
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 6 KPIs de Capital de Trabajo con resaltado en p.p. y días
    wc_c1, wc_c2, wc_c3, wc_c4, wc_c5, wc_c6 = st.columns(6)
    
    # 1. CCE Neto
    b_wc_cce = format_pp_badge(row_sel['CCE_Dias'], row_prev['CCE_Dias'], is_pct=False, lower_is_better=True, is_first_year=is_first_year, suffix_metric="días")
    wc_c1.markdown(render_kpi_card_html("Ciclo de Caja (CCE)", f"{row_sel['CCE_Dias']:.1f} días", b_wc_cce, "DSO + DIO - DPO"), unsafe_allow_html=True)
    
    # 2. PKT (% Ventas)
    b_wc_pkt = format_pp_badge(row_sel['PKT_%'], row_prev['PKT_%'], is_pct=True, lower_is_better=True, is_first_year=is_first_year)
    wc_c2.markdown(render_kpi_card_html("Productividad KT", f"{row_sel['PKT_%']:.2f}%", b_wc_pkt, "KTNO / Ventas"), unsafe_allow_html=True)
    
    # 3. DSO (Días Cartera)
    b_wc_dso = format_pp_badge(row_sel['DSO_Dias'], row_prev['DSO_Dias'], is_pct=False, lower_is_better=True, is_first_year=is_first_year, suffix_metric="días")
    wc_c3.markdown(render_kpi_card_html("Días Cartera (DSO)", f"{row_sel['DSO_Dias']:.1f} días", b_wc_dso, "Plazo medio cobro"), unsafe_allow_html=True)
    
    # 4. DIO (Días Inventario)
    b_wc_dio = format_pp_badge(row_sel['DIO_Dias'], row_prev['DIO_Dias'], is_pct=False, lower_is_better=True, is_first_year=is_first_year, suffix_metric="días")
    wc_c4.markdown(render_kpi_card_html("Días Inventario (DIO)", f"{row_sel['DIO_Dias']:.1f} días", b_wc_dio, "Rotación stock"), unsafe_allow_html=True)
    
    # 5. DPO (Días Proveedores)
    b_wc_dpo = format_pp_badge(row_sel['DPO_Dias'], row_prev['DPO_Dias'], is_pct=False, lower_is_better=False, is_first_year=is_first_year, suffix_metric="días")
    wc_c5.markdown(render_kpi_card_html("Días Proveedores (DPO)", f"{row_sel['DPO_Dias']:.1f} días", b_wc_dpo, "Crédito proveedores"), unsafe_allow_html=True)
    
    # 6. Razón Corriente
    b_wc_rc = format_pp_badge(row_sel['Razon_Corriente'], row_prev['Razon_Corriente'], is_pct=False, lower_is_better=False, is_first_year=is_first_year, suffix_metric="x")
    wc_c6.markdown(render_kpi_card_html("Razón Corriente", f"{row_sel['Razon_Corriente']:.2f}x", b_wc_rc, "Activo C. / Pasivo C."), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_cce_chart, col_cce_metrics = st.columns([1.3, 1])
    
    with col_cce_chart:
        st.markdown("#### ⏱️ Desglose del Ciclo de Conversión de Efectivo (Días)")
        
        fig_cce = go.Figure()
        
        # DSO (Días de Cobro)
        fig_cce.add_trace(go.Bar(
            x=df_metrics['Año'], y=df_metrics['DSO_Dias'],
            name="Días de Cartera (DSO)", marker_color="#3B82F6",
            hovertemplate="DSO: %{y:.1f} días<extra></extra>"
        ))
        # DIO (Días de Inventario)
        fig_cce.add_trace(go.Bar(
            x=df_metrics['Año'], y=df_metrics['DIO_Dias'],
            name="Días de Inventario (DIO)", marker_color="#F59E0B",
            hovertemplate="DIO: %{y:.1f} días<extra></extra>"
        ))
        # DPO (Días de Proveedores) - Resta
        fig_cce.add_trace(go.Bar(
            x=df_metrics['Año'], y=[-x for x in df_metrics['DPO_Dias']],
            name="Días Proveedores (DPO)", marker_color="#10B981",
            hovertemplate="DPO: %{y:.1f} días (crédito)<extra></extra>"
        ))
        # Línea de CCE Neto
        fig_cce.add_trace(go.Scatter(
            x=df_metrics['Año'], y=df_metrics['CCE_Dias'],
            name="CCE Neto (DSO + DIO - DPO)", mode="lines+markers+text",
            text=[f"{x:.0f}d" for x in df_metrics['CCE_Dias']],
            textposition="top center",
            line=dict(color=COLOR_PRIMARY, width=3),
            marker=dict(size=9, color=COLOR_PRIMARY)
        ))
        
        fig_cce.update_layout(
            barmode='relative',
            height=400,
            margin=dict(l=20, r=20, t=30, b=20),
            yaxis_title="Días de Ciclo",
            legend=dict(orientation="h", y=-0.18, x=0.05),
            hovermode="x unified"
        )
        st.plotly_chart(fig_cce, use_container_width=True)
        st.caption("El CCE se comprimió de 75 a 56 días. Cada día optimizado equivale a liberar aprox. COP $328M en caja a nivel de 2025.")

    with col_cce_metrics:
        st.markdown(f"#### 📊 Indicadores de Liquidez y KTNO ({year_selected} vs {year_prev_str})")
        
        # Tabla resumen de Capital de trabajo con deltas
        diff_pkt_val = row_sel['PKT_%'] - row_prev['PKT_%']
        diff_pkt_str = "0.00 p.p." if is_first_year else f"{diff_pkt_val:+.2f} p.p. ({'Favorable' if diff_pkt_val <= 0 else 'Alerta'})"
        
        df_wc_table = pd.DataFrame({
            'Métrica': [
                'Razón Corriente (AC / PC)',
                'Prueba Ácida ((AC - Inv) / PC)',
                'Días de Cartera (DSO)',
                'Días de Inventario (DIO)',
                'Días de Proveedores (DPO)',
                'Ciclo de Conversión Efectivo (CCE)',
                f'KTNO ({simbolo_moneda})',
                'Productividad KT (PKT %)'
            ],
            f'{year_prev_str}': [
                f"{row_prev['Razon_Corriente']:.2f}x",
                f"{row_prev['Prueba_Acida']:.2f}x",
                f"{row_prev['DSO_Dias']:.1f} d",
                f"{row_prev['DIO_Dias']:.1f} d",
                f"{row_prev['DPO_Dias']:.1f} d",
                f"{row_prev['CCE_Dias']:.1f} d",
                f"${row_prev['KTNO']*factor_moneda:,.0f}",
                f"{row_prev['PKT_%']:.2f}%"
            ],
            f'{year_selected}': [
                f"{row_sel['Razon_Corriente']:.2f}x",
                f"{row_sel['Prueba_Acida']:.2f}x",
                f"{row_sel['DSO_Dias']:.1f} d",
                f"{row_sel['DIO_Dias']:.1f} d",
                f"{row_sel['DPO_Dias']:.1f} d",
                f"{row_sel['CCE_Dias']:.1f} d",
                f"${row_sel['KTNO']*factor_moneda:,.0f}",
                f"{row_sel['PKT_%']:.2f}%"
            ],
            'Variación (p.p. / Delta)': [
                "Base" if is_first_year else f"{row_sel['Razon_Corriente'] - row_prev['Razon_Corriente']:+.2f}x",
                "Base" if is_first_year else f"{row_sel['Prueba_Acida'] - row_prev['Prueba_Acida']:+.2f}x",
                "Base" if is_first_year else f"{row_sel['DSO_Dias'] - row_prev['DSO_Dias']:+.1f} d",
                "Base" if is_first_year else f"{row_sel['DIO_Dias'] - row_prev['DIO_Dias']:+.1f} d",
                "Base" if is_first_year else f"{row_sel['DPO_Dias'] - row_prev['DPO_Dias']:+.1f} d",
                "Base" if is_first_year else f"{row_sel['CCE_Dias'] - row_prev['CCE_Dias']:+.1f} d",
                "Base" if is_first_year else f"${(row_sel['KTNO'] - row_prev['KTNO'])*factor_moneda:+,.0f}",
                diff_pkt_str
            ]
        })
        st.dataframe(df_wc_table, hide_index=True, use_container_width=True)
        
        st.markdown(f"""
        <div class="insight-box info" style="margin-top: 10px;">
            <b>🔑 Productividad del Capital de Trabajo (PKT):</b><br>
            En <b>{year_selected}</b>, la PKT se ubicó en <b>{row_sel['PKT_%']:.2f}%</b> ({b_wc_pkt} vs {year_prev_str}).
            Una menor PKT demuestra que la empresa requiere retener menos capital de trabajo operativo por cada peso vendido.
        </div>
        """, unsafe_allow_html=True)

    # GRÁFICA DE KTNO Y EFECTIVO EN CAJA
    st.markdown("#### 💰 Evolución del Capital de Trabajo Neto Operativo (KTNO) y Acumulación de Caja")
    col_kt1, col_kt2 = st.columns(2)
    
    with col_kt1:
        fig_ktno = go.Figure()
        fig_ktno.add_trace(go.Scatter(
            x=df_metrics['Año'], y=df_metrics['KTNO'] * factor_moneda,
            name="KTNO Requerido", mode="lines+markers",
            line=dict(color=COLOR_SECONDARY, width=3),
            marker=dict(size=8)
        ))
        fig_ktno.add_trace(go.Bar(
            x=df_metrics['Año'], y=df_metrics['PKT_%'],
            name="PKT (% de Ventas)", marker_color="#93C5FD",
            opacity=0.6, yaxis="y2"
        ))
        fig_ktno.update_layout(
            height=320,
            margin=dict(l=20, r=20, t=30, b=20),
            yaxis=dict(title=f"KTNO ({simbolo_moneda})"),
            yaxis2=dict(title="PKT (%)", overlaying="y", side="right", range=[10, 22]),
            legend=dict(orientation="h", y=-0.15, x=0.1)
        )
        st.plotly_chart(fig_ktno, use_container_width=True)
        st.caption("Aunque el KTNO absoluto creció para soportar mayores ventas, la intensidad requerida (PKT) cayó fuertemente.")

    with col_kt2:
        fig_cash = px.area(
            df_metrics, x='Año', y=df_metrics['Efectivo'] * factor_moneda,
            title=f"Saldo Final de Caja y Equivalentes ({simbolo_moneda})",
            color_discrete_sequence=['#10B981']
        )
        fig_cash.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20), yaxis_title=f"Efectivo ({simbolo_moneda})")
        st.plotly_chart(fig_cash, use_container_width=True)
        st.caption("En 2021 la caja cayó a un mínimo peligroso ($740M). Para 2025 alcanza un récord de $12,450M gracias a la rotación eficiente.")

# ==============================================================================
# TAB 4: ESTRUCTURA DE CAPITAL Y SOLVENCIA
# ==============================================================================
with tab4:
    # Banner de presentación
    st.markdown(f"""
    <div class="summary-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="font-size: 16px; font-weight: 700; color: #1E3A8A;">
                    📌 Resumen de Estructura de Capital y Solvencia del Año {year_selected}
                </span>
                <div style="font-size: 12.5px; color: #64748B;">
                    Endeudamiento en <b>puntos porcentuales (p.p.)</b>, desapalancamiento y coberturas crediticias vs {year_prev_str}
                </div>
            </div>
            <span style="background: #FFFBEB; color: #B45309; font-weight: 600; padding: 4px 12px; border-radius: 20px; font-size: 12px; border: 1px solid #FDE68A;">
                Solvencia & Deuda
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 6 KPIs de Deuda y Solvencia con resaltado en p.p.
    solv_c1, solv_c2, solv_c3, solv_c4, solv_c5, solv_c6 = st.columns(6)
    
    # 1. Endeudamiento Total (%)
    b_solv_end = format_pp_badge(row_sel['Endeudamiento_%'], row_prev['Endeudamiento_%'], is_pct=True, lower_is_better=True, is_first_year=is_first_year)
    solv_c1.markdown(render_kpi_card_html("Endeudamiento", f"{row_sel['Endeudamiento_%']:.2f}%", b_solv_end, "Pasivo / Activo Total"), unsafe_allow_html=True)
    
    # 2. Apalancamiento D/E
    b_solv_de = format_pp_badge(row_sel['Apalancamiento'], row_prev['Apalancamiento'], is_pct=False, lower_is_better=True, is_first_year=is_first_year, suffix_metric="x")
    solv_c2.markdown(render_kpi_card_html("Apalancamiento (D/E)", f"{row_sel['Apalancamiento']:.2f}x", b_solv_de, "Pasivo / Patrimonio"), unsafe_allow_html=True)
    
    # 3. Deuda Neta / EBITDA
    b_solv_dne = format_pp_badge(row_sel['Deuda_Neta_EBITDA'], row_prev['Deuda_Neta_EBITDA'], is_pct=False, lower_is_better=True, is_first_year=is_first_year, suffix_metric="x")
    solv_c3.markdown(render_kpi_card_html("Deuda Neta / EBITDA", f"{row_sel['Deuda_Neta_EBITDA']:.2f}x", b_solv_dne, "Deuda neta / Flujo"), unsafe_allow_html=True)
    
    # 4. Cobertura Intereses
    b_solv_cov = format_pp_badge(row_sel['Cobertura_Intereses'], row_prev['Cobertura_Intereses'], is_pct=False, lower_is_better=False, is_first_year=is_first_year, suffix_metric="x")
    solv_c4.markdown(render_kpi_card_html("Cobertura Intereses", f"{row_sel['Cobertura_Intereses']:.2f}x", b_solv_cov, "EBITDA / Intereses"), unsafe_allow_html=True)
    
    # 5. Deuda Financiera Total
    b_solv_df = format_nominal_badge(row_sel['Deuda_Financiera'], row_prev['Deuda_Financiera'], is_first_year=is_first_year, lower_is_better=True)
    solv_c5.markdown(render_kpi_card_html("Deuda Financiera", f"${row_sel['Deuda_Financiera']*factor_moneda:,.0f} {simbolo_moneda}", b_solv_df, "CP + LP"), unsafe_allow_html=True)
    
    # 6. Efectivo Disponible
    b_solv_ef = format_nominal_badge(row_sel['Efectivo'], row_prev['Efectivo'], is_first_year=is_first_year)
    solv_c6.markdown(render_kpi_card_html("Caja Disponible", f"${row_sel['Efectivo']*factor_moneda:,.0f} {simbolo_moneda}", b_solv_ef, "Liquidez inmediata"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_debt_mix, col_leverage = st.columns([1.1, 1])
    
    with col_debt_mix:
        st.markdown(f"#### 💳 Estructura de Financiación {year_selected}: Pasivo vs Patrimonio")
        
        pasivo_sel = row_sel['Total_Pasivos'] * factor_moneda
        pat_sel = row_sel['Patrimonio'] * factor_moneda
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=['Pasivos Totales', 'Patrimonio Neto'],
            values=[pasivo_sel, pat_sel],
            hole=.55,
            marker_colors=[COLOR_SECONDARY, COLOR_SUCCESS]
        )])
        fig_donut.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", y=-0.1, x=0.2)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.caption(f"Endeudamiento Total: {row_sel['Endeudamiento_%']:.1f}% ({b_solv_end}) | Apalancamiento D/E: {row_sel['Apalancamiento']:.2f}x")

    with col_leverage:
        st.markdown("#### 🛡️ Deuda Neta / EBITDA y Cobertura de Intereses")
        
        fig_cov = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_cov.add_trace(
            go.Bar(
                x=df_metrics['Año'], y=df_metrics['Deuda_Neta_EBITDA'],
                name="Deuda Neta / EBITDA (x)", marker_color="#EF4444",
                hovertemplate="DN/EBITDA: %{y:.2f}x<extra></extra>"
            ),
            secondary_y=False
        )
        fig_cov.add_trace(
            go.Scatter(
                x=df_metrics['Año'], y=df_metrics['Cobertura_Intereses'],
                name="Cobertura Intereses (EBITDA / Intereses)",
                mode="lines+markers", line=dict(color=COLOR_SUCCESS, width=3),
                marker=dict(size=8),
                hovertemplate="Cobertura: %{y:.2f}x<extra></extra>"
            ),
            secondary_y=True
        )
        
        fig_cov.update_layout(
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", y=-0.18, x=0.05),
            hovermode="x unified"
        )
        fig_cov.update_yaxes(title_text="Deuda Neta / EBITDA (x)", secondary_y=False, range=[0, 2.5])
        fig_cov.update_yaxes(title_text="Cobertura (veces)", secondary_y=True, range=[2, 12])
        st.plotly_chart(fig_cov, use_container_width=True)
        st.caption("Excelente desapalancamiento neto (de 1.69x a 0.51x) y holgura en cobertura de gastos financieros (4.64x a 8.69x).")

    # DETALLE DE OBLIGACIONES FINANCIERAS CP VS LP
    st.markdown("#### 🏛️ Composición de Obligaciones Financieras (Corto Plazo vs Largo Plazo)")
    col_d1, col_d2 = st.columns([1.2, 1])
    
    with col_d1:
        fig_debt_bars = go.Figure()
        fig_debt_bars.add_trace(go.Bar(
            x=df_metrics['Año'], y=df_metrics['Deuda_CP'] * factor_moneda,
            name="Deuda CP (Capital de Trabajo)", marker_color="#60A5FA"
        ))
        fig_debt_bars.add_trace(go.Bar(
            x=df_metrics['Año'], y=df_metrics['Deuda_LP'] * factor_moneda,
            name="Deuda LP (Inversión Estructural)", marker_color="#1E3A8A"
        ))
        fig_debt_bars.update_layout(
            barmode='stack', height=320,
            margin=dict(l=20, r=20, t=30, b=20),
            yaxis_title=f"Deuda Financiera ({simbolo_moneda})",
            legend=dict(orientation="h", y=-0.15, x=0.1)
        )
        st.plotly_chart(fig_debt_bars, use_container_width=True)
        
    with col_d2:
        st.markdown(f"""
        <div class="insight-box info">
            <h5 style="color: #1E3A8A; margin: 0 0 6px 0; font-weight: 700;">📌 Diagnóstico de Endeudamiento:</h5>
            <ul style="font-size: 13px; color: #1E293B; margin: 0; padding-left: 18px;">
                <li><b>Deuda Financiera Bruta ({year_selected}):</b> ${row_sel['Deuda_Financiera']*factor_moneda:,.0f} {simbolo_moneda} 
                (35% CP / 65% LP).</li>
                <li><b>Caja Disponible:</b> ${row_sel['Efectivo']*factor_moneda:,.0f} {simbolo_moneda}.</li>
                <li><b>Deuda Neta Efectiva:</b> ${row_sel['Deuda_Neta']*factor_moneda:,.0f} {simbolo_moneda}.</li>
                <li><b>Capacidad de Repago:</b> La empresa puede extinguir el 66% de su deuda financiera total utilizando únicamente su efectivo disponible.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 5: DUPONT, FCL Y CREACIÓN DE VALOR
# ==============================================================================
with tab5:
    # Banner de presentación
    st.markdown(f"""
    <div class="summary-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="font-size: 16px; font-weight: 700; color: #1E3A8A;">
                    📌 Resumen de Creación de Valor y Retornos (DuPont) del Año {year_selected}
                </span>
                <div style="font-size: 12.5px; color: #64748B;">
                    Rentabilidad del accionista (ROE) y margen neto evaluados en <b>puntos porcentuales (p.p.)</b> vs {year_prev_str}
                </div>
            </div>
            <span style="background: #F5F3FF; color: #6D28D9; font-weight: 600; padding: 4px 12px; border-radius: 20px; font-size: 12px; border: 1px solid #DDD6FE;">
                Creación de Valor
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 6 KPIs de Valor y DuPont con resaltado en p.p.
    dp_c1, dp_c2, dp_c3, dp_c4, dp_c5, dp_c6 = st.columns(6)
    
    # 1. ROE (%)
    b_dp_roe = format_pp_badge(row_sel['ROE_%'], row_prev['ROE_%'], is_pct=True, is_first_year=is_first_year)
    dp_c1.markdown(render_kpi_card_html("Retorno Patrimonio (ROE)", f"{row_sel['ROE_%']:.2f}%", b_dp_roe, "DuPont = MN × Rot × MC"), unsafe_allow_html=True)
    
    # 2. Margen Neto (DuPont 1)
    b_dp_mn = format_pp_badge(row_sel['Margen_Neto_%'], row_prev['Margen_Neto_%'], is_pct=True, is_first_year=is_first_year)
    dp_c2.markdown(render_kpi_card_html("1. Margen Neto", f"{row_sel['Margen_Neto_%']:.2f}%", b_dp_mn, "Eficiencia en rentabilidad"), unsafe_allow_html=True)
    
    # 3. Rotación Activos (DuPont 2)
    b_dp_rot = format_pp_badge(row_sel['Rotacion_Activos'], row_prev['Rotacion_Activos'], is_pct=False, is_first_year=is_first_year, suffix_metric="x")
    dp_c3.markdown(render_kpi_card_html("2. Rotación Activos", f"{row_sel['Rotacion_Activos']:.2f}x", b_dp_rot, "Ventas / Activos"), unsafe_allow_html=True)
    
    # 4. Multiplicador Capital (DuPont 3)
    b_dp_mc = format_pp_badge(row_sel['Multiplicador_Capital'], row_prev['Multiplicador_Capital'], is_pct=False, lower_is_better=True, is_first_year=is_first_year, suffix_metric="x")
    dp_c4.markdown(render_kpi_card_html("3. Multiplicador Capital", f"{row_sel['Multiplicador_Capital']:.2f}x", b_dp_mc, "Activos / Patrimonio"), unsafe_allow_html=True)
    
    # 5. ROA (%)
    b_dp_roa = format_pp_badge(row_sel['ROA_%'], row_prev['ROA_%'], is_pct=True, is_first_year=is_first_year)
    dp_c5.markdown(render_kpi_card_html("Retorno Activos (ROA)", f"{row_sel['ROA_%']:.2f}%", b_dp_roa, "Utilidad Neta / Activos"), unsafe_allow_html=True)
    
    # 6. Flujo de Caja Libre (FCL)
    b_dp_fcl = format_nominal_badge(row_sel['FCL'], row_prev['FCL'], is_first_year=is_first_year)
    dp_c6.markdown(render_kpi_card_html("Flujo de Caja Libre", f"${row_sel['FCL']*factor_moneda:,.0f} {simbolo_moneda}", b_dp_fcl, "Generación real de efectivo"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("#### 🌲 Árbol de Descomposición DuPont del ROE (3 Factores)")
    st.markdown("""
    El análisis DuPont descompone el **Retorno sobre el Patrimonio (ROE)** en tres motores fundamentales: 
    **Eficiencia Operativa** (Margen Neto) $\\times$ **Eficiencia en Uso de Activos** (Rotación) $\\times$ **Estructura Financiera** (Apalancamiento).
    """)
    
    # 4 tarjetas para DuPont del año seleccionado con badges de puntos porcentuales
    d1, d2, d3, d4 = st.columns(4)
    
    d1.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #10B981;">
        <div class="kpi-label">ROE Final ({year_selected})</div>
        <div class="kpi-value">{row_sel['ROE_%']:.2f}%</div>
        <div style="margin-top: 5px;">{b_dp_roe}</div>
        <div class="kpi-subtext">Base 2021: {df_metrics.loc[0, 'ROE_%']:.2f}% (+{row_sel['ROE_%'] - df_metrics.loc[0, 'ROE_%']:.2f} p.p. acumulado)</div>
    </div>
    """, unsafe_allow_html=True)
    
    d2.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #3B82F6;">
        <div class="kpi-label">1. Margen Neto</div>
        <div class="kpi-value">{row_sel['Margen_Neto_%']:.2f}%</div>
        <div style="margin-top: 5px;">{b_dp_mn}</div>
        <div class="kpi-subtext">Base 2021: {df_metrics.loc[0, 'Margen_Neto_%']:.2f}% (+{row_sel['Margen_Neto_%'] - df_metrics.loc[0, 'Margen_Neto_%']:.2f} p.p. acumulado)</div>
    </div>
    """, unsafe_allow_html=True)
    
    d3.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #F59E0B;">
        <div class="kpi-label">2. Rotación Activos</div>
        <div class="kpi-value">{row_sel['Rotacion_Activos']:.2f}x</div>
        <div style="margin-top: 5px;">{b_dp_rot}</div>
        <div class="kpi-subtext">Ventas / Activos Totales</div>
    </div>
    """, unsafe_allow_html=True)
    
    d4.markdown(f"""
    <div class="kpi-card" style="border-top: 4px solid #8B5CF6;">
        <div class="kpi-label">3. Multiplicador Capital</div>
        <div class="kpi-value">{row_sel['Multiplicador_Capital']:.2f}x</div>
        <div style="margin-top: 5px;">{b_dp_mc}</div>
        <div class="kpi-subtext">Activos / Patrimonio (Apalancamiento)</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-box">
        <b>💡 Conclusión DuPont del Analista ({year_selected}):</b><br>
        En 2021, el ROE era de 16.58% con un alto multiplicador de apalancamiento (2.13x). Para {year_selected}, el ROE se sitúa en <b>{row_sel['ROE_%']:.2f}%</b> ({b_dp_roe}), 
        <b>a pesar del desapalancamiento financiero progresivo</b> ({row_sel['Multiplicador_Capital']:.2f}x vs 2.13x). 
        Esto demuestra que la rentabilidad patrimonial es de <b>alta calidad</b>, producto de la expansión del margen neto ({b_dp_mn}).
    </div>
    """, unsafe_allow_html=True)
    
    # COMPARATIVA FCL VS UTILIDAD NETA (QUALITY OF EARNINGS)
    st.markdown("#### ⚖️ Calidad de Ganancias: Flujo de Caja Libre (FCL) vs Utilidad Neta")
    col_qe1, col_qe2 = st.columns([1.2, 1])
    
    with col_qe1:
        fig_fcl = go.Figure()
        fig_fcl.add_trace(go.Bar(
            x=df_metrics['Año'], y=df_metrics['Utilidad_Neta'] * factor_moneda,
            name="Utilidad Neta Contable", marker_color="#94A3B8"
        ))
        fig_fcl.add_trace(go.Bar(
            x=df_metrics['Año'], y=df_metrics['FCL'] * factor_moneda,
            name="Flujo de Caja Libre (FCL = CFO - CAPEX)", marker_color=COLOR_SUCCESS
        ))
        fig_fcl.update_layout(
            barmode='group', height=340,
            margin=dict(l=20, r=20, t=30, b=20),
            yaxis_title=f"Monto ({simbolo_moneda})",
            legend=dict(orientation="h", y=-0.15, x=0.1)
        )
        st.plotly_chart(fig_fcl, use_container_width=True)
        
    with col_qe2:
        st.markdown(f"""
        <div class="insight-box info">
            <h5 style="color: #1E3A8A; margin: 0 0 6px 0; font-weight: 700;">📊 Calidad del Efectivo (CFO / Utilidad):</h5>
            <p style="font-size: 13px; color: #1E293B;">
                En <b>2021</b>, el ratio CFO / Utilidad Neta fue de apenas <b>0.74x</b> (la empresa generaba utilidad contable pero no entraba a caja).
            </p>
            <p style="font-size: 13px; color: #1E293B;">
                Para <b>{year_selected}</b>, el ratio CFO / Utilidad Neta se sitúa en <b>{row_sel['CFO_Utilidad_Neta']:.2f}x</b>, 
                demostrando una extraordinaria tasa de conversión de ganancias contables en efectivo real de libre disposición.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # SIMULADOR INTERACTIVO WHAT-IF & VALOR ECONÓMICO AGREGADO (EVA)
    st.markdown("#### 🧪 Simulador Interactivo What-If: Sensibilidad de Caja & EVA")
    st.markdown("Modifique las variables operativas para simular el impacto en la liquidez disponible y en la generación de valor (EVA):")
    
    col_sim_ctrl, col_sim_res = st.columns([1, 1.2])
    
    with col_sim_ctrl:
        sim_delta_dso = st.slider("Variación en Días de Cartera (DSO):", min_value=-15, max_value=15, value=0, step=1)
        sim_delta_dio = st.slider("Variación en Días de Inventario (DIO):", min_value=-15, max_value=15, value=0, step=1)
        sim_delta_dpo = st.slider("Variación en Días de Proveedores (DPO):", min_value=-10, max_value=10, value=0, step=1)
        sim_wacc = st.slider("Tasa de Costo de Capital WACC (%):", min_value=8.0, max_value=18.0, value=12.5, step=0.5)
        
    with col_sim_res:
        # Cálculo de impacto
        v_dia = (row_sel['Ventas'] / 365.0) * factor_moneda
        cv_dia = (row_sel['Costo_Ventas'] / 365.0) * factor_moneda
        
        impacto_cartera = -sim_delta_dso * v_dia  # Reducir días libera caja (+)
        impacto_inventario = -sim_delta_dio * cv_dia  # Reducir días libera caja (+)
        impacto_proveedores = sim_delta_dpo * cv_dia  # Aumentar días de crédito aporta caja (+)
        
        impacto_total_caja = impacto_cartera + impacto_inventario + impacto_proveedores
        caja_simulada = (row_sel['Efectivo'] * factor_moneda) + impacto_total_caja
        
        # EVA
        pasivo_espontaneo = (row_sel['Proveedores'] + row_sel['Cuentas_Cobrar']*0.1)
        nopat, cap_inv, cap_charge, eva_calc = calculate_eva(
            ebit=row_sel['EBIT'] * factor_moneda,
            tax_rate=0.30,
            total_activos=row_sel['Total_Activos'] * factor_moneda,
            pasivo_espontaneo=pasivo_espontaneo * factor_moneda,
            wacc=sim_wacc / 100.0
        )
        
        st.markdown(f"""
        <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 10px; padding: 18px;">
            <div style="font-weight: 700; color: #0F172A; font-size: 15px; margin-bottom: 12px;">Resultados de la Simulación ({year_selected})</div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>Impacto Neto en Caja por Días de Ciclo:</span>
                <b style="color: {'#059669' if impacto_total_caja >= 0 else '#DC2626'};">${impacto_total_caja:+,.0f} {simbolo_moneda}</b>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>Caja Proyectada Resultante:</span>
                <b>${caja_simulada:,.0f} {simbolo_moneda}</b>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>NOPAT (Utilidad Operativa Neta Impuestos):</span>
                <b>${nopat:,.0f} {simbolo_moneda}</b>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span>Cargo por Costo de Capital (WACC {sim_wacc:.1f}%):</span>
                <b>${cap_charge:,.0f} {simbolo_moneda}</b>
            </div>
            <hr style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; font-size: 16px;">
                <span style="font-weight: 700;">Valor Económico Agregado (EVA):</span>
                <b style="color: {'#059669' if eva_calc >= 0 else '#DC2626'}; font-weight: 800;">${eva_calc:,.0f} {simbolo_moneda}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 6: ESTADOS FINANCIEROS AUDITADOS
# ==============================================================================
with tab6:
    # Banner de presentación
    st.markdown(f"""
    <div class="summary-banner">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="font-size: 16px; font-weight: 700; color: #1E3A8A;">
                    📌 Resumen de Cierre de Estados Financieros Auditados del Año {year_selected}
                </span>
                <div style="font-size: 12.5px; color: #64748B;">
                    Totales contables oficiales y variación en <b>puntos porcentuales (p.p.)</b> vs {year_prev_str}
                </div>
            </div>
            <span style="background: #F8FAFC; color: #0F172A; font-weight: 600; padding: 4px 12px; border-radius: 20px; font-size: 12px; border: 1px solid #CBD5E1;">
                NIIF / IFRS
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 6 KPIs de Estados Financieros con resaltado
    audit_c1, audit_c2, audit_c3, audit_c4, audit_c5, audit_c6 = st.columns(6)
    
    # 1. Total Activos
    b_aud_act = format_nominal_badge(row_sel['Total_Activos'], row_prev['Total_Activos'], is_first_year=is_first_year)
    audit_c1.markdown(render_kpi_card_html("Total Activos", f"${row_sel['Total_Activos']*factor_moneda:,.0f} {simbolo_moneda}", b_aud_act, "Estructura de inversión"), unsafe_allow_html=True)
    
    # 2. Total Pasivos
    b_aud_pas = format_nominal_badge(row_sel['Total_Pasivos'], row_prev['Total_Pasivos'], is_first_year=is_first_year, lower_is_better=True)
    audit_c2.markdown(render_kpi_card_html("Total Pasivos", f"${row_sel['Total_Pasivos']*factor_moneda:,.0f} {simbolo_moneda}", b_aud_pas, "Obligaciones totales"), unsafe_allow_html=True)
    
    # 3. Patrimonio Neto
    b_aud_pat = format_nominal_badge(row_sel['Patrimonio'], row_prev['Patrimonio'], is_first_year=is_first_year)
    audit_c3.markdown(render_kpi_card_html("Patrimonio Neto", f"${row_sel['Patrimonio']*factor_moneda:,.0f} {simbolo_moneda}", b_aud_pat, "Fondos propios"), unsafe_allow_html=True)
    
    # 4. Ventas Netas
    b_aud_vts = format_nominal_badge(row_sel['Ventas'], row_prev['Ventas'], is_first_year=is_first_year)
    audit_c4.markdown(render_kpi_card_html("Ventas Netas", f"${row_sel['Ventas']*factor_moneda:,.0f} {simbolo_moneda}", b_aud_vts, "Ingresos operacionales"), unsafe_allow_html=True)
    
    # 5. Margen Neto Auditado
    b_aud_mn = format_pp_badge(row_sel['Margen_Neto_%'], row_prev['Margen_Neto_%'], is_pct=True, is_first_year=is_first_year)
    audit_c5.markdown(render_kpi_card_html("Margen Neto Auditado", f"{row_sel['Margen_Neto_%']:.2f}%", b_aud_mn, f"${row_sel['Utilidad_Neta']*factor_moneda:,.0f} {simbolo_moneda}"), unsafe_allow_html=True)
    
    # 6. Saldo Efectivo
    b_aud_ef = format_nominal_badge(row_sel['Efectivo'], row_prev['Efectivo'], is_first_year=is_first_year)
    audit_c6.markdown(render_kpi_card_html("Caja Final", f"${row_sel['Efectivo']*factor_moneda:,.0f} {simbolo_moneda}", b_aud_ef, "Efectivo y equivalentes"), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("#### 📑 Tablas Contables Detalladas (2021–2025)")
    st.markdown("Visualización formal bajo normativa contable y NIIF con análisis horizontal y vertical.")
    
    subtab1, subtab2, subtab3 = st.tabs(["Balance General", "Estado de Resultados", "Flujo de Efectivo"])
    
    year_cols = ['2021', '2022', '2023', '2024', '2025']
    with subtab1:
        st.markdown("#### Balance General Consolidado")
        df_bg_display = df_bg.copy()
        for y in year_cols:
            if y in df_bg_display.columns:
                df_bg_display[y] = df_bg_display[y].apply(lambda x: f"${float(x)*factor_moneda:,.0f}" if pd.notnull(x) and str(x).replace('.','',1).replace('-','',1).isdigit() else str(x))
        st.dataframe(df_bg_display, hide_index=True, use_container_width=True)
        
    with subtab2:
        st.markdown("#### Estado de Resultados Integral")
        df_er_display = df_er.copy()
        for y in year_cols:
            if y in df_er_display.columns:
                df_er_display[y] = df_er_display[y].apply(lambda x: f"${float(x)*factor_moneda:,.0f}" if pd.notnull(x) and str(x).replace('.','',1).replace('-','',1).isdigit() else str(x))
        st.dataframe(df_er_display, hide_index=True, use_container_width=True)
        
    with subtab3:
        st.markdown("#### Estado de Flujos de Efectivo (Método Indirecto)")
        df_ef_display = df_ef.copy()
        for y in year_cols:
            if y in df_ef_display.columns:
                df_ef_display[y] = df_ef_display[y].apply(lambda x: f"${float(x)*factor_moneda:,.0f}" if pd.notnull(x) and str(x).replace('.','',1).replace('-','',1).isdigit() else str(x))
        st.dataframe(df_ef_display, hide_index=True, use_container_width=True)
        
    st.divider()
    
    # EXPORTACIÓN A EXCEL COMPLETO
    st.markdown("#### 📥 Exportar Modelo Financiero Completo a Excel")
    
    def generate_excel():
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Hoja 1: Indicadores Financieros
            df_metrics.to_excel(writer, sheet_name='Indicadores_KPIs', index=False)
            # Hoja 2: Balance General
            df_bg.to_excel(writer, sheet_name='Balance_General', index=False)
            # Hoja 3: Estado de Resultados
            df_er.to_excel(writer, sheet_name='Estado_Resultados', index=False)
            # Hoja 4: Flujo de Efectivo
            df_ef.to_excel(writer, sheet_name='Flujo_Efectivo', index=False)
        return output.getvalue()
        
    excel_data = generate_excel()
    st.download_button(
        label="📥 Descargar Modelo Financiero Completo en Excel (.xlsx)",
        data=excel_data,
        file_name="Andina_Comercial_Modelo_Financiero_2021_2025.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# PIE DE PÁGINA
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 12px;">
    <b>Distribuciones Andina Comercial S.A.S. | Dirección de Planeación Financiera & Control de Gestión</b><br>
    Dashboard desarrollado en Python & Streamlit | Normas Internacionales de Información Financiera (NIIF) | 2021–2025
</div>
""", unsafe_allow_html=True)
