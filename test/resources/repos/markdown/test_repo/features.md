# Markdown Features

This document demonstrates various Markdown features for testing.

## Basic Formatting

**Bold text**, *italic text*, and ***bold italic text***.

`Inline code` and ~~strikethrough~~.

## Lists

### Unordered List

- First item
  - Nested item 1
  - Nested item 2
    - Deep nested item
- Second item
- Third item

### Ordered List

1. First step
2. Second step
   1. Sub-step A
   2. Sub-step B
3. Third step

### Task List

- [x] Completed task
- [ ] Pending task
- [ ] Another pending task
  - [x] Completed subtask
  - [ ] Pending subtask

## Tables

| Feature | Support | Notes |
|---------|---------|-------|
| Headers | Yes | H1-H6 supported |
| Links | Yes | Internal and external |
| Images | Yes | With alt text |
| Code | Yes | Fenced and inline |
| Tables | Yes | GFM style |

### Complex Table

| Language | File Extension | LSP Server |
|----------|---------------|------------|
| Markdown | `.md` | Marksman |

## Code Blocks

### YAML Example

```yaml
name: Test
version: 1.0.0
dependencies:
  - marksman
  - node
```

## Links and Images

### Internal Links

- Link to [Introduction](README.md#introduction)
- Link to [Contributing](CONTRIBUTING.md)
- Link to [Top of Page](#markdown-features)

### External Links

- [GitHub](https://github.com)
- [Markdown Guide](https://www.markdownguide.org)
- [CommonMark](https://commonmark.org)

### Images

![Alt text](image.png)
![Another image](https://example.com/image.jpg)

## Blockquotes

> This is a blockquote.
> It can span multiple lines.
>
> > This is a nested blockquote.
> > With multiple lines as well.

## Horizontal Rules

---

## HTML Elements

<details>
<summary>Click to expand</summary>

This content is hidden by default.

</details>

## Math (if supported)

Inline math: $E = mc^2$

Block math:

$$
\frac{1}{2} \sum_{i=1}^{n} x_i^2
$$

## Definitions

Term 1
: Definition of term 1

Term 2
: Definition of term 2
: Alternative definition

## Admonitions (if supported)

!!! note
    This is a note admonition.

!!! warning
    This is a warning admonition.

## Front Matter

---
title: Features Document
author: Test Author
date: 2024-01-01
tags: [test, markdown, features]
---

## Wiki Links (if supported)

[[README]]
[[CONTRIBUTING|How to Contribute]]

## Conclusion

This document covers most Markdown features for comprehensive testing.
