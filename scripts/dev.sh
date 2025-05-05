# scripts/dev.sh
#!/bin/bash
echo "🚀 Modo desarrollo"
cd backend && python api.py &
cd frontend && npm run dev