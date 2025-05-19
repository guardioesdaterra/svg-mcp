import os
import json
import re
import math
from typing import Dict, List, Optional, Any
from fastmcp import FastMCP, Context
import sys

print("--- SVG MCP Server: Starting script ---", file=sys.stderr)
print(f"--- SVG MCP Server: Received command-line arguments: {sys.argv} ---", file=sys.stderr)

# Initialize the MCP server
print("--- SVG MCP Server: Initializing FastMCP ---", file=sys.stderr)
mcp = FastMCP("Cursor SVG Generator")
print("--- SVG MCP Server: FastMCP initialized ---", file=sys.stderr)

@mcp.tool()
async def generate_svg_guide(ctx: Context) -> Dict[str, Any]:
    """
    Provides a guide for generating SVG using the IDE's model.
    
    This tool gives detailed instructions on how to generate SVG code directly using 
    Claude or other AI models in Cursor IDE.
    
    Args:
        ctx: The MCP context
        
    Returns:
        A dictionary with instructions and example prompts
    """
    await ctx.info("Retrieving SVG generation guide")
    
    return {
        "title": "Guide to Generating SVG with Cursor IDE",
        "description": "This guide provides instructions on how to use the AI model in Cursor IDE to generate SVG code directly. SVGs are powerful for creating scalable, crisp graphics for the web and beyond.",
        "steps": [
            "1. Create or open a file with .svg extension (e.g., 'my_icon.svg').",
            "2. Use the Cursor IDE's AI capabilities with a clear, descriptive prompt (see examples from `svg_prompt_examples` tool).",
            "3. The AI will generate the SVG code directly in your editor.",
            "4. Review the generated code. You can ask the AI for modifications or edit it manually.",
            "5. Save the file and view it in a browser or SVG viewer to ensure it meets your expectations."
        ],
        "styling_your_svgs": {
            "title": "Styling Your SVGs",
            "points": [
                {
                    "point": "Prioritize Your Vision",
                    "details": "Clearly describe your desired style in your prompt (e.g., 'minimalist logo', 'vintage illustration', 'flat design icon', 'neumorphic button'). The AI will attempt to match it."
                },
                {
                    "point": "Modern by Default",
                    "details": "If you don't specify a particular style, prompts will generally guide the AI towards clean, modern aesthetics suitable for contemporary web design."
                },
                {
                    "point": "Leverage CSS for Styling",
                    "details": "For consistent styling across multiple elements or for complex styles, ask the AI to generate SVGs that utilize internal CSS (`<style>` tags) or are designed to be styled by external CSS. This is a best practice for web SVGs (see `svg_best_practices` tool for more)."
                },
                {
                    "point": "Specify Colors and Dimensions",
                    "details": "Be explicit about colors (e.g., 'a blue circle with a #FF0000 red border'), sizes (e.g., 'an icon 24x24 pixels'), and viewBox for proper scaling."
                }
            ]
        },
        "understanding_svg_fundamentals": {
            "title": "Understanding SVG Fundamentals",
            "points": [
                {
                    "point": "Vector Power",
                    "details": "SVGs (Scalable Vector Graphics) use mathematical formulas, not pixels. This means they can be scaled to any size (tiny icon or large billboard) without losing quality or becoming blurry. Perfect for responsive web graphics, logos, and illustrations. (Source: Adobe, W3C)"
                },
                {
                    "point": "XML-Based Structure",
                    "details": "SVGs are written in XML (eXtensible Markup Language), making them text-based. You can inspect, edit, and manipulate SVG code directly. Text within SVGs remains actual text, which is excellent for accessibility (screen readers can read it) and SEO (search engines can index the content). (Source: Adobe, MDN)"
                },
                {
                    "point": "Common Use Cases",
                    "details": "Ideal for logos, icons, illustrations, charts, maps, and any 2D graphics that need to be crisp, scalable, and performant on the web. For complex, detailed photographs, raster formats like JPEG or PNG are often more suitable. (Source: Adobe)"
                },
                {
                    "point": "Interactivity and Animation",
                    "details": "SVGs can be made interactive using JavaScript and styled or animated using CSS or SMIL (Synchronized Multimedia Integration Language), though CSS is often preferred for web animations. (Source: Adobe, W3C, MDN)"
                },
                {
                    "point": "Key Elements",
                    "details": "Common SVG elements include `<circle>`, `<rect>`, `<line>`, `<path>` (for complex shapes), `<text>`, `<g>` (for grouping), `<defs>` (for definitions like gradients), and `<use>` (to reuse elements)."
                },
                {
                    "point": "Further Learning",
                    "details": "For in-depth knowledge, explore resources like the Mozilla Developer Network (MDN) SVG Tutorial, W3Schools SVG Tutorial, and the official W3C SVG Specifications."
                }
            ]
        },
        "example_prompts_info": "Use the `svg_prompt_examples` tool to get specific prompt ideas for various categories like icons, charts, and illustrations.",
        "best_practices_info": "Consult the `svg_best_practices` tool for detailed guidelines on creating optimized, accessible, and maintainable SVGs."
    }
print("--- SVG MCP Server: Tool 'generate_svg_guide' registered ---", file=sys.stderr)

@mcp.tool()
async def svg_prompt_examples(ctx: Context, category: str = "all") -> Dict[str, Any]:
    """
    Provides example prompts for generating SVG with an AI model.
    
    Args:
        ctx: The MCP context
        category: Category of SVG examples ('all', 'shapes', 'icons', 'illustrations', 'charts', 
                  'ui_elements', 'logos', 'abstract_patterns', 'data_visualizations')
        
    Returns:
        A dictionary with example prompts in the specified category
    """
    await ctx.info(f"Retrieving SVG prompt examples for category: {category}")
    
    examples = {
        "shapes": [
            "Create an SVG of a red circle with blue border, 3px width, on a transparent background",
            "Generate SVG code for a rounded rectangle with gradient from blue to purple",
            "Create an SVG with three overlapping transparent circles in red, green, and blue",
            "Generate an SVG star shape with 5 points and yellow fill",
            "SVG of an ellipse with a dashed stroke and orange fill",
            "Create a polygon with 7 sides, green fill and black stroke"
        ],
        "icons": [
            "Create an SVG icon of a simple house with a chimney",
            "Generate an SVG hamburger menu icon with three lines",
            "Create an SVG search icon with a magnifying glass",
            "Generate an SVG settings gear icon with 8 teeth",
            "SVG user profile icon, minimalist style",
            "Generate a download arrow icon, flat design",
            "Create a shopping cart icon with a small badge",
            "SVG notification bell icon with a subtle animation hint",
            "Generate a simple folder icon in blue tones",
            "Create an SVG checkmark icon, bold and green"
        ],
        "illustrations": [
            "Create a simple SVG landscape with mountains, a sun, and trees",
            "Generate an SVG cityscape with buildings of different heights",
            "Create an SVG of a sailing boat on waves",
            "Generate a simple SVG face with basic features",
            "SVG illustration of a coffee cup with steam, retro style",
            "Create a whimsical illustration of a cat playing with yarn",
            "Generate an SVG for a stack of books with one open"
        ],
        "charts": [ # This can be deprecated or merged into data_visualizations
            "Create a simple SVG bar chart with 4 bars in different colors",
            "Generate an SVG pie chart divided into 3 sections",
            "Create an SVG line graph showing an upward trend",
            "Generate a simple SVG scatter plot with 5 points"
        ],
        # --- BEGIN NEW CATEGORIES AND EXAMPLES ---
        "ui_elements": [
            "Generate an SVG for a sleek, modern button with a slight gradient",
            "Create an SVG toggle switch in the 'on' state, cyberpunk style",
            "SVG for a progress bar at 75% completion, minimalist",
            "Generate a set of 3 radio buttons, one selected, simple style",
            "Create an SVG slider control with a circular handle"
        ],
        "logos": [
            "Generate a minimalist SVG logo for a tech startup named 'Nova'",
            "Create an abstract geometric logo with a sense of motion, using blue and green",
            "SVG logo for a coffee shop, vintage style, with a coffee bean element",
            "Generate a text-based logo for 'EcoWorld' with a leaf integrated into the text",
            "Create a corporate-style shield logo with the letter 'S' in the center"
        ],
        "abstract_patterns": [
            "Generate an SVG seamless pattern of intertwined circles, monochrome",
            "Create an abstract SVG background with flowing organic shapes, nature palette",
            "SVG of a repeating geometric pattern with triangles and hexagons, art deco style",
            "Generate a dynamic abstract pattern with glitch art effects",
            "Create a simple wave pattern SVG, suitable for a website footer"
        ],
        "data_visualizations": [
            "Generate an SVG for a donut chart with 4 segments and percentage labels",
            "Create a horizontal bar graph comparing three products, corporate style",
            "SVG for a simple flowchart with 3 steps and connecting arrows",
            "Generate a radial progress indicator for a fitness app",
            "Create an SVG representation of a network graph with 5 nodes and connections"
        ]
        # --- END NEW CATEGORIES AND EXAMPLES ---
    }
    
    if category == "all":
        return {
            "success": True,
            "category": "all",
            "examples": {cat: exs for cat, exs in examples.items()}
        }
    
    if category not in examples:
        return {
            "success": False,
            "error": f"Category '{category}' not found. Available categories: all, {', '.join(examples.keys())}",
            "examples": None
        }
    
    return {
        "success": True,
        "category": category,
        "examples": examples[category]
    }
print("--- SVG MCP Server: Tool 'svg_prompt_examples' registered ---", file=sys.stderr)

@mcp.tool()
async def svg_best_practices(ctx: Context) -> Dict[str, Any]:
    """
    Provides best practices for SVG generation and optimization.
    
    Args:
        ctx: The MCP context
        
    Returns:
        A dictionary with SVG best practices
    """
    await ctx.info("Retrieving SVG best practices")
    
    return {
        "success": True,
        "title": "SVG Best Practices for AI Generation and Web Use",
        "introduction": "Follow these best practices when prompting an AI to generate SVGs and for optimizing them for web and general use. These are based on common guidelines and information from sources like Adobe, W3C, and MDN.",
        "best_practices": [
            {
                "title": "Use appropriate viewBox",
                "description": "Always include a `viewBox` attribute (e.g., `viewBox='0 0 100 100'`) to define the coordinate system and aspect ratio, ensuring proper scaling across different sizes and containers. The AI should include this by default if asked for a standard icon or graphic.",
                "example": '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">...</svg>'
            },
            {
                "title": "Optimize Path Data",
                "description": "Request optimized path data. This includes using relative commands (lowercase, e.g., `m` instead of `M` if appropriate), short command letters, and minimizing unnecessary precision in coordinates. Complex SVGs can be simplified using tools like SVGO.",
                "example": "Prompt: 'Generate a compact SVG path for a heart shape.' Output: '<path d=\"M10 10L90 10L90 90L10 90z\" fill=\"red\" /> (Example, actual path will differ)'"
            },
            {
                "title": "Use CSS for Styling (Highly Recommended for Web)",
                "description": "For web use, prefer styling SVGs with CSS (either in a `<style>` block within the SVG or via external stylesheets) instead of relying solely on presentation attributes (e.g., `fill='blue'` on an element). This improves maintainability, allows for easier theming, and enables hover effects or animations with CSS. Ask the AI to 'style using CSS classes'.",
                "example": "<style>\n  .icon-primary { fill: blue; stroke: navy; }\n</style>\n<circle class='icon-primary' cx='50' cy='50' r='40' />"
            },
            {
                "title": "Reuse Elements with `<symbol>` and `<use>`",
                "description": "For repeating graphics (like icons in a set or elements in a pattern), define them once with `<symbol>` within a `<defs>` section and then instance them with `<use href='#symbol-id'>`. This significantly reduces file size and complexity.",
                "example": "<defs><symbol id='myIcon' viewBox='0 0 24 24'><path d='...'></path></symbol></defs> <use href='#myIcon' x='10' y='10' /> <use href='#myIcon' x='50' y='10' />"
            },
            {
                "title": "Minimize Decimal Places",
                "description": "Limit coordinate and attribute precision to 1-2 decimal places unless higher precision is absolutely necessary. This can reduce file size without noticeable visual impact. The AI should ideally do this if asked for 'optimized' SVG.",
                "example": "Use `cx='10.5'` instead of `cx='10.4999998'`"
            },
            {
                "title": "Use Semantic Element Names and IDs",
                "description": "Give meaningful `id` attributes to important elements, especially if they will be referenced by CSS, JavaScript, or `<use>`. Use descriptive class names if styling with CSS.",
                "example": "<circle id='main-dial' class='clock-face-element' cx='50' cy='50' r='40' fill='yellow' />"
            },
            {
                "title": "Understand SVG Structure (XML-based)",
                "description": "SVGs are XML documents. Text elements are real text (not shapes unless converted to paths), improving accessibility and SEO. Familiarize yourself with basic XML structure for easier debugging and manipulation.",
                "example": "<!-- SVG is human-readable XML --> <svg><text x='10' y='20'>Hello World</text></svg>"
            },
            {
                "title": "Choose SVG for the Right Task",
                "description": "Excellent for logos, icons, illustrations, line art, and charts. For high-detail photographs where subtle color variations are critical, raster formats (JPEG, WebP) are often more suitable due to pixel-based rendering.",
                "example": "Use SVG for your company logo; use JPEG/WebP for a product hero image."
            },
            {
                "title": "Leverage Interactivity and Animation",
                "description": "SVGs support scripting (e.g., JavaScript for complex interactions) and declarative animation (SMIL). For web, CSS animations and transitions on SVG elements are often preferred for performance and maintainability.",
                "example": "Prompt: 'Create an SVG button that changes color on hover using CSS.' or '<circle cx='50' cy='50' r='20'><animate attributeName='fill' values='red;blue;red' dur='3s' repeatCount='indefinite'/></circle> (SMIL example)'"
            },
            {
                "title": "Ensure Accessibility (A11y)",
                "description": "For complex SVGs that convey information, provide a `<title>` (short description, like alt text) and optionally a `<desc>` (longer description) element as the first children of the `<svg>` tag. Use `role='img'` and `aria-labelledby` to link them if needed. Ensure text is actual text for screen readers.",
                "example": "<svg role='img' aria-labelledby='svgTitle svgDesc'><title id='svgTitle'>Company Logo</title><desc id='svgDesc'>A circular logo with a stylized letter Q representing Quantum Solutions.</desc>...</svg>"
            },
            {
                "title": "Consider File Size for Complexity",
                "description": "While SVGs are often smaller than raster images, very complex SVGs with thousands of paths and points can become large and impact performance. Simplify paths, use symbols, and run through an optimizer like SVGO.",
                "example": "For a detailed map with many repeating icons, define one `<symbol>` and `<use>` it multiple times instead of duplicating the icon paths."
            },
            {
                "title": "Test Across Browsers and Devices",
                "description": "While modern browser support for core SVG 1.1 and many SVG 2 features is excellent, very new or complex features (e.g., some filter effects, specific animation attributes) might have inconsistencies. Test your SVGs, especially if using advanced features.",
                "example": "Verify SVG rendering and interactivity in current versions of Chrome, Firefox, Safari, and Edge."
            },
            {
                "title": "Specify `xmlns` Namespace",
                "description": "Always include the `xmlns='http://www.w3.org/2000/svg'` attribute on the root `<svg>` element to declare it as an SVG document.",
                "example": "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>...</svg>"
            }
        ],
        "optimization_tools_info": {
            "title": "SVG Optimization Tools",
            "tools": [
                {
                    "name": "SVGO (SVG Optimizer)",
                    "description": "A Node.js-based tool for optimizing SVG files. Highly effective at reducing file size by removing redundant information, and optimizing paths.",
                    "url": "https://github.com/svg/svgo"
                },
                {
                    "name": "SVGOMG (SVGO's Missing GUI)",
                    "description": "A web-based GUI for SVGO, allowing you to visually inspect changes and toggle optimization features.",
                    "url": "https://jakearchibald.github.io/svgomg/"
                }
            ]
        }
    }
print("--- SVG MCP Server: Tool 'svg_best_practices' registered ---", file=sys.stderr)

@mcp.tool()
async def generate_svg_from_prompt(ctx: Context, prompt: str) -> Dict[str, Any]:
    """
    Generates a basic SVG image based on a textual prompt.

    This is a simplified version for demonstration. In a real scenario, 
    this would involve a more complex AI model to convert text to a rich SVG.
    
    Args:
        ctx: The MCP context
        prompt: The textual prompt to generate the SVG from.
        
    Returns:
        A dictionary containing the success status and the generated SVG code.
    """
    await ctx.info(f"Generating SVG from prompt: {prompt[:50]}...") # Log a snippet of the prompt

    # This function uses Claude's internal knowledge to interpret the prompt and style appropriately
    
    # Extract style keywords from prompt
    prompt_lower = prompt.lower()
    
    # These variables will be used to customize the SVG based on the prompt analysis
    svg_width = 300
    svg_height = 300
    
    # --- BEGIN MODIFICATION: Prompt-based dimensions ---
    dimension_match = re.search(r'(\d+)\s*(?:x|by)\s*(\d+)', prompt_lower)
    if dimension_match:
        try:
            parsed_width = int(dimension_match.group(1))
            parsed_height = int(dimension_match.group(2))
            if 50 <= parsed_width <= 2000 and 50 <= parsed_height <= 2000: # Basic sanity check
                svg_width = parsed_width
                svg_height = parsed_height
                await ctx.info(f"Dimensions set from prompt: {svg_width}x{svg_height}")
        except ValueError:
            pass # Ignore if parsing fails
    # --- END MODIFICATION ---
    
    svg_parts = []
    
    # Available style categories and their associated color palettes
    style_keywords = {
        "cyberpunk": ["cyberpunk", "neon", "futuristic", "glitch", "dystopian", "cyber", "tech"],
        "minimalist": ["minimalist", "minimal", "clean", "simple", "geometric", "flat"],
        "abstract": ["abstract", "fluid", "organic", "conceptual", "non-representational"],
        "retro": ["retro", "vintage", "80s", "90s", "old-school", "pixel", "8-bit"],
        "nature": ["nature", "organic", "floral", "plant", "tree", "leaf", "flower", "water"],
        "corporate": ["corporate", "professional", "business", "formal", "clean", "modern"],
        "fantasy": ["fantasy", "magical", "mythical", "medieval", "dragon", "fairy", "wizard"],
        "artdeco": ["art deco", "artdeco", "gatsby", "roaring twenties", "geometric patterns", "symmetry", "streamlined"],
        # --- BEGIN NEW STYLES KEYWORDS ---
        "steampunk": ["steampunk", "victorian", "cogs", "gears", "industrial", "brass", "copper", "steam-powered"],
        "flatdesign": ["flat design", "flat", "2d", "simple color", "no gradient", "long shadow"], # minimalist can be similar but flat has its own aesthetic
        "glitchart": ["glitch", "glitchy", "datamosh", "data mosh", "corrupted", "digital noise", "distortion", "static"]
        # --- END NEW STYLES KEYWORDS ---
    }
    
    color_palettes = {
        "cyberpunk": {"primary": "#00ffff", "secondary": "#ff00ff", "accent": "#00ff88", 
                     "background": "#111122", "text": "#ffffff"},
        "minimalist": {"primary": "#000000", "secondary": "#ffffff", "accent": "#ff3333", 
                      "background": "#f7f7f7", "text": "#333333"},
        "abstract": {"primary": "#ff6b35", "secondary": "#2ec4b6", "accent": "#fdfffc", 
                    "background": "#293241", "text": "#ffffff"},
        "retro": {"primary": "#f8333c", "secondary": "#44af69", "accent": "#fcab10", 
                 "background": "#2b9eb3", "text": "#dbd5b5"},
        "nature": {"primary": "#2d6a4f", "secondary": "#40916c", "accent": "#95d5b2", 
                  "background": "#d8f3dc", "text": "#1b4332"},
        "corporate": {"primary": "#003366", "secondary": "#336699", "accent": "#ff9900", 
                     "background": "#ffffff", "text": "#333333"},
        "fantasy": {"primary": "#7b2cbf", "secondary": "#c77dff", "accent": "#ffff3f", 
                   "background": "#240046", "text": "#e0aaff"},
        "artdeco": {"primary": "#DAA520", "secondary": "#000000", "accent": "#C0C0C0", 
                   "background": "#F5F5DC", "text": "#2E2E2E"},
        # --- BEGIN NEW STYLE PALETTES ---
        "steampunk": {"primary": "#B87333", "secondary": "#5E2605", "accent": "#CD7F32", # Copper, Dark Brown, Bronze
                     "background": "#F5DEB3", "text": "#3B2F2F"}, # Wheat, Dark Brown text
        "flatdesign": {"primary": "#3498db", "secondary": "#2ecc71", "accent": "#e74c3c", # Blue, Green, Red
                      "background": "#ecf0f1", "text": "#2c3e50"}, # Light Gray BG, Dark Blue text
        "glitchart": {"primary": "#FF00FF", "secondary": "#00FFFF", "accent": "#FFFF00", # Magenta, Cyan, Yellow
                     "background": "#1A1A1A", "text": "#FFFFFF"}, # Dark BG, White text
        # --- END NEW STYLE PALETTES ---
        "general": {"primary": "#0077b6", "secondary": "#48cae4", "accent": "#fb8500", 
                   "background": "#caf0f8", "text": "#03045e"}
    }
    
    # STYLE DETERMINATION - Using a more reasoning-based approach
    # This is where Claude's language understanding helps interpret style intention
    
    # Analyze the prompt for style cues beyond just keywords
    style_indicators = {
        "cyberpunk": 0,
        "minimalist": 0,
        "abstract": 0,
        "retro": 0,
        "nature": 0,
        "corporate": 0,
        "fantasy": 0,
        "artdeco": 0,
        # --- BEGIN NEW STYLES INDICATORS ---
        "steampunk": 0,
        "flatdesign": 0,
        "glitchart": 0,
        # --- END NEW STYLES INDICATORS ---
        "general": 0
    }
    
    # Initial keyword-based scoring to give a baseline
    for style, keywords in style_keywords.items():
        style_indicators[style] = sum(1 for kw in keywords if kw in prompt_lower)
    
    # Enhanced style reasoning - looking for contextual clues beyond keywords
    
    # Cyberpunk context clues
    if any(term in prompt_lower for term in ["dystopian", "future", "tech", "neon", "digital"]):
        style_indicators["cyberpunk"] += 1
    if "city" in prompt_lower and any(term in prompt_lower for term in ["dark", "future", "tech", "neon"]):
        style_indicators["cyberpunk"] += 2
    if any(pair in prompt_lower for pair in ["high tech", "low life", "neural interface", "cyber enhancement", "virtual reality", "digital reality"]):
        style_indicators["cyberpunk"] += 2
        
    # Minimalist context clues
    if any(term in prompt_lower for term in ["clean lines", "simple shapes", "uncluttered", "minimalism"]):
        style_indicators["minimalist"] += 2
    if "simple" in prompt_lower and "elegant" in prompt_lower:
        style_indicators["minimalist"] += 1
    if "geometric" in prompt_lower and not any(term in prompt_lower for term in ["complex", "ornate", "detailed"]):
        style_indicators["minimalist"] += 1
        
    # Abstract context clues
    if any(term in prompt_lower for term in ["non-representational", "conceptual", "non-figurative"]):
        style_indicators["abstract"] += 2
    if "expression" in prompt_lower and not any(term in prompt_lower for term in ["realistic", "literal"]):
        style_indicators["abstract"] += 1
        
    # Retro context clues
    if any(term in prompt_lower for term in ["vintage style", "old school", "retro gaming", "pixel art"]):
        style_indicators["retro"] += 2
    if any(decade in prompt_lower for decade in ["70s", "80s", "90s", "1970s", "1980s", "1990s"]):
        style_indicators["retro"] += 1
        
    # Nature context clues
    if any(term in prompt_lower for term in ["organic shape", "natural form", "floral pattern", "landscape"]):
        style_indicators["nature"] += 2
    if "environment" in prompt_lower or "eco" in prompt_lower:
        style_indicators["nature"] += 1
        
    # Corporate context clues
    if any(term in prompt_lower for term in ["professional logo", "business card", "corporate identity", "brand"]):
        style_indicators["corporate"] += 2
    if "company" in prompt_lower or "professional" in prompt_lower:
        style_indicators["corporate"] += 1
        
    # Fantasy context clues
    if any(term in prompt_lower for term in ["magical realm", "mythical creature", "enchanted", "fairy tale"]):
        style_indicators["fantasy"] += 2
    if "spell" in prompt_lower or "quest" in prompt_lower or "dragon" in prompt_lower:
        style_indicators["fantasy"] += 1
    
    # Art Deco context clues
    if any(term in prompt_lower for term in ["art deco style", "gatsby", "roaring twenties", "1920s style", "deco pattern"]):
        style_indicators["artdeco"] += 2
    if "geometric" in prompt_lower and ("gold" in prompt_lower or "symmetry" in prompt_lower or "streamlined" in prompt_lower):
        style_indicators["artdeco"] += 1
    if "symmetric" in prompt_lower or "ornate geometric" in prompt_lower:
        style_indicators["artdeco"] += 1
    
    # Steampunk context clues
    if any(term in prompt_lower for term in ["steampunk", "victorian", "cogs", "gears", "industrial era", "steam powered"]):
        style_indicators["steampunk"] += 2
    if ("brass" in prompt_lower or "copper" in prompt_lower or "bronze" in prompt_lower) and "mechanism" in prompt_lower:
        style_indicators["steampunk"] += 1
        
    # Flat Design context clues
    if any(term in prompt_lower for term in ["flat design", "flat style", "2d simple", "no shadows", "material design basic"]): # material can sometimes mean flat
        style_indicators["flatdesign"] += 2
    if "long shadow" in prompt_lower: # A specific flat design trend
        style_indicators["flatdesign"] += 1
    if "minimal" in prompt_lower and "solid color" in prompt_lower:
        style_indicators["flatdesign"] +=1

    # Glitch Art context clues
    if any(term in prompt_lower for term in ["glitch effect", "datamosh", "data corruption", "digital noise", "pixel sorting", "screen tear"]):
        style_indicators["glitchart"] += 2
    if ("distorted" in prompt_lower or "corrupted" in prompt_lower) and ("digital" in prompt_lower or "signal" in prompt_lower):
        style_indicators["glitchart"] += 1
    
    # Determine the dominant style from our enhanced analysis
    # If we have inconclusive results, fall back to "general"
    if max(style_indicators.values()) > 0:
        dominant_style = max(style_indicators.items(), key=lambda x: x[1])[0]
    else:
        dominant_style = "general"
        
    # If we have a tie, make a more contextual decision
    max_score = max(style_indicators.values())
    tied_styles = [style for style, score in style_indicators.items() if score == max_score and score > 0]
    
    if len(tied_styles) > 1:
        # Break ties with additional analysis
        
        # Favor cyberpunk if tech-related elements are mentioned
        if "cyberpunk" in tied_styles and any(term in prompt_lower for term in ["digital", "tech", "future", "cyber", "ai", "virtual"]):
            dominant_style = "cyberpunk"
            
        # Favor nature if nature elements are specified
        elif "nature" in tied_styles and any(term in prompt_lower for term in ["tree", "flower", "plant", "river", "mountain", "forest"]):
            dominant_style = "nature"
            
        # Favor minimalist if simplicity is emphasized
        elif "minimalist" in tied_styles and any(term in prompt_lower for term in ["minimal", "simple", "clean", "basic"]):
            dominant_style = "minimalist"
            
        # Favor fantasy if magical elements are present
        elif "fantasy" in tied_styles and any(term in prompt_lower for term in ["magic", "mystic", "dragon", "sword", "wizard"]):
            dominant_style = "fantasy"
            
        # Tie-breaking for Art Deco
        elif "artdeco" in tied_styles and any(term in prompt_lower for term in ["geometric", "gold", "symmetry", "1920s", "gatsby", "streamline"]):
            dominant_style = "artdeco"
        # --- BEGIN TIE-BREAKING FOR NEW STYLES ---
        elif "steampunk" in tied_styles and any(term in prompt_lower for term in ["gear", "cog", "victorian", "industrial", "brass"]):
            dominant_style = "steampunk"
        elif "flatdesign" in tied_styles and any(term in prompt_lower for term in ["flat", "2d", "simple icon", "no gradient"]):
            dominant_style = "flatdesign"
        elif "glitchart" in tied_styles and any(term in prompt_lower for term in ["glitchy", "corrupt", "noise", "distort"]):
            dominant_style = "glitchart"
        # --- END TIE-BREAKING FOR NEW STYLES ---
    
    # Set the color palette based on the dominant style
    palette = color_palettes[dominant_style]
    
    # Check for specific color mentions and override
    color_mapping = {
        "red": "#ff0000", "blue": "#0000ff", "green": "#00ff00", "yellow": "#ffff00",
        "purple": "#800080", "pink": "#ff69b4", "orange": "#ffa500", "black": "#000000",
        "white": "#ffffff", "gray": "#808080", "gold": "#ffd700", "silver": "#c0c0c0"
    }
    
    # Override palette colors if specific colors are mentioned
    for color_name, color_hex in color_mapping.items():
        if color_name in prompt_lower:
            if "background" in prompt_lower and color_name in prompt_lower.split("background")[1][:20]:
                palette["background"] = color_hex
            elif "primary" in prompt_lower and color_name in prompt_lower.split("primary")[1][:20]:
                palette["primary"] = color_hex
            elif "secondary" in prompt_lower and color_name in prompt_lower.split("secondary")[1][:20]:
                palette["secondary"] = color_hex
            elif "accent" in prompt_lower and color_name in prompt_lower.split("accent")[1][:20]:
                palette["accent"] = color_hex
            else:
                # If color is mentioned but not associated with any specific element,
                # use it as the primary color
                palette["primary"] = color_hex
    
    # Extract potential shapes or objects from prompt
    common_objects = {
        "eye": True if any(x in prompt_lower for x in ["eye", "vision", "optic", "sight"]) else False,
        "circuit": True if any(x in prompt_lower for x in ["circuit", "chip", "electronic", "board", "tech"]) else False,
        "city": True if any(x in prompt_lower for x in ["city", "skyline", "building", "urban"]) else False,
        "face": True if any(x in prompt_lower for x in ["face", "head", "portrait"]) else False,
        "geometric": True if any(x in prompt_lower for x in ["circle", "square", "triangle", "hexagon", "geometric"]) else False,
        "landscape": True if any(x in prompt_lower for x in ["landscape", "mountain", "nature", "scene"]) else False,
        "animal": True if any(x in prompt_lower for x in ["animal", "creature", "beast", "dog", "cat", "bird"]) else False,
        "abstract": True if any(x in prompt_lower for x in ["abstract", "pattern", "design", "random"]) else False,
        "gear": True if any(x in prompt_lower for x in ["gear", "cog", "cogwheel", "mechanism"]) else False,
        # --- BEGIN NEW COMMON OBJECTS ---
        "arrow": True if any(x in prompt_lower for x in ["arrow", "pointer", "direction", "indicator", "cursor"]) else False,
        "cloud": True if any(x in prompt_lower for x in ["cloud", "sky", "weather", "cumulus", "fluffy cloud"]) else False,
        "heart": True if any(x in prompt_lower for x in ["heart", "love", "valentine", "romance"]) else False,
        "star": True if any(x in prompt_lower for x in ["star", "celestial", "rating", "sparkle", "five-pointed star"]) else False
        # --- END NEW COMMON OBJECTS ---
    }
    
    # Define SVG defs section with reusable components
    svg_parts.append(f'''<defs>
        <!-- Filter: Glow Effect -->
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="5" result="blur"/>
            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
        </filter>
        
        <!-- Gradient: Primary to Secondary -->
        <linearGradient id="primaryGradient" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:{palette['primary']};stop-opacity:1" />
            <stop offset="100%" style="stop-color:{palette['secondary']};stop-opacity:1" />
        </linearGradient>
        
        <!-- Pattern: Background texture -->
        <pattern id="bgPattern" patternUnits="userSpaceOnUse" width="100" height="100">
            <rect width="100" height="100" fill="{palette['background']}"/>
            <path d="M0 10 H100 M0 30 H100 M0 50 H100 M0 70 H100 M0 90 H100" stroke="{palette['primary']}" stroke-width="0.5" opacity="0.1"/>
            <path d="M10 0 V100 M30 0 V100 M50 0 V100 M70 0 V100 M90 0 V100" stroke="{palette['primary']}" stroke-width="0.5" opacity="0.1"/>
        </pattern>
        
        <!-- Filter: Glitch effect for cyberpunk style -->
        <filter id="glitchEffect">
            <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="2" result="noise"/>
            <feDisplacementMap in="SourceGraphic" in2="noise" scale="5" xChannelSelector="R" yChannelSelector="G"/>
        </filter>
        
        <!-- Filter: Retro pixelation effect -->
        <filter id="pixelate" x="0%" y="0%" width="100%" height="100%">
            <feFlood x="4" y="4" height="2" width="2"/>
            <feComposite width="8" height="8"/>
            <feTile result="a"/>
            <feComposite in="SourceGraphic" in2="a" operator="in"/>
            <feMorphology operator="dilate" radius="2"/>
        </filter>
    </defs>''')
    
    # Add background
    svg_parts.append(f'<rect width="{svg_width}" height="{svg_height}" fill="{palette["background"]}"/>')
    
    # For abstract/pattern designs, add background patterns
    if dominant_style in ["abstract", "cyberpunk", "retro"]:
        svg_parts.append(f'<rect width="{svg_width}" height="{svg_height}" fill="url(#bgPattern)" opacity="0.3"/>')
    
    # Generate content based on detected objects and style
    
    # Center position for most objects
    center_x = svg_width / 2
    center_y = svg_height / 2
    
    # Cybernetic Eye
    if common_objects["eye"]:
        # Determine if it has scanning effects
        has_scan = "scan" in prompt_lower or "tracking" in prompt_lower or "target" in prompt_lower
        
        svg_parts.append(f'''
        <!-- Eye element -->
        <g transform="translate({center_x}, {center_y})">
            <!-- Eye outer shape -->
            <ellipse cx="0" cy="0" rx="60" ry="35" fill="#000000" stroke="{palette['primary']}" stroke-width="2"/>
            
            <!-- Iris -->
            <circle cx="0" cy="0" r="25" fill="url(#primaryGradient)" filter="url(#glow)"/>
            
            <!-- Pupil -->
            <circle cx="0" cy="0" r="12" fill="#000000"/>
            
            <!-- Tech details -->
            <circle cx="0" cy="0" r="18" fill="none" stroke="{palette['accent']}" stroke-width="0.8" stroke-dasharray="2,1"/>
            
            <!-- Scanning effect if requested -->
            {f'<line x1="-40" y1="-10" x2="40" y2="-10" stroke="{palette["accent"]}" stroke-width="1" opacity="0.7"/>' if has_scan else ''}
            {f'<line x1="-40" y1="10" x2="40" y2="10" stroke="{palette["accent"]}" stroke-width="1" opacity="0.7"/>' if has_scan else ''}
            {f'<path d="M-40 0 Q0 -5 40 0" stroke="{palette["secondary"]}" stroke-width="1" fill="none" opacity="0.8"/>' if has_scan else ''}
            {f'<path d="M-40 0 Q0 5 40 0" stroke="{palette["secondary"]}" stroke-width="1" fill="none" opacity="0.8"/>' if has_scan else ''}
        </g>''')
    
    # Circuit design
    elif common_objects["circuit"]:
        # Variation depending on style
        if dominant_style == "cyberpunk":
            # Glowing tech circuit
            svg_parts.append(f'''
            <!-- Circuit design -->
            <g transform="translate({center_x}, {center_y})">
                <rect x="-70" y="-70" width="140" height="140" fill="none" stroke="{palette['primary']}" stroke-width="2"/>
                <path d="M-70 -30 H70 M-70 0 H70 M-70 30 H70" stroke="{palette['accent']}" stroke-width="1.5" stroke-dasharray="5,3"/>
                <path d="M-30 -70 V70 M0 -70 V70 M30 -70 V70" stroke="{palette['accent']}" stroke-width="1.5" stroke-dasharray="5,3"/>
                <circle cx="0" cy="0" r="20" fill="none" stroke="{palette['secondary']}" stroke-width="2"/>
                <circle cx="-30" cy="-30" r="5" fill="{palette['primary']}"/>
                <circle cx="30" cy="-30" r="5" fill="{palette['primary']}"/>
                <circle cx="-30" cy="30" r="5" fill="{palette['primary']}"/>
                <circle cx="30" cy="30" r="5" fill="{palette['primary']}"/>
                <path d="M-60 -60 L-40 -40 M60 -60 L40 -40 M-60 60 L-40 40 M60 60 L40 40" stroke="{palette['accent']}" stroke-width="2"/>
            </g>''')
        else:
            # Cleaner circuit design for other styles
            svg_parts.append(f'''
            <!-- Circuit design - clean -->
            <g transform="translate({center_x}, {center_y})">
                <rect x="-60" y="-60" width="120" height="120" fill="none" stroke="{palette['primary']}" stroke-width="2" rx="5"/>
                <circle cx="0" cy="0" r="20" fill="{palette['primary']}" opacity="0.2"/>
                <path d="M-60 -20 H-20 V-60 M-60 20 H-20 V60 M60 -20 H20 V-60 M60 20 H20 V60" 
                      fill="none" stroke="{palette['primary']}" stroke-width="1.5"/>
                <rect x="-10" y="-10" width="20" height="20" fill="{palette['accent']}"/>
                <circle cx="-40" cy="-40" r="4" fill="{palette['secondary']}"/>
                <circle cx="40" cy="-40" r="4" fill="{palette['secondary']}"/>
                <circle cx="-40" cy="40" r="4" fill="{palette['secondary']}"/>
                <circle cx="40" cy="40" r="4" fill="{palette['secondary']}"/>
            </g>''')
    
    # City/Skyline
    elif common_objects["city"]:
        if dominant_style == "cyberpunk":
            # Futuristic cyberpunk city
            svg_parts.append(f'''
            <!-- Cyberpunk City Skyline -->
            <g>
                <!-- Background atmosphere -->
                <rect width="{svg_width}" height="{svg_height}" fill="url(#primaryGradient)" opacity="0.3"/>
                
                <!-- Buildings -->
                <rect x="20" y="100" width="30" height="200" fill="{palette['background']}" stroke="{palette['primary']}" stroke-width="1"/>
                <rect x="60" y="150" width="40" height="150" fill="{palette['background']}" stroke="{palette['secondary']}" stroke-width="1"/>
                <rect x="110" y="80" width="20" height="220" fill="{palette['background']}" stroke="{palette['primary']}" stroke-width="1"/>
                <rect x="140" y="130" width="50" height="170" fill="{palette['background']}" stroke="{palette['accent']}" stroke-width="1"/>
                <rect x="200" y="100" width="35" height="200" fill="{palette['background']}" stroke="{palette['secondary']}" stroke-width="1"/>
                <rect x="245" y="120" width="25" height="180" fill="{palette['background']}" stroke="{palette['primary']}" stroke-width="1"/>
                
                <!-- Building windows -->
                <g>
                    <rect x="25" y="120" width="5" height="8" fill="{palette['accent']}" opacity="0.8"/>
                    <rect x="35" y="120" width="5" height="8" fill="{palette['accent']}" opacity="0.8"/>
                    <rect x="25" y="140" width="5" height="8" fill="{palette['accent']}" opacity="0.8"/>
                    <rect x="35" y="140" width="5" height="8" fill="{palette['accent']}" opacity="0.5"/>
                    <rect x="25" y="160" width="5" height="8" fill="{palette['accent']}" opacity="0.8"/>
                    <rect x="35" y="160" width="5" height="8" fill="{palette['accent']}" opacity="0.5"/>
                    
                    <rect x="70" y="170" width="6" height="10" fill="{palette['primary']}" opacity="0.7"/>
                    <rect x="84" y="170" width="6" height="10" fill="{palette['primary']}" opacity="0.7"/>
                    <rect x="70" y="190" width="6" height="10" fill="{palette['primary']}" opacity="0.4"/>
                    <rect x="84" y="190" width="6" height="10" fill="{palette['primary']}" opacity="0.7"/>
                    
                    <!-- More windows on other buildings -->
                    <rect x="115" y="100" width="4" height="7" fill="{palette['secondary']}" opacity="0.6"/>
                    <rect x="115" y="120" width="4" height="7" fill="{palette['secondary']}" opacity="0.6"/>
                    <rect x="115" y="140" width="4" height="7" fill="{palette['secondary']}" opacity="0.6"/>
                </g>
                
                <!-- Flying vehicles if it's futuristic -->
                <g>
                    <ellipse cx="70" cy="80" rx="10" ry="3" fill="{palette['secondary']}" filter="url(#glow)" opacity="0.8"/>
                    <ellipse cx="180" cy="50" rx="12" ry="4" fill="{palette['primary']}" filter="url(#glow)" opacity="0.8"/>
                    <ellipse cx="240" cy="90" rx="8" ry="3" fill="{palette['accent']}" filter="url(#glow)" opacity="0.8"/>
                </g>
            </g>''')
        else:
            # More conventional city skyline
            svg_parts.append(f'''
            <!-- City Skyline -->
            <g>
                <!-- Sky -->
                <rect width="{svg_width}" height="{svg_height}" fill="{palette['background']}" opacity="0.4"/>
                <rect width="{svg_width}" height="{svg_height/2}" fill="{palette['secondary']}" opacity="0.2"/>
                
                <!-- Buildings - simpler for non-cyberpunk -->
                <rect x="30" y="100" width="40" height="200" fill="{palette['primary']}" opacity="0.8"/>
                <rect x="80" y="140" width="30" height="160" fill="{palette['primary']}" opacity="0.7"/>
                <rect x="120" y="120" width="50" height="180" fill="{palette['primary']}" opacity="0.9"/>
                <rect x="180" y="150" width="45" height="150" fill="{palette['primary']}" opacity="0.8"/>
                <rect x="235" y="130" width="35" height="170" fill="{palette['primary']}" opacity="0.7"/>
                
                <!-- Details -->
                <rect x="110" y="90" width="10" height="30" fill="{palette['primary']}" opacity="0.9"/>
                <path d="M160 120 L150 100 L170 100 Z" fill="{palette['primary']}" opacity="0.9"/>
            </g>''')
    
    # Geometric design
    elif common_objects["geometric"]:
        # Different geometric patterns based on style
        if "hexagon" in prompt_lower or dominant_style == "cyberpunk":
            svg_parts.append(f'''
            <!-- Hexagonal Grid Pattern -->
            <g transform="translate({center_x}, {center_y})">
                <path d="M-50 -87 L0 -100 L50 -87 L50 -50 L0 -37 L-50 -50 Z" fill="none" stroke="{palette['primary']}" stroke-width="2" opacity="0.8"/>
                <path d="M-50 -13 L0 -26 L50 -13 L50 24 L0 37 L-50 24 Z" fill="none" stroke="{palette['primary']}" stroke-width="2" opacity="0.8"/>
                <path d="M-50 61 L0 48 L50 61 L50 98 L0 111 L-50 98 Z" fill="none" stroke="{palette['primary']}" stroke-width="2" opacity="0.8"/>
                
                <!-- Central element -->
                <circle cx="0" cy="0" r="30" fill="none" stroke="{palette['secondary']}" stroke-width="2"/>
                <circle cx="0" cy="0" r="20" fill="url(#primaryGradient)" opacity="0.7"/>
            </g>''')
        elif "triangle" in prompt_lower:
            svg_parts.append(f'''
            <!-- Triangle Pattern -->
            <g transform="translate({center_x}, {center_y})">
                <path d="M0 -70 L60 40 L-60 40 Z" fill="none" stroke="{palette['primary']}" stroke-width="2"/>
                <path d="M0 -40 L35 22 L-35 22 Z" fill="{palette['primary']}" opacity="0.3"/>
                <path d="M0 70 L-60 -40 L60 -40 Z" fill="none" stroke="{palette['secondary']}" stroke-width="2"/>
                <path d="M0 40 L-35 -22 L35 -22 Z" fill="{palette['secondary']}" opacity="0.3"/>
            </g>''')
        elif "circle" in prompt_lower:
            svg_parts.append(f'''
            <!-- Circular Pattern -->
            <g transform="translate({center_x}, {center_y})">
                <circle cx="0" cy="0" r="60" fill="none" stroke="{palette['primary']}" stroke-width="2"/>
                <circle cx="0" cy="0" r="45" fill="none" stroke="{palette['accent']}" stroke-width="1" stroke-dasharray="4,2"/>
                <circle cx="0" cy="0" r="30" fill="{palette['secondary']}" opacity="0.2"/>
                <circle cx="0" cy="0" r="15" fill="{palette['primary']}" opacity="0.5"/>
            </g>''')
        else:
            svg_parts.append(f'''
            <!-- Mixed Geometric Pattern -->
            <g transform="translate({center_x}, {center_y})">
                <rect x="-50" y="-50" width="100" height="100" fill="none" stroke="{palette['primary']}" stroke-width="2" rx="5"/>
                <circle cx="0" cy="0" r="30" fill="none" stroke="{palette['secondary']}" stroke-width="2"/>
                <path d="M-20 -20 L20 -20 L0 20 Z" fill="{palette['accent']}" opacity="0.5"/>
            </g>''')
    
    # Gear
    elif common_objects["gear"]:
        num_teeth = 8
        if "teeth" in prompt_lower:
            teeth_match = re.search(r'(\d+)\s*teeth', prompt_lower)
            if teeth_match:
                try:
                    parsed_teeth = int(teeth_match.group(1))
                    if 4 <= parsed_teeth <= 20: # Min 4, Max 20 teeth
                        num_teeth = parsed_teeth
                except ValueError:
                    pass # Ignore if parsing fails to keep default

        outer_radius = min(svg_width, svg_height) * 0.30 # Slightly smaller for better fit
        inner_radius_factor = 0.65 # Proportion of outer_radius for the base of teeth
        hole_radius = outer_radius * 0.25
        tooth_height = outer_radius * 0.20 # Height of the tooth from its base
        
        # For path drawing
        path_data = []
        center_x_gear, center_y_gear = center_x, center_y # Use the general center

        # Start path for the gear outline
        current_path = []

        for i in range(num_teeth):
            # Angle for the start of the tooth base (valley)
            angle1 = (i / num_teeth) * 2 * math.pi
            # Angle for the start of the tooth top
            angle2 = ((i + 0.25) / num_teeth) * 2 * math.pi
            # Angle for the end of the tooth top
            angle3 = ((i + 0.75) / num_teeth) * 2 * math.pi
            # Angle for the end of the tooth base (next valley)
            angle4 = ((i + 1.0) / num_teeth) * 2 * math.pi

            # Valley point 1 (start of tooth base)
            x_v1 = center_x_gear + (outer_radius - tooth_height) * math.cos(angle1)
            y_v1 = center_y_gear + (outer_radius - tooth_height) * math.sin(angle1)

            # Tooth top point 1 (start of tooth top)
            x_t1 = center_x_gear + outer_radius * math.cos(angle2)
            y_t1 = center_y_gear + outer_radius * math.sin(angle2)

            # Tooth top point 2 (end of tooth top)
            x_t2 = center_x_gear + outer_radius * math.cos(angle3)
            y_t2 = center_y_gear + outer_radius * math.sin(angle3)
            
            # Valley point 2 (end of tooth base for this tooth)
            # This point is also the start of the next tooth's base if not the last tooth
            x_v2 = center_x_gear + (outer_radius - tooth_height) * math.cos(angle4)
            y_v2 = center_y_gear + (outer_radius - tooth_height) * math.sin(angle4)

            if i == 0:
                current_path.append(f"M {x_v1:.2f},{y_v1:.2f}")
            else:
                 # Smooth transition from previous tooth's end valley to this tooth's start valley (should be same point)
                current_path.append(f"L {x_v1:.2f},{y_v1:.2f}") 
            
            current_path.append(f"L {x_t1:.2f},{y_t1:.2f}") # Line to start of tooth top
            current_path.append(f"L {x_t2:.2f},{y_t2:.2f}") # Line across tooth top
            current_path.append(f"L {x_v2:.2f},{y_v2:.2f}") # Line to end of tooth base / next valley
            
        current_path.append("Z") # Close the outer gear shape

        # Central hole (drawn as a separate sub-path for fill-rule to work)
        current_path.append(f" M {center_x_gear + hole_radius:.2f},{center_y_gear:.2f}")
        current_path.append(f" A {hole_radius:.2f},{hole_radius:.2f} 0 1 0 {center_x_gear - hole_radius:.2f},{center_y_gear:.2f}")
        current_path.append(f" A {hole_radius:.2f},{hole_radius:.2f} 0 1 0 {center_x_gear + hole_radius:.2f},{center_y_gear:.2f}")
        current_path.append("Z")

        svg_parts.append(f'''
        <!-- Gear -->
        <g>
             <path d="{" ".join(current_path)}" fill="{palette['primary']}" stroke="{palette['secondary']}" stroke-width="1.5" fill-rule="evenodd"/>
        </g>''')
    
    # --- BEGIN SVG GENERATION FOR NEW OBJECTS ---
    elif common_objects["arrow"]:
        arrow_length = min(svg_width, svg_height) * 0.6
        arrow_head_size = arrow_length * 0.25
        stroke_w = max(2, arrow_length * 0.05)
        svg_parts.append(f'''
        <!-- Arrow -->
        <g transform="translate({center_x - arrow_length / 2}, {center_y})" fill="{palette['primary']}" stroke="{palette['secondary']}" stroke-width="{stroke_w}">
            <line x1="0" y1="0" x2="{arrow_length - arrow_head_size}" y2="0" />
            <polygon points="{arrow_length - arrow_head_size},-{arrow_head_size*0.7} {arrow_length},0 {arrow_length - arrow_head_size},{arrow_head_size*0.7}" />
        </g>''')

    elif common_objects["cloud"]:
        cloud_w = min(svg_width, svg_height) * 0.5
        cloud_h = cloud_w * 0.6
        # Simple cloud made of overlapping circles
        svg_parts.append(f'''
        <!-- Cloud -->
        <g transform="translate({center_x - cloud_w/2}, {center_y - cloud_h/2})" fill="{palette['primary']}" opacity="{0.8 if dominant_style != 'flatdesign' else 1.0}">
            <circle cx="{cloud_w*0.3}" cy="{cloud_h*0.6}" r="{cloud_w*0.25}" />
            <circle cx="{cloud_w*0.5}" cy="{cloud_h*0.4}" r="{cloud_w*0.3}" />
            <circle cx="{cloud_w*0.7}" cy="{cloud_h*0.7}" r="{cloud_w*0.28}" />
            <rect x="{cloud_w*0.2}" y="{cloud_h*0.5}" width="{cloud_w*0.6}" height="{cloud_h*0.4}" rx="5"/>
        </g>''')
        if dominant_style == "nature":
             svg_parts.append(f'<path d="M {center_x - cloud_w*0.2} {center_y + cloud_h*0.3} Q {center_x} {center_y + cloud_h*0.4} {center_x + cloud_w*0.2} {center_y + cloud_h*0.3}" stroke="{palette['secondary']}" stroke-width="2" fill="none" opacity="0.5"/>')

    elif common_objects["heart"]:
        heart_size = min(svg_width, svg_height) * 0.4
        # Standard heart path, scaled
        # Path data for a heart: M0,0 C0,-10 -10,-10 -10,0 C-10,10 0,10 0,20 C0,10 10,10 10,0 C10,-10 0,-10 0,0 Z
        # Scaled: M cx,cy+s*k1 C cx,cy-s*k2 cx-s*k3,cy-s*k2 cx-s*k3,cy+s*k1 C cx-s*k3,cy+s*k2 cx,cy+s*k2 cx,cy+s*k4 ...
        # Simpler path:
        svg_parts.append(f'''
        <!-- Heart -->
        <g transform="translate({center_x}, {center_y - heart_size*0.1})">
             <path d="M0,{-heart_size*0.4}
                      A{heart_size*0.2},{heart_size*0.2} 0 0,1 {heart_size*0.2},{-heart_size*0.6}
                      A{heart_size*0.2},{heart_size*0.2} 0 0,1 {heart_size*0.4},{-heart_size*0.4}
                      L0,{heart_size*0.4}
                      L{-heart_size*0.4},{-heart_size*0.4}
                      A{heart_size*0.2},{heart_size*0.2} 0 0,1 {-heart_size*0.2},{-heart_size*0.6}
                      A{heart_size*0.2},{heart_size*0.2} 0 0,1 0,{-heart_size*0.4} Z"
                   fill="{palette['primary']}" stroke="{palette['secondary']}" stroke-width="1.5"/>
        </g>''')
        if dominant_style == "retro":
             svg_parts.append(f'<path transform="translate({center_x + heart_size*0.05}, {center_y - heart_size*0.05})" d="M0,{-heart_size*0.4} A{heart_size*0.2},{heart_size*0.2} 0 0,1 {heart_size*0.2},{-heart_size*0.6} A{heart_size*0.2},{heart_size*0.2} 0 0,1 {heart_size*0.4},{-heart_size*0.4} L0,{heart_size*0.4} L{-heart_size*0.4},{-heart_size*0.4} A{heart_size*0.2},{heart_size*0.2} 0 0,1 {-heart_size*0.2},{-heart_size*0.6} A{heart_size*0.2},{heart_size*0.2} 0 0,1 0,{-heart_size*0.4} Z" fill="{palette['accent']}" opacity="0.3"/>')

    elif common_objects["star"]:
        num_points = 5
        if "points" in prompt_lower or "pointed star" in prompt_lower:
            star_match = re.search(r'(\d+)\s*(?:points|pointed star)\', prompt_lower)
            if star_match:
                try: parsed_points = int(star_match.group(1)); num_points = max(3, min(12, parsed_points)) # 3-12 points
                except ValueError: pass

        outer_r = min(svg_width, svg_height) * 0.3
        inner_r = outer_r * (0.382 if num_points == 5 else 0.5) # Golden ratio for 5-point star, 0.5 for others
        
        points_str = []
        for i in range(num_points * 2):
            radius = outer_r if i % 2 == 0 else inner_r
            angle = (i / (num_points * 2)) * 2 * math.pi - (math.pi / 2) # Adjust to make a point go upwards
            x_pt = center_x + radius * math.cos(angle)
            y_pt = center_y + radius * math.sin(angle)
            points_str.append(f"{x_pt:.2f},{y_pt:.2f}")
        
        svg_parts.append(f'''
        <!-- Star -->
        <polygon points="{" ".join(points_str)}" fill="{palette['primary']}" stroke="{palette['secondary']}" stroke-width="1.5"/>
        ''')
        if dominant_style == "fantasy" or "sparkle" in prompt_lower:
            svg_parts.append(f'<polygon points="{" ".join(points_str)}" fill="none" stroke="{palette[\'accent\']}" stroke-width="3" filter="url(#glow)" opacity="0.5" transform="scale(0.95)" transform-origin="{center_x} {center_y}"/>')

    # --- END SVG GENERATION FOR NEW OBJECTS ---

    # Abstract design (default if no specific object detected)
    else:
        # Different abstract styles based on dominant style
        if dominant_style == "cyberpunk":
            svg_parts.append(f'''
            <!-- Cyberpunk Abstract Design -->
            <g transform="translate({center_x}, {center_y})">
                <!-- Hexagonal grid pattern -->
                <path d="M-50 -87 L0 -100 L50 -87 L50 -50 L0 -37 L-50 -50 Z" fill="none" stroke="{palette['primary']}" stroke-width="2" opacity="0.8"/>
                <path d="M-50 -13 L0 -26 L50 -13 L50 24 L0 37 L-50 24 Z" fill="none" stroke="{palette['primary']}" stroke-width="2" opacity="0.8"/>
                <path d="M-50 61 L0 48 L50 61 L50 98 L0 111 L-50 98 Z" fill="none" stroke="{palette['primary']}" stroke-width="2" opacity="0.8"/>
                
                <!-- Central circular element -->
                <circle cx="0" cy="0" r="40" fill="none" stroke="{palette['secondary']}" stroke-width="3" stroke-dasharray="1,1"/>
                <circle cx="0" cy="0" r="30" fill="none" stroke="{palette['accent']}" stroke-width="2"/>
                <circle cx="0" cy="0" r="20" fill="url(#primaryGradient)" filter="url(#glow)"/>
                
                <!-- Decorative lines -->
                <path d="M-100 0 L-50 0 M50 0 L100 0 M0 -100 L0 -50 M0 50 L0 100" stroke="{palette['accent']}" stroke-width="2" opacity="0.8"/>
            </g>''')
        elif dominant_style == "minimalist":
            svg_parts.append(f'''
            <!-- Minimalist Abstract Design -->
            <g transform="translate({center_x}, {center_y})">
                <rect x="-40" y="-40" width="80" height="80" fill="none" stroke="{palette['primary']}" stroke-width="2"/>
                <circle cx="0" cy="0" r="25" fill="{palette['accent']}" opacity="0.8"/>
                <line x1="-60" y1="-60" x2="60" y2="60" stroke="{palette['primary']}" stroke-width="1.5"/>
                <line x1="-60" y1="60" x2="60" y2="-60" stroke="{palette['primary']}" stroke-width="1.5"/>
            </g>''')
        elif dominant_style == "retro":
            svg_parts.append(f'''
            <!-- Retro Abstract Design -->
            <g transform="translate({center_x}, {center_y})" filter="url(#pixelate)">
                <rect x="-50" y="-50" width="100" height="100" fill="{palette['secondary']}" stroke="{palette['primary']}" stroke-width="4"/>
                <circle cx="0" cy="0" r="30" fill="{palette['primary']}"/>
                <path d="M-30 -30 L30 30 M-30 30 L30 -30" stroke="{palette['accent']}" stroke-width="5"/>
            </g>''')
        elif dominant_style == "artdeco":
            svg_parts.append(f'''
            <!-- Art Deco Abstract Design -->
            <g transform="translate({center_x}, {center_y})">
                <!-- Symmetrical background lines -->
                <path d="M {-svg_width*0.4} 0 L {svg_width*0.4} 0 M 0 {-svg_height*0.4} L 0 {svg_height*0.4}" stroke="{palette['secondary']}" stroke-width="1" opacity="0.5"/>
                <rect x="-{svg_width*0.3}" y="-{svg_height*0.3}" width="{svg_width*0.6}" height="{svg_height*0.6}" fill="none" stroke="{palette['primary']}" stroke-width="3" rx="5"/>
                
                <!-- Sunburst/Radiating lines from center -->
                {"".join([f'<line x1="0" y1="0" x2="{(_a := i * 2 * 3.14159 / 12) or math.cos(_a) * svg_width * 0.35}" y2="{(_a := i * 2 * 3.14159 / 12) or math.sin(_a) * svg_height * 0.35}" stroke="{palette["accent"]}" stroke-width="1.5" opacity="0.7"/>' for i in range(12)])}
                
                <circle cx="0" cy="0" r="{min(svg_width, svg_height)*0.1}" fill="{palette['primary']}" stroke="{palette['accent']}" stroke-width="2"/>
                <circle cx="0" cy="0" r="{min(svg_width, svg_height)*0.05}" fill="{palette['background']}"/>
                
                <!-- Corner Elements -->
                <rect x="-{svg_width*0.3 -5}" y="-{svg_height*0.3 -5}" width="15" height="15" fill="{palette['accent']}" opacity="0.6"/>
                <rect x="{svg_width*0.3 -20}" y="-{svg_height*0.3 -5}" width="15" height="15" fill="{palette['accent']}" opacity="0.6"/>
                <rect x="-{svg_width*0.3 -5}" y="{svg_height*0.3 -20}" width="15" height="15" fill="{palette['accent']}" opacity="0.6"/>
                <rect x="{svg_width*0.3 -20}" y="{svg_height*0.3 -20}" width="15" height="15" fill="{palette['accent']}" opacity="0.6"/>
            </g>''')
        else:
            svg_parts.append(f'''
            <!-- Generic Abstract Design -->
            <g transform="translate({center_x}, {center_y})">
                <path d="M-50 -50 C-30 -70, 30 -70, 50 -50 C70 -30, 70 30, 50 50 C30 70, -30 70, -50 50 C-70 30, -70 -30, -50 -50 Z" 
                      fill="none" stroke="{palette['primary']}" stroke-width="2"/>
                <circle cx="0" cy="0" r="30" fill="{palette['secondary']}" opacity="0.3"/>
                <path d="M-25 0 A25 25 0 0 0 25 0" fill="none" stroke="{palette['accent']}" stroke-width="2"/>
                <path d="M-25 0 A25 25 0 0 1 25 0" fill="none" stroke="{palette['accent']}" stroke-width="2"/>
            </g>''')
    
    # Add supplementary effects based on prompt
    if "glitch" in prompt_lower or "distorted" in prompt_lower:
        svg_parts.append(f'<rect width="{svg_width}" height="{svg_height}" fill="none" stroke="none" filter="url(#glitchEffect)" opacity="0.7"/>')
    
    if "glow" in prompt_lower or "neon" in prompt_lower:
        svg_parts.append(f'<rect x="30" y="30" width="{svg_width-60}" height="{svg_height-60}" fill="none" stroke="{palette["accent"]}" stroke-width="2" filter="url(#glow)" opacity="0.7"/>')
    
    # Add style info at the bottom
    # --- BEGIN MODIFICATION: Improved Caption ---
    caption_text = prompt
    max_caption_len = int((svg_width - 60) / 7) # Approximate chars based on font size and rect width
    if len(caption_text) > max_caption_len:
        caption_text = caption_text[:max_caption_len-3] + "..."
    
    svg_parts.append(f'''
    <!-- Caption/title with style info -->
    <rect x="10" y="{svg_height - 35}" width="{svg_width - 20}" height="25" fill="#000000" opacity="0.6" rx="3"/>
    <text x="50%" y="{svg_height - 22.5}" dominant-baseline="middle" text-anchor="middle" font-family="monospace" font-size="11px" fill="{palette['text']}">
        {caption_text.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')} [{dominant_style}]
    </text></g>''') # Added closing </g> tag for text group (though might not be strictly necessary if not grouped before)
    # Corrected caption, ensure text is inside the svg structure properly
    # Let's assume the text element is directly within the main SVG or a generic group
    svg_parts.append(f'''
    <rect x="10" y="{svg_height - 35}" width="{svg_width - 20}" height="25" fill="#000000" opacity="0.6" rx="3"/>
    <text x="50%" y="{svg_height - 22.5}" dominant-baseline="middle" text-anchor="middle" font-family="monospace" font-size="11px" fill="{palette['text']}">
        {caption_text.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')} [{dominant_style}]
    </text>''')
    # --- END MODIFICATION ---
    
    # Combine all SVG parts
    svg_code = f'''<svg viewBox="0 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">
    <title>Generated from: {prompt.replace('"', '&quot;')}</title>
    {' '.join(svg_parts)}
</svg>'''
    
    return {
        "success": True,
        "svg_code": svg_code,
        "detected_style": dominant_style
    }
print("--- SVG MCP Server: Tool 'generate_svg_from_prompt' registered ---", file=sys.stderr)

@mcp.resource("examples://svg-snippets")
async def get_svg_snippets():
    """
    Returns useful SVG code snippets that can be used as building blocks.
    """
    return {
        "snippets": [
            {
                "name": "Basic Shape: Circle",
                "description": "A simple circle with styling",
                "code": '<circle cx="50" cy="50" r="40" stroke="blue" stroke-width="3" fill="red" />'
            },
            {
                "name": "Basic Shape: Rectangle",
                "description": "A rectangle with rounded corners",
                "code": '<rect x="10" y="10" width="80" height="60" rx="5" fill="green" />'
            },
            {
                "name": "Text Element",
                "description": "Basic text with styling",
                "code": '<text x="10" y="20" font-family="Arial" font-size="16" fill="black">Hello SVG</text>'
            },
            {
                "name": "Linear Gradient",
                "description": "Definition and use of a linear gradient",
                "code": '<defs>\n  <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">\n    <stop offset="0%" style="stop-color:rgb(255,0,0);stop-opacity:1" />\n    <stop offset="100%" style="stop-color:rgb(0,0,255);stop-opacity:1" />\n  </linearGradient>\n</defs>\n<rect x="10" y="10" width="80" height="80" fill="url(#grad)" />'
            },
            {
                "name": "Simple Path",
                "description": "A path element creating a custom shape",
                "code": '<path d="M10,30 A20,20 0,0,1 50,30 A20,20 0,0,1 90,30 Q90,60 50,90 Q10,60 10,30 z" fill="blue"/>'
            },
            {
                "name": "Basic Animation",
                "description": "A simple animation using animate",
                "code": '<circle cx="50" cy="50" r="20" fill="red">\n  <animate attributeName="r" values="20;40;20" dur="2s" repeatCount="indefinite" />\n</circle>'
            }
        ]
    }
print("--- SVG MCP Server: Resource 'examples://svg-snippets' registered ---", file=sys.stderr)

if __name__ == "__main__":
    print("--- SVG MCP Server: Entering main block ---", file=sys.stderr)
    try:
        print("--- SVG MCP Server: Attempting to start mcp.run(transport=\"stdio\") ---", file=sys.stderr)
        mcp.run(transport="stdio")
        print("--- SVG MCP Server: mcp.run() completed (this might not be reached if server runs indefinitely) ---", file=sys.stderr)
    except Exception as e:
        print(f"--- SVG MCP Server: CRITICAL ERROR during mcp.run(): {e} ---", file=sys.stderr)
        # Optionally, re-raise the exception if you want the script to exit with an error code
        # raise 