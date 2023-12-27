# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# XBMC entry point
# ------------------------------------------------------------

import os
import sys
import xbmc

# functions that on kodi 19 moved to xbmcvfs
try:
    import xbmcvfs
    xbmc.translatePath = xbmcvfs.translatePath
    xbmc.validatePath = xbmcvfs.validatePath
    xbmc.makeLegalFilename = xbmcvfs.makeLegalFilename
except:
    pass
from platformcode import config, logger,platformtools

logger.info("init...")

librerias = xbmc.translatePath(os.path.join(config.get_runtime_path(), 'lib'))
sys.path.insert(0, librerias)
os.environ['TMPDIR'] = config.get_temp_file('')

from platformcode import launcher

if sys.argv[2] == "":
    launcher.start()

with open(config.updateFile, 'r') as fileC: # new function to control version
                Update = fileC.readline()
                logger.info("Versione:", Update)



import default1 #build 

#if Update ==('5.0.1'): #('/5\.0\.0/'):
#    update_ok=platformtools.dialog_yesno("Lo Scienziato Pazzo","E' disponibile una nuova versione della build\nVuoi scaricarla?\nClicca su Build universale per installare gli aggiornamenti e attendi che il download sia completato\nKodi verrà riavviato e una volta aperto sarà aggiornato.")
#    if update_ok:
#        xbmc.executebuiltin("UpdateLocalAddons")
#        xbmc.executebuiltin("StopScript(plugin.video.lo-scienziato-pazzo)")
#        xbmc.executebuiltin("RunAddon(plugin.video.lo-scienziato-pazzo)")
#        xbmc.executebuiltin("RunScript(special://home/addons/plugin.video.lo-scienziato-pazzo/default.py)")
#    else :
#        platformtools.dialog_ok("Lo Scienziato Pazzo","La Build è aggiornata")
               
         
