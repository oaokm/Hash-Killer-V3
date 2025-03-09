# Hash Killer Version 3

<p align="center">
  <a href="https://github.com/oaokm/Hash-Killer-V3/blob/main/READMD.ar.md">العربية</a>
  &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="https://github.com/oaokm/Hash-Killer-V3/blob/main/README.md">English</a>
</p>

This is the enhanced version of [Version 2](https://github.com/Omar-KL/Hash_Killer.V2) developed by [Omar-KL](https://github.com/Omar-KL). The program uses hash algorithms for generation and matching with the aim of discovering the origin of a word or data.

## Download Instructions

* First: You need to ensure that the [`git`](https://git-scm.com/downloads) software is installed on your system. If your operating system is Windows, you need to download the software. If you are using a GNU/Linux distribution or macOS, there is no need to install it. Alternatively, you can simply [click here](https://github.com/oaokm/Hash-Killer-V3/archive/refs/heads/main.zip) to download the repository.

* Second: If you want to download using `git`, open the command line (terminal) and type the following:

```sh
~$ git clone https://github.com/oaokm/Hash-Killer-V3
```

* Third: Navigate to the `Hash-Killer-V3` folder and type the following command in the command line to install the necessary libraries to run the program:

```sh
~$ pip install -r requirement.txt
```

## Program Files

```
.
├── ASCII-Art.art
├── config.py
├── hash_killer.py
├── images
│   └── .
├── lab.ipynb
├── log
│   ├── log.json
│   └── log.log
├── logger.py
├── READMD.ar.md
├── READMD.md
├── storage
│   └── .
└── url.py
```

| Folder | Purpose |
| ------ | ------ |
| images | A folder dedicated to images related to the project |
| storage | A folder dedicated to the list of passwords downloaded from the internet |
| log | A folder that keeps track of all operations performed during the program's execution |

| File | Purpose |
| ------ | ------ |
| ASCII-Art.art | Contains an ASCII art drawing |
| config.py | Configuration file |
| hash_killer.py | The main file that contains all the instructions to run the Hash Killer |
| lab.ipynb | A Jupyter file containing test "codes" for some features added in `hash_killer.py` |
| logger.py | A simple program that logs all operations, displays them to the user, and saves them in a file within the `log` folder |
| url.py | A simple program that checks if the provided text is indeed a link, with the ability to recognize and classify parts of the link |
| requirement.txt | Contains the non-standard libraries used to run the program |

## How to Use the Program?

Currently, you can use the program as a library that you can call using [`import`](https://docs.python.org/3/reference/import.html). You can do this by creating a Python file with any name inside the `Hash-Killer-V3` folder (which you downloaded earlier) and applying the following:

### Hash Generation
There are two types of generation:

* [Salting](https://en.wikipedia.org/wiki/Salt_%28cryptography%29): A random value added to the hash to increase complexity.
* Regular generation: Without salt :)

#### Regular Generation

First, we call the `hash_killer` object and define it as `hash_k`, then use the `Hash_generater` function to generate the hash.

```py
# Importing the library
from hash_killer import hash_killer

# Defining the object
hash_k = hash_killer()

# Command to generate the hash  
hash_gen = hash_k.Hash_generater(
    hashType='sha384', 
    text='iloveyou'
)

print(hash_gen)

# Output: 6b008bafd02f6c9ea7a63996e1705b2fdd8163aa67a0ce7ecc783432ea0eac1a6a43340855b89fb5cbb8508065ff1ac7
```

#### Salting Generation

You only need to add two options: `useSalt` and `length` arguments alongside `Hash_generater`.
The function of each is:

* `useSalt` (bool): A boolean option that, if set to "True", will add "salt" next to the original word to increase the complexity of the hash. It is set to "False" by default.

* `length` (int): Specifies the length of the "salted" text added to the original text. It is set to 20 by default.

```py
# Importing the library
from hash_killer import hash_killer

# Defining the object
hash_k = hash_killer()

# Command to generate the hash with salting enabled
hash_gen = hash_k.Hash_generater(
    hashType='sha384', 
    text='iloveyou',
    useSalt=True,
    length=20
)

print(hash_gen)

# Output: a1df82bc9a5c95f80694aea32686c32f13afaa1b3bc701461045d6ed74ca87745a9db80ae971813be81edde29203ae6b
```

### Match Detection
What distinguishes hash algorithms is their irreversibility; this means they differ from conventional encryption techniques, which are based on One-to-One function. Hashing uses a specific function that prevents collisions and reversibility.

![hashing-vs-encryption](https://github.com/oaokm/Hash-Killer-V3/blob/main/images/hashing-vs-encryption.png?raw=true)

Therefore, one of the solutions for discovering the origin of a word or data before subjecting it to hash algorithms is to detect matches by comparing the hash to be checked and identifying the type of hash algorithm, then matching it against a large set of texts and data by converting them into a hash that meets the criteria of the hash to be checked. If a match is "found", this means the check result is positive, and the result is the origin; if there is no match, the result is negative.

In Hash Killer, a system has been developed to detect matches and a method to download files from the internet. All you need to do is use the `foundMatch` function and enable the following options:

* `hash` (string): Here you place the hash you want to check.
* `pathfileOrURL` (string): Here you place a link to a file from the web or the path to the file on your device. The file must be a text file.

> Note: In this example, we will use the file [rockyou.txt](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt) from GitHub.

```py
# Importing the library
from hash_killer import hash_killer

# Defining the object
hash_k = hash_killer()

hash_word = '6b008bafd02f6c9ea7a63996e1705b2fdd8163aa67a0ce7ecc783432ea0eac1a6a43340855b89fb5cbb8508065ff1ac7'

# In pathfileOrURL, you can place a link or the path to the file.
# If you provide the link, the file will be downloaded and placed in the `./storage` folder.
result = hash_k.foundMatch(
    hash=hash_word,
    pathfileOrURL='https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt'
)

print(result)
```

## Support
Get me a little bit Caffeine goods! :)

<a href="https://www.buymeacoffee.com/oaokm" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

