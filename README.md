# ntdsSearch

Tool developed to search for passwords in secretsdump.

## Starting

### Usage
_Get a specific username hash_
```
python3 ntdsSearch.py -f <secretsdump_output> -u <username>
```

_Get users by its hash ntlm_
```
python3 ntdsSearch.py -f <secretsdump_output> -n <hashntlm>
```

_Get users by its password_
```
python3 ntdsSearch.py -f <secretsdump_output> -p <password>
```

_Get all the users of the domain that have their hash repeated_
```
python3 ntdsSearch.py -f <secretsdump_output> -r
```

_You can also use all of these features with the -q parameter to remove old passwords (password history). For example:_
```
python3 ntdsSearch.py -f <secretsdump_output> -r -q
```


