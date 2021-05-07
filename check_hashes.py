#!/usr/bin/env python3

#Purpose: To check for and reveal AD user accounts that share passwords using a hashdump from a Domain Controller
#Script requires a command line argument of a file containing usernames/hashes in the format of user:sid:LMHASH:NTLMHASH:::
# ./check_hashes.py <hash_dump>

import argparse
import re

parser = argparse.ArgumentParser(description="Check user hashes against each other to find users that share passwords")
parser.add_argument('pwdump', help="Hashes in the pwdump format")
parser.add_argument("--prefix",'--pre', help="Optional filter based on prefix", required=False)
parser.add_argument("--suffix",'--post', help="Optional filter based on suffix ", required=False)
parser.add_argument("--regex", help="Optional regex filter", required=False)
parser.add_argument("--file", help="Optional file containing a list of admin users to use as a filter", required=False)

args = parser.parse_args()

pwdump = args.pwdump
prefix = args.prefix
suffix = args.suffix
regex = args.regex
admin_file = args.file

admin_users = []
if admin_file:
    with open(admin_file) as i:
        for line in i:
            admin_users.append(line.rstrip())

if prefix:
    prefix_pattern = re.compile(r'^((.*\\)?'+prefix+r'[^:]+):',re.IGNORECASE)
    with open(pwdump) as pdump:
        for line in pdump:
            _username = prefix_pattern.match(line.rstrip())
            if _username:
                username = _username.group(1)
                admin_users.append(username.rstrip())

if suffix:
    suffix_pattern = re.compile(r'^([^:]+'+suffix+r'):',re.IGNORECASE)
    with open(pwdump) as pdump:
        for line in pdump:
            _username = suffix_pattern.match(line.rstrip())
            if _username:
                username = _username.group(1)
                admin_users.append(username.rstrip())

if regex:
    regex_pattern = re.compile(r'^('+regex.strip("'")+'):',re.IGNORECASE)
    with open(pwdump) as pdump:
        for line in pdump:
            _username = regex_pattern.match(line.rstrip())
            if _username:
                username = _username.group(1)
                admin_users.append(username.rstrip())
if admin_file:
    _admin_users = []
    with open(admin_file) as a:
        for line in a:
            _admin_users.append(line.rstrip())
    with open(pwdump) as pdump:
        for line in pdump:
            adminuser_pattern = re.compile(r'^((.*\\)?(' + '|'.join(_admin_users) + r')):', re.IGNORECASE)
            _username = adminuser_pattern.match(line.rstrip())
            if _username:
                username = _username.group(1)
                admin_users.append(username.rstrip())


hashes = {}
with open(pwdump) as infile:
    for line in infile:
        ntlmhash = line.split(':')[3]
        lmhash = line.split(':')[2]
        user = line.split(':')[0]
        try:
            hashes[ntlmhash].append(user)
        except KeyError:
            hashes[ntlmhash] = [user]

largest_group = 0

for hash in hashes:
    if hash != '31d6cfe0d16ae931b73c59d7e0c089c0':
        if len(hashes[hash]) > largest_group:
            largest_group = len(hashes[hash])

print()

if len(admin_users) == 0:
    for x in range(2,largest_group+1):
        for hash in hashes:
            if len(hashes[hash]) == x:
                for user in hashes[hash]:
                    print(user)
                print()
else:
    for x in range(2,largest_group+1):
        for hash in hashes:
            if len(hashes[hash]) == x:
                if any(user in admin_users for user in hashes[hash]):
                    for user in hashes[hash]:
                        print(user)
                    print()

