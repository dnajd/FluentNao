# Shutdown Protocol

**Trigger Condition**: When you are asked to shutdown

Acknowledge this protocol on boot. Execute it when the user asks to shut down, end the session, or says goodbye.

Run these steps in order:

## 1. Say goodbye
```
curl -s -X POST http://localhost:5050/exec -d "nao.say('Goodbye. See you next boot.')"
```

## 2. Sit and shutdown NAO cleanly
```
curl -s -X POST http://localhost:5050/exec -d "nao.sit()"
# wait 2 seconds
curl -s -X POST http://localhost:5050/exec -d "nao.shutdown()"
```
Note: `nao.shutdown()` may produce harmless unsubscribe errors for modules that were never started — ignore them.

## 3. Stop the session monitor
```
pkill -f session_monitor.py
```

## 4. Cancel any running cron jobs
Use `CronDelete` for any active cron job IDs from this session.

## 5. Stop the FluentNao server
```
cd ~/code/oss/FluentNao && make stop
```
