"""
This module contins utilities for parsing the Pardot API documentation
and dumping the information to stdout.

This can be used to populate the RESOURCE_OPERATIONS constant in
constants.py
"""

import re
import html
import string

from pprintpp import pprint

import requests


def get_resource_urls():
    """
    Returns a list of URLs for API resources
    """
    base_url = 'http://developer.pardot.com/'
    pattern = re.compile(
        r'(?ims)\<a [^>]*?href="(kb/api-version-3/[^>]*?/)"[^>]*?\>'
        r'[^<]*?\</a\>')
    response = requests.get(base_url)
    return [
        '%s/%s' % (base_url, url) for url in pattern.findall(response.text)]


def get_resource_tables(resource_url):
    """
    Returns a list of all the HTML tables for the resource documented at
    resource_url
    """
    pattern = re.compile(r'(?ims)(\<table\>.*?\</table\>)')
    response = requests.get(resource_url)
    return pattern.findall(response.text)


def get_table_headers(table):
    """
    Returns a list of the table headers values for table
    """
    pattern = re.compile(r'(?ims)\<thead\>(.*?)\</thead\>')
    head = pattern.findall(table)[0]

    pattern = re.compile(r'(?ims)\<th.*?\>([^<]+?)\<.*?/th\>')
    return pattern.findall(head)


def get_table_data(table):
    """
    Returns a list of the table row data values for table
    """
    pattern_body = re.compile(r'(?ims)\<tbody\>(.*?)\</tbody\>')
    pattern_rows = re.compile(r'(?ims)\<tr\>(.*?)\</tr\>')
    pattern_cols = re.compile(r'(?ims)\<td.*?\>([^<]+?)\<.*?/td\>')

    body = pattern_body.findall(table)[0]
    return [
        list(map(lambda x: html.unescape(x), pattern_cols.findall(row)[:3]))
        for row in pattern_rows.findall(body)]


def get_resource_operations(resource_url):
    """
    Returns a list of operations details for the resource documented at
    resource_url
    """
    required_headers = ('Operation', 'URL Format', 'Required Parameters')
    for table in get_resource_tables(resource_url):
        headers = get_table_headers(table)
        if not set(required_headers).issubset(headers):
            continue
        for row in get_table_data(table):
            yield row


def print_resource_operations():
    results = {}
    for resource_url in get_resource_urls():
        for row in get_resource_operations(resource_url):
            try:
                resource_name = row[1].split('/')[2]
                operation = row[0]
                parameters = map(lambda x: x.strip(), row[2].split(','))
                parameters = filter(
                    lambda x: x not in ('user_key', 'api_key'), parameters)
                parameters = filter(
                    lambda x: x[0] in string.ascii_lowercase, parameters)
                data = results.setdefault(resource_name, {})
                data = data.setdefault(operation, [])
                data.append(tuple(parameters))
            except Exception as e:
                e.args += ('Row data: %s' % row,)
                raise

    pprint(results)


if __name__ == '__main__':
    print_resource_operations()
