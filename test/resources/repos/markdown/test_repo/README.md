# Project Documentation

This is the main documentation file for testing Markdown symbol operations.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)

## Introduction

This section provides an overview of the project. It contains multiple paragraphs
and demonstrates the hierarchical structure of Markdown documents.

### Background

Some background information about the project.

### Goals

The main goals of this project are:
1. Test symbol detection in Markdown
2. Validate link references
3. Support navigation features

## Installation

```bash
npm install marksman
```

### Prerequisites

Before installing, ensure you have:
- Node.js >= 18.0.0
- npm >= 9.0.0

### Step-by-step Guide

1. Clone the repository
2. Install dependencies
3. Run the application

## Usage

Here's how to use the project:

```javascript
const example = require('example');
example.run();
```

### Basic Example

This is a basic usage example.

### Advanced Example

This demonstrates more complex usage patterns.

## API Reference

### Functions

#### `processMarkdown(text)`

Processes markdown text and returns structured data.

**Parameters:**
- `text` (string): The markdown text to process

**Returns:**
- Object: Processed markdown structure

#### `validateLinks(doc)`

Validates all links in the document.

### Classes

#### `MarkdownParser`

Main parser class for processing Markdown documents.

##### Methods

- `parse(text)`: Parses the markdown text
- `getSymbols()`: Returns document symbols
- `findReferences(symbol)`: Finds references to a symbol

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Code of Conduct

We follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Footnotes

[^1]: This is a footnote example.
[^2]: Another footnote with more information.

## References

- [Marksman GitHub](https://github.com/artempyanykh/marksman)
- [CommonMark Spec](https://commonmark.org/)
- [Markdown Guide](https://www.markdownguide.org/)