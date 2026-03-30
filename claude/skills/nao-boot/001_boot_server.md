# Boot Server

**Trigger Condition**: Always

# 1. Check prerequisites

Use `Bash` to verify the NAO_IP environment variable is set:

```
echo $NAO_IP
```

If empty, stop and ask them to export it

# 2. Start the server

Use `Bash` with `run_in_background: true` to start the FluentNao Docker container:

```
cd ~/code/oss/FluentNao && NAO_IP=$NAO_IP make serve
```

This runs `docker compose run --service-ports` which starts the Python 2.7 HTTP bridge on port 5050 inside the container, forwarded to `localhost:5050` on the host.

# 3. Wait for health check

Use `Bash` to poll the health endpoint. Allow up to 15 seconds for the container to start:

```
sleep 8 && curl -s http://localhost:5050/health
```

Expected response: `{"status": "ready"}`

If it fails, wait a few more seconds and retry. If it still fails, check `docker ps` for container status.

# 4. Verify robot connection

Use `Bash` to send a test command:

```
curl -s -X POST http://localhost:5050/exec -d "nao.say('ready')"
```

Expected response: `{"ok": true, "result": "..."}`. The robot should say "ready" out loud.
