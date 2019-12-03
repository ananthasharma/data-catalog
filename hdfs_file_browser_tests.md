# Testing hdfs file browser api's


```python
#Start django instance
```

# assuming the application is running on port ```8000```

```base_URL = "http://localhost:8000/"```
### for when we want to list files from SAN
```context_path = "file_manager/local/browse/"```
### for when we want to list files from HDFS
**```context_path = "file_manager/hdfs/browse/"```**
### for when we want to upload files to SAN
```context_path = "file_manager/local/upload/"```
### for when we want to download files to SAN
```context_path = "file_manager/local/download/"```

### for all requests
```query_param = "path"```

#### query parameter accepts a string with the path to target folder

# <span style="background:cyan">assumed configuration</span>


```"/LAN33" maps to "/var"```

```"/LAN34" maps to "/opt"```

```"/LAN35" maps to "/usr"```

```"/LAN36" maps to "/opt/mapr"```


## Test with folder path
### when the param ```path``` is sent and exists in the system | <span style="background:lightgreen"> HAPPY PATH </span>


```python
!curl -s http://localhost:8000/file_manager/hdfs/browse/?path=/ | json_pp
```

    [
       {
          "simple_name" : ".DS_Store",
          "name" : "/.DS_Store",
          "type" : "file",
          "file_size" : 0
       },
       {
          "name" : "/.file",
          "simple_name" : ".file",
          "type" : "file",
          "file_size" : 0
       },
       {
          "contents" : [],
          "simple_name" : ".fseventsd",
          "name" : "/.fseventsd",
          "type" : "directory"
       },
       {
          "type" : "directory",
          "simple_name" : ".vol",
          "name" : "/.vol",
          "contents" : []
       },
       {
          "name" : "/Applications",
          "simple_name" : "Applications",
          "type" : "directory",
          "contents" : []
       },
       {
          "contents" : [],
          "type" : "directory",
          "simple_name" : "Library",
          "name" : "/Library"
       },
       {
          "contents" : [],
          "name" : "/System",
          "simple_name" : "System",
          "type" : "directory"
       },
       {
          "simple_name" : "Users",
          "name" : "/Users",
          "type" : "directory",
          "contents" : []
       },
       {
          "contents" : [],
          "name" : "/Volumes",
          "simple_name" : "Volumes",
          "type" : "directory"
       },
       {
          "type" : "directory",
          "simple_name" : "bin",
          "name" : "/bin",
          "contents" : []
       },
       {
          "contents" : [],
          "name" : "/cores",
          "simple_name" : "cores",
          "type" : "directory"
       },
       {
          "type" : "directory",
          "simple_name" : "dev",
          "name" : "/dev",
          "contents" : []
       },
       {
          "contents" : [],
          "simple_name" : "etc",
          "name" : "/etc",
          "type" : "directory"
       },
       {
          "name" : "/home",
          "simple_name" : "home",
          "type" : "directory",
          "contents" : []
       },
       {
          "simple_name" : "lan34",
          "type" : "directory",
          "name" : "/lan34",
          "contents" : []
       },
       {
          "contents" : [],
          "simple_name" : "private",
          "type" : "directory",
          "name" : "/private"
       },
       {
          "type" : "directory",
          "simple_name" : "sbin",
          "name" : "/sbin",
          "contents" : []
       },
       {
          "name" : "/tmp",
          "simple_name" : "tmp",
          "type" : "directory",
          "contents" : []
       },
       {
          "type" : "directory",
          "simple_name" : "lan35",
          "name" : "/lan35",
          "contents" : []
       },
       {
          "type" : "directory",
          "simple_name" : "lan33",
          "name" : "/lan33",
          "contents" : []
       }
    ]


## Test with non-existent folder path | <span style="background:red"> FAIL PATH </span>


```python
!curl -s http://localhost:8000/file_manager/hdfs/browse/?path=/non-existent-folder | json_pp
```

    [
       {
          "name" : "/non-existent-folder",
          "type" : "directory",
          "contents" : []
       }
    ]


# when ```path``` param wasn't sent to the service | <span style="background:red"> FAIL PATH </span>


```python
!curl -s http://localhost:8000/file_manager/hdfs/browse/ | json_pp
```

    {
       "error" : "`path` parameter in http GET is mandatory"
    }

