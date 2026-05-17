# Automatización de Certificados y Envíos Masivos 📜🚀

Este repositorio contiene un conjunto de scripts en Python diseñados para automatizar el flujo completo de gestión de certificados para eventos (como la TeleWeek). 

El flujo de trabajo permite tomar un único PDF masivo exportado desde plataformas de diseño (como Canva), dividirlo, renombrar cada página según una base de datos en Excel, y enviar los documentos automáticamente por correo electrónico a cada destinatario.

---

## 🛠️ Requisitos Previos

Asegúrate de tener instalado Python 3.x en tu sistema. Luego, instala las librerías necesarias ejecutando:

```bash
pip install pandas openpyxl pypdf
