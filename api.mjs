import { defaultProvider } from "@aws-sdk/credential-provider-node";
import { HttpRequest } from "@aws-sdk/protocol-http";
import { SignatureV4 } from "@aws-sdk/signature-v4";
import { Sha256 } from "@aws-crypto/sha256-js";

async function invokeStream(
  urlStr,
  method = "POST",
  service = "lambda",
  region = "us-east-1"
) {
  const credentials = defaultProvider(); // credenciales default
  const url = new URL(urlStr);
  const body = JSON.stringify({});

  const request = new HttpRequest({
    method,
    protocol: url.protocol,
    hostname: url.hostname,
    path: url.pathname,
    headers: {
      host: url.hostname,
      "content-type": "application/json",
    },
    //body,
  });

  const signer = new SignatureV4({
    credentials,
    region,
    service,
    sha256: Sha256,
  });
  const signed = await signer.sign(request);

  const response = await fetch(
    `${signed.protocol}//${signed.hostname}${signed.path}`,
    {
      method,
      headers: signed.headers,
      // body,
    }
  );

  const reader = response.body?.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    let idx;
    while ((idx = buffer.indexOf("\n")) >= 0) {
      const line = buffer.slice(0, idx).trim();
      buffer = buffer.slice(idx + 1);
      if (line) {
        console.log(JSON.parse(line));
      }
    }
  }
}

const url = process.argv[2];
const method = process.argv[3] || "GET";

invokeStream(url, method);
