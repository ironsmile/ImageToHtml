## Introduction

Small GUI tool to convert your pictures into a colourful HTML

## Requires

* Python >= 2.7 or Python >= 3.4
* [Pillow](https://python-pillow.org/) >= 4.x
* [wxPython](https://wxpython.org/) >= 4.x

## Installation

To run this program from source you would need [pip](https://pip.pypa.io/). Just run:

```
pip install -r requirements.txt
```

## Usage

Run the executable script `./pic_to_html`. This would start the GUI.

Alternatively you can use the converter in the command line directly:

```bash
python src/classes/img_to_html.py input.jpg output.html \
    --chars-width 150 \
    --font-size 10
```

See `--help` for more options.

## Thanks to

Elena for calculating the MAGICK constant.
