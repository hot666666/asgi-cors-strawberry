import fnmatch

ACCESS_CONTROL_ALLOW_ORIGIN = b"Access-Control-Allow-Origin"
ACCESS_CONTROL_ALLOW_HEADERS = b"Access-Control-Allow-Headers"
CONTENT_TYPE = b"content-type"
DEFAULT_HEADERS = {ACCESS_CONTROL_ALLOW_ORIGIN, ACCESS_CONTROL_ALLOW_HEADERS, CONTENT_TYPE}


def cors_options(allow_all=True, hosts=[], host_wildcards=[], headers=["content-type"]):
    hosts = set(h.encode("utf8") if isinstance(h, str) else h for h in hosts)
    host_wildcards = [
        h.encode("utf8") if isinstance(h, str) else h for h in host_wildcards
    ]
    headers = [
        h.encode("utf8") if isinstance(h, str) else h for h in headers]

    return allow_all, hosts, host_wildcards, headers


class CorsMiddleware:
    def __init__(self, app, allow_all=True, hosts=[], host_wildcards=[], headers=["content-type"]):
        self.app = app
        self.allow_all, self.hosts, self.host_wildcards, self.access_control_allow_headers = cors_options(
            allow_all, hosts, host_wildcards, headers)

    async def __call__(self, scope, receive, send):
        async def _base_send(event):
            if event["type"] == "http.response.start":
                original_headers = event.get("headers") or []  # send_headers
                access_control_allow_origin = None
                if self.allow_all:
                    access_control_allow_origin = b"*"
                elif self.hosts or self.host_wildcards:
                    incoming_origin = dict(
                        scope.get("headers") or []).get(b"origin")
                    if incoming_origin:
                        matches_hosts = incoming_origin in self.hosts
                        matches_wildcards = any(
                            fnmatch.fnmatch(incoming_origin, host_wildcard)
                            for host_wildcard in self.host_wildcards
                        )
                        if matches_hosts or matches_wildcards:
                            access_control_allow_origin = incoming_origin

                if access_control_allow_origin:
                    # preflight in consumer -> status is 405
                    status = 200 if scope["method"] == "OPTIONS" else event["status"]
                    event = {
                        "type": "http.response.start",
                        "status": status,
                        "headers":
                            [h for h in original_headers if h[0] not in DEFAULT_HEADERS] +
                            [(ACCESS_CONTROL_ALLOW_ORIGIN, access_control_allow_origin),
                             (ACCESS_CONTROL_ALLOW_HEADERS, b", ".join(self.access_control_allow_headers))]
                    }
            await send(event)

        # _base_send -> send in ASGIHandler or AsyncConsumer
        return await self.app(scope, receive, _base_send)
