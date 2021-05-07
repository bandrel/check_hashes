#Check Hashes

Purpose: To check for and reveal AD user accounts that share passwords using a hashdump from a Domain Controller
Script requires a command line argument of a file containing usernames/hashes in the format of user:sid:LMHASH:NTLMHASH:::
./check_hashes.py <hash_dump>

If using Docker can use the bash function in your ~/.bash_aliases file

```
alias check_hashes="docker run -t -v $(pwd):$(pwd) bandrel/check_hashes:latest"
```

only requirement is the file needs to be in the pwd and you need to fully qualify the filename or use `$(pwd)/`

