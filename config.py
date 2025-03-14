import json
import os


class Config(dict):

    def __init__(self):
        super().__init__()
        if not os.path.exists('config.json'):
            with open('config.json', 'w') as f:
                config = {
                    'whisper': 'base',
                    'siliconflow_key': 'sk-*',
                    'moonshot_key': 'sk-*',
                    'audio': {
                        'uri': 'speech:*',
                        'siliconflow_key': 'auto',
                    }
                }
                f.write(json.dumps(config, indent=4))

        with open('config.json', 'r') as f:
            config = json.loads(f.read())

        if config.get('siliconflow_key') == 'sk-*':
            siliconflow_key = input('请输入你的硅基流动api key: ')
            config['siliconflow_key'] = siliconflow_key
        if config.get('moonshot_key') == 'sk-*':
            moonshot_key = input('请输入你的moonshot api key: ')
            config['moonshot_key'] = moonshot_key



config = Config()
