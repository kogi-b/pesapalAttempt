# Pesapal Attempt

This is a Python repository which attempts for dealing with word pluralization.
This is a Python repository which attempts to solve Problem 1 from <a href="https://pesapal.freshteam.com/jobs/2OU7qEKgG4DR/junior-developer-23">the Pesapal Careers portal.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```


## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Problem 1: A static-site generator..
Design and implement a simple static-site generator. 

It should be able to take a folder containing Markdown (or another non-HTML markup-type format) pages and produce a website. There should be support for a homepage, articles and supporting pages (e.g. an about page and some error pages).

## Solution
I created my static site generator using Python3 and jinja templates primarily. In the root directory, there are four folders. These are the backbone of the project. In the root directory, there is a main.py file which is the static site generator. The static folder contains folders with css and an image folder (img). In the templates folder you will find all templates that can be used with this static site generator. The content is where markdown files are stored, in the root of the content folder, there is a posts folder which is where all the posts go, There are other files such as the about.md and index.md which are essential for this static site generator. The output goes in the output folder.



