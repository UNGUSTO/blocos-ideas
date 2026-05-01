# 🧠 BLOCOS-IDEAS - Ideas de Negocio

Sistema automático para capturar, clasificar y gestionar ideas de negocio.

**Actualización automática:** Cada idea nuevase sincroniza aquí en tiempo real.

## 📊 Estadísticas

- **Total de ideas:** [AUTO-ACTUALIZADO]
- **Última actualización:** [AUTO-ACTUALIZADO]
- **Fuentes:** Telegram, WhatsApp, Audio

## 📁 Estructura de archivos

```
blocos-ideas/
├── IDEAS_TODAS.md          - Todas las ideas
├── IDEAS_Offroad.md        - Ideas categoría Offroad
├── IDEAS_4PL.md            - Ideas categoría 4PL
├── IDEAS_Bolsos_Reciclados.md - Ideas categoría Bolsos
├── IDEAS_TPR.md            - Ideas categoría TPR
├── IDEAS_COMEX.md          - Ideas categoría COMEX
├── IDEAS.json              - Formato JSON (para programas)
├── STATS.json              - Estadísticas en tiempo real
└── CHANGELOG.md            - Historial de cambios
```

## 🚀 Acceso desde Claude Code

```python
import requests
import json

# Obtener todas las ideas directamente desde GitHub
url = "https://raw.githubusercontent.com/tu-usuario/blocos-ideas/main/IDEAS_TODAS.md"
response = requests.get(url)
ideas = response.text

# Usar como contexto en tu proyecto
print(ideas)
```

## 🔄 Flujo automático

1. **Idea en Telegram** → Bot recibe
2. **Clasificación automática** → 9 categorías
3. **Almacenamiento local** → SQLite + MongoDB
4. **Sincronización GitHub** → Push automático
5. **Disponible en Claude** → Contexto en tiempo real

## 📞 Generado automáticamente por BLOCOS-IDEAS
