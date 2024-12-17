const ScaleDenominatorList = [
  559082264.0287178, 279541132.0143589, 139770566.00717944, 69885283.00358972,
  34942641.50179486, 17471320.75089743, 8735660.375448715, 4367830.1877243575,
  2183915.0938621787, 1091957.5469310894, 545978.7734655447, 272989.38673277234,
  136494.69336638617, 68247.34668319309, 34123.67334159654, 17061.83667079827,
  8530.918335399136, 4265.459167699568, 2132.729583849784, 1066.364791924892,
  533.182395962446, 266.591197981223,
];

function create_TileMatrixs(min: number = 0, max: number = 18): string {
  let matrixs = "";
  for (let i = min; i <= max; i++) {
    const width = 1 << i;
    let height = 1;
    if (i != 0) {
      height = width / 2;
    }
    matrixs += `      <TileMatrix>
          <ows:Identifier>${i}</ows:Identifier>
          <ScaleDenominator>${ScaleDenominatorList[i]}</ScaleDenominator>
          <TopLeftCorner>90 -180</TopLeftCorner>
          <TileWidth>256</TileWidth>
          <TileHeight>256</TileHeight>
          <MatrixWidth>${width}</MatrixWidth>
          <MatrixHeight>${height}</MatrixHeight>
        </TileMatrix>
  `;
  }
  return matrixs;
}

export function create_capabilities(
  name: string,
  url: string,
  zmin: number,
  zmax: number
): string {
  const matrixs = create_TileMatrixs(zmin, zmax);
  const u = url
    .replace(/\{z\}/g, "{TileMatrix}")
    .replace(/\{x\}/g, "{TileCol}")
    .replace(/\{y\}/g, "{TileRow}")
    .replace(/&/g, "&amp;");
  return `<?xml version="1.0"?>
<Capabilities xmlns="http://www.opengis.net/wmts/1.0"
  xmlns:ows="http://www.opengis.net/ows/1.1"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns:gml="http://www.opengis.net/gml"
  xsi:schemaLocation="http://www.opengis.net/wmts/1.0 http://schemas.opengis.net/wmts/1.0/wmtsGetCapabilities_response.xsd"
  version="1.0.0">
  <ows:ServiceIdentification>
    <ows:Title>山东天地图历史影像</ows:Title>
    <ows:Abstract>山东天地图历史影像</ows:Abstract>
    <ows:ServiceType>OGC WMTS</ows:ServiceType>
    <ows:ServiceTypeVersion>1.0.0</ows:ServiceTypeVersion>
    <ows:Fees>none</ows:Fees>
    <ows:AccessConstraints>none</ows:AccessConstraints>
  </ows:ServiceIdentification>
  <Contents>
    <Layer>
      <ows:Title>${name}</ows:Title>
      <ows:Abstract>${name}</ows:Abstract>
      <ows:WGS84BoundingBox>
        <ows:LowerCorner>114.2298 33.9389</ows:LowerCorner>
        <ows:UpperCorner>123.4005 38.9048</ows:UpperCorner>
      </ows:WGS84BoundingBox>
      <ows:Identifier>${name}</ows:Identifier>
      <Style>
        <ows:Identifier>default</ows:Identifier>
      </Style>
      <Format>image/png</Format>
      <TileMatrixSetLink>
        <TileMatrixSet>default028mm</TileMatrixSet>
      </TileMatrixSetLink>
      <ResourceURL format="image/png" resourceType="tile"
        template="${u}" />
    </Layer>
    <!-- 瓦片矩阵集 -->
    <TileMatrixSet>
      <ows:Identifier>default028mm</ows:Identifier>
      <ows:SupportedCRS>urn:ogc:def:crs:EPSG::4490</ows:SupportedCRS>
      ${matrixs.trim()}
    </TileMatrixSet>
  </Contents>
</Capabilities>`;
}
