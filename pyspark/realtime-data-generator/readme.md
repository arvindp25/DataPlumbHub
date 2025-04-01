

to run on local via docker

goto directory where docker file is located

```
docker build . -t realtime-data-gen:dev
```

```
docker run -p 8080:8080 realtime-data-gen:dev
```