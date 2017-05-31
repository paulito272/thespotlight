import datetime
import os

import httplib2
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from collections import OrderedDict

# Define the auth scopes to request.
scope = ['https://www.googleapis.com/auth/analytics.readonly']

# Use the developer console and replace the values with your
# service account email and relative location of your key file.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_EMAIL = 'ele-thespotlight@thespotlight-169213.iam.gserviceaccount.com'
SERVICE_ACCOUNT_PKCS12_FILE_PATH = os.path.join(BASE_DIR, 'keys', 'thespotlight-a503d4a089dd.p12')


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


def get_pageviews(service, profile_id):
    # Last week
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)

    return service.data().ga().get(
        ids='ga:' + profile_id,
        dimensions='ga:pageTitle,ga:pagePath',
        metrics='ga:pageviews,ga:uniquePageviews',
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        sort='-ga:pageviews').execute()


def get_most_read_pages():
    # Authenticate and construct service.
    service = get_service('analytics', 'v3', scope, SERVICE_ACCOUNT_PKCS12_FILE_PATH, SERVICE_ACCOUNT_EMAIL)
    profile = get_first_profile_id(service)

    # Fetch last week's most read pages
    results = get_pageviews(service, profile)

    most_read_pages = OrderedDict()
    NUM_OF_PAGES = 10

    if results:
        top_pages = results.get('rows')

        for page in top_pages:
            if (len(most_read_pages) == NUM_OF_PAGES):
                break
            slug = page[1].strip('/')
            if slug:
                if 'category' not in slug and 'tag' not in slug:
                    most_read_pages[slug] = slug

    return most_read_pages


def main():
    slugs = get_most_read_pages()
    if slugs:
        for slug in slugs:
            print(slug)


if __name__ == '__main__':
    main()
