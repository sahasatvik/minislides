# minislides

This is a script for parsing markdown files into minimal HTML/CSS slide decks, which can be presented in the browser.

Take a look at this [demo](https://sahasatvik.github.io/minislides/demo.html) presentation.
Note that this only works well on a landscape screen! You may have to zoom in or out to correctly scale the text, depending on your screen size.
Compare with the input markdown file, [demo.md](demo.md).

Here's the title slide of the demo.
![Title](https://user-images.githubusercontent.com/16478483/116789159-1f96ed80-aacb-11eb-8f9a-ef9f4af2dd6b.jpg)

### Dependencies
The `minislides.py` script uses the [marko](https://github.com/frostming/marko) library for parsing markdown.
Install it using 
```
pip install marko
```

## Writing a presentation
The [demo.md](demo.md) demonstrates the format for writing slides, along with a few additional features of the default css style.
Use [GitHub flavored markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet), separating slides with `---` surrounded by blank lines.
You should also specify a header including the title slide information, as in the following example.

````markdown
title: Quickstart
subtitle: A short demo of minislides
author: John Doe
affiliation: Unseen University

---

## Title of your first slide!

This is a sentence, on its own paragraph.

You can use the usual markdown features, like **bold** and _italicized_ text.

---

## Your second slide.

Including [hyperlinks](https://github.com) and images is simple.

![Random image](https://source.unsplash.com/random)

---

Code highlighting is supported by [highlight.js](https://highlightjs.org), and math is supported
using $\KaTeX$.

```python
a, b = 0, 1
for i in range(20):
    a, b = b, a + b
    print(a)
```

This prints the Fibonacci numbers, which satisfy $$
  F_n = F_{n - 1} + F_{n - 2}.
$$

````

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

Suppose that the example code above was saved as `quickstart.md`. To compile this to HTML, with slide numbers, run
```
./minislides.py -n quickstart.md -o quickstart.html
```
Now, you can open `quickstart.html` in your browser of choice and start presenting!
Here's what the slides look like.
![Quickstart](https://user-images.githubusercontent.com/16478483/116789320-eca12980-aacb-11eb-999e-819b1aaefccf.jpeg)


### Navigation
Navigation using arrow keys is built in using javascript.
Use the forward and backward arrow keys (or `j` and `k` if you prefer vim keybindings) to change slides.
Press `0` or `9` to jump to the start or end of the presentation respectively.

### Printing or saving to pdf
These slides print to pdf best in Chrome. Make sure to print in A4 landscape, remove headers and footers, and set margins to 'none'.
You can choose to include background graphics to keep the slide background colour.
