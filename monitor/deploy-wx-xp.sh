# python 2.7.18 
pip install -U pip --user
pip install wxPython==4.1.0  -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install -U nuitka -i https://pypi.tuna.tsinghua.edu.cn/simple


# Build to exe 

python -m nuitka --onefile --disable-console --windows-icon-from-ico=your-icon.png program.py

