from pardot import constants
from pardot.resource import Resource


class APIClient(object):
    """
    An API client to interact with the Pardot API
    """

    def __init__(self, email, password, user_key, retries=0):
        """
        Stores the API credentials and sets the maximum number of
        retries on network errors.
        """
        self.email = email
        self.password = password
        self.user_key = user_key
        self.retries = retries

        # leave options open for Pardot API version 4 support in future
        self.api_version = 3

    def __getattr__(self, resource_name):
        """
        Returns a Pardot API Resource instance.

        Resource name must match the name on the Pardot API, eg
        'prospect' or 'dynamicContent'.  Alternatively snake case
        resource names may be used, eg 'dynamic_content'.
        """
        api_resource_name = resource_name
        if '_' in resource_name:
            # convert to camel case with first letter lower-cased
            api_resource_name = '%s%s' % (
                resource_name.split('_')[0],
                ''.join(part.title() for part in resource_name.split('_')[1:]))

        if api_resource_name not in constants.RESOURCE_OPERATIONS:
            raise Exception('Resource "%s" not supported' % api_resource_name)

        return Resource(
            api_resource_name, self.email, self.password, self.user_key,
            self.retries, self.api_version)
