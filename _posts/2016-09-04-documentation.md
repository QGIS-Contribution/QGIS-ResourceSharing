---
layout: page
title: "Documentation"
category: dev
date: 2016-09-04 21:15:55
order: 2
---
We are using Jekyll for our documentation (i.e this website). If you want to 
contribute to the documentation, please check out ```gh-pages``` branch (yes,
 this documentation is hosted on Github pages). 
 
This documentation is divided into 3 categories: for users, for authors, 
 and for developers section. To update a particular page, find the markdown 
 file in ```_posts``` directory. To make a new page, run ```bin/jekyll-page [page title] [category_code]```. The codes for the category are: ```user``` 
 (will be put in For User section), ```author``` (for authors section), and 
 ```dev``` (for developers section).
 
After you make changes to the documentation, please make a PR to branch 
 ```gh-pages``` in the upstream repository.
  
If you have images to show, put it in ```assets``` directory and to use it in
 your post, just like usual in markdown, you can reference it by writing: ```![alt_text]({{ site.baseurl }}/assets/[the_image_path])```
 


