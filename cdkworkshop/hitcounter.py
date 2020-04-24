from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    core,
)

class HitCounter(core.Construct):

    @property
    def handler(self):
        return self._handler    

    def __init__(self, scope: core.Construct, id: str, downstream: _lambda.IFunction, **kwargs):
        super().__init__(scope, id, **kwargs)

        # define a DynamoDB table with 'path' as the partition key
        # **every DynamoDB table must have a single partition key
        table = ddb.Table(
            self, 'Hits',
            table_name="dyna-HitCountDB", 
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING}
        )

        # define a Lambda function
        self._handler = _lambda.Function(
            self, 'HitCountHandler',
            function_name="dyna-HitCount",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler='hitcount.handler',
            code=_lambda.Code.asset('lambda'),
    
            # wire the Lambda's environment variables
            # to the function_name and table_name of our resources
            environment={
                'DOWNSTREAM_FUNCTION_NAME': downstream.function_name,
                'HITS_TABLE_NAME': table.table_name,
            }
        )
        # allow lambda to read/write the DynamoDB table
        table.grant_read_write_data(self.handler)
        # Grant invoke permissions
        downstream.grant_invoke(self.handler)