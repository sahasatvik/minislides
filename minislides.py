#!/usr/bin/env python3

from marko.ext.gfm import gfm
import argparse
import re
import sys
import errno


# Minified default css styling
minislides = """
@import url('https://fonts.googleapis.com/css2?family=Gentium+Basic:ital,wght@0,400;0,700;1,400;1,700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Fira+Code&display=swap');
:root{--background-light: #fdfdfd;--text-dark: #101010;--blue: #4271ae;--green: #718c00;--orange: #f5871f;--gray-light: #bbbbbb;}*{margin: 0;padding: 0;}body{background: gray;}.slides section{position: relative;box-sizing: border-box;background: var(--background-light);margin: 16px auto 8px auto;padding: 2rem;height: calc(100vh - 16px);width: calc((100vh - 16px) * 1.414);max-width: calc(100vw - 16px);display: flex;flex-direction: column;justify-content: center;align-items: center;font-family: 'Gentium Basic', serif;}.slides section:nth-child(1){margin-top: 8px;}@media (max-width: 600px), (max-height: 500px) {.slides section { height: auto;min-height: calc(100vh - 16px);}}.slides.numbered{counter-reset: section;}.slides.numbered section::after{position: absolute;bottom: 1rem;right: 1.5rem;counter-increment: section;content: counter(section);font-size: 1rem;color: var(--text-dark);opacity: 0.7;}.slides.numbered section:nth-child(1)::after{counter-increment: none;content: '';}@media print {body { background: var(--background-light);}    .slides section{margin: 0 !important;height: 100vh !important;width: 100% !important;page-break-after: always;page-break-inside: avoid;}}.slides h1,.slides h2,.slides h3,.slides p,.slides ul,.slides ol,.slides blockquote{text-align: left;-webkit-hyphens: auto;-moz-hyphens: auto;-ms-hyphens: auto;hyphens: auto;width: 70%;max-width: 70%;color: var(--text-dark);}@media (max-width: 500px) {.slides h1, .slides h2, .slides h3, .slides p, .slides ul, .slides ol, .slides blockquote { width: 90%;max-width: 90%;}}.slides.centered h1, .slides section.centered h1,.slides.centered h2, .slides section.centered h2,.slides.centered h3, .slides section.centered h3,.slides.centered p, .slides section.centered p,.slides.centered ul, .slides section.centered ul,.slides.centered ol, .slides section.centered ol,.slides.centered blockquote, .slides section.centered blockquote{text-align: center;width: auto;}.slides .centered{text-align: center;}.slides h1{padding: 0 0 1rem 0;font-size: 3rem;opacity: 0.85;box-shadow: inset 0 -3px var(--orange);}.slides .subtitle{margin: 1rem 0;font-size: 1.5rem;opacity: 0.7;}.slides .author{margin: 4rem 0 0 0;font-size: 1.9rem;font-style: italic;}.slides .affiliation{margin: 0.1rem 0;font-style: italic;opacity: 0.7;}.slides h2{font-size: 2rem;margin: 1.5rem 0;}.slides h3{font-size: 1.7rem;margin: 1rem 0 0.5rem 0;}.slides p{font-size: 1.5rem;margin: 0.5rem 0;line-height: 1.4em;}.slides ul,.slides ol{font-size: 1.5rem;margin: 0.3rem 0;line-height: 1.2em;}.slides blockquote{margin: 1rem 0;box-shadow: inset 8px 0 var(--gray-light);}.slides blockquote p{width: auto;padding-left: 6ch;opacity: 0.9;font-style: italic;}.slides i,.slides em{color: var(--green);}.slides b,.slides strong{color: var(--orange);}.slides a{text-decoration: none;color: var(--blue);}.slides code,.slides pre{font-family: 'Fira Code', monospace;background: none;}.slides p code{font-size: 1.2rem;color: var(--blue);}.slides pre{max-width: 100%;}.slides pre code{font-size: 1.2rem;margin: 1rem 0;overflow-x: scroll;}.slides img{max-width: 70%;max-height: 80%;margin: 1rem 0;}.slides img.large{max-width: 100%;max-height: 100%;}.slides table{font-size: 1.5rem;margin: 1rem 0;overflow: scroll;border-collapse: collapse;}.slides th,.slides td{padding: 0.2rem 0.5rem;}.slides thead{border-bottom: 2px solid var(--text-dark);}.katex{font-size: 1.07em !important;}
"""

# Minified js for keyboard navigation
navigation = """
var slides=document.getElementsByTagName("section");var totalSlides=slides.length;var prev=[37,75,72];var next=[39,74,76,13];var start=[48];var end=[57];function percentageVisible(element){const viewHeight=(window.innerHeight||document.documentElement.clientHeight);const bounds=element.getBoundingClientRect();if(bounds.bottom<0||bounds.top>viewHeight){return 0;}
if(bounds.top<0&&bounds.bottom>viewHeight){return bounds.height*100/viewHeight;}else if(bounds.top<0){return bounds.bottom*100/viewHeight;}else if(bounds.bottom>viewHeight){return(viewHeight-bounds.top)*100/viewHeight;}
return 100;}
function getCurrentSlide(){var index=0;var maxPercent=0;for(var i=0;i<totalSlides;i++){let p=percentageVisible(slides[i]);if(p>maxPercent){index=i;maxPercent=p;}}
return index;}
function navigate(nextSlide){let target=nextSlide;if(nextSlide<0){target=0;}else if(nextSlide>=totalSlides){target=totalSlides-1;}
window.scrollTo(0,slides[target].offsetTop-8);}
document.addEventListener("keydown",event=>{let code=event.keyCode;let currentSlide=getCurrentSlide();if(prev.includes(code)){navigate(currentSlide-1);}else if(next.includes(code)){navigate(currentSlide+1);}else if(start.includes(code)){navigate(0);}else if(end.includes(code)){navigate(totalSlides-1);}});
"""

# Katex settings
katex = r"""
    document.addEventListener("DOMContentLoaded", function() {
        renderMathInElement(document.body, {
          delimiters: [
              {left: '$$', right: '$$', display: true},
              {left: '$', right: '$', display: false},
              {left: '\\(', right: '\\)', display: false},
              {left: '\\[', right: '\\]', display: true}
          ],
          throwOnError : false
        });
    });
"""


# Read the contents of a text file
def readfile(filename):
    try:
        with open(filename, "r") as f:
            text = f.read()
        return text
    except FileNotFoundError:
        print("Cannot find " + filename)
        sys.exit(errno.ENOENT)


# Parse a block of markdown into an HTML section slide
def parse_block(block):
    # Convert block from markdown to HTML
    html = gfm.convert(block)
    # Strip out <p></p> surrounding image tags
    html = re.sub(r"<p>(<img[\s\S]*?)</p>", r"\1", html)
    # Wrap in a section tag
    return "<section>\n" + html + "</section>\n"


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate html/css slides from a markdown file")
    parser.add_argument("source", help="your markdown source file")
    parser.add_argument("-o" ,"--output", default="", help="destination file for html output")
    parser.add_argument("-c" ,"--centered", default=False, action="store_true", help="center all slide content")
    parser.add_argument("-n" ,"--numbered", default=False, action="store_true", help="show slide numbers")
    parser.add_argument("--notitle", default=False, action="store_true", help="suppress the title slide")
    parser.add_argument("--css", default="", help=".css file for additional styling")
    parser.add_argument("--js", default="", help=".js file for additional functionality")
    args = parser.parse_args()

    # Set css classes for centering and numbering
    centered = "centered" if args.centered else ""
    numbered = "numbered" if args.numbered else ""

    # Read markdown text
    text = readfile(args.source)

    # Split the markdown file into slides
    blocks = text.split("\n---\n")
    
    # Peel off the header
    header = blocks[0]

    # Set default title slide information
    title = "minislides"
    subtitle = ""
    author = ""
    affiliation = ""

    # Read the markdown header information
    for line in header.splitlines():
        line = line.strip()
        if line.startswith("title"):
            title = line.split(":", 1)[1].strip()
        elif line.startswith("subtitle"):
            subtitle = line.split(":", 1)[1].strip()
        elif line.startswith("author"):
            author = line.split(":", 1)[1].strip()
        elif line.startswith("affiliation"):
            affiliation = line.split(":", 1)[1].strip()

    # Build title slide
    titlesection = f"""
        <section>
            <h1>{title}</h1>
            <p class="subtitle">{subtitle}</p>
            <p class="author">{author}</p>
            <p class="affiliation">{affiliation}</p>
        </section>
    """ if not args.notitle else ""

    # Parse remaining blocks as GitHub flavoured markdown
    sections = ''.join(map(parse_block, blocks[1:]))

    # Add the tile slide to the beginning
    sections = titlesection + sections


    # Get the additional css and js files
    css = readfile(args.css) if args.css else ""
    js = readfile(args.js) if args.js else ""

    # Build complete html document
    html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{title}</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.7.2/styles/tomorrow.min.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.7.2/highlight.min.js"></script>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.13.3/dist/katex.min.css" integrity="sha384-ThssJ7YtjywV52Gj4JE/1SQEDoMEckXyhkFVwaf4nDSm5OBlXeedVYjuuUd0Yua+" crossorigin="anonymous">
            <script defer src="https://cdn.jsdelivr.net/npm/katex@0.13.3/dist/katex.min.js" integrity="sha384-Bi8OWqMXO1ta+a4EPkZv7bYGIes7C3krGSZoTGNTAnAn5eYQc7IIXrJ/7ck1drAi" crossorigin="anonymous"></script>
            <script defer src="https://cdn.jsdelivr.net/npm/katex@0.13.3/dist/contrib/auto-render.min.js" integrity="sha384-vZTG03m+2yp6N6BNi5iM4rW4oIwk5DfcNdFfxkk9ZWpDriOkXX8voJBFrAO7MpVl" crossorigin="anonymous"></script>

            <style type="text/css" media="all">
                {minislides}    
                {css}
            </style>
        </head>
        <body>
            <div class="slides {centered} {numbered}">
                {sections}
            </div>    
            <script type="text/javascript" charset="utf-8">
                hljs.highlightAll();
                {katex}
                {navigation}
                {js}
            </script>
        </body>
        </html>
    """

    # Dump to the command line unless the --output option is specified
    if not args.output:
        print(html)
    else:
        with open(args.output, "w") as f:
            f.write(html)


if __name__ == '__main__':
    sys.exit(main())
