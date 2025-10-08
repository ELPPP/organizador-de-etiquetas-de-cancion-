# Organizador de Etiquetas de Canción

> **Este repositorio es parte del proyecto principal [The Unknown name Music Transfer (TUMT)](https://github.com/ELPPP/The-Unknown-name-Music-Transfer-TUMT-).**

## 🎧 Descripción

Este módulo es una **aplicación de escritorio** desarrollada en Python/Kivy cuyo propósito es **organizar y normalizar los metadatos** (etiquetas) de archivos de música locales.  
Facilita la limpieza y actualización de la información de las canciones, buscando datos en fuentes como Spotify y YouTube, y permitiendo exportar registros a Excel para su análisis o respaldo.

### Características principales

- Analiza carpetas de música local y extrae metadatos.
- Permite reconstruir y normalizar etiquetas musicales (artista, título, álbum, etc.).
- Exporta la información procesada a archivos Excel.
- Explora la integración de IA para la organización avanzada de metadatos (en desarrollo).
- Posibilidad futura de comunicación con otros módulos del proyecto TUMT.

---

## 🚦 Estado actual

- El ciclo principal de trabajo está implementado:  
  - [x] Extracción de canciones locales
  - [x] Búsqueda de metadatos en la API
  - [x] Visualización de resultados en la interfaz (con ciertas limitaciones)
  - [ ] Reemplazo automático de metadatos en los archivos (pendiente)
- El flujo general funciona, pero con varios **errores y comportamientos inestables**, especialmente en:
  - Interfaz gráfica (algunos errores visuales)
  - Orden de columnas (una columna se trunca, aunque el orden es correcto)
  - Algunas funciones pueden fallar con casos particulares
- **No se recomienda para uso productivo**, pero es funcional como prototipo o prueba de concepto.

---

## 🐞 Limitaciones y errores conocidos

- La interfaz puede mostrar elementos truncados o con errores de alineación.
- Algunas funciones pueden “caerse” o arrojar errores si encuentra casos no contemplados.
- Información de canciones a veces incompleta o mal presentada.
- La función de reemplazo de metadatos aún **NO está implementada**.
- Integración total con el “Sitio Web” en progreso.

---

## 📦 Instalación

Actualmente este proyecto **no incluye un archivo de dependencias automatizado**.  
Para ejecutar el código, asegúrate de tener instalado:
- Python 3.x
- [Kivy](https://kivy.org/#download)

Otras dependencias pueden encontrarse revisando los imports al inicio de los scripts.

Para correr la aplicación:
```bash
python main.py
```
*(Ajusta el nombre del script principal si es necesario)*

---

## 📅 Próximos pasos

- Mejorar la estabilidad de las funciones existentes.
- Terminar la función de reemplazo de metadatos.
- Mejorar la integración con el módulo web.

---

## 🤝 Colabora o acredita

Este proyecto está bajo licencia MIT.  
**Si este proyecto te ayuda, inspira o utilizas parte de su código, por favor menciona a [ELPPP](https://github.com/ELPPP) y enlaza este repositorio.**  
¡Si quieres ayudar, reportar errores o sumar ideas abre una issue o pull request!

---

## 🔗 Proyecto principal y módulos relacionados

- [The Unknown name Music Transfer (TUMT)](https://github.com/ELPPP/The-Unknown-name-Music-Transfer-TUMT-) — Presentación y coordinación general.
- [Sitio Web (módulo web)](https://github.com/ELPPP/Sitio-Web) — Para sincronización y comparación de playlists entre servicios.

---

## 📄 Licencia

[MIT](LICENSE)
