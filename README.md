# wordwise_generator
## Prequisites
```
conda install gooey -c conda-forge
pip install pyinstaller
```
## Run App
`python main.py`

## Packaging
`pyinstaller --onefile --noconsole main.py` --> `./dist/main.exe` will be generated
## Usage
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
