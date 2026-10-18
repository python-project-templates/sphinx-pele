import { build } from "esbuild";
import { copyFile, mkdir } from "node:fs/promises";

const outdir = "../sphinx_pele/extension/cdn";
await mkdir(outdir, { recursive: true });
await build({
  entryPoints: {
    "sphinx-pele": "src/ts/index.ts",
  },
  outdir,
  bundle: true,
  minify: true,
  format: "iife",
  target: "es2020",
});
await copyFile("src/css/index.css", `${outdir}/sphinx-pele.css`);
await copyFile("node_modules/pele/LICENSE", `${outdir}/pele-LICENSE`);
