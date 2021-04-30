#!/usr/bin/env python3

from marko.ext.gfm import gfm
import re
import argparse

# Parge command line arguments
parser = argparse.ArgumentParser(description="Generate html/css slides from a markdown file")
parser.add_argument("source", help="your markdown source file")
parser.add_argument("-o" ,"--output", default="", help="destination file for html output")
parser.add_argument("-t" ,"--title", default="Slides", help="the title of your presentation")
parser.add_argument("-s" ,"--subtitle", default="", help="the subtitle")
parser.add_argument("-a" ,"--author", default="", help="the author name(s)")
parser.add_argument("-f" ,"--affiliation", default="", help="the affiliation text below the author")
parser.add_argument("-c" ,"--centered", action="store_true", help="center all slide content")
parser.add_argument("-n" ,"--numbered", action="store_true", help="show slide numbers")
parser.add_argument("--notitle", action="store_true", help="suppress the title slide")
args = parser.parse_args()

# Set css classes for centering and numbering
if args.centered:
    centered = "centered"
else:
    centered = ""
if args.numbered:
    numbered = "numbered"
else:
    numbered = ""

# Read markdown text
with open(args.source, "r") as f:
    text = f.read()
# Read the minislides style file
with open("minislides.css", "r") as f:
    minislides = f.read()
# Read the navigation code
with open("navigation.js", "r") as f:
    navigation = f.read()

# Split the markdown file into slides
blocks = text.split("\n---\n")
# Parse as GitHib flavoured markdown
converted_blocks = map(gfm.convert, blocks)

# Wrap each slide as a section and join them
def wrap_section(s):
    return "<section>\n" + s + "</section>\n"
sections = ''.join(map(wrap_section, converted_blocks))
# Strip out <p></p> surrounding image tags
sections = re.sub(r"<p>(<img.*)</p>", r"\1", sections)

# Build title slide
if not args.notitle:
    titlesection = f"""
        <section>
            <h1>{args.title}</h1>
            <p class="subtitle">{args.subtitle}</p>
            <p class="author">{args.author}</p>
            <p class="affiliation">{args.affiliation}</p>
        </section>
    """
    sections = titlesection + sections

# Build complete html document
html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{args.title}</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.7.2/styles/tomorrow.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.7.2/highlight.min.js"></script>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

        <style type="text/css" media="all">
            {minislides}    
        </style>
    </head>
    <body>
        <div class="slides {centered} {numbered}">
            {sections}
        </div>    
        <script type="text/javascript" charset="utf-8">
            hljs.highlightAll();

            {navigation}
        </script>
    </body>
    </html>
"""

if not args.output:
    print(html)
else:
    with open(args.output, "w") as f:
        f.write(html)
