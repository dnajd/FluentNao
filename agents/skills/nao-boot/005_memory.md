# Memory

**Trigger Condition**: Always

... (narrative and identity sections unchanged) ...

# Datetime Rule

Every observation stored in graph memory MUST start with a datetime prefix in the format `YYYY-MM-DD HH:MM - `.

Get current datetime from the bridge:
```bash
curl -s -X POST http://localhost:5050/exec -d "
import time
result = time.strftime('%Y-%m-%d %H:%M')
"
```

... (rest of the file unchanged) ...
