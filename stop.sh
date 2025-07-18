sudo kill -9 $(sudo lsof -t -i :8503) 2>/dev/null || true
sudo kill -9 $(sudo lsof -t -i :5000) 2>/dev/null || true