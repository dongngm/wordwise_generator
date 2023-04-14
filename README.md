# wordwise_generator
## Basic Usage
- Windows executables are uploaded at https://drive.google.com/drive/folders/13Y6qbp7dxoqnaT1nqzS2gAAsfwEePrbq?usp=sharing
## Advanced Usage
### Prerequisites
```
# Install Calibre: https://calibre-ebook.com/download
# python=3.8.16
conda install pillow=9.0.1
conda install -c conda-forge gooey=1.0.8.1
```
### Run App
`python main.py`

### Packaging
`pip install pyinstaller==5.10.0`

`pyinstaller --onefile --noconsole main.py` --> `./dist/main.exe` will be generated
### Note
- Put `main.exe` in the same folder with `data`
```
├── data
│   ├── custom.csv
│   ├── en.csv
│   ├── filter.txt
│   └── vi.csv
├── main.exe
```
- Works on `Windows 11 build 22621.1413` `Windows 10 build 19045.2728`
## Credit
`https://github.com/xnohat/wordwisecreator`

`https://www.facebook.com/doduc.dnad`
