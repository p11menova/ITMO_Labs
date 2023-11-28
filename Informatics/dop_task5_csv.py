from main import ParserJson

class ToCsv:
    @staticmethod
    def load(data):
        data = data['schedule']
        res = ''
        dict_keys = ['Lang', 'Group', 'Day', 'Lesson number'] + sorted(list(map(lambda x: str(x).capitalize(), data['lessons']['lesson_1'].keys())))
        res += ','.join(dict_keys)+'\n'

        lang, group, day = data['lang'], data['group'], data['day']
        for k, v in data['lessons'].items():
            print(k, v)
            values = [lang, group, day, k] + [i[1] for i in sorted(v.items(), key=lambda x: x[0])]
            print(values)
            res += ','.join(list(map(lambda x: str(ToCsv.parse(x)), values))) + '\n'
        return res
    @staticmethod
    def parse(s):
        if isinstance(s,str):
            return f'"{s}"'
        return str(s).replace(', ', ';')


with open('src/schedule.json', encoding='utf-8') as f:
    data = ParserJson.parse_json(f.read())
    res = ToCsv.load(data)
    with open('src/out.csv', mode='w', encoding='utf-8') as f:
        print(res, file=f)
