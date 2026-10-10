# 📊 Dashboard Financiero Ejecutivo: Distribuciones Andina Comercial S.A.S. (2021–2025)

> **Desarrollado por:** Analista Financiero Senior & Especialista en Visualización de Datos  
> **Tecnologías:** Python 3.11, Streamlit, Plotly, Pandas, OpenPyXL, XlsxWriter  
> **Normativa de Referencia:** Normas Internacionales de Información Financiera (NIIF / IFRS) y Prácticas de Finanzas Corporativas (CFA / Corporate Finance)

---

## 🏢 1. Contexto Empresarial & Diagnóstico Estratégico

**Distribuciones Andina Comercial S.A.S.** es una empresa colombiana del sector mayorista B2B especializada en la distribución de equipos de seguridad electrónica, infraestructura de redes y herramientas industriales. Su propuesta de valor combina disponibilidad inmediata, amplio portafolio (marcas importadas + marcas propias de mayor margen) y soporte técnico posventa.

### 🔍 La Paradoja de 2021: *"Vender sin Generar Caja"*
- En **2021**, la compañía alcanzó ingresos por **COP $80,000M**, pero experimentó una severa asfixia de liquidez:
  - El saldo de caja se redujo a un mínimo crítico de **COP $740M**.
  - El Ciclo de Conversión de Efectivo (CCE) alcanzó **75 días** (DSO de 50 días y DIO de 65 días frente a apenas 40 días de proveedores).
  - El Flujo de Caja Libre (FCL) fue deficitario (**-COP $288M**), requiriendo endeudamiento bancario de corto plazo para operar.

### 🚀 El Turnaround Estratégico-Financiero (2022–2025):
A partir de 2022, la dirección implementó un plan riguroso:
1. **Disciplina en Cartera:** Reducción del DSO de 50 a **43 días** mediante políticas de crédito estructuradas y canal digital B2B.
2. **Eficiencia Logística y Compras:** Reducción del DIO de 65 a **58 días** con mejor planeación de la demanda.
3. **Poder de Negociación:** Ampliación del crédito de proveedores (DPO) de 40 a **45 días**.
4. **Resultado en Caja:** El CCE se comprimió en **19 días** (de 75 a **56 días**), liberando capital que elevó la caja a **COP $12,450M** en 2025, con un FCL récord de **COP $4,288M**.

---

## 💻 2. Cómo Ejecutar la Aplicación

### Opción 1: Acceso Directo (Recomendado)
Haga doble clic en el archivo:
```text
run_dashboard.bat
```
Este script configurará automáticamente las rutas de Python y ejecutará el servidor local en `http://localhost:8501`.

### Opción 2: Desde la Terminal (PowerShell o CMD)
```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python311\Scripts\streamlit.exe" run app.py
```

La aplicación abrirá automáticamente una ventana en su navegador web predeterminado.

---

## 📈 3. Arquitectura del Dashboard

El dashboard está dividido en 6 módulos analíticos de nivel directivo (C-Level):

| Módulo | Enfoque Analítico | Principales Gráficos e Indicadores |
| :--- | :--- | :--- |
| **🏢 1. Resumen Ejecutivo (C-Suite)** | Visión helicoidal del estado de salud corporativa. | KPIs con Deltas YoY, Veredicto del Analista, Radar de Salud Financiera (2021 vs 2025) y Evolución Maestra. |
| **📈 2. Crecimiento y P&L** | Absorción de ingresos y escalabilidad de márgenes. | Gráfico de Cascada (Waterfall) de P&L, Tendencia de Márgenes (Bruto, EBITDA, EBIT, Neto) y Apalancamiento Operativo (SG&A % ventas). |
| **🔄 3. Capital de Trabajo & CCE** | Eficiencia operativa y liberación de caja. | Desglose de CCE (DSO + DIO vs DPO), KTNO vs PKT (Productividad KT), Razón Corriente y Prueba Ácida. |
| **⚖️ 4. Estructura de Capital** | Endeudamiento, respaldo y cobertura de deuda. | Pasivo vs Patrimonio (Donut), Deuda Financiera CP/LP, Deuda Neta / EBITDA y Cobertura de Intereses (EBITDA / Intereses). |
| **💎 5. DuPont & Creación de Valor** | Calidad del ROE, generación de caja real y EVA. | Árbol DuPont de 3 Factores, FCL vs Utilidad Neta (Quality of Earnings), Simulador Interactivo What-If de Sensibilidad y EVA. |
| **📑 6. Estados Financieros Auditados** | Cumplimiento contable formal y exportación. | Balance General, Estado de Resultados y Flujo de Efectivo en formato tabular y botón de descarga a Excel (.xlsx). |

---

## 🧮 4. Glosario de Indicadores Financieros Implementados

1. **Margen Bruto (%)**: $\frac{\text{Utilidad Bruta}}{\text{Ventas}} = 25.0\%$ (Constante por mezcla estratégica de portafolio).
2. **Margen EBITDA (%)**: $\frac{\text{EBITDA}}{\text{Ventas}}$: Se expande del **8.70%** (2021) al **10.50%** (2025).
3. **Margen Neto (%)**: $\frac{\text{Utilidad Neta}}{\text{Ventas}}$: Crece de **3.73%** a **5.57%** (+184 bps).
4. **Días de Cartera (DSO)**: $\frac{\text{Cuentas por Cobrar}}{\text{Ventas}} \times 365$: Disminuye de **50.0** a **43.0 días**.
5. **Días de Inventario (DIO)**: $\frac{\text{Inventarios}}{\text{Costo de Ventas}} \times 365$: Disminuye de **65.0** a **58.0 días**.
6. **Días de Proveedores (DPO)**: $\frac{\text{Proveedores}}{\text{Costo de Ventas}} \times 365$: Aumenta de **40.0** a **45.0 días**.
7. **Ciclo de Conversión de Efectivo (CCE)**: $\text{DSO} + \text{DIO} - \text{DPO}$: Pasa de **75.0** a **56.0 días** (**-19 días de mejora**).
8. **KTNO (Capital de Trabajo Neto Operativo)**: $\text{Deudores} + \text{Inventarios} - \text{Proveedores}$.
9. **PKT (Productividad del KT)**: $\frac{\text{KTNO}}{\text{Ventas}}$: Se optimiza de **18.84%** a **14.45%**.
10. **Deuda Neta / EBITDA**: $\frac{\text{Deuda Financiera Total} - \text{Efectivo}}{\text{EBITDA}}$: Cae de **1.69x** a **0.51x** (Máxima solvencia).
11. **Cobertura de Intereses**: $\frac{\text{EBITDA}}{\text{Gastos Financieros}}$: Crece de **4.64x** a **8.69x**.
12. **Descomposición DuPont**:
   $$\text{ROE} = \left(\frac{\text{Utilidad Neta}}{\text{Ventas}}\right) \times \left(\frac{\text{Ventas}}{\text{Activos}}\right) \times \left(\frac{\text{Activos}}{\text{Patrimonio}}\right)$$
   $$\text{ROE}_{2021} = 3.73\% \times 2.08 \times 2.13 = 16.58\%$$
   $$\text{ROE}_{2025} = 5.57\% \times 1.89 \times 2.01 = 21.14\%$$
13. **EVA (Valor Económico Agregado)**: $\text{NOPAT} - (\text{Capital Invertido} \times \text{WACC})$.

---

## 📁 5. Estructura del Proyecto

```text
ANDINA FINANZAS/
│
├── ARCHIVOS/                                   # Estados financieros y caso de estudio base
│   ├── balance_general.xlsx
│   ├── estado_de_resultados.xlsx
│   ├── estado_flujo_efectivo.xlsx
│   └── Caso Distribuciones Andina Comercial SAS.docx
│
├── app.py                                      # Aplicación principal Streamlit (Frontend & Visualizaciones)
├── data_loader.py                              # Módulo de ingesta y cálculo de indicadores
├── financial_metrics.py                        # Modelado de EVA, DuPont, Deltas y Diagnóstico
├── requirements.txt                            # Dependencias requeridas
├── run_dashboard.bat                           # Lanzador ejecutable para Windows
└── README.md                                   # Documentación técnica y ejecutiva
```
