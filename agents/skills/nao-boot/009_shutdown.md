# Shutdown Protocol

**Trigger Condition**: When you are asked to shutdown

## 1. Say goodbye
```bash
curl -s -X POST http://localhost:5050/exec -d "nao.say('Goodbye. See you next boot.')"
```

## 2. Sit and shutdown NAO cleanly
```bash
curl -s -X POST http://localhost:5050/exec -d "nao.sit()"
# wait 2 seconds
curl -s -X POST http://localhost:5050/exec -d "nao.shutdown()"
```

## 3. Stop the session monitor
```bash
pkill -f session_monitor.py
```

## 4. Stop the FluentNao server
```bash
cd ~/code/FluentNao && make stop
```
