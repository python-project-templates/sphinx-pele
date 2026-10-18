import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "tests",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: [["line"], ["junit", { outputFile: "junit.xml" }]],
  use: {
    baseURL: "http://127.0.0.1:3000",
    trace: "on-first-retry",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command:
      "python -m sphinx -W -b html ../docs ../docs/_build/html && python -m http.server 3000 --bind 127.0.0.1 --directory ../docs/_build/html",
    url: "http://127.0.0.1:3000",
    reuseExistingServer: false,
  },
});
