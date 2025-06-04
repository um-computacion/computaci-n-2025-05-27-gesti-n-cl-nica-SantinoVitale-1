# 📄 Documentación del Sistema de Gestión para una Clínica

## 📦 Estructura del Proyecto

```
.
├── src/
│   ├── modelo.py      # Lógica del modelo y validaciones
│   └── cli.py         # Interfaz de consola (CLI)
├── tests/
│   └── test_modelo.py # Pruebas unitarias con unittest
├── README.md
└── DOCUMENTACION.md   # (Este archivo)
```

---

## ▶️ Cómo ejecutar el sistema

1. **Abrir una terminal** en la raíz del proyecto.
2. Ejecutar el siguiente comando para iniciar la interfaz de consola:

   ```
   python src/cli.py
   ```

   El sistema mostrará un menú interactivo para gestionar pacientes, médicos, turnos, recetas e historias clínicas.

---

## 🧪 Cómo ejecutar las pruebas

1. **Abrir una terminal** en la raíz del proyecto.
2. Ejecutar todas las pruebas unitarias con:

   ```
   python -m unittest discover tests
   ```

   Esto ejecutará todos los tests definidos en `tests/test_modelo.py` y mostrará los resultados.

---

## 🏗️ Explicación de diseño general

- **Modelo (`src/modelo.py`)**  
  Contiene las clases principales del dominio: `Paciente`, `Medico`, `Especialidad`, `Turno`, `Receta`, `HistoriaClinica` y `Clinica`.  
  Todas las validaciones y reglas de negocio se implementan aquí, incluyendo el uso de **excepciones personalizadas** para manejar errores de dominio (por ejemplo, duplicados, datos inválidos, turnos ocupados, etc.).

- **Interfaz de consola (`src/cli.py`)**  
  Proporciona un menú interactivo para el usuario.  
  Solicita los datos necesarios, llama a los métodos del modelo y muestra mensajes claros según el resultado o los errores capturados.

- **Pruebas unitarias (`tests/test_modelo.py`)**  
  Validan los casos principales y los errores del modelo usando el módulo `unittest`.  
  Incluyen pruebas para registros duplicados, validaciones de turnos, recetas, especialidades y manejo de excepciones.

---

## ⚠️ Notas importantes

- **No se realizan validaciones de negocio en la CLI**: toda la lógica y validación está en el modelo.
- **El sistema es extensible**: puedes agregar más funcionalidades fácilmente siguiendo la estructura actual.
- **El código está documentado y es legible**, facilitando el mantenimiento y la corrección de errores.

---

**Autor:** Santino Vitale  
**Año:** 2025  
**Materia:** Computación - Ingeniería en Informática  