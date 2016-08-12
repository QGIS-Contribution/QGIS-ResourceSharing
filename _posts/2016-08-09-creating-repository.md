---
layout: page
title: "Creating Repository"
category: author
date: 2016-08-09 11:13:38
order: 1
---
#### Preparing the Repository
In order for the tools to parse the repository correctly, you need to prepare
 the repository to have a certain structure. This is what you need to do:
  
  * The repository has to follow the structure. Please go to [this page]({{ 
  site.baseurl }}/author/repository-structure.html) that explains about it
  * Create the correct metadata for the repository. For that, please read 
  [this page]({{ site.baseurl }}/author/creating-metadata.html)
  * Once you have it prepared, you can check if the repository is all good by
   trying it using file system handler. In the plugin, go to ```Settings``` 
   tab and add a new repository pointing to the root of the repository in 
   your local file system. The repository URL might look like 
   this on Linux: ```file:///home/pointing/to/repository_root``` or in Windows
    it looks more like this: ```file://C:/home/pointing/to/repository_root```

#### Where can you  share it?
There are some options where you can put your repository: on Github, 
Bitbucket (they need to be public repositories), local file system 
(if you want to share the collections with your colleagues on the network), 
or in your own server with http(s) protocol.

##### Github and Bitbucket
So you decided to put your repositories on this platform. There is nothing 
complicated here if you are already familiar with git. After preparing the 
repository in your local machine, you can make it as git repository like 
usual. In general, you can do:

```
cd <repository root>
git init
git add .
git commit -m "Created a cool repository for cool users."
git remote add origin <remote repository URL>
git push origin master
```

Note that right now you need to use branch ```master``` for your repository.

##### Local File System
Well, this one is even simpler. After preparing the repository, you can use 
it right away. In the ```Settings``` tab, try to add a repository with URL 
pointing to the repository root in your local machine. It's as simple as that. If there is a problem with metadata or other issues when adding the 
repository, the tools will tell you.

##### Your Own Server
This option could be useful in some cases e.g you want to make private 
collections available for your customers. There are some additional 
requirements that you need to be aware of if you choose this option:

  * The URL structure of the repository. Let's say your base repository URL 
  is ```http://www.akbargumbira.com/repository```. You need to put the 
  metadata available on this URL: ```http://www.akbargumbira
  .com/repository/metadata.ini```
  * The collections must be in zip format. For example, if you have a 
  collection named ```test_collection```, the collection must exist in: 
  ```http://www.akbargumbira.com/repository/collections/test_collection.zip```
  * The preview images are relative to the collection base URL. As an example,
   if you define the preview images in the metadata ```preview=preview/prev1.png, preview/prev2.png```, it is needed that you have to make the previews 
  available for collection ```test_collection``` in this URL: ```http://www.akbargumbira.com/repository/collections/test_collection/preview/prev1.png``` and ```http://www.akbargumbira.com/repository/collections/test_collection/preview/prev2.png```

You can also put authentication to this repository as you wish. In the 
plugin, users can configure authentication details so that they will be able 
to fetch the repository and the collections inside.

