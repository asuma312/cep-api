import json
from dotenv import load_dotenv
import os
load_dotenv()

class nosqldb:
    def __init__(self,userhash):
        self.dbpath = os.getenv('DB_PATH')
        self.userhash = userhash

    def create_user_path(self):
        userpath = os.path.join(self.dbpath, str(self.userhash))
        if not os.path.exists(userpath):
            os.makedirs(userpath)

    def create_specific_path(self,foldername):
        userpath = os.path.join(self.dbpath, str(self.userhash))
        specificpath = os.path.join(userpath, foldername)
        if not os.path.exists(specificpath):
            os.makedirs(specificpath)

    def get_all_dbs(self,specificpath=None):
        jsonpath = os.path.join(self.dbpath, str(self.userhash))
        if specificpath:
            jsonpath = os.path.join(jsonpath, specificpath)
        if not os.path.exists(jsonpath):
            return []
        return os.listdir(jsonpath)


    def get_json(self, jsonname, specificpath=None):
        userpath = os.path.join(self.dbpath, str(self.userhash))
        jsonfile_path = os.path.join(userpath, f'{jsonname}.json')
        if specificpath:
            jsonfile_path = os.path.join(userpath, specificpath, f'{jsonname}.json')
        print(jsonfile_path)
        if not os.path.exists(jsonfile_path):
            raise FileNotFoundError(f'O arquivo {jsonname}.json não existe para o usuário {self.userhash}.')
        with open(jsonfile_path, 'r') as jsonfile:
            return json.load(jsonfile)

    def write_json(self, jsonname, data, specificpath=None):
        userpath = os.path.join(self.dbpath, str(self.userhash))
        self.create_user_path()
        jsonfile_path = os.path.join(userpath, f'{jsonname}.json')
        if specificpath:
            jsonfile_path = os.path.join(userpath, specificpath, f'{jsonname}.json')
        with open(jsonfile_path, 'w') as jsonfile:
            json.dump(data, jsonfile)

    def update_json(self, jsonname, key, value):
        data = self.get_json(jsonname, self.userhash)
        data[key] = value
        self.write_json(jsonname, data, self.userhash)

    def delete_db(self,jsonname,specificpath=None):
        userpath = os.path.join(self.dbpath, self.userhash)
        jsonfile_path = os.path.join(userpath, f'{jsonname}.json')
        if specificpath:
            jsonfile_path = os.path.join(userpath, specificpath, f'{jsonname}.json')
        if os.path.exists(jsonfile_path):
            os.remove(jsonfile_path)
        else:
            raise FileNotFoundError(f'O arquivo {jsonname}.json não existe para o usuário {self.userhash}.')


    def create_json(self, jsonname, data,specificpath=None):
        userpath = os.path.join(self.dbpath, self.userhash)
        self.create_user_path()
        jsonfile_path = os.path.join(userpath, f'{jsonname}.json')
        if specificpath:
            jsonfile_path = os.path.join(userpath, specificpath, f'{jsonname}.json')
        with open(jsonfile_path, 'w') as jsonfile:
            json.dump(data, jsonfile)

    def verify_create_json(self, jsonname, data,specificpath=None):
        userpath = os.path.join(self.dbpath, self.userhash)
        self.create_user_path()
        jsonfile_path = os.path.join(userpath, f'{jsonname}.json')
        if specificpath:
            jsonfile_path = os.path.join(userpath, specificpath, f'{jsonname}.json')
        if not os.path.exists(jsonfile_path):
            with open(jsonfile_path, 'w') as jsonfile:
                json.dump(data, jsonfile)
                return True
        return False

class cache_controller(nosqldb):
    def __init__(self):
        super().__init__('cache')


