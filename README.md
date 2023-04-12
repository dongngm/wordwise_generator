# wordwise_generator
## Prequisites
```
conda install gooey -c conda-forge
pip install pyinstaller
```
## Packaging
`pyinstaller --onefile --noconsole main.py` --> `./dist/main.exe` will be generated
## Usage
- Put `main.exe` in the same folder with `data`
```
├── data
│   ├── custom.csv
│   ├── en.csv
│   ├── filter.txt
│   ├── main.php
│   └── vi.csv
├── main.exe
```
## Credit
`https://www.facebook.com/doduc.dnad`