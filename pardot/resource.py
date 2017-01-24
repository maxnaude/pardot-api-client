import logging
import urllib
from time import sleep
from math import sqrt

from six.moves.urllib.parse import urlencode

import hammock

from pardot import constants


logger = logging.getLogger(__name__)


def fib(n):
    """
    Returns the nth number in the Fibonacci sequence.
    """
    return ((1 + sqrt(5))**n - (1 - sqrt(5))**n) / (2**n * sqrt(5))


class PardotAPIException(Exception):
    """
    Custom exception class that stores the error code, message and
    request for failed Pardot API calls
    """

    def __init__(self, code, message, request):
        self.code = code
        self.message = message
        self.request = request

    def __str__(self):
        return 'Pardot API call failed with Code %s: "%s" for request: %s' % (
            self.code, self.message, self.request)


class Resource(object):
    """
    Representation of a Pardot API resource
    """

    def __init__(self, name, email, password, user_key, retries, api_version):
        """
        Stores the resource name and API credentials and sets up the
        Hammock request chain for subsequent calls
        """
        self.name = name
        self.email = email
        self.password = password
        self.user_key = user_key
        self.retries = retries
        self.api_version = api_version

        # set up the base Hammock request chain
        self.api = hammock.Hammock('https://pi.pardot.com/api')

        # initialise the api_key to None to flag that login is required
        self.api_key = None

    def __getattr__(self, operation):
        """
        Returns a resource operation as a callable method.
        """
        def response(*args, **kwargs):
            """
            Builds a hammock request chain for the resource, operation
            and (optionally) identity.

            Runs the request against the API and returns the response.
            """
            if operation not in constants.RESOURCE_OPERATIONS[self.name]:
                raise Exception('Operation "%s" not supported for "%s"' % (
                    operation, self.name))

            request = self.api(
                self.name, 'version', self.api_version, 'do', operation)

            # some calls require an resource identifier like email or id
            # to keep the API simple the parameters are guessed based on
            # the args and some conventional assumptions mapped in
            # constants
            identifiers = self.get_parameter_identifiers(
                constants.RESOURCE_OPERATIONS[self.name][operation], args)

            if len(args) != len(identifiers):
                raise Exception(
                    'Arguments (%d) do not match identifiers (%d) for '
                    'operation %s on %s' % (
                        len(args), len(identifiers), operation, self.name))

            for i, arg in enumerate(args):
                # ensure that the identifier is url-safe
                urlsafe_arg = urlencode({'': arg})[1:]

                # add the identifier field name and value to the request
                request = request(identifiers[i], urlsafe_arg)

            return self.get_response_content(request, **kwargs)

        return response

    def get_parameter_identifiers(self, valid_identifiers, arguments):
        """
        Guesses the correct indentifiers for resource operation
        parameters based on the arguments.

        Returns a list of identifier names.
        """
        if len(valid_identifiers) == 1:
            # there is only one valid set of parameters
            return valid_identifiers[0]

        for identifiers in valid_identifiers:
            matched_identifiers = []
            for i in range(min(len(identifiers), len(arguments))):
                found = False
                for test in constants.RESOURCE_PARAMETER_TYPE_TESTS.values():
                    if test(identifiers[i], arguments[i]):
                        found = True
                        break
                matched_identifiers.append(found)

            if all(matched_identifiers):
                return identifiers

        return []

    def get_api_response(self, request, **kwargs):
        """
        Runs the request against the Pardot API.

        Returns the response content as a dictionary.
        """
        # ensure Accept headers are always set on requests
        params = {'headers': {'Accept': 'application/json'}}
        params.update(kwargs)

        # run the API request
        retried = 0
        while 1:
            try:
                response = request.POST(**params)
                break
            except Exception as e:
                # TODO:  retry only on network errors here
                if retried < self.retries:
                    retried += 1
                    # incremental backoff up to 55 seconds
                    # (10th value in the Fibonacci sequence)
                    sleep(fib(min(retried, 10)))
                else:
                    raise

        # decode the JSON response
        try:
            content = response.json()
        except Exception as e:
            logger.exception(e)
            raise Exception(
                'Failed to decode JSON response from API request %s '
                '(status code %s) - error was: %s' % (
                    request, response.status_code, e))

        # detect error responses from the API
        if content.get('@attributes', {}).get('stat', '') != 'ok':
            raise PardotAPIException(
                content.get('@attributes', {}).get('err_code', ''),
                content.get('err', 'Unknown error'),
                request)

        return content

    def login(self):
        """
        Logs in to the Pardot API and sets api_key for the instance
        """
        payload = {
            'email': self.email,
            'password': self.password,
            'user_key': self.user_key,
            'format': 'json',
            }

        request = self.api('login', 'version', self.api_version)
        content = self.get_api_response(request, data=payload)

        self.api_key = content['api_key']

    def get_response_content(self, request, **kwargs):
        """
        Returns the API response content for a request and method,
        optionally passing parameters as GET or POST payload.

        Retries requests on login failures if the api_key for the
        instance has expired.
        """
        # initialise the request parameters
        payload = {
            'email': self.email,
            'user_key': self.user_key,
            'format': 'json',
            }

        # update the request parameters from kwargs
        payload.update(kwargs)

        # make sure we're logged in
        if not self.api_key:
            self.login()

        payload['api_key'] = self.api_key

        # run the request and retry once if the request fails with a
        # login error (Pardot API error code '1')
        retried_login = False
        while 1:
            try:
                content = self.get_api_response(request, data=payload)
            except PardotAPIException as e:
                if e.code == '1' and not retried_login:
                    # API key might have expired - log in and retry
                    self.login()
                    payload['params']['api_key'] = self.api_key
                    retried_login = True
                else:
                    raise

            break

        return content
