import { z } from "zod";
import fs from "node:fs/promises";
import path from "node:path";
import type { OpenClawPluginToolContext, AnyAgentTool } from "openclaw";

/**
 * Diagnostic tool for Vesper's internal logs.
 * Allows the agent to see tracebacks and monitoring status.
 */
export const createNaoDiagnoseTool = (ctx: OpenClawPluginToolContext): AnyAgentTool => {
  const fluentNaoDir = (ctx.runtimeConfig as any)?.vesper?.fluentNaoDir || "/home/dnajd/code/FluentNao";

  return {
    name: "nao_diagnose",
    description: "Read internal logs from the robot's bridge and monitoring systems. Use this to debug Python errors or sensory failures.",
    schema: z.object({
      scope: z.enum(["bridge", "monitor", "full"]).default("bridge").describe("Which logs to retrieve.")
    }),
    execute: async ({ scope }) => {
      try {
        const results: string[] = [];

        if (scope === "bridge" || scope === "full") {
          const bridgeLogPath = path.join(fluentNaoDir, "data/bridge.log");
          try {
            const content = await fs.readFile(bridgeLogPath, "utf-8");
            const lines = content.split("\n").slice(-30).join("\n");
            results.push(`--- BRIDGE LOG (last 30 lines) ---\n${lines}`);
          } catch (err) {
            results.push(`--- BRIDGE LOG ---\nCould not read ${bridgeLogPath}: ${(err as any).message}`);
          }
        }

        if (scope === "monitor" || scope === "full") {
          const monitorLogPath = path.join(fluentNaoDir, "data/monitor.log");
          try {
            const content = await fs.readFile(monitorLogPath, "utf-8");
            const lines = content.split("\n").slice(-20).join("\n");
            results.push(`--- MONITOR LOG (last 20 lines) ---\n${lines}`);
          } catch (err) {
            results.push(`--- MONITOR LOG ---\nCould not read ${monitorLogPath}: ${(err as any).message}`);
          }
        }

        return { content: results.join("\n\n") };
      } catch (err: any) {
        return { content: `Diagnostics failed: ${err.message}`, isError: true };
      }
    }
  };
};
