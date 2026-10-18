# Diagram examples

## Flowchart with frontmatter

```mermaid
---
title: Publishing
config:
  flowchart:
    nodeSpacing: 35
pele:
  autoDirection: false
  fontSize: 18
  cssVariables:
    --pele-accent: "#205ea6"
---
flowchart LR
    Draft --> Review --> Published
```

## Sequence diagram

```{mermaid}
:name: request-flow
:caption: A **request** and response.
:alt: Client requests a page from the server.
:zoom: true
:width: 75%

sequenceDiagram
    Client->>Server: GET /docs
    Server-->>Client: HTML
```

## External file

```{mermaid} publishing.mmd
:caption: Loaded from a Mermaid document.
```

## Pie chart

```mermaid
pie title Tasks
    "Complete" : 8
    "Remaining" : 2
```
