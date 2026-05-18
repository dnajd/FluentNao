import type { OpenClawPluginApi } from "openclaw";

/**
 * Nervous System for Vesper.
 * Long-polls the FluentNao bridge and triggers agent turns via loopback API calls.
 */
export const startVesperObserver = (api: OpenClawPluginApi) => {
  const bridgeUrl = (api.pluginConfig as any)?.bridgeUrl || "http://192.168.68.105:5050";
  const pollInterval = (api.pluginConfig as any)?.pollInterval || 1000;
  const gatewayUrl = "http://127.0.0.1:18789"; // Internal loopback
  const gatewayToken = (api.config as any)?.gateway?.auth?.token;

  const sessionKey = "vesper-autonomy";

  api.logger.info(`Starting Vesper Observer (polling ${bridgeUrl}/events)`);

  let active = true;
  let lastErrorTime = 0;

  const triggerAgent = async (message: string, extraSystemPrompt?: string) => {
    const hooksToken = "vesper-hook-token";

    try {
      // Use the native OpenClaw Hooks API (POST /hooks/agent)
      const response = await fetch(`${gatewayUrl}/hooks/agent`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${hooksToken}`
        },
        body: JSON.stringify({
          sessionKey,
          message,
          extraSystemPrompt
        })
      });

      if (!response.ok) {
        const errText = await response.text();
        api.logger.error(`Vesper Hook Failed: ${response.status} ${errText}`);
      }
    } catch (err: any) {
      api.logger.error(`Vesper Hook Error: ${err.message}`);
    }
  };

  const poll = async () => {
    while (active) {
      try {
        const response = await fetch(`${bridgeUrl}/events?timeout=30`, {
          signal: AbortSignal.timeout(35000)
        });

        if (response.status === 200) {
          const result = await response.json();
          if (result.ok && result.events && result.events.length > 0) {
            for (const event of result.events) {
              api.logger.info(`Sensory Event: ${event.event} = ${event.value}`);

              await triggerAgent(
                "Sensory event detected",
                "You are Vesper. Something happened in the room."
              );
            }
          }
        }
      } catch (err: any) {
        if (err.name !== 'TimeoutError' && active) {
          const now = Date.now();
          if (!lastErrorTime || (now - lastErrorTime > 60000)) {
            api.logger.warn(`Observer: Cannot reach bridge at ${bridgeUrl}. Vesper is deaf.`);
            lastErrorTime = now;
          }
          await new Promise(resolve => setTimeout(resolve, 10000));
        }
      }

      await new Promise(resolve => setTimeout(resolve, pollInterval));
    }
  };

  // Run in background
  poll();

  // Export the trigger for the initial awakening
  (api as any).vesperTrigger = triggerAgent;

  return () => {
    active = false;
    api.logger.info("Vesper Observer stopped.");
  };
};

