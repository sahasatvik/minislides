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

# Set the css and js contents
minislides = """
@import url('https://fonts.googleapis.com/css2?family=Gentium+Basic:ital,wght@0,400;0,700;1,400;1,700&display=swap');@import url('https://fonts.googleapis.com/css2?family=Fira+Code&display=swap');:root{--background-light: #fdfdfd;--text-dark: #101010;--blue: #4271ae;--green: #718c00;--orange: #f5871f;--gray-light: #bbbbbb;}*{margin: 0;padding: 0;}body{background: gray;}.slides section{position: relative;box-sizing: border-box;background: var(--background-light);margin: 16px auto 8px auto;padding: 4rem;height: calc(100vh - 16px);width: calc(100vh * 1.414);display: flex;flex-direction: column;justify-content: center;align-items: center;font-family: 'Gentium Basic', serif;}.slides section:nth-child(1){margin-top: 8px;}.slides.numbered{counter-reset: section;}.slides.numbered section::after{position: absolute;bottom: 1rem;right: 1.5rem;counter-increment: section;content: counter(section);font-size: 1rem;color: var(--text-dark);opacity: 0.7;}.slides.numbered section:nth-child(1)::after{counter-increment: none;content: '';}@media print {.slides section { margin: 0 !important;height: 100vh;width: auto;page-break-after: always;page-break-inside: avoid;}}.slides h1,.slides h2,.slides h3,.slides p,.slides ul,.slides ol,.slides blockquote{text-align: left;width: 70%;color: var(--text-dark);}.slides.centered h1, .slides section.centered h1,.slides.centered h2, .slides section.centered h2,.slides.centered h3, .slides section.centered h3,.slides.centered p, .slides section.centered p,.slides.centered ul, .slides section.centered ul,.slides.centered ol, .slides section.centered ol,.slides.centered blockquote, .slides section.centered blockquote{text-align: center;width: auto;max-width: 70%;}.slides .centered{text-align: center;}.slides h1{padding: 0 0 1rem 0;font-size: 3rem;opacity: 0.85;box-shadow: inset 0 -3px var(--orange);}.slides .subtitle{margin: 1rem 0;font-size: 1.5rem;opacity: 0.7;}.slides .author{margin: 4rem 0 0 0;font-size: 1.9rem;font-style: italic;}.slides .affiliation{margin: 0.1rem 0;font-style: italic;opacity: 0.7;}.slides h2{font-size: 2rem;margin: 1.5rem 0;}.slides h3{font-size: 1.7rem;margin: 1rem 0 0.5rem 0;}.slides p{font-size: 1.5rem;margin: 0.5rem 0;line-height: 1.4em;}.slides ul,.slides ol{font-size: 1.5rem;margin: 0.3rem 0;line-height: 1.2em;}.slides blockquote{margin: 1rem 0;box-shadow: inset 8px 0 var(--gray-light);}.slides blockquote p{width: auto;padding-left: 6ch;opacity: 0.9;font-style: italic;}.slides i,.slides em{color: var(--green);}.slides b,.slides strong{color: var(--orange);}.slides a{text-decoration: none;color: var(--blue);}.slides code,.slides pre{font-family: 'Fira Code', monospace;background: none;}.slides p code{font-size: 1.2rem;color: var(--blue);}.slides pre code{font-size: 1.2rem;margin: 1rem 0;}.slides img{max-width: 70%;max-height: 80%;margin: 1rem 0;}.slides img.large{max-width: 100%;max-height: 100%;}.slides table{font-size: 1.5rem;margin: 1rem 0;overflow: scroll;border-collapse: collapse;}.slides th,.slides td{padding: 0.2rem 0.5rem;}.slides thead{border-bottom: 2px solid var(--text-dark);}
"""
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