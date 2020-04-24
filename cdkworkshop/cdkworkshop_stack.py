from aws_cdk import (
    core,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)

from hitcounter import HitCounter

class CdkworkshopStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            function_name='dyna-hello',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda'),
            handler='hello.handler',
        )

        # Add a hit counter to stack
        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstream=my_lambda,
        )

        apigw.LambdaRestApi(
            self, 'Endpoint',

            # change the API Gateway handler to hello_with_counter.handler
            # instead of my_lambda            
            handler=hello_with_counter.handler,
        )