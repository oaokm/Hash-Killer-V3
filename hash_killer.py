from fake_useragent import UserAgent
from pydantic import BaseModel
from config import config
from logger import logger
from tqdm import tqdm
import re, os, base64
from url import URL
import requests
import hashlib

class downloadFiles:
    def __init__(self, url:str, destination:str):
        self.url         = url
        self.destination = destination
        self.session     = requests.Session()
        self.logger      = logger()
        # Create a UserAgent object
        ua = UserAgent()
        
        # Set a random User-Agent header
        self.session.headers.update({'User-Agent': ua.random})

    
    def startDownload(self):
        try:
            response = self.session.get(self.url, stream=True, proxies=config.proxy)
            
            #? Raise an error if the request was unsuccessful
            response.raise_for_status()

            #* discavrd the total size file
            total_size = int(response.headers.get('content-length', 0))
            
            #* Download Part
            with open(self.destination, 'wb') as file:
                with tqdm(total=total_size, unit='B', unit_scale=True, 
                          desc=f"download file, and put it on : `{self.destination}`", 
                          disable=not config.enableTqdm) as bar:
                    for data in response.iter_content(chunk_size=(1024*2)):
                        file.write(data)
                        bar.update(len(data))
            
            self.logger.write(loggerBody(level='success', message=f"Download a file successfully on `{self.destination}`").model_dump_json())


        #! Error for fail internet connection
        except requests.exceptions.ConnectionError as err:
            self.logger.write(loggerBody(level='error', message=f"Sorry, there is no any connection with internet, please check your network. message: {err}").model_dump_json())
        
        #! Error for fail to access the file (an another word: HTTP status code is not 200)
        except requests.exceptions.HTTPError as err:
            self.logger.write(loggerBody(level='error', message=f"Sorry, you have error causing the connection to fail. message: {err}").model_dump_json())


class loggerBody(BaseModel):
    level:str
    message:str


class hash_killer(config):
    def __init__(self):
        #* Step Zero: Set a values & simple func & 
        self.hashs   = {
            "md5": (hashlib.md5, r"^[a-f0-9]{32}$"),
            "sha1": (hashlib.sha1, r"^[a-f0-9]{40}$"),
            "sha256": (hashlib.sha256, r"^[a-f0-9]{64}$"),
            "sha224": (hashlib.sha224, r"^[a-f0-9]{56}$"),
            "sha384": (hashlib.sha384, r"^[a-f0-9]{96}$"),
            "sha512": (hashlib.sha512, r"^[a-f0-9]{128}$")
        }
        self.generate_salt   = lambda length: base64.b64encode(os.urandom(length)).decode("utf-8")
        self.combined_string = lambda generate_salt, text: generate_salt + text
        self.logger = logger()
        self.binaryList = []


    def foundMatch(self, hash:str, pathfileOrURL:str):
        urlchecker = URL(pathfileOrURL)
        #* Step Zero: check if the session have permission to use internet and if `pathfileOrURL` is 
        if urlchecker._is_url:
            # Step One:  befor connect with page by url, check if file exsits befor, then download if the session have permission
            filename = urlchecker.components().get('pathWithoutPramter').split('/')[-1]
            filePath = os.path.join(config.folderSaveingFilesPath, filename)
            
            self.logger.write(loggerBody(level='debug', message=f"filename is: `{filename}`, and filePath is : `{filePath}`").model_dump_json())
            
            os.makedirs(config.folderSaveingFilesPath, exist_ok=True)
            
            if not os.path.exists(path=filePath):
                self.logger.write(loggerBody(level='debug', message=f"result of url.components: {urlchecker.components()}").model_dump_json())
                self.logger.write(loggerBody(level='info', message=f"Start conntcting with: {pathfileOrURL}").model_dump_json())
                downloadFiles(
                    url=pathfileOrURL,
                    destination=filePath
                ).startDownload()
                wordListPath     = filePath
            else:
                self.logger.write(loggerBody(level='info', message=f"file in `{filePath}` is exist").model_dump_json())
                wordListPath  = filePath
        elif os.path.exists(path=pathfileOrURL):
            wordListPath = pathfileOrURL
        else:
            wordListPath = False
        

        if wordListPath:
            isHash = False
            for hash_type, itme in self.hashs.items(): 
                hashing, regex = itme
                if re.match(regex, hash):
                    isHash = True
                    self.logger.write(loggerBody(level='debug', message=f"the hash is likely `{hash_type}`").model_dump_json())

                    #* Open in binary mode
                    with open(wordListPath, 'rb') as file:  
                        for line_number, line in tqdm(enumerate(file), desc="Processing lines", disable=not config.enableTqdm):
                            try:
                                #* Decode each line, ignoring errors
                                text = line.decode('utf-8')  # You can change the encoding if needed
                                
                                hash_word = hashing(text.strip().encode('utf-8')).hexdigest()
                                if hash_word == hash:
                                    self.logger.write(loggerBody(level='success', message=f"We found it! the de-hash is : `{text.strip()}`").model_dump_json())
                                    return text.strip()
                                else:
                                    continue
                            except UnicodeDecodeError as err:
                                self.binaryList.append({
                                    'line_number': line_number,
                                    'line': line,
                                    'error': err
                                })
                        countBinaryList = len(self.binaryList)
                        if countBinaryList > 0:
                            self.logger.write(loggerBody(level='warning', message=f"Excpted Error: We found a binary lines between words. and their number: {countBinaryList}. and he saved on self.binaryList").model_dump_json())
                        else:
                            None
                else:
                    continue
            
            if not isHash:
                self.logger.write(loggerBody(level='warning', message=f"Sorry, your entry is not hash.").model_dump_json())
                return False
            else:
                self.logger.write(loggerBody(level='warning', message=f"there is not match!").model_dump_json())
                return False

        else:
            self.logger.write(loggerBody(level='error', message=f"Unfortunately, the `pathfileOrURL` variable is not URL or a file exists on your system").model_dump_json())
            return False
             

    def Hash_generater(self, text:str, hashType:str, useSalt=False, length=20):
        if hashType in list(self.hashs.keys()):
            hash_function = self.hashs[hashType][0]
            if useSalt:
                combined_string =  self.combined_string(
                    generate_salt=self.generate_salt(length=length),
                    text=text
                )
                salted_hash = hash_function(combined_string.encode('utf-8')).hexdigest()
                
                self.logger.write(loggerBody(level='success', message=f"your hash is : ({salted_hash}) and he hashed from text: ({text}), hash type: ({hashType}), and your salt option: {useSalt}").model_dump_json())
                return salted_hash
            
            else:
                hashGen = hash_function(text.encode('utf-8')).hexdigest()
                self.logger.write(loggerBody(level='success', message=f"your hash is : ({hashGen}) and he hashed from text: ({text}), hash type: ({hashType}), and your salt option: {useSalt}").model_dump_json())
                return hashGen
        else:
            self.logger.write(loggerBody(level='error', message=f"Sorry, hash type ({hashType}) is not on the list of hashs. hashs list: {list(self.hashs.keys())}").model_dump_json())
            


if __name__ == '__main__':
    # https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
    
    hash = '6b008bafd02f6c9ea7a63996e1705b2fdd8163aa67a0ce7ecc783432ea0eac1a6a43340855b89fb5cbb8508065ff1ac7'
    print(open('./ASCII-Art.art', 'r').read())
    
    hash_k = hash_killer()
    
    hash_k.logger.write(loggerBody(level='debug', message=f"testing for `generate_salt`: ({hash_k.generate_salt(19)})").model_dump_json())
    hash_k.foundMatch(hash=hash, pathfileOrURL='https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt')
    hash_k.Hash_generater(hashType='sha384', text='iloveyou', useSalt=True, length=20)

