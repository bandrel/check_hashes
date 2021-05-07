#Check Hashes

Purpose: To check for and reveal AD user accounts that share passwords using a hashdump from a Domain Controller
Script requires a command line argument of a file containing usernames/hashes in the format of user:sid:LMHASH:NTLMHASH:::
./check_hashes.py <hash_dump>

If using Docker can use the bash function in your ~/.bash_aliases file

```
checkhashes() {
docker run -t -v $(pwd):/out/ bandrel/check_hashes:latest "/out/$*"
}
```

This will allow you to input and output to the pwd. 

