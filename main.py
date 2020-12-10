import argparse
import string
import json
import os
import sys
import urllib.parse
import urllib.request
import subprocess

with open(os.path.dirname(os.path.abspath(__file__)) + '/config.json') as j:
    config = json.load(j)

AUTH_KEY = config['auth_key']
DEEPL_TRANSLATE_EP = 'https://api.deepl.com/v2/translate'
T_LANG_CODES = ["DE", "EN", "FR", "IT", "JA", "ES",
                "NL", "PL", "PT-PT", "PT-BR", "PT", "RU", "ZH"]
S_LANG_CODES = ["DE", "EN", "FR", "IT",
                "JA", "ES", "NL", "PL", "PT", "RU", "ZH"]

p = argparse.ArgumentParser()
p.add_argument('-t', '--target',
               help=f'target language code (Default: ES). allowed lang code : {str(T_LANG_CODES)}',
               default='ES')
p.add_argument('-s', '--source',
               help=f'source language code (Default: auto). allowed lang code : {str(S_LANG_CODES)}',
               default='')
p.add_argument('-f', '--srt_file',
               help='.srt subtitles file to translate. Required',
               default='')
p.add_argument('-o', '--output_file',
               help=f'output .srt file. Default: translation_output.srt',
               default='translation_output.srt')
args = p.parse_args()


def translate(text, s_lang='', t_lang='ES'):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; utf-8'
    }

    params = {
        'auth_key': AUTH_KEY,
        'text': text,
        'target_lang': t_lang
    }

    if s_lang != '':
        params['source_lang'] = s_lang

    req = urllib.request.Request(
        DEEPL_TRANSLATE_EP,
        method='POST',
        data=urllib.parse.urlencode(params).encode('utf-8'),
        headers=headers
    )

    try:
        with urllib.request.urlopen(req) as res:
            res_json = json.loads(res.read().decode('utf-8'))
            #print(json.dumps(res_json, indent=2, ensure_ascii=False))
    except urllib.error.HTTPError as e:
        print(e)

    return(res_json)

if __name__ == '__main__':
  srt_file = args.srt_file
  t_lang = args.target
  s_lang = args.source
  out_file = args.output_file

  if t_lang not in T_LANG_CODES:
      print((
          f'ERROR: Invalid target language code "{t_lang}". \n'
          f'Allowed lang code are following. \n{str(T_LANG_CODES)}'
      ))
      sys.exit(1)
  if s_lang != '' and s_lang not in S_LANG_CODES:
      print((
          f'WARNING: Invalid source Language code "{s_lang}". \n'
          'The source language is automatically determined in this request. \n'
          f'Allowed source lang code are following. \n{str(S_LANG_CODES)} \n\n'
      ))
      s_lang = ''


  f = open(srt_file, "r")
  Lines = f.readlines() 

  #output file
  file1 = open(out_file, 'w') 
  #list used to join the lines and translate
  L = [] 
 
  text_lines_count = 0
  for line in Lines: 
    #lines thata start with digit should not be sent to the API, and directly written to output file
    if line[0].isdigit():
      file1.write(line)
      print(line, end='') 
    elif (line=="\n"):
      if (text_lines_count==1): #<------ single line sentences
        response = translate(" ".join(L), t_lang=t_lang, s_lang=s_lang)
        print(response['translations'][0]['text'])
        file1.write("".join(response['translations'][0]['text']) + "\n")
        L.pop()
      text_lines_count = 0
    else:
      text_lines_count = text_lines_count + 1 
      if (text_lines_count==2):  #<------ double line sentences
        L.append(line)
        L[0] = L[0].strip()
        response = translate(" ".join(L), t_lang=t_lang, s_lang=s_lang)
        oracion = response['translations'][0]['text']
        lista_oracion = oracion.split()

        palabra_modificada = lista_oracion[len(lista_oracion)//2]
        palabra_modificada = palabra_modificada + "\n"
        lista_oracion[len(lista_oracion)//2] = palabra_modificada
        print(" ".join(lista_oracion),"\n")
        file1.writelines(" ".join(lista_oracion) + "\n\n")
        L.pop()
        L.pop()
        text_lines_count = 0
      else:
        L.append(line)

 # Closing file 
  file1.close() 

#removes that extra space in the second line
subprocess.call(["sed", "-i", 's/^[ \t]*//', out_file])

 