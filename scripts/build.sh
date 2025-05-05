# scripts/build.sh
#!/bin/bash
echo "📦 Construyendo para producción"
cd frontend && npm run build
cd ../backend && python api.py