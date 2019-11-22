# Testing the solution (just the local file browser apis)


```python
#Start instance by running

!#python manage.py runserver
```


```python
# assuming the application is running on port 8000
```


```python
base_URL = "http://localhost:8000/"
context_path = "files/local/list/"
query_param = "folder"
#query parameter accepts a string with the path to target folder
```

## Test with folder path
### defaults to folder / when the param ```folder``` isn't sent


```python
!curl http://localhost:8000/files/local/list/
# this command is the same as above

!echo "\n\nthis command is the same as above\n\n"

!ls -l /
```

    [{"type":"directory","name":"/","contents":[{"type":"directory","name":"//home","contents":[]},{"type":"directory","name":"//usr","contents":[]},{"type":"directory","name":"//bin","contents":[]},{"type":"directory","name":"//sbin","contents":[]},{"type":"directory","name":"//etc","contents":[]},{"type":"directory","name":"//var","contents":[]},{"type":"directory","name":"//Library","contents":[]},{"type":"directory","name":"//System","contents":[]},{"type":"directory","name":"//.fseventsd","contents":[]},{"type":"directory","name":"//private","contents":[]},{"type":"directory","name":"//.vol","contents":[]},{"type":"directory","name":"//Users","contents":[]},{"type":"directory","name":"//Applications","contents":[]},{"type":"directory","name":"//opt","contents":[]},{"type":"directory","name":"//dev","contents":[]},{"type":"directory","name":"//Volumes","contents":[]},{"type":"directory","name":"//tmp","contents":[]},{"type":"directory","name":"//cores","contents":[]}]}]
    
    this command is the same as above
    
    
    total 10
    drwxrwxr-x+ 62 root  admin  1984 Nov 17 17:44 [34mApplications[m[m
    drwxr-xr-x  68 root  wheel  2176 Nov 13 10:18 [34mLibrary[m[m
    drwxr-xr-x@  8 root  wheel   256 Sep 29 16:23 [34mSystem[m[m
    drwxr-xr-x   7 root  admin   224 Sep 29 16:22 [34mUsers[m[m
    drwxr-xr-x   5 root  wheel   160 Nov 17 17:44 [34mVolumes[m[m
    drwxr-xr-x@ 38 root  wheel  1216 Nov 13 10:15 [34mbin[m[m
    drwxr-xr-x   2 root  wheel    64 Aug 24 18:24 [34mcores[m[m
    dr-xr-xr-x   3 root  wheel  4805 Nov 13 10:21 [34mdev[m[m
    lrwxr-xr-x@  1 root  admin    11 Oct  7 23:37 [35metc[m[m -> private/etc
    lrwxr-xr-x   1 root  wheel    25 Nov 13 10:22 [35mhome[m[m -> /System/Volumes/Data/home
    drwxr-xr-x   4 root  wheel   128 Oct  7 23:46 [34mopt[m[m
    drwxr-xr-x   6 root  wheel   192 Nov 13 10:16 [34mprivate[m[m
    drwxr-xr-x@ 64 root  wheel  2048 Nov 13 10:15 [34msbin[m[m
    lrwxr-xr-x@  1 root  admin    11 Oct  7 23:41 [35mtmp[m[m -> private/tmp
    drwxr-xr-x@ 11 root  wheel   352 Oct  7 23:41 [34musr[m[m
    lrwxr-xr-x@  1 root  admin    11 Oct  7 23:41 [35mvar[m[m -> private/var


## Test with non-existent folder path


```python
!curl "http://localhost:8000/files/local/list/?folder=/non-existent-folder"
# this command is the same as above

!echo "\n\nthis command is the same as above\n\n"

!ls -l /non-existent-folder
```

    [{"name":"/non-existent-folder","contents":[{"error":"opening dir"}]}]
    
    this command is the same as above
    
    
    ls: /non-existent-folder: No such file or directory


# testing file download feature
### can be only run when we know the full path of a file

# when file doesn't exist


```python

!curl "http://localhost:8000/files/local/download/?file_path=/path/does/not/exist/to/this/file.txt"
# this command is the same as above

!echo "\n\nthis command is the same as above\n\n"

!cat /path/does/not/exist/to/this/file.txt
```

    "no file was found at /path/does/not/exist/to/this/file.txt"
    
    this command is the same as above
    
    
    cat: /path/does/not/exist/to/this/file.txt: No such file or directory


# when file param wasnt sent to the service


```python

!curl "http://localhost:8000/files/local/download/"

```

    "`file_path` is a mandatory field and cannot be empty"

# when folder name is sent for download


```python

!curl "http://localhost:8000/files/local/download/?file_path=/Users"
# this command is the same as above

!echo "\n\nthis command is the same as above\n\n"

!cat /Users
```

    "this /Users is not a file"
    
    this command is the same as above
    
    
    cat: /Users: Is a directory


# when correct file name was sent for download


```python

!curl "http://localhost:8000/files/local/download/?file_path=/Users/asharma/Downloads/1.txt"
# this command is the same as above

!echo "\n\nthis command is the same as above\n\n"

!cat /Users/asharma/Downloads/1.txt
```

    ["hello \n"]
    
    this command is the same as above
    
    
    hello 


## Test file upload
### service saves file into the give folder

### service tries to create folder if it doesn't exist; if it fails to then it returns a ```http/304 - not modified``` since nothing was modified on the server


```python
!curl -X PUT \
  http://0.0.0.0:8000/files/local/list/ \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Length: 4420811' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Host: 0.0.0.0:8000' \
  -H 'Postman-Token: 462c9038-2e3d-4764-a36e-46e50931118c,9f5dff71-6675-43f9-872b-fcf4997c8202' \
  -H 'User-Agent: PostmanRuntime/7.19.0' \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F 'file_ref=@/bin/bash' \
  -F file_name=bash.command \
  -F file_location=/tmp/folder/

```
