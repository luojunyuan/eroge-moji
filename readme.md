#### Run and Build  

Please install Python 3.6 x86 or Python 3.7 x86_amd64 for PySide first.

About run

```cmd
git clone eroge-moji.git
cd eroge-moji
pip install virtualenv
virtualenv venv -p C:\Users\yourname\AppData\Local\Programs\Python\Python36-32\python.exe
venv\Scripts\activate
pip install https://www.lfd.uci.edu/~gohlke/pythonlibs/PySide‑1.2.4‑cp36‑cp36m‑win32.whl
venv\Lib\site-package\PySide\pyside-rcc.exe resource.qrc -o resource.py -py3
python main.py
```

##### Attetion

make sure to generate resource.py before run code everytime

pyside-rcc is located in python\Lib\site-packages\PySide

install Pyinstaller to build executebal program

`pip install pyinstaller`

`pyinstaller main.py -y --windowed --additional-hooks-dir pyi_hooks/`

Then move /libs to dist/main/libs

if you use python3.7 64bit

`pip install https://www.lfd.uci.edu/~gohlke/pythonlibs/PySide‑1.2.4‑cp37‑cp37m‑win_amd64.whl`
