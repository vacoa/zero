import os
import json
import urllib.request


class Gyoutube():
    def __init__(self,secretFile):
        with open(secretFile) as f:
            data = json.load(f)
        self.__key = data['key']
        self.service = 'https://www.googleapis.com/youtube'
        self.version = 'v3'

    def searchPlaylist(self,query):
        params = {'part':'snippet',
          'maxResults':'1',
          'type':'playlist',
          'regionCode':'US',
          'q':query}
        return self.request('search',params)
        
    def searchPlaylistItems(self,query):
        resp = self.searchPlaylist(query)
        listId = resp['items'][0]['id']['playlistId']
        params = {'part':'snippet',
          'maxResults':'5',
          'playlistId':listId}
        return self.request('playlistItems',params)
        
        
    def searchPlaylistItemsInfo(self,query):
        resp = self.searchPlaylistItems(query)
        list = []
        for it in resp['items']:
            list.append({'id': it['snippet']['resourceId']['videoId'],
                         'title': it['snippet']['title'],
                         'description': it['snippet']['description']})
        return list
        
    def searchAudio(self,query):
        params = {'part':'snippet',
          'maxResults':'20',
          'type':'video',
          'videoCategoryId':'10',
          'regionCode':'US',
          'q':query}
        return self.request('search',params)
    
    def searchAudioInfo(self,query):
        resp = self.searchAudio(query)
        list = []
        for it in resp['items']:
            list.append({'id': it['id']['videoId'],
                         'title': it['snippet']['title'],
                         'description': it['snippet']['description']})
        return list
        
    def request(self,action,params):
        url = self.service + '/' + self.version + '/' + action
        params['key'] = self.__key
        urlval = urllib.parse.urlencode(params)
        r = urllib.request.urlopen(url + '?' + urlval).read()
        return json.loads(r.decode('ISO-8859-1'))
        

