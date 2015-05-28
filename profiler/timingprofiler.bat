

echo "running ODMTools timing profiler"
python -m cProfile -o profile.dat D:\\DEV\\ODMTools\\ODMToolsPython\\ODMTools.py

echo "view timing profiler result"
python D:\\DEV\\ODMTools\\ODMToolsPython\profiler\runsnake.py profile.dat

