Flickr Crawler
=============

Flickr photo/friendship crawler

## General description

In this project we implemented two crawlers for Flickr website. Our code is in Python and it runs in two levels.

## Author
 
Kazem Jahanbakhsh

## Technical details

This project includes the following two crawlers:

## Friendship graph crawler
 
This Python code runs a BFS on social graph of Flickr (the friendship graph) to extract the friendship connectivities among Flickr users.
    
## Photos crawler

This crawler uses the social graph collected by the first crawler. It examines every node in frienship graph and collects all possible information about users social profiles by using the Flickr API. It also crawls all photosets uploaded by each user and downloads different attributes of each photo. However, this code does not download the photos itself. You can run the crawler as follows:

	python flickr-crawler.py
