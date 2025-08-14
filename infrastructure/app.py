#!/usr/bin/env python3
import aws_cdk as cdk

from stacks.lambda_stack import LambdaStreamingAndConsumersExampleStack


app = cdk.App()
LambdaStreamingAndConsumersExampleStack(
    app,
    "LambdaStreamingAndConsumersExampleStack",
)

app.synth()
