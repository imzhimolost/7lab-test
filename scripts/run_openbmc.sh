#!/bin/sh

# Заглушка вместо настоящего OpenBMC
echo "🚀 Запускаем OpenBMC Mock Server..."
echo "   Доступ по: http://localhost:4430"

# Запускаем mock-сервер в фоне
cd /var/jenkins_home/workspace/openbmc-ci/mock-openbmc
python3 server.py > qemu.log 2>&1 &
SERVER_PID=$!

# Сохраняем PID
echo $SERVER_PID > /tmp/qemu.pid

# Ждём готовности (mock запускается мгновенно)
echo "⏳ Ожидание готовности OpenBMC..."
sleep 2

# Проверяем через HTTP, а не HTTPS!
if curl -s http://localhost:4430/redfish/v1 > /dev/null; then
    echo "✅ OpenBMC Mock готов!"
    exit 0
else
    echo "❌ Mock не ответил"
    kill $SERVER_PID 2>/dev/null || true
    exit 1
fi