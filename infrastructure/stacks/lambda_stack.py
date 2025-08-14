import platform
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    Duration,
    CfnOutput,
)
from constructs import Construct


class LambdaStreamingAndConsumersExampleStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        if "arm" in platform.machine():
            architecture = lambda_.Architecture.ARM_64
        else:
            architecture = lambda_.Architecture.X86_64

        fn = lambda_.DockerImageFunction(
            self,
            "NumberStreamer",
            architecture=architecture,
            code=lambda_.DockerImageCode.from_image_asset(
                "./api",
                cache_disabled=True,
                asset_name="number-streamer",
                display_name="number-streamer",
                file="Dockerfile",
                build_args={
                    # "--platform": "linux/amd64",
                    "--provenance": "false",
                },
            ),
            timeout=Duration.minutes(1),
        )

        fn_url = fn.add_function_url(
            auth_type=lambda_.FunctionUrlAuthType.AWS_IAM,
            invoke_mode=lambda_.InvokeMode.RESPONSE_STREAM,
        )
        fn.add_environment("LWA_INVOKE_MODE", "RESPONSE_STREAM")
        fn.add_environment("AWS_LWA_INVOKE_MODE", "RESPONSE_STREAM")
        fn.add_environment("AWS_LWA_ENABLE_RESPONSE_STREAMING", "true")
        fn.add_environment("PORT", "8080")

        CfnOutput(self, "LambdaURL", value=fn_url.url)
