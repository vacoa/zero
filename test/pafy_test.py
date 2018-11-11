import pafy


import youtube_dl

id = '5m2HN2y0yV8'

#mystream = pafy.new(id).getbest()


ydl_opts = {}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=5m2HN2y0yV8'])
