# poll-shm

This Docker app polls your Sentinel Hub Batch API requests for status changes\* and logs the duration of requests to a file called `duration.csv`. This file is exposed at `localhost:5000`.

\* observed request status change: `status==PROCESSING && userAction==START --> status==DONE`

## Usage instructions

```
docker build -t poll-shm:latest .

docker run -p 5000:5000 -e SH_CLIENT_ID=<your-client-id> -e SH_CLIENT_SECRET=<your-client-secret> poll-shm
```

Then open `localhost:5000` in your webbrowser.
