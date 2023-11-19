@echo off
python.exe -m pip install nuitka
mkdir output
cd src
REM python.exe -m nuitka --onefile --follow-imports --output-dir=..\output --show-progress --include-module=pdat --include-module=binaryhelper --include-module=pvdb --remove-output main.py
python.exe -m nuitka --standalone --follow-imports --output-dir=..\output --show-progress --include-module=build_as --include-module=build_seg --remove-output build.py
python.exe -m nuitka --standalone --follow-imports --output-dir=..\output --show-progress --remove-output build_as.py
python.exe -m nuitka --standalone --follow-imports --output-dir=..\output --show-progress --remove-output build_seg.py
python.exe -m nuitka --standalone --follow-imports --output-dir=..\output --show-progress --remove-output build_vlab.py

python.exe -m nuitka --standalone --follow-imports --output-dir=..\output --show-progress --enable-plugin=tk-inter --include-module=build_as --include-module=build_seg --include-module=build_vlab --remove-output gui.py
cd ..\output
