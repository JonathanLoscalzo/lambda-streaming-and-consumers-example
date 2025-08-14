import boto3
import json
import httpx
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest


def sigv4_request(
    url,
    method="POST",
    body=None,
    service="lambda",
    region="us-east-1",
):
    session = boto3.Session()  # credenciales default
    credentials = session.get_credentials().get_frozen_credentials()

    req = AWSRequest(
        method=method,
        url=url,
        # data=body,
        headers={"content-type": "application/x-json-stream"},
        stream_output=True,
    )
    SigV4Auth(credentials, service, region).add_auth(req)
    req = req.prepare()

    with httpx.stream(
        method,
        req.url,
        headers=req.headers,
        data=req.body,
        timeout=None,
    ) as response:
        response.raise_for_status()
        for chunk in response.iter_lines():
            if chunk:
                print(json.loads(chunk))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True)
    args = parser.parse_args()

    sigv4_request(
        args.url,
        method="GET",
        body=json.dumps({}),
        region="us-east-1",
    )
