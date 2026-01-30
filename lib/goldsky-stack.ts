import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda-nodejs';
import { Construct } from 'constructs';
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class GoldskyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    new lambda.NodejsFunction(this, 'goldsky', {
      entry: 'lib/first-lambda.ts', // path to your code
      handler: 'handler',
    });
    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'GoldskyQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
  }
}
