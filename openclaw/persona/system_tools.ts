import { z } from "zod";
import { exec } from "node:child_process";
import { promisify } from "node:util";
import type { OpenClawPluginToolContext, AnyAgentTool } from "openclaw";

const execAsync = promisify(exec);

/**
 * Infrastructure tools for Vesper to maintain her own "Body" container.
 */
export const createVesperSystemTools = (ctx: OpenClawPluginToolContext): AnyAgentTool[] => {
  return [
    {
      name: "bridge_restart",
      description: "Perform a hard restart of the FluentNao Docker bridge. Use this only if nao_diagnose shows the bridge is unresponsive or if deep infrastructure changes were made.",
      schema: z.object({}),
      execute: async () => {
        try {
          // Note: This assumes the agent has permission to run docker commands on the host.
          // In the bb-turnkey environment, we target the specific service.
          const { stdout, stderr } = await execAsync("cd ~/code/FluentNao && docker compose restart fluentnao");
          return {
            content: `Bridge restart initiated.\nSTDOUT: ${stdout}\nSTDERR: ${stderr}\n\nNOTE: The observer will automatically reconnect in ~10 seconds.`
          };
        } catch (err: any) {
          return {
            content: `Failed to restart bridge: ${err.message}`,
            isError: true
          };
        }
      }
    }
  ];
};
