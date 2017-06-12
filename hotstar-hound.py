import sys
import requests as r
import json
import livestreamer
import webbrowser as wb
import os

### GLOBAL VARIABLES ###
streams = None
quality = 'best'
stream_url_hls = None
#######################

def getLink():
    link = raw_input('Enter URL : ')
    return link

def fetchStreamURL(video_id):
    cdn_url = "http://getcdn.hotstar.com/AVS/besc?action=GetCDN&asJson=Y&channel=TABLET&id=" + video_id + "&type=VOD"
    response = r.get(cdn_url)

    if str(response) == '<Response [200]>':
        json_response = json.loads(response.text.encode('utf-8'))
        stream_url = json_response['resultObj']['src'].encode('utf-8')
    else:
        print('HTTP Error. Unable to connect to Hotstar. Exiting.\n')
        sys.exit(0)

    return stream_url

def parseStreamURL(stream_url):
    global streams, quality, stream_url_hls
    stream_url_hls = 'hlsvariant://' + stream_url
    streams = livestreamer.streams(stream_url_hls)
    #print '\n' + stream_url_hls

    print('\nAvailable streams : %s' % str(streams.keys()))
    quality = raw_input('Enter stream quality <leave empty for default> : ')
    
    if quality == '':
        quality = 'best'
        stream_url = streams[quality].url
        print('Using the "best" possible quality...\n')
    elif quality in streams.keys():
        stream_url = streams[quality].url
    else:
        print('Incorrect option. Switching to default...\n')
        quality = 'best'
        stream_url = streams[quality].url
    print stream_url
    return stream_url

def openStream(stream_url):
    global quality, stream_url_hls, streams
    print(
        '''
        ----------------- Menu -----------------
         1. Open stream in default Browser 
         2. Open stream in default Media Player
         3. Exit
           ''')
    choice = raw_input('Enter choice : ')

    try:
        choice = int(choice)
    except ValueError:
        print('Please enter an integer. Exiting.\n')
        sys.exit(0)

    if choice == 1:
        try:
            browser = wb.get('safari')
        except wb.Error:
            try:
                browser = wb.get('chrome')
            except wb.Error:
                try:
                    browser = wb.get('google-chrome')
                except wb.Error:
                    browser = wb.get()
        browser.open_new_tab(stream_url)    
    elif choice == 2:
        #os.system("livestreamer '" + stream_url_hls + "' '" + quality + "'")
        os.system("vlc " + stream_url)
    elif choice == 3:
        print('Exiting.\n')
        sys.exit(0)
    else:
        print('Incorrect choice. Exiting.\n')
        sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        link = sys.argv[1]
        v_id = link.split("/")[-1]
        try:
            v_id_int = int(v_id)    
        except ValueError:
            print('Unable to extract video ID. Exiting.\n')
            sys.exit(0)
    elif len(sys.argv) == 1:
        link = getLink()
        v_id = link.split("/")[-1]
        try:
            v_id_int = int(v_id)    
        except ValueError:
            print('Unable to extract video ID. Exiting.\n')
            sys.exit(0)
    else:
        print("Incorrect number of arguments. Exiting.\n")
        sys.exit(0)

    stream_url = parseStreamURL(fetchStreamURL(v_id))
    openStream(stream_url)
    
