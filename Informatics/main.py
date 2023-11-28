import re


class ParserJson:

    @staticmethod
    def is_int(s: str) -> bool:
        return s.isdigit()

    @staticmethod
    def parse_int(s: str) -> int:
        return int(s)

    @staticmethod
    def is_float(s: str) -> bool:
        return bool(re.match(r'[\d+][.,][\d+]', s))

    @staticmethod
    def parse_float(s: str) -> float:
        return float(s)

    @staticmethod
    def is_bool(s: str) -> bool:
        return s in {'True', 'true'}

    @staticmethod
    def parse_bool(s: str) -> bool:
        return True if s in {'true', 'True'} else False

    @staticmethod
    def is_null(s: str) -> bool:
        return s == 'null'

    @staticmethod
    def parse_null(s: str) -> None:
        return None

    @staticmethod
    def parse(s: str):

        is_parse_d = {
            ParserJson.is_int: ParserJson.parse_int,
            ParserJson.is_float: ParserJson.parse_float,
            ParserJson.is_bool: ParserJson.parse_bool,
            ParserJson.is_null: ParserJson.parse_null
        }
        for f1, f2 in is_parse_d.items():
            if f1(s):
                return f2(s)
        return ''

    @staticmethod
    def get_data(s, i):

        while i < len(s):
            cur = s[i]
            if cur== '[':
                text = '['
                brackets = 1
                i += 1
                while brackets != 0:
                    if s[i] == '[':
                        brackets += 1
                    elif s[i] == ']':
                        brackets -= 1
                    text += s[i]
                    i += 1
                return ParserJson.parse_array(text), i
            elif cur == '{':
                text = '{'
                brackets = 1
                i += 1
                while brackets != 0:
                    if s[i] == '{':
                        brackets += 1
                    elif s[i] == '}':
                        brackets -= 1
                    text += s[i]
                    i += 1
                return ParserJson.parse_json(text), i
            elif cur.isalnum():
                text = ''
                while i < len(s) and (s[i].isalnum() or s[i] == '.'):
                    text += s[i]
                    i += 1
                return ParserJson.parse(text), i
            else:
                i += 1

    @staticmethod
    def parse_array(s):
        s = s.strip()[1:-1]
        res = []
        i = 0
        while i < len(s):
            cur = s[i]
            if cur.isalnum() or cur in {'[', '{'}:
                data, i = ParserJson.get_data(s, i)
                res.append(data)
            elif cur == '"':
                text = ''
                i += 1
                while s[i] != '"':
                    text += s[i]
                    i += 1
                res.append(text)
            else:
                i += 1
        return res

    @staticmethod
    def parse_json(s):
        s = s.strip()[1:-1]
        res = dict()
        key = ''
        i = 0

        while i < len(s):
            cur = s[i]
            if cur == '"':
                text = ''
                i += 1
                while s[i] != '"':
                    text += s[i]
                    i += 1
                i += 1
                if key == '':
                    key = text
                else:
                    res[key] = text
                    key = ''

            elif cur.isalnum() or cur in {'[', '{'}:
                v, i = ParserJson.get_data(s, i)
                res[key] = v
                key = ''
            else:
                i += 1
        return res


class ToXML:
    @staticmethod
    def load(data, name='', enclosure=0):
        # enclosure - уровень вложенности
        xml_text = ''
        for k, v in data.items():
            if isinstance(v, dict):
                xml_text += ToXML.load(v, name=k, enclosure=enclosure + 1)
            elif isinstance(v, list):
                xml_text += '\t' * enclosure + '<' + k.replace(' ', '_') + '>\n'
                for i in v:
                    xml_text += ToXML.load({'elem_' + k: i}, enclosure=enclosure + 1)
                xml_text += '\t' * enclosure + "</" + k.replace(' ', '_') + ">\n"
            else:
                if ParserJson.is_float(k):
                    k = 'num_' + k
                xml_text += '\t' * enclosure + '<' + k.replace(' ', '_') + '>'
                xml_text += str(v)
                xml_text += '</' + k.replace(' ', '_') + '>\n'

        if name:
            name = name.replace(' ', '_')
            return '\t' * (enclosure - 1) + f'<{name}>' + '\n' + xml_text + '\t' * (enclosure - 1) + f'</{name}>' + '\n'
        return xml_text

def main():
    with open('src/schedule.json', encoding='utf-8') as f:
        data = ParserJson.parse_json(f.read())
        with open('src/schedule.xml', mode='w', encoding='utf-8') as f_out:
            data = ToXML.load(data)
            print(data, file=f_out)

if __name__ == '__main__':
    main()