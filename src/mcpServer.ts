import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { query, getRecord, stats } from "./core.js";

export const server = new Server(
  { name: "taxi-trips-dataset", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler("list_tools", async () => ({
  tools: [
    {
      name: "query_dataset",
      description: "Filter Individual taxi trip records by field equality and paginate",
      inputSchema: {
        type: "object",
        properties: {
          filters: { type: "object", description: "Field equality filters, e.g. { city: \"London\" }" },
          limit: { type: "number", default: 25 },
          offset: { type: "number", default: 0 },
        },
      },
    },
    {
      name: "get_record",
      description: "Fetch a single record by id field",
      inputSchema: {
        type: "object",
        properties: {
          idValue: { type: "string" },
          idField: { type: "string", default: "id" },
        },
        required: ["idValue"],
      },
    },
    {
      name: "get_stats",
      description: "Summary statistics (min/max/mean) for numeric fields",
      inputSchema: { type: "object", properties: {} },
    },
  ],
}));

server.setRequestHandler("call_tool", async (request) => {
  const { name, arguments: args } = request.params;
  if (name === "query_dataset") {
    const r = await query(args.filters || {}, args.limit || 25, args.offset || 0);
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  }
  if (name === "get_record") {
    const r = await getRecord(args.idValue, args.idField || "id");
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  }
  if (name === "get_stats") {
    const r = await stats();
    return { content: [{ type: "text", text: JSON.stringify(r, null, 2) }] };
  }
  throw new Error("Unknown tool");
});
