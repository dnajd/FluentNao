import { z } from "zod";
import type { OpenClawPluginToolContext, AnyAgentTool } from "openclaw";

/**
 * Generative Python execution tool for Vesper.
 * Allows the agent to send raw Python code to the FluentNao bridge.
 */
export const createNaoExecuteTool = (ctx: OpenClawPluginToolContext): AnyAgentTool => {
  const bridgeUrl = (ctx.runtimeConfig as any)?.vesper?.bridgeUrl || "http://192.168.68.105:5050";

  return {
    name: "nao_execute",
    description: "Execute a multi-line Python 2.7 script on the NAO robot via the FluentNao bridge. Use this to control the robot's body (say, move, sense).",
    schema: z.object({
      script: z.string().describe("The multi-line Python script to execute. The 'nao' object is available in the global scope.")
    }),
    execute: async ({ script }) => {
      try {
        const response = await fetch(`${bridgeUrl}/exec`, {
          method: "POST",
          headers: { "Content-Type": "text/plain" },
          body: script
        });

        const result = await response.json();
        
        if (!result.ok) {
          return {
            content: `Execution failed: ${result.error}\n\nTIP: Use nao_diagnose() to see the full Python traceback in the bridge logs.`,
            isError: true
          };
        }

        return {
          content: result.result !== undefined ? `Result: ${result.result}` : "Success (no return value)"
        };
      } catch (err: any) {
        return {
          content: `Failed to connect to FluentNao bridge at ${bridgeUrl}: ${err.message}`,
          isError: true
        };
      }
    }
  };
};
