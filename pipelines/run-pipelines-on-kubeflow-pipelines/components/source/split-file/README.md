
### Build the component container image

```
$ make container-image
```

### Publish the component container image

Customize the variables in [`Makefile`](Makefile) and run the following command to publish the container image on Docker Hub and/or Quay.

```
$ make publish-container-image 
```

### Customize the component YAML file

In [`truncate-file.yaml`](truncate-file.yaml) update the value of `implementation.container.image` as required.
