# detect-scrobble

To run:

```sh
# Build the Docker image
docker build -t detect-scrobble .

# Run the container
docker run -d --restart unless-stopped --name detect-scrobble-container detect-scrobble
```

To check logs:

```sh
docker exec -it detect-scrobble-container tail -f /var/log/cron.log
```
