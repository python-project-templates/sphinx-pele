import { test, expect } from "@playwright/test";

test("renders Sphinx diagrams offline with options, captions, and unique SVG IDs", async ({
  page,
}) => {
  const errors = [];
  const remote = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.route("**/*", (route) => {
    if (!route.request().url().startsWith("http://127.0.0.1:3000/")) {
      remote.push(route.request().url());
      return route.abort();
    }
    return route.continue();
  });
  await page.goto("/src/examples.html");
  await expect(page.locator(".sphinx-pele svg.pele")).toHaveCount(16);
  await expect(page.locator(".sphinx-pele").first()).toContainText(
    "Publishing",
  );
  await expect(page.locator("#request-flow .caption-text")).toContainText(
    "A request and response.",
  );
  await expect(page.locator("#request-flow .sphinx-pele")).toHaveAttribute(
    "aria-label",
    "Client requests a page from the server.",
  );
  await expect(page.locator(".sphinx-pele").first()).toHaveCSS(
    "--pele-accent",
    "#205ea6",
  );
  await expect(page.locator(".sphinx-pele svg text").first()).toHaveCSS(
    "font-size",
    "18px",
  );
  await expect(
    page.locator(".sphinx-pele").first().getByRole("button"),
  ).toHaveCount(0);
  const zoom = page
    .locator("#request-flow")
    .getByRole("button", { name: "Zoom in", exact: true });
  await expect(zoom).toBeVisible();
  const viewport = await page
    .locator("#request-flow svg.pele")
    .getAttribute("viewBox");
  await zoom.click();
  await expect(page.locator("#request-flow svg.pele")).not.toHaveAttribute(
    "viewBox",
    viewport,
  );
  const wide = await page
    .locator(".sphinx-pele svg.pele")
    .first()
    .boundingBox();
  const ids = await page
    .locator(".sphinx-pele svg [id]")
    .evaluateAll((nodes) => nodes.map((node) => node.id));
  expect(new Set(ids).size).toBe(ids.length);
  expect(remote).toEqual([]);
  expect(errors).toEqual([]);
  await page.setViewportSize({ width: 375, height: 800 });
  await expect
    .poll(
      async () =>
        (await page.locator(".sphinx-pele svg.pele").first().boundingBox())
          ?.width ?? Infinity,
    )
    .toBeLessThan(wide.width);
  await expect(page.locator(".sphinx-pele svg.pele")).toHaveCount(16);
});

test("source remains readable without JavaScript", async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto("http://127.0.0.1:3000/src/examples.html");
  await expect(page.locator(".sphinx-pele pre").first()).toContainText(
    "flowchart LR",
  );
  await context.close();
});

test("a malformed diagram does not stop subsequent diagrams or execute source", async ({
  page,
}) => {
  await page.goto("/index.html");
  await page.evaluate(() => {
    for (const source of [
      "<img src=x onerror=window.injected=true>",
      "flowchart LR\n A --> B",
    ]) {
      const container = document.createElement("div");
      container.className = "sphinx-pele";
      const pre = document.createElement("pre");
      pre.textContent = source;
      container.append(pre);
      document.body.append(container);
    }
  });
  await page.addScriptTag({ url: "/_static/sphinx-pele.js" });
  await expect(page.locator(".sphinx-pele").first()).toContainText(
    /unsupported|diagram/i,
  );
  await expect(page.locator(".sphinx-pele svg.pele")).toHaveCount(1);
  expect(await page.evaluate(() => window.injected)).toBeUndefined();
});

test("documentation homepage links to guides and reStructuredText examples render", async ({
  page,
}) => {
  await page.goto("/");
  await expect(
    page
      .locator(".body")
      .getByRole("heading", { name: "sphinx-pele", exact: true }),
  ).toBeVisible();
  await expect(
    page.locator('.document a[href="src/tutorial.html"]').first(),
  ).toBeVisible();
  await page.goto("/src/rst-examples.html");
  await expect(page.locator(".sphinx-pele")).toHaveCount(4);
  await expect(page.locator(".sphinx-pele svg.pele")).toHaveCount(4);
  await expect(page.locator("#review-states .caption-text")).toContainText(
    "Document review states",
  );
  await expect(
    page.getByRole("button", { name: "Enlarge", exact: true }),
  ).toBeVisible();
  await expect(page.locator(".sphinx-pele-title")).toHaveText(
    "Review decision",
  );
});
