import collections

import six


RESOURCE_OPERATIONS = {
    'account': {
        'read': [()]
    },
    'campaign': {
        'create': [()],
        'query': [()],
        'read': [('id', )],
        'update': [('id', )],
    },
    'customField': {
        'create': [()],
        'delete': [('id', )],
        'query': [()],
        'read': [('id', )],
        'update': [('id', )],
    },
    'customRedirect': {
        'query': [()],
        'read': [('id', )]
    },
    'dynamicContent': {
        'query': [()],
        'read': [('id', )]
    },
    'email': {
        'read': [('email', )],
        'send': [
            ('campaign_id', 'name', 'subject'),
            ('list_ids[]', 'campaign_id', 'name', 'subject'),
        ],
        'stats': [('email', )],
    },
    'emailClick': {
        'query': [('search_criteria', 'result_set_criteria')]
    },
    'emailTemplate': {
        'listOneToOne': [()],
        'read': [('emailTemplateId', )]
    },
    'form': {
        'query': [()],
        'read': [('id', )]
    },
    'lifecycleHistory': {
        'query': [()],
        'read': [('id', )]
    },
    'lifecycleStage': {
        'query': [()]
    },
    'list': {
        'create': [()],
        'delete': [('id', )],
        'query': [()],
        'read': [('id', )],
        'update': [('id', )],
    },
    'listMembership': {
        'create': [('list_id', 'prospect_id')],
        'delete': [('id', ), ('list_id', 'prospect_id')],
        'query': [()],
        'read': [('id', ), ('list_id', 'prospect_id')],
        'update': [('id', ), ('list_id', 'prospect_id')],
    },
    'opportunity': {
        'query': [()],
        'create': [
            ('prospect_email', 'name', 'value', 'probability'),
            ('prospect_id', 'name', 'value', 'probability'),
        ],
        'delete': [('id', )],
        'read': [('id', )],
        'undelete': [('id', )],
        'update': [('id', )],
    },
    'prospect': {
        'query': [()],
        'assign': [('email', ), ('id', )],
        'batchCreate': [('prospects', )],
        'batchUpdate': [('prospects', )],
        'batchUpsert': [('prospects', )],
        'create': [('email', )],
        'delete': [('email', ), ('id', )],
        'read': [('email', ), ('id', )],
        'unassign': [('email', ), ('id', )],
        'update': [('email', ), ('id', )],
        'upsert': [('email', ), ()],
    },
    'prospectAccount': {
        'assign': [('id', 'user_id')],
        'create': [()],
        'describe': [()],
        'query': [()],
        'read': [('id', )],
        'update': [('id', )],
    },
    'tag': {
        'query': [()],
        'read': [('id', )]
    },
    'tagObject': {
        'query': [()],
        'read': [('id', )]
    },
    'user': {
        'query': [()],
        'read': [('email', ), ('id', )]
    },
    'visit': {
        'query': [('visitor_ids', 'prospect_ids)')],
        'read': [('id', )]
    },
    'visitor': {
        'assign': [('id', )],
        'query': [()],
        'read': [('id', )]
    },
    'visitorActivity': {
        'query': [('search_criteria', 'result_set_criteria')],
        'read': [('id', )],
    },
}

RESOURCE_PARAMETER_TYPE_TESTS = {
    'ids': lambda x, y:
        x == 'id' or x.endswith('_id') and
        isinstance(y, six.integer_types),
    'emails': lambda x, y:
        x == 'email' or x.endswith('_email') and
        isinstance(y, six.string_types),
    'lists': lambda x, y:
        x == x.endswith('[]') and isinstance(y, collections.Sequence) and
        not isinstance(y, six.string_types),
}
