This repository contains archived source code for the public-facing website for South 
Charlotte Presbyterian Church in Charlotte, NC. This code is no longer hosted.

The site is backed by the Django and Wagtail CMS frameworks and it builds with Yarn and 
webpack. It runs in [Divio Cloud](https://www.divio.com/wagtail/), and a number of Python 
scripts and configuration files are auto-generated by the Divio platform. The main 
implementation lives in the following directories:

| Directory | Contents |
|-----------|----------|
| `scpc/`   | Django backend |
| `static/scpc/` | SCSS, JS/ES2015+, fonts, and images |
| `templates/` | HTML |
