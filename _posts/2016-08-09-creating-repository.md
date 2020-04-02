---
layout: page
title: "Creating a repository"
category: author
date: 2016-08-09 11:13:38
order: 1
---
#### Preparing the Repository
In order for the tools to parse the repository correctly, the repository
must have a certain structure. This is what you need to do:
  
  * Go to [this page]({{site.baseurl }}/author/repository-structure.html)
    to get information about the structure.
  * Create correct metadata for the repository (consult
    [this page]({{ site.baseurl }}/author/creating-metadata.html)).
  * When you have prepared your repository, you can check if the repository
    is all good by trying it using the file system handler.
    In the plugin, go to the ```Settings``` tab and add a new repository
    pointing to the root of the repository in your local file system.
    The repository URL looks like this on Linux:
    ```file:///home/pointing/to/repository_root``` and like this:
    ```file://C:/home/pointing/to/repository_root``` on Windows.

#### Where can you  share it?
These are the options for sharing: on Github, Bitbucket (they need to be
public repositories), local file system (if you want to share the
collections with your colleagues on the network), or in your own server
with the HTTP(S) protocol.

**Github and Bitbucket**

There is nothing complicated here if you are already familiar with git.
After preparing the repository on your local machine, you can make it
into a git repository as usual. In general, you can do:

```
cd <repository root>
git init
git add .
git commit -m "Created a cool repository for cool users."
git remote add origin <remote repository URL>
git push origin master
```

Note that you currently need to use the ```master``` branch
for your repository.


**Local File System**

This is even simpler. After preparing the repository, you can use 
it right away. In the ```Settings``` tab, you add a repository with URL 
pointing to the repository root in your local machine (absolute path,
example: `file:/home/user/QGIS-collections/mycollection`).
It's as simple as that.
If there is a problem with metadata or other issues when adding the 
repository, you will be told.


**Your Own Server**

This option could be useful in some cases, e.g. if you want to make private 
collections available for your customers.
There are some additional requirements that you need to be aware of if you
choose this option:

  * The URL structure of the repository. If your base repository URL 
    is ```http://www.akbargumbira.com/repository```, you must make the 
    metadata available on:
    ```http://www.akbargumbira.com/repository/metadata.ini```
  * The collections must be in zip format. For example, if you have a 
    collection named ```test_collection```, the collection must exist in: 
    ```http://www.akbargumbira.com/repository/collections/test_collection.zip```
  * The preview images are relative to the collection base URL. As an example,
   if you define the preview images in the metadata
   (```preview=preview/prev1.png, preview/prev2.png```), you have to make the
   previews available for collection ```test_collection``` in this URL:
   ```http://www.akbargumbira.com/repository/collections/test_collection/preview/prev1.png```
   and
   ```http://www.akbargumbira.com/repository/collections/test_collection/preview/prev2.png```

You can also use authentication for this repository.
In the  plugin, users can configure authentication details so that they will
be able to fetch the repository and the collections inside.
