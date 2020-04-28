import csv, time
from datetime import datetime
from os import getenv

# Oauth
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

# Your client credentials
client_id = getenv('SH_CLIENT_ID')
client_secret = getenv('SH_CLIENT_SECRET')

# Create a session
token_url = 'https://services.sentinel-hub.com/oauth/token'
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)

token = oauth.fetch_token(token_url=token_url,
                          client_id=client_id, client_secret=client_secret)

resp = oauth.get("https://services.sentinel-hub.com/oauth/tokeninfo")


# MAIN
url = 'https://services.sentinel-hub.com/batch/v1/process/'

old_rids = set()
active_rids = set()

while True:
    # Fetch new token when needed
    if token['expires_at'] - time.time() < 600:
        token = oauth.fetch_token(
            token_url='https://services.sentinel-hub.com/oauth/token',
            client_id=client_id, client_secret=client_secret
        )
        print(datetime.today().isoformat(), 'NEW TOKEN FETCHED')

    # Query REST endpoint for all requests
    viewtoken = 0
    requests = []
    while viewtoken is not None:
        response = oauth.request('GET', f'{url}?viewtoken={viewtoken}').json()
        requests.extend(response['member'])
        viewtoken=response['view']['nextToken']

    active_rids = set([r['id'] for r in requests if r['status'] == 'PROCESSING' and r['userAction'] == 'START'])
    print(datetime.today().isoformat(), 'CURRENTLY PROCESSING:', active_rids)

    # Log end time of finished requests
    finished_rids = old_rids - active_rids
    for frid in finished_rids:
        response = oauth.request('GET', f'{url}{frid}').json()
        status = response['status']
        creation_dt = datetime.fromisoformat(response['created'].strip('Z'))
        if status == 'DONE':
            duration = datetime.utcnow()-creation_dt
            description = response['description']
            with open('static/duration.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow([description, frid, duration]) # log end time
            print(datetime.today().isoformat(), frid, 'TOOK', duration, 'TO COMPLETE')

    # Outdate active request ids
    old_rids = active_rids

    time.sleep(1)
