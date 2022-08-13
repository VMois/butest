# butest

## Task 1 - Product feed

### How to run

1. Place SQLite database file in the folder, name it `data.sqlite`.
2. In the terminal, run `python task1.py` (recommended *Python 3.9*). The script will generate `feed.xml` file.
3. The script `feed.xml` is geneCheck generated `feed.xml` file.

### Explanations

The database size is small, so we can work with data in-memory.
The script itself is a simple ETL process:

1. Fetch additional images for projects in order. Save them in-memory.
2. Fetch products with description and brand values. Populate them with additional images from previous step. 
3. Generate and save Google Product XML file.

Notes:

- `sqlite` standard package is used over `sqlalchemy` to simplify the script.
- `Product` class is a simple abstraction. It is good enough for assigment, but something like proper `sqlalchemy` models might be better.

### References

- [Google Product XML file example](https://support.google.com/merchants/answer/160589?hl=en)
- [Google Product Data specification](https://support.google.com/merchants/answer/7052112#zippy=,quick-reference)
- [RSS specification](https://validator.w3.org/feed/docs/rss2.html#:~:text=RSS%20is%20a%20Web%20content,Web%20Consortium%20(W3C)%20website.
)
- [Google Product Feed article on Bluewinston](https://www.bluewinston.com/what-is-google-shopping-product-feed-specification-and-how-can-it-benefit-you/
)
- [Online SQLite Viewer](https://inloop.github.io/sqlite-viewer/)

## Task 2 - Cypress

### How to run

1. Run `npm install` to get all packages.
2. Run `npx cypress run` to launch tests in the command line OR run `npx cypress open` to launch Cypress app and browser for interactive environment.
3. Check screenshot `*.png` with test output results.

### Explanations

I have never used Cypress, so it was interesting experience.
Not much to say. I have followed tutorials, docs and Google to complete the task.

Notes:
- the website is a bit different from what is stated in the task, so some adjustments were need.