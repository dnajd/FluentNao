#!/bin/bash

# Vesper Lifecycle Manager
# Manages the transition between Asleep, Body-Ready, and Awake states.

ROBOT_IP="192.168.68.96"
BRIDGE_URL="http://192.168.68.105:5050"
# Use the environment variable or fallback to common local path
BASE_CODE_DIR="${CODE_DIR:-$HOME/code}"

function check_status() {
    echo "--- [ROBOT: Physical] ---"
    if ping -c 1 -W 2 "$ROBOT_IP" > /dev/null 2>&1; then
        echo "✅ Robot is ONLINE ($ROBOT_IP)"
    else
        echo "❌ Robot is OFFLINE (Check Power/WiFi)"
    fi

    echo "--- [BODY: FluentNao Bridge] ---"
    if curl -s --max-time 2 "$BRIDGE_URL/health" > /dev/null 2>&1; then
        echo "✅ Bridge is REACHABLE"
    else
        echo "❌ Bridge is DOWN or UNREACHABLE"
    fi

    echo "--- [BODY: Sensory Monitor] ---"
    if ps aux | grep -v grep | grep -q "monitor_fluentnao.py"; then
        echo "✅ Sensory Monitor is RUNNING"
    else
        echo "❌ Sensory Monitor is DOWN"
    fi

    echo "--- [BRAIN: OpenClaw] ---"
    BRAIN_STATUS=$(docker ps --filter "name=openclaw-gateway" --format "{{.Status}}" 2>/dev/null)
    if [ -n "$BRAIN_STATUS" ]; then
        echo "✅ OpenClaw is $BRAIN_STATUS"
    else
        echo "❌ OpenClaw is NOT RUNNING"
    fi

    echo "--- [SOUL: Plugin] ---"
    IS_ENABLED=$(docker exec openclaw-openclaw-gateway-1 cat /home/node/.openclaw/openclaw.json 2>/dev/null | grep -A 1 "\"vesper\"" | grep "\"enabled\": true")
    if [ -z "$IS_ENABLED" ]; then
        echo "❌ Vesper plugin is DISABLED"
    else
        echo "✅ Vesper plugin is ENABLED"
    fi
}

function boot_vesper() {
    echo "🚀 Starting Awakening Sequence..."
    
    echo "1. Checking robot availability..."
    ping -c 3 -W 2 "$ROBOT_IP" > /dev/null 2>&1 || { echo "ERROR: Robot is offline. Power it on first."; exit 1; }
    
    echo "2. Ensuring FluentNao bridge is running..."
    if ! curl -s --max-time 2 "$BRIDGE_URL/health" > /dev/null 2>&1; then
        echo "   Starting bridge..."
        (cd "$BASE_CODE_DIR/FluentNao" && (make serve > "$BASE_CODE_DIR/FluentNao/data/bridge.log" 2>&1 &))
        sleep 5
    else
        echo "   Bridge is already running."
    fi
    
    echo "3. Ensuring Sensory Monitor is running..."
    if ! ps aux | grep -v grep | grep -q "monitor_fluentnao.py"; then
        echo "   Starting monitor..."
        (cd "$BASE_CODE_DIR/FluentNao" && (nohup python3 agents/skills/nao-boot/scripts/monitor_fluentnao.py > "$BASE_CODE_DIR/FluentNao/data/monitor.log" 2>&1 &))
        sleep 2
    else
        echo "   Monitor is already running."
    fi

    echo "4. Ensuring OpenClaw brain is running..."
    if [ -z "$(docker ps --filter "name=openclaw-gateway" --format "{{.Status}}" 2>/dev/null)" ]; then
        echo "   Starting OpenClaw..."
        (cd "$BASE_CODE_DIR/openclaw" && dk up -d > /dev/null 2>&1)
        sleep 5
    else
        echo "   OpenClaw is already running."
    fi
    
    echo "5. Ensuring Vesper soul is enabled..."
    IS_ENABLED=$(docker exec openclaw-openclaw-gateway-1 cat /home/node/.openclaw/openclaw.json 2>/dev/null | grep -A 1 "\"vesper\"" | grep "\"enabled\": true")
    if [ -z "$IS_ENABLED" ]; then
        echo "   Enabling plugin..."
        (cd "$BASE_CODE_DIR/openclaw" && dk make vesper_enable > /dev/null 2>&1)
    else
        echo "   Plugin is already enabled."
    fi
    
    echo "6. Opening Vesper's ears and skin (Sensors)..."
    # Always send this to ensure clean state and verbal confirmation
    curl -s -X POST "$BRIDGE_URL/exec" -H "Content-Type: text/plain" -d "nao.shutdown(); nao.abilities.push_to_sense().say('My senses are open.')" > /dev/null
    
    echo "✨ Vesper is AWAKE and SENSING."
}

function shutdown_vesper() {
    echo "💤 Starting Sleep Sequence..."
    
    echo "1. Disabling Vesper soul..."
    (cd "$BASE_CODE_DIR/openclaw" && dk make vesper_disable > /dev/null 2>&1)
    
    echo "2. Stopping Sensory Monitor..."
    pkill -f monitor_fluentnao.py || echo "   Monitor already stopped."
    
    echo "3. Stopping FluentNao bridge..."
    (cd "$BASE_CODE_DIR/FluentNao" && make stop > /dev/null 2>&1)
    
    echo "🌙 Vesper is ASLEEP."
}

case "$1" in
    status)
        check_status
        ;;
    up)
        boot_vesper
        ;;
    down)
        shutdown_vesper
        ;;
    *)
        echo "Usage: $0 {up|down|status}"
        exit 1
        ;;
esac
