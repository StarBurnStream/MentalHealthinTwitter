import json, sys
import unicodedata as ud
import codecs


    
class JsonLoad:
    def __init__(self, jsonfile = None):
        self.jsonfile = jsonfile
        
    def readJson(self,jsonfile):
        json_diclist = []
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        with open(jsonfile) as f:
           for parsed_json in load_json_multiple(f):
               for i in range(len(list(parsed_json.values()))):
                   if isinstance(list(parsed_json.values())[i],str):
                       temp= list(parsed_json.values())[i].translate(non_bmp_map)
                       key = list(parsed_json.keys())[i]
                       parsed_json[key] = temp
               json_diclist += [parsed_json]
        return json_diclist
        
def load_json_multiple(segments):
    chunk = ""
    for segment in segments:
        chunk += segment
        try:
            yield json.loads(chunk)
            chunk = ""
        except ValueError:
            pass

def main():
    j = JsonLoad("stream_sad_USA_3.json")
    json_diclist = j.readJson(j.jsonfile)
    for i in range(len(json_diclist)):
        try:
            print(json_diclist[i])
        except Exception as e:
            print("Error: %s" % str(e))

main()

