const filePath = "./mapdata.json";

const fileContent = await Deno.readTextFile(filePath);

// 将 JSON 字符串解析为 JavaScript 对象
const jsonData = JSON.parse(fileContent);

// 按照 st 字段进行排序
jsonData.sort((a, b) => b.st - a.st);

// 输出排序后的数据
// console.log(jsonData);

jsonData.forEach((element) => {
  const name = element.name;
  const url = element.url;
  const map_id = url.split("/").at(-1);
  const el = element.el;
  const r = `    - name: 山东 - ${name}
      uri: crs=EPSG:4490&dpiMode=7&featureCount=10&format=image/png&layers=${map_id}&styles=default&tileMatrixSet=default028mm&tilePixelRatio=0&url=https://wmts.deno.dev/sdhis/${map_id}/${el}?tk%3Dee5c67bbafffd91385530796fb58d0f6`;
  console.log(r);
});
