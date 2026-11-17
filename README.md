# Prototipo Funcional de Gestión de Riesgos Informáticos - TRL 5
### Universidad Nacional Abierta y a Distancia (UNAD)
**Curso:** Proyecto de Grado (Código: 202016907)  
**Caso de Estudio:** Plan de Ciberseguridad y Continuidad de Negocio para Granados y Arismendi S.A.S. (Bogotá D.C.)

---

## 📑 Información General del Componente Práctico
* **Estrategia Metodológica:** Aprendizaje Basado en Proyectos (Scrum)
* **Nivel de Maduración Tecnológica:** TRL 5 (Tecnología validada en entorno relevante/simulado)
* **Periodo Académico:** Noviembre 2026

## 👥 Integrantes (Equipo de Desarrollo Scrum)
* **Carlos Adolfo Granados Camargo** (Ingeniería de Sistemas)
* **Luisa Fernanda Pérez Meza** (Ingeniería de Sistemas)
* **Tutor del Curso:** Daniel Andrés Guzmán Arévalo

---

## 💻 Módulos del Prototipo Ejecutable
Software desarrollado en **Python** con arquitectura de tres capas y persistencia en **SQLite** bajo los controles de **GTC-ISO/IEC 27002:2022**:
1. **Gestión y Visualización de Activos:** Registro y clasificación por categorías (Hardware, Software, Información, Red, Recurso Humano e Infraestructura Física).
2. **Evaluación y Matriz de Riesgos:** Cálculo automatizado ($R = P \times I$) en escala de 1 a 5 con priorización visual por semaforización (Bajo, Medio, Alto y Crítico).
3. **Generación de Diagnóstico ISO 27002:** Mapeo automático de controles y recomendaciones técnicas por cada amenaza detectada.
4. **Reportes Ejecutivos:** Exportación directa a formato Excel (`.xlsx`) e Informe Diagnóstico en PDF (`.pdf`).
5. **Dashboard de Indicadores:** Panel resumen del estado general de seguridad de la organización.

---

## 🛠️ Requisitos e Instrucciones de Ejecución
1. Asegúrese de tener **Python 3.x** instalado.
2. Instale las dependencias externas necesarias desde la terminal:
   ```bash
   pip install openpyxl reportlab
   ```
3. Clone el repositorio o descargue los archivos (`app.py` y `riesgos.db`) y ejecute:
   ```bash
   python app.py
