export default {
  async fetch(request, env) {
    // 1. 你的 GitHub 私有仓库 JSON 文件的原始地址
    // 注意：格式为 https://raw.githubusercontent.com/用户名/仓库名/分支名/文件路径
    const GITHUB_RAW_URL = "https://raw.githubusercontent.com/enn844/palmchef-data/main/recipes.json";

    try {
      // 2. 发起带 Token 的请求
      const response = await fetch(GITHUB_RAW_URL, {
        headers: {
          // 这里的 GITHUB_TOKEN 必须在 Cloudflare 控制台的 Variables 中设置
          "Authorization": `Bearer ${env.GITHUB_TOKEN}`,
          "User-Agent": "ShiYuJi-API-Service",
          "Accept": "application/vnd.github.v3.raw"
        }
      });

      // 3. 如果 GitHub 返回错误（比如 Token 无效或文件不存在）
      if (!response.ok) {
        return new Response(JSON.stringify({
          error: "无法从存储中心获取数据",
          status: response.status
        }), { 
          status: response.status,
          headers: { "Content-Type": "application/json" }
        });
      }

      // 4. 读取 JSON 内容
      const data = await response.json();

      // 5. 返回给你的 HarmonyOS 应用，并添加跨域支持
      return new Response(JSON.stringify(data), {
        headers: {
          "Content-Type": "application/json;charset=UTF-8",
          "Access-Control-Allow-Origin": "*", // 允许你的 App 跨域访问
          "Cache-Control": "public, max-age=3600" // 缓存 1 小时，减轻 GitHub 压力
        }
      });

    } catch (error) {
      // 捕获网络或解析错误
      return new Response(JSON.stringify({ error: "服务器内部错误" }), { 
        status: 500,
        headers: { "Content-Type": "application/json" }
      });
    }
  }
};