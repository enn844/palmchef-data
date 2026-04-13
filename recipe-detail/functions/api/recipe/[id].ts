/**
 * Cloudflare Pages Function：GET /api/recipe/:id
 *
 * 部署：以本目录 `recipe-detail` 作为 Pages 项目根（与 index.html、recipe/ 同级），
 * 将 `functions/` 与 `_routes.json` 一并随 Git / wrangler pages deploy 发布。
 *
 * 环境变量（Cloudflare Pages → 设置 → 环境变量）：
 *   RECIPE_API_ORIGIN — 上游 API 根地址，无尾部斜杠，例如 https://api.example.com
 *   实际请求：${RECIPE_API_ORIGIN}/api/recipe/${id}
 *
 * 若上游路径不同，请改下方 buildUpstreamUrl。
 */

interface Env {
  RECIPE_API_ORIGIN: string;
}

const JSON_HEADERS = {
  "content-type": "application/json; charset=utf-8",
  "cache-control": "public, max-age=60, s-maxage=300",
};

function json(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: JSON_HEADERS,
  });
}

function buildUpstreamUrl(origin: string, id: string): string {
  const base = origin.replace(/\/+$/, "");
  const safeId = encodeURIComponent(id);
  return `${base}/api/recipe/${safeId}`;
}

export async function onRequestGet(context: {
  request: Request;
  env: Env;
  params: Record<string, string | string[] | undefined>;
}): Promise<Response> {
  const rawId = context.params.id;
  const id = Array.isArray(rawId) ? rawId[0] : rawId;
  if (!id || typeof id !== "string") {
    return json(400, { error: "missing_id", message: "路径中缺少菜谱 id" });
  }

  const origin = context.env.RECIPE_API_ORIGIN;
  if (!origin || typeof origin !== "string") {
    return json(503, {
      error: "misconfigured",
      message: "未配置 RECIPE_API_ORIGIN，请在 Pages 环境变量中设置上游 API 根地址",
    });
  }

  const url = buildUpstreamUrl(origin, id);
  let upstream: Response;
  try {
    upstream = await fetch(url, {
      method: "GET",
      headers: {
        accept: "application/json",
        "user-agent": context.request.headers.get("user-agent") ?? "recipe-detail-pages-proxy",
      },
    });
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return json(502, { error: "upstream_fetch_failed", message: msg });
  }

  const ct = upstream.headers.get("content-type") ?? "";
  const body = await upstream.arrayBuffer();

  const headers = new Headers();
  headers.set("content-type", ct.includes("json") ? ct : "application/json; charset=utf-8");
  headers.set("cache-control", upstream.headers.get("cache-control") ?? "public, max-age=60");

  return new Response(body, { status: upstream.status, statusText: upstream.statusText, headers });
}
