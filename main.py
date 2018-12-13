import urllib, urllib2, json, webbrowser, operator, jinja2, os, logging
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                                       extensions=['jinja2.ext.autoescape'],
                                       autoescape=True)

tvals = {'usernames': []}


def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)


def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print 'The server couldn\'t fulfill the request.'
        print 'Error code: ', e.code
    except urllib2.URLError, e:
        print 'We failed to reach a server'
        print 'Reason: ', e.reason
    return None


import lastfm_key


def lfmREST(baseurl='http://ws.audioscrobbler.com/2.0/',
            method='user.getTopTracks',
            api_key=lastfm_key.key,
            format='json',
            params={},
            printurl=False
            ):
    params['method'] = method
    params['api_key'] = api_key
    params['format'] = format
    if format == "json": params["nojsoncallback"] = True
    url = baseurl + "?" + urllib.urlencode(params)
    if printurl:
        print(url)
    return safeGet(url)


class User:
    def __init__(self, username, limit=10):
        self.username = username
        self.limit = limit

    def getTopTracks(self):
        req = lfmREST(params={"user": self.username, "limit": self.limit}, printurl=False)
        tracks = req.read().decode('utf-8').encode('ascii', 'replace')
        tdata = json.loads(tracks)
        tracks = []
        for track in range(len(tdata["toptracks"]["track"])):
            tracks.append(Song(tdata["toptracks"]["track"][track]))
        return tracks

    def getTrackTags(self):
        return None

    def getTaggedTracks(self, tag):
        return None

    def __str__(self):
        tracks = self.getTopTracks()
        # print(pretty(tdata))
        header = self.username + "'s Top Tracks\n- - - - - - - - - - - - - - -\n"
        list = ""
        for track in tracks:
            list += track.rank + ". " + str(track)
        return header + list


class Playlist:
    def __init__(self, users, genre=None):
        self.genre = genre
        if genre is not None:
            self.title = genre + " music with " + users[0].username + " and friends"
            self.songs = self.genreFilter(users, genre)
        else:
            self.title = users[0].username + " and friends"
            self.songs = self.combine(users)
        self.length = 1

    def getActualLength(self):
        return 1

    def combine(self, users):
        songs = {}
        for user in users:
            for song in user.getTopTracks():
                if song.value is None:
                    song.setValue(users)
                if songs.get(str(song), 0) == 0:
                    songs[str(song)] = song
                else:
                    song.value += 50
        return sorted(songs, key=lambda x: songs[x].value, reverse=True)

    def genreFilter(self, users, genre):
        genrePlaylist = {}
        for user in users:
            for song in user.getTopTracks():
                if genre in song.tags:
                    if song.value is None:
                        song.setValue(users)
                    if genrePlaylist.get(str(song), 0) == 0:
                        genrePlaylist[str(song)] = song
                    else:
                        song.value += 50
        return sorted(genrePlaylist, key=lambda x: genrePlaylist[x].value, reverse=True)

    def strList(self):
        str_songs = []
        for song in self.songs:
            str_songs.append(song)
        return str_songs

    def __str__(self):
        list = ""
        for song in self.songs:
            list += song
        return list


class Song:
    def __init__(self, sdata):
        self.rank = sdata["@attr"]["rank"]
        self.title = sdata["name"]
        self.artist = sdata["artist"]["name"]
        self.tags = self.getTags()
        self.duration = sdata["duration"]
        self.value = None
        if len(sdata["image"]) != 0:
            self.image = sdata["image"][len(sdata["image"]) - 1]
        self.url = sdata["url"]

    def getTags(self):
        tagreq = lfmREST(method="track.gettoptags", params={"artist": self.artist, "track": self.title}, printurl=False)
        tags = tagreq.read().decode('utf-8').encode('ascii', 'replace')
        tagdata = json.loads(tags)
        tags = []
        # if (len(tagdata["toptags"]["tag"]) > 1):
        #     print(pretty(tagdata["toptags"]["tag"][0]["name"]))
        try:
            for tag_pos in range(len(tagdata["toptags"]["tag"])):
                if len(tagdata["toptags"]["tag"]) > 1:
                    tags.append(tagdata["toptags"]["tag"][tag_pos]["name"])
        except KeyError:
            return tags
        return tags

    def setValue(self, users):
        totalplays = 0
        for user in users:
            playreq = lfmREST(method="track.getinfo", params={"artist": self.artist, "track": self.title,
                                                               "user": user.username}, printurl=False)
            playdata = json.loads(playreq.read().decode('utf-8').encode('ascii', 'replace'))
            try:
                totalplays += int(playdata["track"]["userplaycount"])
            except KeyError:
                totalplays += 0
        self.value = totalplays

    def __str__(self):
        return self.artist + " - " + self.title + "\n"


# sunf = User("sunfreezfilms")
# madz = User("sheriffmaddy")
# friends = [sunf, madz]
# print(Playlist(friends,"indie"))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("In MainHandler")

        tvals['page_title'] = "MixMatch"
        tvals["usernames"] = ["sunfreezfilms", "sheriffmaddy"]
        tvals["genre"] = None
        tvals["length"] = None
        template = JINJA_ENVIRONMENT.get_template('mixmatchhome.html')
        self.response.write(template.render(tvals))


class MixMatchResponseHandler(webapp2.RequestHandler):
    def post(self):
        if self.request.POST.get('addbttn'):
            uname_add = self.request.get('uinput')
            if uname_add is not None and uname_add != "":
                tvals['usernames'].append(uname_add)

            template = JINJA_ENVIRONMENT.get_template('mixmatchhome.html')
            self.response.write(template.render(tvals))
        elif self.request.POST.get('rmbttn'):
            if len(tvals['usernames']) != 0:
                tvals['usernames'].pop()

            template = JINJA_ENVIRONMENT.get_template('mixmatchhome.html')
            self.response.write(template.render(tvals))
        elif self.request.POST.get('genrebttn'):
            tvals["genre"] = self.request.get("genre")

            template = JINJA_ENVIRONMENT.get_template('mixmatchhome.html')
            self.response.write(template.render(tvals))
        elif self.request.POST.get('lengthbttn'):
            length = self.request.get('length')
            tvals["length"] = length

            template = JINJA_ENVIRONMENT.get_template('mixmatchhome.html')
            self.response.write(template.render(tvals))
        elif self.request.POST.get("getbttn"):
            tvals['page_title'] = "Match Results"
            if 2 <= len(tvals['usernames']) <= 10:
                users = []
                if tvals["length"] is not None and .5 <= int(tvals["length"]) <= 24:
                    limit = (int(tvals["length"])*20)/len(tvals['usernames'])
                    for username in tvals["usernames"]:
                        users.append(User(username, limit))
                else:
                    for username in tvals["usernames"]:
                        users.append(User(username))
                if tvals["genre"] is not None:
                    p = Playlist(users, tvals["genre"])
                else:
                    p = Playlist(users)
                tvals["playlist_title"] = p.title
                tvals["combined_playlist"] = p.strList()

                template = JINJA_ENVIRONMENT.get_template('matchresults.html')
                self.response.write(template.render(tvals))
        elif self.request.POST.get('backbttn'):
            template = JINJA_ENVIRONMENT.get_template('mixmatchhome.html')
            self.response.write(template.render(tvals))



application = webapp2.WSGIApplication([ \
    ('/matchresults', MixMatchResponseHandler),
    ('/.*', MainHandler)
], debug=True)
