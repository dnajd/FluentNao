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
        listAccountIds: async () => ["vesper-body"],
        resolveAccount: async (id) => ({ id: "vesper-body", name: "NAO" })
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

    api.logger.info("Vesper Plugin Activated with Body Channel.");

    return () => {
      stopObserver();
    };
  }
};

export default plugin;
