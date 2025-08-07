#!/usr/bin/env bash
set -o errexit

echo "🔧 Instalando dependencias del sistema para WeasyPrint..."

apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev

echo "✅ Dependencias instaladas correctamente."
