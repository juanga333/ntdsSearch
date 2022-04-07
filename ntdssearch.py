import argparse
import hashlib
import binascii


def repeated(dict):
    rev_dict = {}
    for key, value in dict.items():
        rev_dict.setdefault(value, set()).add(key)

    result = [key for key, values in rev_dict.items()
              if len(values) > 1]
    for i in result:
        getUsernameByHash(dict, i)


def getUsernameHash(dict, username):
    if username in dict:
        print(f"{username} hash: {dict[args.username]}")
    else:
        print(f"{username} not in dump")


def getUsernameByHash(dict, hash, password=None):
    a = 0
    for key, value in dict.items():
        if hash == value:
            if a == 0:
                print(f"Hash: {value} : {password}")
            print(f"\t {key}")
            a = a + 1


def getNTLM(password):
    genhash = hashlib.new('md4', password.encode('utf-16le')).digest()
    genHash = binascii.hexlify(genhash)
    return genHash


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool developed to search for passwords in secretsdump")
    parser.add_argument("-f", "--file", required=True, help="Secretsdump output")
    parser.add_argument("-q", "--removeHistory", required=False, action='store_true',
                        help="Remove history hashes from list")
    parser.add_argument("-u", "--username", required=False, help="Get hash by username")
    parser.add_argument("-r", "--repeated", required=False, action='store_true', help="Get repeated hashes")
    parser.add_argument("-n", "--getUsernamesByHash", required=False, help="Get usernames by hash")
    parser.add_argument("-p", "--getUsernameByPassword", required=False, help="Get usernames by password")
    parser.add_argument("-pL", "--getUsernameByPasswordList", required=False, help="Get usernames by password")
    args = parser.parse_args()

    f = open(args.file, "r")
    Lines = f.readlines()
    f.close()
    dict = {}

    if args.removeHistory:
        for line in Lines:
            try:
                if "$" not in line and "_history" not in line:
                    split = line.split(":")
                    dict[split[0]] = split[3]
            except:
                pass
    else:
        for line in Lines:
            try:
                if "$" not in line:
                    split = line.split(":")
                    dict[split[0]] = split[3]
            except:
                pass

    if args.repeated:
        repeated(dict)

    username = args.username
    if username is not None:
        getUsernameHash(dict, username)

    hash = args.getUsernamesByHash
    if hash is not None:
        getUsernameByHash(dict, hash)

    password = args.getUsernameByPassword
    if password is not None:
        genHash = getNTLM(password)
        getUsernameByHash(dict, genHash.decode(), password)

    passwordList = args.getUsernameByPasswordList
    if passwordList is not None:
        f = open(passwordList, "r")
        Lines = f.read().split("\n")
        f.close()
        for line in Lines:
            if line != "":
                genHash = getNTLM(line)
                getUsernameByHash(dict, genHash.decode(), line)
