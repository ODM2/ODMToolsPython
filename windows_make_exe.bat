pyinstaller --clean ^
	--distpath="setup\Windows" ^
	--workpath="setup\Windows\work" ^
	--hidden-import=pyodbc ^
	--upx-dir="setup\Windows" ^
	--noconfirm ^
	ODMTools.py

pause