# How to run
```
    cd {{root_dir}}
    make run
```

# build docker
```
docker build -t ms .
```

# run docker
```
docker run --rm -d -p 8080:8080 ms:latest
```