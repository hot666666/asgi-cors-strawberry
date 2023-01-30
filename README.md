# asgi-cors-strawberry

[![PyPI](https://img.shields.io/pypi/v/asgi-cors-strawberry.svg)](https://pypi.org/project/asgi-cors-strawberry/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/hot666666/asgi-cors-strawberry/blob/main/LICENSE)

ASGI middleware to apply CORS header especially for Strawberry GraphQL

## installation

```
 pip install asgi-cors-strawberry
```

## when to use

According to mdn [MDN - CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS), cross-origin requests are preflighted using OPTIONS method.
The response from preflight has Access-Control-Allow-Origin, Access-Control-Allow-Headers, etc.

Since [Strawberry GraphQL Consumer](https://strawberry.rocks/docs/integrations/channels#creating-the-consumers) is designed to handle only GET and POST methods, if you use general ASGI CORS middleware, you will get a 405 code as a response to preflight.

- Our middleware responds with Okay status in case of OPTIONS method
- Our middleware checks Access-Control-Allow-Origin from hosts, wildcards setting, _All hosts are allowed by default!_
- Our middleware adds Content-Type in Access-Control-Allow-Headers, because gql will be passed to the request

Additional settings are not yet supported.
It will be sorted out and updated soon.

## how to use

```python
# asgi.py


from asgi_cors_strawberry import CorsMiddleware
...

application = ProtocolTypeRouter(
    {
        "http": URLRouter(
            [
                re_path(r"^graphql", GraphQLHTTPConsumer.as_asgi(schema=schema)),
                re_path(r"^", get_asgi_application()),
            ]
        ),
        "websocket": URLRouter([
            re_path(r"^graphql", GraphQLWSConsumer.as_asgi(schema=schema))
        ])

    }
)


application = CorsMiddleware(application)

```

The example above is an ASGI application using [Strawberry-GraphQL[Channels]](https://strawberry.rocks/docs/integrations/channels)

## left to do

- [ ] initialize - allow_all, hosts, host_wildcards, access_control_allow_headers
- [ ] testcase
