# DataRush – Del Insight a la Acción: Recomendaciones Estratégicas

> Equipo **Correcaminos**
> Objetivo: detectar patrones con EDA/visualización en datos reales y convertirlos en **recomendaciones claras** para negocios.
---

## Link
https://drive.google.com/file/d/1nFEGbdKNKyOXc--aZwT-C97tbF536Per/view

## Resumen

1. **Volumen ≠ Apertura internacional.**

   * **EE. UU.** y **China** son los países con **más pasajeros totales**, pero \~**90% doméstico / 10% internacional**.
   * **Reino Unido** lidera por **proporción de pasajeros internacionales**.
2. **Viajes en proporción y bienestar.**

   * Entre los **10 países con más pasajeros por millón de habitantes**, la **mayoría** aparece también entre los **más felices** del mundo (World Happiness Report 2015–2019).
   * Interpretación: no afirmamos causalidad; sí una **asociación consistente** entre mayor movilidad y entornos de mayor bienestar.
3. **Estacionalidad clara por hemisferio.**

   * En el **hemisferio norte** los picos de pasajeros ocurren en **verano**; en el **sur**, en el **invierno del norte**.
   * Implicación: la **capacidad** (flota/rutas) y las **campañas** deben sincronizarse con la **estación dominante** de cada país.

---

## Datos utilizados

* `recursos/datos/monthly_passengers.csv` – Pasajeros por país/mes.
* `recursos/datos/global_holidays.csv` – Feriados por país/fecha.
* `recursos/datos/countries.csv` – Catálogo de países.
* `recursos/datosHappiness/*.csv` – World Happiness Report 2015–2019.

> **Nota:** para comparar “en proporción”, calculamos **pasajeros por millón de habitantes**.

---

## Metodología (EDA)

1. **Limpieza y normalización**

   * Renombrado de llaves, parseo de fechas y tipado.
   * En holidays, opcionalmente filtramos `Type == "Public holiday"` para análisis de feriados oficiales.
2. **Hemisferio y estaciones**

   * Asignación de `Hemisphere` y mapeo **mes → estación** por hemisferio.
   * Métrica `Season_%` = pasajeros de una estación / pasajeros anuales del país.

4. **Intensidad de viaje (en proporción)**

   * `Passengers_per_Million = Σ Total / Población (millones)`.
---

## ✅ Insights → 💼 Recomendaciones

**Aerolíneas**

* *Países con gran turismo doméstico* (USA/CHN): **más capacidad doméstica** en **verano** y **puentes** y flota flexible.
* *Países donde predomina el turismo internacional* (UK, SGP, UAE): **reforzar julio–agosto y diciembre**, alianzas y despliegue de aviones con mayor capacidad en las rutas internacionales críticas.

**Turismo**

* Campañas **familiares** en feriados largos.

**Retail/Servicios**

* **Staffing** e **inventario** alineados a la **estación dominante** por país; horarios extendidos en semanas pico.

---

## 🧪 Notas y límites

* **Asociación, no causalidad.** Reportamos correlaciones; no afirmamos “viajar causa felicidad”.
* **Doméstico** incluye viajes no estrictamente turísticos.
* Resultados **reproducibles** para 2015–2019; patrón consistente entre regiones.

---

## 👥 Equipo

**Correcaminos**
Edgar Mauricio Sánchez Carreón - A00840950
Francisco Daniel Mendoza Melo - A00840940
