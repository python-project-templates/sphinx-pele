import { mount, type MountOptions } from "pele";

function renderDiagrams() {
  for (const element of document.querySelectorAll<HTMLElement>(
    ".sphinx-pele",
  )) {
    const source = element.querySelector("pre")?.textContent;
    if (!source || element.dataset.peleMounted) continue;
    element.dataset.peleMounted = "true";
    const options: MountOptions = JSON.parse(
      element.dataset.peleOptions || "{}",
    );
    const variables: Record<string, string> = JSON.parse(
      element.dataset.peleCss || "{}",
    );
    for (const [name, value] of Object.entries(variables)) {
      element.style.setProperty(name, value);
    }
    for (const dimension of ["width", "height"] as const) {
      const value =
        element.dataset[dimension === "width" ? "peleWidth" : "peleHeight"];
      if (value)
        element.style[dimension] = /^\d+(\.\d+)?$/.test(value)
          ? `${value}px`
          : value;
    }
    if (element.dataset.peleTitle) {
      const heading = document.createElement("p");
      heading.className = "sphinx-pele-title";
      heading.textContent = element.dataset.peleTitle;
      element.before(heading);
    }
    mount(element, source, options);
  }
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", renderDiagrams, { once: true });
} else {
  renderDiagrams();
}
