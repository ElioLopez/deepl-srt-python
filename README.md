# deepl-srt-python
This project was based on https://github.com/michimani/deepl-api-sample
but instead of translate phrases from command line, its translate entire .srt files.
It requires an API key that you get when you suscribe to deepl developer
(roughly $4.99/month and $1/50k translalted characters)

## Motivation
When you try to translate a .srt file in deepl web (copy and paste), the translation
is not accurate because of the line breaks.
for example:
```bash
157
00:12:48,520 --> 00:12:52,160
Er will Heinrich IV. in
seinem Sinne erziehen.
```

is translated as:
```bash
157
00:12:48,520 --> 00:12:52,160
He wants Henry IV in
educate his senses.
```
when the translation should be really:
```bash
157
00:12:48,520 --> 00:12:52,160
He wants to educate Henry IV
in his spirit.
```

This python script takes the two lines phrases in the file, joint them and send it
to deepl API, then split the answer back to an output file (is not sendig the line
numbers and start-end times, so you won't be charged for that).
Single line files are translated as is.

## Usage

### Preparing
Create a `config.json` by copying `config.json.sample`.

```bash
$ cp config.json.sample config.json
```

```json
{
  "auth_token": "your-deelpl-api-auth-token"
}
```
### python setup

#### create virtual env
```bash
python3 -m venv env
```
#### activate virtual env
```bash
source env/bin/activate
```
#### install required packages
```bash
pip install requests
```
#### deactivate virtual env
```bash
source env/bin/deactivate
```

## Features

- translate
- monitoring usage

```bash
python main.py -h
usage: main.py [-h] [-t TARGET] [-s SOURCE] [-f SRT_FILE] [-o OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        target language code (Default: ES). allowed lang code
                        : ['DE', 'EN', 'FR', 'IT', 'JA', 'ES', 'NL', 'PL',
                        'PT-PT', 'PT-BR', 'PT', 'RU', 'ZH']
  -s SOURCE, --source SOURCE
                        source language code (Default: auto). allowed lang
                        code : ['DE', 'EN', 'FR', 'IT', 'JA', 'ES', 'NL',
                        'PL', 'PT', 'RU', 'ZH']
  -f SRT_FILE, --srt_file SRT_FILE
                        .srt subtitles file to translate. Required
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        output .srt file. Default: translation_output.srt
```

### translation example

```bash
python main.py -f Die.Deutschen.S01E02.srt -o Die.Deutschen.S01E02.SPA.srt -s DE
```

### monitoring usage
```bash
python3 usage.py
{
  "character_count": 157644,
  "character_limit": 10000000
}
```

