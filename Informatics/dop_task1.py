import json
import dict2xml

def task1():
    with open('src/schedule.json', encoding='utf-8') as f_in:
        py_dict = json.loads(f_in.read())
        with open('src/schedule_xml_dict.xml', mode='w', encoding='utf-8') as f_out:
            print(dict2xml.dict2xml(py_dict, indent="\t"), file=f_out)


if __name__ == '__main__':
    task1()