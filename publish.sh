#!/bin/bash

pelican content -o output -s publishconf.py --delete
ghp-import output
git push https://BertrandBordage@github.com/BertrandBordage/BertrandBordage.github.io gh-pages:master
