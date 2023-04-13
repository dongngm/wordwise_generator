# wordwise_generator
## Prequisites
```
# Install Calibre: https://calibre-ebook.com/download
# python=3.8.16
conda install pillow=9.0.1
conda install -c conda-forge gooey=1.0.8.1
```
## Run App
`python main.py`
## Packaging
`pip install pyinstaller==5.10.0`

`pyinstaller --onefile --noconsole main.py` --> `./dist/main.exe` will be generated
### Usage
- Put `main.exe` in the same folder with `data`
```
├── data
│   ├── custom.csv
│   ├── en.csv
│   ├── filter.txt
│   └── vi.csv
├── main.exe
```
## Credit
`https://github.com/xnohat/wordwisecreator`

`https://www.facebook.com/doduc.dnad`
