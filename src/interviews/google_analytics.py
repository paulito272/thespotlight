import os

import httplib2
from apiclient.discovery import build
from decouple import config
from oauth2client.service_account import ServiceAccountCredentials

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_EMAIL = config('SERVICE_ACCOUNT_EMAIL')
SERVICE_ACCOUNT_PKCS12 = config('SERVICE_ACCOUNT_PKCS12')

# Use the developer console and replace the values with your
# service account email and relative location of your key file.
SERVICE_ACCOUNT_PKCS12_FILE_PATH = os.path.join(BASE_DIR, 'keys', SERVICE_ACCOUNT_PKCS12)

# Define the auth scopes to request.
scope = ['https://www.googleapis.com/auth/analytics.readonly']


def get_service(api_name, api_version, scope, key_file_location, service_account_email):
    """Get a service that communicates to a Google API.

    Args:
      api_name: The name of the api to connect to.
      api_version: The api version to connect to.
      scope: A list auth scopes to authorize for the application.
      key_file_location: The path to a valid service account p12 key file.
      service_account_email: The service account email address.

    Returns:
      A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_p12_keyfile(service_account_email, key_file_location, scopes=scope)

    http = credentials.authorize(httplib2.Http())

    # Build the service object.
    service = build(api_name, api_version, http=http)

    return service


def get_first_profile_id(service):
    # Use the Analytics service object to get the first profile id.

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        # Get the first Google Analytics account.
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(
            accountId=account).execute()

        if properties.get('items'):
            # Get the first property id.
            property = properties.get('items')[0].get('id')

            # Get a list of all views (profiles) for the first property.
            profiles = service.management().profiles().list(
                accountId=account,
                webPropertyId=property).execute()

            if profiles.get('items'):
                # return the first view (profile) id.
                return profiles.get('items')[0].get('id')
    return None


# Get week's top 3 pages (ignore: /, /home, /tag/, /twos/, /category/)
def get_top3_week_pages(service, profile_id):
    return service.data().ga().get(
        ids='ga:' + profile_id,
        start_date='7daysAgo',
        end_date='today',
        metrics='ga:uniquePageviews',
        dimensions='ga:pagePathLevel1,ga:pagePath',
        sort='-ga:uniquePageviews',
        filters='ga:pagePath!=/;ga:pagePath!=/home;ga:pagePathLevel1!=/tag/;'
                'ga:pagePathLevel1!=/twos/;ga:pagePathLevel1!=/category/',
        max_results='3').execute()


def get_most_read_pages():
    most_read_pages = {}

    # Authenticate and construct service.
    service = get_service('analytics', 'v3', scope, SERVICE_ACCOUNT_PKCS12_FILE_PATH, SERVICE_ACCOUNT_EMAIL)
    profile = get_first_profile_id(service)
    results = get_top3_week_pages(service, profile)

    if results:
        top_pages = results.get('rows')
        for page in top_pages:
            slug = page[1].replace('/', '')
            views = page[2]
            if slug:
                most_read_pages[slug] = views

    return most_read_pages
