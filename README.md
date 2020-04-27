# poll-shm

## Usage instructions

```
docker build -t poll-shm:latest .

docker run -p 5000:5000 -e SH_CLIENT_ID=<your-client-id> -e SH_CLIENT_SECRET=<your-client-secret> -d poll-shm
```

Then open `localhost:5000` in your webbrowser.
