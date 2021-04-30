title: A brief demonstration of minislides
subtitle: Simple presentations using HTML/CSS
author: Satvik Saha
affiliation: Indian Institute of Science Education and Research, Kolkata


---


## Basic text

This is a sentence.

This is another sentence, with **bold** and _italics_.

> This is a blockquote!

~~This sentence has been struck off.~~

### Subheading

This is a [hyperlink](https://github.com/sahasatvik/minislides) to the GitHub repository of this project.


---


## Displaying code

This slide contains a block of python code.
```python
import marko

with open("markdown.md", "r") as f:
    text = f.read()

html = marko.convert(text)
```

The `with open(...) as f` construct ensures that the file is closed after reading from it.


---


## Math expressions

This slide demonstrates the use of math expressions, supported by MathJax.

### Cauchy's Integral Formula
Let \\(U\\) be an open subset of the complex plane, and let \\(D\\) be a closed disk completely contained in \\(U\\).
Let \\(f\\) be a holomorphic function on \\(U\\), and let \\(\\gamma\\) be the circle oriented counter-clockwise forming the boundary of \\(D\\).
Then for every \\(z_0\\) in the interior of \\(D\\), \\[
    f(z_0) = \\frac{1}{2\\pi i}\\oint_\\gamma \\frac{f(z)}{z - z_0}\\:dz.
\\]


---


## Lists

This is an unordered list.

* Item 1
* Item 2
* Item 3

<br>

This is an ordered list

1. Item 1
2. Item 2
3. Item 3


---


## Tables

| Left aligned | Centered  | Right aligned |
|--------------|:---------:|--------------:|
| Item 1       |  Item 2   |        Item 3 |
| Item 4       |  Item 5   |        Item 4 |
| Item 5       |  Item 6   |        Item 7 |


---


## Images

<p class="centered">
This is a random image from <a href="https://source.unsplash.com">unsplash</a>.
</p>

![Nature](https://source.unsplash.com/featured/?nature)

<p class="centered">The next slide shows a large image</p>


---


<img class="large" src="https://source.unsplash.com/featured/?space" alt="">


---


## Using raw HTML tags

The previous two slides contained raw paragraph and image tags in the markdown source, to center text and specify a large image.

```html
<p class="centered">This is centered text</p>

<img class="large" 
    src="https://source.unsplash.com/featured/?space" 
    alt="This is a large image">
```

Note that markdown syntax does not work within raw HTML tags!
