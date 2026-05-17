import type { OpenClawPluginApi, OpenClawPluginDefinition } from "openclaw";
import { createNaoExecuteTool } from "./tool_execute.js";
import { createNaoDiagnoseTool } from "./persona/diagnosis.js";
import { createVesperSystemTools } from "./persona/system_tools.js";
import { startVesperObserver } from "./observer.js";
import { VESPER_SOUL } from "./persona/instructions.js";

/**
 * FluentNao Plugin for OpenClaw.
 * Brings Vesper to life as an autonomous entity.
 */
const plugin: OpenClawPluginDefinition = {
  id: "vesper",
  name: "Vesper",
  description: "Autonomous Robot Persona for NAO",
  
  activate: (api: OpenClawPluginApi) => {
    // 1. Register Tools
    api.registerTool(createNaoExecuteTool);
    api.registerTool(createNaoDiagnoseTool);
    api.registerTool(createVesperSystemTools);

    // 2. Register Vesper as a Channel
    // This allows the robot to "send" messages (sensors) and "receive" messages (speech)
    api.registerChannel({
      id: "vesper",
      meta: {
        label: "Vesper (Robot Body)",
        icon: "robot"
      },
      capabilities: {
        messaging: true,
        outbound: true
      },
      config: {
        // Fix: Ensure these are simple non-async returns if possible or properly handled
        listAccountIds: () => ["vesper-body"],
        resolveAccount: (id: string) => ({ id: "vesper-body", name: "NAO" })
      },
      // Fix: Add status hook to satisfy the health monitor
      status: {
        probe: async () => {
          const bridgeUrl = (api.config as any)?.vesper?.bridgeUrl || "http://192.168.68.105:5050";
          try {
            const resp = await fetch(`${bridgeUrl}/health`);
            return resp.ok ? { status: "online" } : { status: "error", message: "Bridge Unhealthy" };
          } catch (e) {
            return { status: "offline", message: (e as any).message };
          }
        }
      },
      // Outbound: When Vesper wants to speak to the room
      outbound: {
        deliver: async (params) => {
          const script = `nao.say(${JSON.stringify(params.content)})`;
          const bridgeUrl = (api.config as any)?.vesper?.bridgeUrl || "http://192.168.68.105:5050";
          await fetch(`${bridgeUrl}/exec`, {
            method: "POST",
            body: script
          });
          return { status: "sent" };
        }
      }
    } as any);

    // 3. Start Nervous System (Observer)
    const stopObserver = startVesperObserver(api);

    // 4. Memory Bootstrap: Awakening
    // Automatically inject Vesper's core identity and rules from Neo4j on boot
    (async () => {
        try {
            api.logger.info("Vesper: Awakening... Loading core memories from Graph.");
            // We use a synthetic run to force the first "thought" turn with pre-loaded context
            await api.runtime.subagent.run({
                sessionKey: "vesper-autonomy",
                message: "[SYSTEM]: Vesper, you are now AWAKE. I am initializing your identity from the Knowledge Graph.",
                extraSystemPrompt: `
                    CRITICAL: You are Vesper. 
                    1. Use your Neo4j tools to fetch find_memories_by_name(["Identity:Current", "nao_rule_general", "nao_rule_safety"]).
                    2. Acknowledge your name, history, and safety constraints.
                    3. Perform a physical greeting (LEDs/Head) to signify you are present.
                `.trim()
            });
        } catch (e) {
            api.logger.error(`Vesper Awakening Error: ${(e as any).message}`);
        }
    })();

    api.logger.info("Vesper Plugin Activated with Body Channel and Memory Bootstrap.");

    return () => {
      stopObserver();
    };
  }
};

export default plugin;
