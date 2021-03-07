# Model as a Service - playground

Here you may find comfortable playground to test staff while workshop.

## Environment build
To build playground simply run:
```bash
repo_root/playground$ docker build -t maas/v2/playground . 
```

## Environment run
To run playground use the following command:
```bash
docker run --network host -it maas/v2/playground:latest
```