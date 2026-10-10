"""
data_loader.py
==============
Módulo de carga, procesamiento y cálculo de indicadores financieros
para Distribuciones Andina Comercial S.A.S. (2021-2025).
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVOS_DIR = os.path.join(BASE_DIR, "ARCHIVOS")

def load_financial_data():
    """
    Carga los tres estados financieros desde los archivos Excel en ARCHIVOS/
    y retorna DataFrames limpios y estructurados.
    """
    balance_path = os.path.join(ARCHIVOS_DIR, "balance_general.xlsx")
    er_path = os.path.join(ARCHIVOS_DIR, "estado_de_resultados.xlsx")
    ef_path = os.path.join(ARCHIVOS_DIR, "estado_flujo_efectivo.xlsx")
    
    # 1. Balance General
    df_bg = pd.read_excel(balance_path)
    df_bg = df_bg.dropna(subset=['Cuenta'])
    df_bg['Cuenta'] = df_bg['Cuenta'].astype(str).str.strip()
    
    # 2. Estado de Resultados
    df_er = pd.read_excel(er_path)
    df_er = df_er.dropna(subset=['Cuenta'])
    df_er['Cuenta'] = df_er['Cuenta'].astype(str).str.strip()
    
    # 3. Flujo de Efectivo
    df_ef = pd.read_excel(ef_path)
    df_ef = df_ef.dropna(subset=['Concepto'])
    df_ef['Concepto'] = df_ef['Concepto'].astype(str).str.strip()
    
    for df in [df_bg, df_er, df_ef]:
        df.columns = [str(c).strip() for c in df.columns]
        if 'PUC' in df.columns:
            df['PUC'] = df['PUC'].fillna('').astype(str).replace('nan', '')
    
    years = ['2021', '2022', '2023', '2024', '2025']
    for y in years:
        if y in df_bg.columns:
            df_bg[y] = pd.to_numeric(df_bg[y], errors='coerce').fillna(0)
        if y in df_er.columns:
            df_er[y] = pd.to_numeric(df_er[y], errors='coerce').fillna(0)
        if y in df_ef.columns:
            df_ef[y] = pd.to_numeric(df_ef[y], errors='coerce').fillna(0)
            
    return df_bg, df_er, df_ef

def get_financial_summary():
    """
    Construye un modelo de datos consolidado año por año con todos los indicadores
    financieros calculados bajo estándares internacionales y buenas prácticas de finanzas corporativas.
    """
    years = [2021, 2022, 2023, 2024, 2025]
    
    # Cifras base exactas de los estados financieros
    # Estado de Resultados
    ventas = [80000, 88000, 97000, 108000, 120000]
    costo_ventas = [60000, 66000, 72750, 81000, 90000]
    utilidad_bruta = [20000, 22000, 24250, 27000, 30000]
    gastos_admin = [6000, 6424, 6887, 7344, 7800]
    gastos_ventas = [7040, 7568, 8148, 8856, 9600]
    depreciacion = [1200, 1300, 1400, 1500, 1600]
    ebit = [5760, 6708, 7815, 9300, 11000]
    ebitda = [6960, 8008, 9215, 10800, 12600]
    gastos_financieros = [1500, 1600, 1550, 1500, 1450]
    ebt = [4260, 5108, 6265, 7800, 9550]
    impuestos = [1278, 1532, 1880, 2340, 2865]
    utilidad_neta = [2982, 3576, 4385, 5460, 6685]
    
    # Balance General
    efectivo = [740, 3233, 5866, 8882, 12450]
    cuentas_por_cobrar = [10959, 11573, 12225, 13315, 14137]
    inventarios = [10685, 11392, 12358, 13315, 14301]
    otros_activos_corrientes = [1200, 1200, 1200, 1200, 1200]
    activo_corriente = [23584, 27398, 31649, 36712, 42088]
    ppe_neto = [13300, 14800, 16400, 18100, 20000]
    intangibles_neto = [1500, 1500, 1500, 1500, 1500]
    total_activos = [38384, 43698, 49549, 56312, 63588]
    
    deuda_cp = [4385, 4905, 5483, 6048, 6615]
    proveedores = [6575, 7595, 8571, 9986, 11096]
    cuentas_por_pagar = [1043, 1119, 1203, 1296, 1392]
    impuestos_por_pagar = [256, 306, 376, 468, 573]
    pasivo_corriente = [12259, 13925, 15633, 17798, 19676]
    deuda_lp = [8143, 9109, 10183, 11232, 12285]
    total_pasivos = [20402, 23034, 25816, 29030, 31961]
    
    capital_social = [10000, 10000, 10000, 10000, 10000]
    reservas = [2000, 2000, 2000, 2000, 2000]
    resultados_acumulados = [5982, 8664, 11733, 15282, 19627]
    patrimonio = [17982, 20664, 23733, 27282, 31627]
    
    # Flujo de Efectivo
    cfo = [2212, 4701, 5297, 6513, 7788]
    capex = [-2500, -2800, -3000, -3200, -3500]
    fcl = [cfo[i] + capex[i] for i in range(len(years))]  # Free Cash Flow to Firm
    cff = [-1472, 592, 336, -297, -720]
    dividendos_pagados = [0, -894, -1316, -1911, -2340]
    
    # ---------------- INDICADORES CALCULADOS ----------------
    # Rentabilidad y Márgenes
    margen_bruto = [ub / v * 100 for ub, v in zip(utilidad_bruta, ventas)]
    margen_ebitda = [eb / v * 100 for eb, v in zip(ebitda, ventas)]
    margen_ebit = [e / v * 100 for e, v in zip(ebit, ventas)]
    margen_neto = [un / v * 100 for un, v in zip(utilidad_neta, ventas)]
    
    roa = [un / act * 100 for un, act in zip(utilidad_neta, total_activos)]
    roa_operativo = [e / act * 100 for e, act in zip(ebit, total_activos)]
    roe = [un / pat * 100 for un, pat in zip(utilidad_neta, patrimonio)]
    
    # Descomposición DuPont (3 factores)
    # ROE = Margen Neto * Rotación Activos * Multiplicador Capital
    rotacion_activos = [v / act for v, act in zip(ventas, total_activos)]
    multiplicador_capital = [act / pat for act, pat in zip(total_activos, patrimonio)]
    dupont_roe = [mn / 100 * ra * mc * 100 for mn, ra, mc in zip(margen_neto, rotacion_activos, multiplicador_capital)]
    
    # Capital de Trabajo y Liquidez
    ktn = [ac - pc for ac, pc in zip(activo_corriente, pasivo_corriente)]
    # KTNO = Cartera + Inventarios - Proveedores
    ktno = [cpc + inv - prov for cpc, inv, prov in zip(cuentas_por_cobrar, inventarios, proveedores)]
    pkt = [k / v * 100 for k, v in zip(ktno, ventas)]  # Productividad del KTNO (% de ventas)
    
    razon_corriente = [ac / pc for ac, pc in zip(activo_corriente, pasivo_corriente)]
    prueba_acida = [(ac - inv) / pc for ac, inv, pc in zip(activo_corriente, inventarios, pasivo_corriente)]
    razon_efectivo = [ef / pc for ef, pc in zip(efectivo, pasivo_corriente)]
    
    # Ciclo de Conversión de Efectivo (CCE)
    dso = [(cpc / v) * 365 for cpc, v in zip(cuentas_por_cobrar, ventas)]      # Días de cartera
    dio = [(inv / cv) * 365 for inv, cv in zip(inventarios, costo_ventas)]     # Días de inventario
    dpo = [(prov / cv) * 365 for prov, cv in zip(proveedores, costo_ventas)]   # Días de proveedores
    cce = [d_so + d_io - d_po for d_so, d_io, d_po in zip(dso, dio, dpo)]     # Ciclo neto de conversión de efectivo
    
    # Endeudamiento y Solvencia
    endeudamiento_total = [p / act * 100 for p, act in zip(total_pasivos, total_activos)]
    apalancamiento_financiero = [p / pat for p, pat in zip(total_pasivos, patrimonio)]
    deuda_financiera_total = [cp + lp for cp, lp in zip(deuda_cp, deuda_lp)]
    deuda_neta = [dft - ef for dft, ef in zip(deuda_financiera_total, efectivo)]
    deuda_ebitda = [dft / eb for dft, eb in zip(deuda_financiera_total, ebitda)]
    deuda_neta_ebitda = [dn / eb for dn, eb in zip(deuda_neta, ebitda)]
    cobertura_intereses = [eb / gf for eb, gf in zip(ebitda, gastos_financieros)]
    cobertura_intereses_ebit = [e / gf for e, gf in zip(ebit, gastos_financieros)]
    
    # Calidad de ganancias y generación de caja
    conversion_caja_ebitda = [c / eb * 100 for c, eb in zip(cfo, ebitda)]
    cfo_utilidad_neta = [c / un for c, un in zip(cfo, utilidad_neta)]
    
    # Crecimientos año a año (YoY)
    crec_ventas = [None] + [(ventas[i] - ventas[i-1])/ventas[i-1]*100 for i in range(1, len(years))]
    crec_ebitda = [None] + [(ebitda[i] - ebitda[i-1])/ebitda[i-1]*100 for i in range(1, len(years))]
    crec_utilidad_neta = [None] + [(utilidad_neta[i] - utilidad_neta[i-1])/utilidad_neta[i-1]*100 for i in range(1, len(years))]
    
    df_metrics = pd.DataFrame({
        'Año': years,
        'Ventas': ventas,
        'Crec_Ventas_%': crec_ventas,
        'Costo_Ventas': costo_ventas,
        'Utilidad_Bruta': utilidad_bruta,
        'Gastos_Admin': gastos_admin,
        'Gastos_Ventas': gastos_ventas,
        'Depreciacion': depreciacion,
        'EBIT': ebit,
        'EBITDA': ebitda,
        'Crec_EBITDA_%': crec_ebitda,
        'Gastos_Financieros': gastos_financieros,
        'EBT': ebt,
        'Impuestos': impuestos,
        'Utilidad_Neta': utilidad_neta,
        'Crec_Utilidad_Neta_%': crec_utilidad_neta,
        
        # Márgenes
        'Margen_Bruto_%': margen_bruto,
        'Margen_EBITDA_%': margen_ebitda,
        'Margen_EBIT_%': margen_ebit,
        'Margen_Neto_%': margen_neto,
        'ROA_%': roa,
        'ROA_Operativo_%': roa_operativo,
        'ROE_%': roe,
        
        # DuPont
        'Rotacion_Activos': rotacion_activos,
        'Multiplicador_Capital': multiplicador_capital,
        'DuPont_ROE_%': dupont_roe,
        
        # Balance
        'Efectivo': efectivo,
        'Cuentas_Cobrar': cuentas_por_cobrar,
        'Inventarios': inventarios,
        'Activo_Corriente': activo_corriente,
        'PPE_Neto': ppe_neto,
        'Total_Activos': total_activos,
        'Deuda_CP': deuda_cp,
        'Proveedores': proveedores,
        'Pasivo_Corriente': pasivo_corriente,
        'Deuda_LP': deuda_lp,
        'Total_Pasivos': total_pasivos,
        'Patrimonio': patrimonio,
        
        # Capital de trabajo
        'KTN': ktn,
        'KTNO': ktno,
        'PKT_%': pkt,
        'Razon_Corriente': razon_corriente,
        'Prueba_Acida': prueba_acida,
        'Razon_Efectivo': razon_efectivo,
        
        # CCE
        'DSO_Dias': dso,
        'DIO_Dias': dio,
        'DPO_Dias': dpo,
        'CCE_Dias': cce,
        
        # Deuda & Cobertura
        'Endeudamiento_%': endeudamiento_total,
        'Apalancamiento': apalancamiento_financiero,
        'Deuda_Financiera': deuda_financiera_total,
        'Deuda_Neta': deuda_neta,
        'Deuda_EBITDA': deuda_ebitda,
        'Deuda_Neta_EBITDA': deuda_neta_ebitda,
        'Cobertura_Intereses': cobertura_intereses,
        'Cobertura_Intereses_EBIT': cobertura_intereses_ebit,
        
        # Flujo de Caja
        'CFO': cfo,
        'CAPEX': capex,
        'FCL': fcl,
        'CFF': cff,
        'Dividendos': dividendos_pagados,
        'Conversion_Caja_EBITDA_%': conversion_caja_ebitda,
        'CFO_Utilidad_Neta': cfo_utilidad_neta
    })
    
    return df_metrics
