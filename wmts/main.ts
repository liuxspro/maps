import { Application } from "jsr:@oak/oak/application";
import { Router } from "jsr:@oak/oak/router";
import { create_capabilities } from "./wmts.ts";

const router = new Router();

router.get("/", (ctx) => {
  ctx.response.body = "On Deno Deploy 💖";
});

router.get("/sdhis/:id/:el", (ctx) => {
  const { id, el } = ctx.params;
  const z = parseInt(el);
  // 获取查询参数
  const url = new URL(ctx.request.url.toString());
  const tk = url.searchParams.get("tk") || "";

  const server_url = `https://service.sdmap.gov.cn/hisimage/${id}`;
  const tile_url = `${server_url}?tk=${tk}&layer=c&style=c&tilematrixset=c&Service=WMTS&Request=GetTile&TileMatrix={z}&TileCol={x}&TileRow={y}`;

  ctx.response.type = "text/xml";
  ctx.response.body = create_capabilities(id, tile_url, 3, z);
});

const app = new Application();
app.use(router.routes());
app.use(router.allowedMethods());

app.listen({ port: 80 });
