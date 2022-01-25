REM Delete this line and all 'REM' words below this line

@ECHO ON
START Python/mirror_modBus_master_multiprocessing.py
SLEEP 2
START Mirrors.exe
TIMEOUT /T 10 
REM mirrorFix.exe


