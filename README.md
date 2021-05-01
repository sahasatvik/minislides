# minislides

This is a script for parsing markdown files into minimal HTML/CSS slide decks, which can be presented in the browser.

Take a look at this [demo](https://sahasatvik.github.io/minislides/demo.html) presentation.
Note that this only works well on a landscape screen! You may have to zoom in or out to correctly scale the text, depending on your screen size.
Compare with the input markdown file, [demo.md](demo.md).

### Dependencies
The `minislides.py` script uses the [marko](https://github.com/frostming/marko) library for parsing markdown.
Install it using 
```
pip install marko
```

## Writing a presentation
The [demo.md](demo.md) demonstrates the format for writing slides. Use [GitHub flavored markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet),
separating slides with `---` surrounded by blank lines.
You should also specify a header including the title slide information, as follows.

```markdown
title: A snappy title
subtitle: Additional information
author: John Doe
affiliation: Unseen University

---

## Slide 1

This is a sentence.

---

## Slide 2

More text, **bold** and _italicized_.
```

The demo also shows how to use raw HTML tags in your markdown.

### Compiling to HTML
Run `./minislides.py -h` (make sure you are using python3) to get a list of available options.
```
usage: minislides [-h] [-o OUTPUT] [-c] [-n] [--notitle] [--css CSS] [--js JS] source

Generate html/css slides from a markdown file

positional arguments:
  source                your markdown source file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        destination file for html output
  -c, --centered        center all slide content
  -n, --numbered        show slide numbers
  --notitle             suppress the title slide
  --css CSS             .css file for additional styling
  --js JS               .js file for additional functionality
```

The command used to compile the demo presentation was 
```sh 
./minislides.py --numbered demo.md --output demo.html
```

### Navigation
Navigation using arrow keys is built in using javascript.
Use the forward and backward arrow keys (or `j` and `k` if you prefer vim keybindings) to change slides.
Press `0` or `9` to jump to the start or end of the presentation respectively.

### Printing or saving to pdf
These slides print to pdf best in Chrome. Make sure to print in A4 landscape, remove headers and footers, and set margins to 'none'.
You can choose to include background graphics to keep the slide background colour.
