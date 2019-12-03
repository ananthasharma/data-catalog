# Testing local file browser api's


```python
#Start django instance
```

# assuming the application is running on port ```8000```

```base_URL = "http://localhost:8000/"```
### for when we want to list files from SAN
```context_path = "file_manager/local/browse/"```
### for when we want to list files from HDFS
```context_path = "file_manager/hdfs/browse/"```
### for when we want to upload files to SAN
```context_path = "file_manager/local/upload/"```
### for when we want to download files to SAN
```context_path = "file_manager/local/download/"```

### for all requests
```query_param = "path"```

#### query parameter accepts a string with the path to target folder

## Test with folder path
### when the param ```path``` is sent and exists in the system | <span style="background:lightgreen"> HAPPY PATH </span>


```python
!curl -s http://localhost:8000/file_manager/local/browse/?path=/ | json_pp
```

    [
       {
          "contents" : [
             {
                "type" : "directory",
                "name" : "/home",
                "contents" : []
             },
             {
                "type" : "directory",
                "contents" : [],
                "name" : "/usr"
             },
             {
                "type" : "directory",
                "name" : "/bin",
                "contents" : []
             },
             {
                "type" : "directory",
                "name" : "/sbin",
                "contents" : []
             },
             {
                "contents" : [],
                "name" : "/etc",
                "type" : "directory"
             },
             {
                "type" : "directory",
                "contents" : [],
                "name" : "/var"
             },
             {
                "type" : "directory",
                "contents" : [],
                "name" : "/Library"
             },
             {
                "type" : "directory",
                "name" : "/System",
                "contents" : []
             },
             {
                "name" : "/.fseventsd",
                "contents" : [],
                "type" : "directory"
             },
             {
                "name" : "/private",
                "contents" : [],
                "type" : "directory"
             },
             {
                "name" : "/.vol",
                "contents" : [],
                "type" : "directory"
             },
             {
                "type" : "directory",
                "contents" : [],
                "name" : "/Users"
             },
             {
                "type" : "directory",
                "name" : "/Applications",
                "contents" : []
             },
             {
                "type" : "directory",
                "contents" : [],
                "name" : "/opt"
             },
             {
                "type" : "directory",
                "contents" : [],
                "name" : "/dev"
             },
             {
                "type" : "directory",
                "name" : "/Volumes",
                "contents" : []
             },
             {
                "name" : "/tmp",
                "contents" : [],
                "type" : "directory"
             },
             {
                "type" : "directory",
                "contents" : [],
                "name" : "/cores"
             },
             [
                {
                   "name" : "/.DS_Store",
                   "simple_name" : ".DS_Store",
                   "type" : "file",
                   "file_size" : 0
                },
                {
                   "name" : "/.file",
                   "simple_name" : ".file",
                   "type" : "file",
                   "file_size" : 0
                }
             ]
          ],
          "name" : "/",
          "type" : "directory"
       }
    ]


## Test with non-existent folder path | <span style="background:red"> FAIL PATH </span>


```python
!curl -s http://localhost:8000/file_manager/local/browse/?path=/non-existent-folder | json_pp
```

    [
       {
          "name" : "/non-existent-folder",
          "contents" : [
             {
                "error" : "opening dir"
             }
          ]
       }
    ]


# testing file download feature
### can be only run when we know the full path of a file

# when file doesn't exist |  <span style="background:red"> FAIL PATH </span>


```python
!curl -s http://localhost:8000/file_manager/local/download/?path=/non-existent-file | json_pp
```

    {
       "error" : "no file was found at /non-existent-file"
    }


# when ```path``` param wasn't sent to the service | <span style="background:red"> FAIL PATH </span>


```python
!curl -s http://localhost:8000/file_manager/local/download/ | json_pp
```

    {
       "error" : "`path` parameter in http GET is mandatory"
    }


# when folder name is sent for download | <span style="background:red"> FAIL PATH </span>


```python

!curl -s "http://localhost:8000/file_manager/local/download/?path=/Users" | json_pp
# this command is the same as above

!echo "\n\nthis command is the same as above\n\n"

!cat /Users
```

    {
       "error" : "The path [/Users] is not a file"
    }
    
    
    this command is the same as above
    
    
    cat: /Users: Is a directory


# when correct file name was sent for download  | <span style="background:lightgreen"> HAPPY PATH </span>


```python
!curl -s "http://localhost:8000/file_manager/local/download/?path=/Users/asharma/Downloads/1.txt"
```

    ["hello \n"]

# Test file upload  | <span style="background:lightgreen"> HAPPY PATH </span>
### service saves file into the give folder

### service tries to create folder if it doesn't exist; if it fails to then it returns a ```http/304 - not modified``` since nothing was modified on the server


```python
!curl -s \
  -F 'file_ref=@/bin/bash' \
  -F 'file_name=bash.command' \
  -F "file_location=/tmp/folder2/" \
    "http://0.0.0.0:8000/file_manager/local/upload/" | json_pp
```

    [
       {
          "type" : "directory",
          "contents" : [
             [
                {
                   "simple_name" : "bash.command",
                   "name" : "/tmp/folder2/bash.command",
                   "file_size" : 623344,
                   "type" : "file"
                }
             ]
          ],
          "name" : "/tmp/folder2/"
       }
    ]


# Test file upload  | <span style="background:red"> FAIL PATH </span>
### service tries to save an already existing file (basically, replace isn't allowed)


```python
!curl -si \
  -F 'file_ref=@/bin/bash' \
  -F 'file_name=bash.command' \
  -F "file_location=/tmp/folder2/" \
    "http://0.0.0.0:8000/file_manager/local/upload/" 
```

    
    
    
    
    
    
    
    
    
    
    



```python

```


```python

```
