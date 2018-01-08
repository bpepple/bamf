Bamf is a Django project that allow you to read comic book archives. It is based on [Tenma](https://github.com/Tenma-Server/Tenma) and uses the [ComicVine](http://comicvine.gamespot.com) [API](http://comicvine.gamespot.com/api) to retrieve the comic metadata. Most of the difference are behind the interface like:
* Instead of querying Comic Vine for matches, we read in the comic archive comicinfo.xml (which means you need to tag your comic archives with [ComicTagger](https://github.com/davide-romanini/comictagger)), and get the detailed information from Comic Vine.
* Read the comic archive directly, instead of unzipping the file in a directory.
* Images from comic vine are resized on import, and the original is removed.

### Features ###
* Reads comic archives (cbz)
* See how your comics are connected by characters, creators, teams, story arcs and publishers.
* Comic navigation with arrow buttons, or with your keyboard's arrow keys.
* REST API

### Installation ###
To install, please refer to the [Bamf Wiki](https://github.com/bpepple/bamf/wiki/Installation-on-Linux).

### Screenshots ###
#### Series List ####
![series](/screenshots/series-list.jpg?raw=true "Series List")
#### Series Detail ####
![series-detail](/screenshots/series-detail.jpg?raw=true "Series Detal")
#### Issue Detail ####
![issue-detail](/screenshots/issue-detail.jpg?raw=true "Issue Detail")
#### Reader ####
![reader](/screenshots/reader.jpg?raw=true "Reader")
