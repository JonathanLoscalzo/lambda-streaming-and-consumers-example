# Using AWS Lambda streaming with AWS IAM (SignatureV4 Authentication)

## Infrastructure

Go to [internal readme](./infrastructure/README.md)

```bash
cd infrastructure
AWS_PROFILE=<your profile> make deploy
npm i -g aws-cdk #or install cdk as you wish
```

## Run the code

**Run python**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
AWS_PROFILE=<your profile> python -m api --url <lambda url>/numbers
```

**Run js**

```bash
npm i
AWS_PROFILE=<your profile> node <lambda url>/numbers
```

## vscode debuggers

If you want vscode debuggers

```json
{
    "name": "API",
    "type": "debugpy",
    "request": "launch",
    "program": "api.py",
    "console": "integratedTerminal",
    "args": [
    "--url",
    "https:/your.lambda.url/numbers"
    ],
    "env": {
    "AWS_PROFILE": "your profile"
    }
},
{
    "name": "Launch Program",
    "program": "${workspaceFolder}/api.mjs",
    "request": "launch",
    "skipFiles": ["<node_internals>/**"],
    "type": "node",
    "args": [
    "https://your.lambda.url/numbers"
    ],
    "env": {
    "AWS_PROFILE": "your profile"
    }
}
```
