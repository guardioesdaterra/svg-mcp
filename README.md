# SVG-MCP for Cursor IDE

A Model Context Protocol (MCP) server that provides tools and guidance for generating SVG code directly within Cursor IDE.

## Features

- Provides guidance on generating SVGs with Cursor IDE's AI
- Offers example prompts optimized for AI SVG generation
- Includes SVG best practices and optimization guidelines
- Uses Cursor IDE's integrated AI model
- Features intelligent style detection based on natural language prompts

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the MCP server with stdio transport for direct integration with Cursor IDE:

```bash
python svg_mcp_server.py
```

The server communicates directly with Cursor IDE through the Model Context Protocol (MCP).

## Available Tools

### `generate_svg_guide`

Provides a comprehensive guide for generating SVG using Cursor IDE's AI capabilities.

### `svg_prompt_examples`

Provides example prompts for generating different types of SVG with AI.

Example:
```python
result = await client.call_tool("svg_prompt_examples", {"category": "icons"})
examples = result.content["examples"]
```

### `svg_best_practices`

Returns a list of best practices for SVG generation and optimization.

### `generate_svg_from_prompt`

Takes a textual prompt and generates an SVG based on style analysis and content detection. The tool uses advanced reasoning to identify the appropriate style from the prompt's language rather than simple keyword matching.

Available style categories:
- Cyberpunk
- Minimalist
- Abstract
- Retro
- Nature
- Corporate
- Fantasy
- General (fallback)

Example:
```python
result = await client.call_tool("generate_svg_from_prompt", {"prompt": "A futuristic cyberpunk city skyline"})
if result.content.get("success"):
    svg_code = result.content.get("svg_code")
    detected_style = result.content.get("detected_style")  # Returns "cyberpunk" in this example
    # Now you can use/display the svg_code
```

#### Style Detection Features

The style detection uses advanced reasoning to understand your intent:

- Analyzes context and phrases beyond simple keywords
- Resolves ambiguous prompts by prioritizing the most relevant style
- Handles tie-breaking for prompts with multiple style indicators
- Returns the detected style in the response

For example, "a simple geometric pattern with clean lines" would be detected as "minimalist" style, while "a glowing circuit board with neon paths" would be detected as "cyberpunk" style.

## Resources

The server also provides resources that can be accessed via the MCP protocol:

- `examples://svg-snippets` - Useful SVG code snippets that can be used as building blocks

## How to Generate SVGs with Cursor IDE

1. Create a new file with `.svg` extension
2. Get SVG prompt examples with the MCP tools
3. Ask Cursor's AI to generate SVG based on the examples
4. View and modify the SVG in your editor
5. Use the best practices guide for optimization 