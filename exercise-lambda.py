import boto3
import cfnresponse
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

def lambda_handler(event, context):
    def get_parameters(item):
        client = boto3.client('ssm')
        response_value = client.get_parameter(
            Name=item,
            WithDecryption=True|False
        )
        return response_value

    try:
        name = get_parameters('Name')['Parameter'].get('Value', None)
        user_name = get_parameters('Value')['Parameter'].get('Value', None)

        with open("testfile.txt", "w") as out:
            out.write(name + '\n')
            out.write(user_name + '\n')

        # Method 2: Client.put_object()
        client = boto3.client('s3')
        responseData = client.put_object(Body="testfile.txt", Bucket='nehagundkal-testbkt', Key='file-to-s3.txt')
        cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)
    except:
        cfnresponse.send(event, context, cfnresponse.FAILED, "FAILED Event")
        log.exception("Lambda execution has failed!")




