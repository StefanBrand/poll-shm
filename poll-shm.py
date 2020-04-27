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

    # Query REST endpoint for all requests
    viewtoken = 0
    requests = []
    while viewtoken is not None:
        response = oauth.request('GET', f'{url}?viewtoken={viewtoken}').json()
        requests.extend(response['member'])
        viewtoken=response['view']['nextToken']

    active_rids = set([r['id'] for r in requests if r['status'] == 'PROCESSING' and r['userAction'] == 'START'])
    now = datetime.today().isoformat()
    print('active:', active_rids, now)

    # Log end time of finished requests
    finished_rids = old_rids - active_rids
    for frid in finished_rids:
        status = oauth.request('GET', f'{url}{frid}').json()['status']
        if status == 'DONE':
            with open('static/endtimestamps.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow([frid,datetime.today().isoformat()]) # log end time

    # Outdate active request ids
    old_rids = active_rids
    print('old:', old_rids)

    time.sleep(1)
