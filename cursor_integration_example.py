"""
SVG Generator MCP - Cursor IDE Integration Example

This example shows how to use the SVG Generator MCP with Cursor IDE.
"""

from fastmcp import Client

async def get_svg_guide():
    """
    Example of getting the SVG generation guide.
    """
    async with Client("svg_mcp_server.py") as client:
        # Get the guide for generating SVG
        result = await client.call_tool("generate_svg_guide")
        
        # Print the guide
        print("SVG Generation Guide:")
        print(f"Title: {result.content['title']}")
        print(f"Description: {result.content['description']}")
        
        print("\nSteps:")
        for step in result.content['steps']:
            print(f"- {step}")
        
        print("\nExample Prompts:")
        for example in result.content['example_prompts']:
            print(f"- {example['title']}: \"{example['prompt']}\"")

async def get_prompt_examples(category="icons"):
    """
    Example of getting SVG prompt examples.
    """
    async with Client("svg_mcp_server.py") as client:
        # Get SVG prompt examples
        result = await client.call_tool("svg_prompt_examples", {"category": category})
        
        if result.content['success']:
            print(f"\nSVG Prompt Examples for '{category}':")
            # Check if examples is a list (for specific category) or dict (for 'all')
            if isinstance(result.content['examples'], list):
                for example in result.content['examples']:
                    print(f"- \"{example}\"")
            elif isinstance(result.content['examples'], dict): # Handle 'all' category
                for cat, exs in result.content['examples'].items():
                    print(f"  Category: {cat}")
                    for ex in exs:
                        print(f"  - \"{ex}\"")
        else:
            print(f"\nError: {result.content['error']}")

# How to use:
"""
To run this example, you need to have the SVG Generator MCP server running.

1. In one terminal, run:
   python svg_mcp_server.py

2. In another terminal, run:
   python -c "import asyncio; from cursor_integration_example import get_svg_guide, get_prompt_examples; asyncio.run(get_svg_guide()); asyncio.run(get_prompt_examples('illustrations'))"

But the main purpose of this MCP is to provide guidance for using Cursor IDE's built-in AI to generate SVG directly:

1. Open Cursor IDE
2. Create a new file with .svg extension
3. Use the AI to generate SVG based on the examples
   Example prompt: "Generate an SVG icon of a house with a chimney"
4. The AI will generate the SVG code directly in your editor
5. Save and view the SVG in a browser
""" 