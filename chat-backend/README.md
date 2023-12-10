

Components:

- [Backend](application) (test coverage: ![test coverage backend](test/test-coverage/coverage.svg))


### Build everything

docker build -t webis/chatnoir-chat:0.0.3 -f docker/Dockerfile .

### Update the development container

```
docker build -t webis/chatnoir-chat:0.0.1-dev -f docker/Dockerfile.dev .
docker push webis/chatnoir-chat:0.0.1-dev
```
