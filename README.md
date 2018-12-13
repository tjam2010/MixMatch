# MixMatch: A Mixtape for Every Match
The general idea of MixMatch was to create a web app that allowed for users to create a custom group-playlist based upon Last.fm data.
To see the app in action, visit http://mixmatch-hcde310.appspot.com

For a brief overview, watch this introduction video:

[![MixMatch Intro]()](https://youtu.be/z8JA6_gg-aQ "MixMatch Intro")

# The Proposal
In this project, I will build a playlist-generating web application, combining information from multiple users on Last.fm that revolve around a specific tag. Often times it can be difficult for people to decide on music to listen to in a group setting, or to find similar tastes. This tool could help solve that issue, and may be of interest to multiple audiences:

- Friends and families may want to find music that they all enjoy for an event, roadtrip, or other occasion while still taking everyone’s tastes into consideration equally. They may also be curious to find new music from each other or see what songs they enjoy that overlap.
- Classes may also want to use this tool to create a playlist for the classroom that everyone has a say in and can enjoy.
- Individuals who are interested in exploring new music could find this tool useful to discover music that other people with some similar tastes listen to. 

I have chosen to a build a web application because it allows for an easily accessible interface that can be used globally. The interface can provide the ability to instantly see information and update queries to best fit the user. The value of this project depends upon whether or not users and those that they wish to create a playlist with regularly scrobble with Last.fm.

### Data Sources, Libraries, and Planned Processing
The project will take in data from Last.fm, a scrobbling service that records all of the music that users listen to and when they listen to it. Songs, artists, and albums on Last.fm have tags regarding specific genres and types of music. Each user has their own set of scrobbles that have been logged over the duration of time that they have been an active user. The Last.fm API provides both JSON and XML formats of user and musician data. I will get top tracks from the input users and also get the tags for the tracks. 

I will process the tracks to prioritize any duplicate tracks among the various users, and use the tags to identify individual songs that fit the specified genre or style. To make the playlist more useful, I will allow users to specify a length for the playlist in an effort to better suit the music to their needs.

If time permits, I will also use the Spotify API to create the playlist on their Spotify account, as opposed to providing a Last.fm or text version. This could provide an instant and tangible way for users to explore and interact with the data. I would also like to improve the organization of playlists, if time permits, finding a comfortable balance between commonly enjoyed songs and individually preferred music.


The web interface will feature input fields for the usernames of the group, decision power regarding the genre or musical style through a dropdown field, and a way for them to export the playlist to their Spotify account if desired. Ideally this playlist will maintain a consistent musical speed and tone, if I am able to fine tune the organization of the selected tracks in the time allotted.

### Tentative Development Plan

#### Week 1:
- Write Python application for downloading the top tracks of a list of users and combining them into one large list
- Obtain the users through a web interface and display their combined top tracks in a readable fashion

#### Week 2:
- Obtain tag(s) from user input through the web interface
- Filter the top tracks for common threads and selected tags

#### Week 3:
- Limit the amount of songs shared based upon user input through the web interface, and prioritize the most-likely-to-be-enjoyed songs
- Create a curated playlist for the user in text form with a title and description

#### If time permits:
- Connect to Spotify to generate a playable playlist on a specified user’s account
- Design the playlist to maintain a consistent tone and evenly mix commonly enjoyed songs with more exploratory ones
# The Obstacles
Throughout the creation of the project, several obstacles resulted in a pivot in the direction of the app. While many minor changes did occur, such as the need to include buttons to gather length and genre information, there were only a few large scale adjustments made.
Most of the large scale adjustments were a direct result of the limitations of a basic API key, since the API key restricted the amount of information that could be gathered at once. Here are some of the features that were foregone:
- The creation of extremely lengthy playlists
  - While this is still and option, there is a note warning users that the API key may not be able to handle their request
- Create a specific length for a genre filtered playlist
  - The action of filtering requests a large amount of information from Last.fm and would overload the API key were the playlist creation method to keep running until the playlist was full
- The creation of a Spotify playlist
  - I simply did not have the time to integrate the Spotify API into the app, but this is not off of the table for future updates
# The Result
Here are some screenshots of the website in its current state:
### Mobile Screenshots
### Desktop Screenshots
