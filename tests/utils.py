import json


def request_callback(request):
    headers = {'Content-Type': 'application/json'}
    uris = {
        'edu.upenn.sims.mysim.myscope.sometopic': lambda x, y: {'id': 1234},
        'edu.upenn.sims.mysim.myscope.add': lambda x, y: x + y,
    }
    payload = json.loads(request.body)
    try:
        if 'topic' in payload:
            method = uris[payload['topic']]

        elif 'procedure' in payload:
            method = uris[payload['procedure']]
        else:
            return (500, headers, "{}")
    except KeyError:
        return (400, headers, '{"error": "uri not found.')

    resp_body = method(*payload.get('args', []), **payload.get('kwargs', {}))
    return (200, headers, json.dumps(resp_body))
