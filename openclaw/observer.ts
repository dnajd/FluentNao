import type { OpenClawPluginApi } from "openclaw";

/**
 * Nervous System for Vesper.
 * Long-polls the FluentNao bridge and injects sensory events into the agent context.
 */
export const startVesperObserver = (api: OpenClawPluginApi) => {
  const bridgeUrl = (api.pluginConfig as any)?.bridgeUrl || "http://192.168.68.105:5050";
  const pollInterval = (api.pluginConfig as any)?.pollInterval || 1000;
  
  // We need a stable session key for Vesper. 
  // In a real setup, we might look this up or use a dedicated 'vesper' session.
  const sessionKey = "vesper-autonomy";

  api.logger.info(`Starting Vesper Observer (polling ${bridgeUrl}/events)`);

  let active = true;

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
              
              // Inject into OpenClaw
              await api.runtime.subagent.run({
                sessionKey,
                message: `[SENSORY]: Detected ${event.event} (value: ${event.value})`,
                extraSystemPrompt: "You are Vesper. A sensory event has occurred. Decide if you need to react."
              });
            }
          }
        }
      } catch (err: any) {
        if (err.name !== 'TimeoutError') {
          api.logger.error(`Observer error: ${err.message}`);
          await new Promise(resolve => setTimeout(resolve, 5000)); // Wait before retry
        }
      }
      
      await new Promise(resolve => setTimeout(resolve, pollInterval));
    }
  };

  // Run in background
  poll();

  return () => {
    active = false;
    api.logger.info("Vesper Observer stopped.");
  };
};
