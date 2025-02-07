import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs, os,sys
import shutil
import urllib
import re, requests
import extract
import time
import downloader
import plugintools
import zipfile
import ntpath

from updates import init as update
from platformcode import config

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
base='https://github.com/aandroide/myaddon'
ADDON=xbmcaddon.Addon(id='plugin.video.lo-scienziato-pazzo')
dialog = xbmcgui.Dialog()    
VERSION = "5.0.0"
PATH = "" 

def CATEGORIES():
    #link = OPEN_URL('https://loscienziatopazzo.altervista.org/ght/ght.xml').replace('\n','').replace('\r','')
    link = OPEN_URL('https://loscienziatopazzo.altervista.org/ght/ght.xml').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description in match:
        addDir(name,url,1,iconimage,fanart,description)
    
    commit_sha,commit_message=update.getSavedCommit()
    update_des=str(config.get_addon_version(False))+'('+commit_sha[:7]+')\n\ncommit: '+commit_message
    addDir("Check for update","",2,"" ,"",update_des)
    
    setView('movies', 'MAIN')
        
    
def OPEN_URL(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'}
    response = requests.get(url, headers = headers)
    link=response.text
    return link
    
def wizard(name,url,description):
    path = xbmcvfs.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("LO SCIENZIATO PAZZO","In Download \n\n Attendere Prego")
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmcvfs.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(int(0),"\n Sto estraendo i file, attendi un attimo")
    print('=======================================')
    print(addonfolder)
    print('=======================================')
    extract.all(lib,addonfolder)#,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("DOWNLOAD COMPLETATO", 'Per vedere le modifiche della nuova Build occorre riavviare Kodi \n Clicca su Ok per riavviare,')
    os._exit(1)
    killxbmc()
        
      
        
def killxbmc():
    choice = xbmcgui.Dialog().yesno('Force Close Kodi', 'Chiusura Forzata di Kodi \n Vuoi continuare?', nolabel='No, Cancel',yeslabel='Yes, Close')
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print("Platform: " + str(myplatform))
    if myplatform == 'osx': # OSX
        print("############   try osx force close  #################")
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Installazione completata con SUCCESSO. Si prega di riavviare XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print( "############   try linux force close  #################")
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Installazione FALLITA. Si prega di riavviare XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print( "############   try android force close  #################")
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Sei su un sistema Android. Per visualizzare le modifiche chiudi Kodi dall'apposito tasto.", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Either close using Task Manager (If unsure pull the plug).")
    elif myplatform == 'windows': # Windows
        print( "############   try windows force close  #################")
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Installazione FALLITA. Si prega di riavviare XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print( "############   try atv force close  #################")
        try: os.system('killall AppleTV')
        except: pass
        print("############   try raspbmc force close  #################") #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Installazione FALLITA. Si prega di riavviare XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    

def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'


def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.parse.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.parse.quote_plus(name)+"&iconimage="+urllib.parse.quote_plus(iconimage)+"&fanart="+urllib.parse.quote_plus(fanart)+"&description="+urllib.parse.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name)
        liz.setArt({'icon':"DefaultFolder.png",'thumb':iconimage})
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
       
        
def get_params():
        param=[]
        if len(sys.argv)<=2:
            return param
        
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


try:
        url=urllib.parse.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.parse.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.parse.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.parse.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.parse.unquote_plus(params["description"])
except:
        pass
        
        
print(str(PATH)+': '+str(VERSION))
print("Mode: "+str(mode))
print("URL: "+str(url))
print("Name: "+str(name))
print("IconImage: "+str(iconimage))


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )
        
if mode==2:
    update.run()        
elif mode==None or url==None or len(url)<1:
        CATEGORIES()       
elif mode==1:
        wizard(name,url,description)
        

        
xbmcplugin.endOfDirectory(int(sys.argv[1]))

