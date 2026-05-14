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

## 3. Stop background processes
Stop the session monitor and any lingering agent polls:
```bash
pkill -f session_monitor.py
pkill -f "http://localhost:5050/events"
```

## 4. Stop the FluentNao server
```bash
cd ~/code/FluentNao && make stop
```

## 5. Clean up exited containers
Remove orphan/exited FluentNao containers to keep the environment clean:
```bash
docker ps -aq --filter ancestor=fluentnao:dev --filter status=exited | xargs -r docker rm
```
