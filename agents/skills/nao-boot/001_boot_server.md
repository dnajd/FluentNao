# Boot Server

**Trigger Condition**: Always

# 1. Check prerequisites

Verify the environment variable is set (should be in `~/.bashrc`):
- `NAO_IP`: The Robot's IP address (e.g., `192.168.68.96`).

```bash
echo "Robot: $NAO_IP"
```

# 2. Start the server

Start the FluentNao Docker container locally. 
Note: On the home server, we use the `default` context and standard volume mounts for "Live Coding."

```bash
cd ~/code/FluentNao && docker compose down && make serve
```

# 3. Wait for health check

Poll the health endpoint on localhost:

```bash
sleep 8 && curl -s http://localhost:5050/health
```

Expected response: `{"status": "ready"}`

# 4. Verify and Prep Robot

Send a test command and ensure the photos directory exists:

```bash
curl -s -X POST http://localhost:5050/exec -d "nao.say('ready')" && \
mkdir -p ~/code/FluentNao/data/photos
```

# 5. Physical Health Check

Check battery and motor status:

```bash
curl -s -X POST http://localhost:5050/exec -d "
import time
result = {
    'battery': nao.sensors.battery_level(),
    'stiff': any(nao.joint_angles('Body', True)),
    'time': time.strftime('%H:%M')
}
"
```
