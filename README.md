# minislides

This is a very minimal setup for displaying a deck of presentation slides in the browser.
Navigation using arrow keys is built in.

Take a look at this [demo](https://sahasatvik.github.io/minislides/).
This only works well on a landscape screen! You may have to zoom in or out to correctly scale the text, depending on your screen size.

These slides print to pdf best in Chrome. Make sure to print in A4 landscape, remove headers and footers, and set margins to 'none'.
You can choose to include background graphics to keep the slide background colour.

### Navigation
Use the forward and backward arrow keys (or `j` and `k` if you like vim keybindings) to change slides.
Press `0` or `9` to jump to the start or end of the presentation respectively.

### Creating slides
You can mirror the format of the demo, `index.html`. Under the `.slides` div, each slide is a section which can contain
headings, paragraphs, lists, code blocks, and images. Page numbering can be turned off by removing the `.numbering` class from
the `.slides` div.
