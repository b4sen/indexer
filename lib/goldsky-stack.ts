import * as cdk from 'aws-cdk-lib';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as lambda from 'aws-cdk-lib/aws-lambda-nodejs';
import { Construct } from 'constructs';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';

export class GoldskyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const handler = new lambda.NodejsFunction(this, 'goldsky', {
      entry: 'lib/first-lambda.ts', // path to your code
      handler: 'handler',
    });

    const periodicLambda = new lambda.NodejsFunction(this, 'periodic-lambda', {
      entry: 'lib/periodic-lambda.ts',
      handler: 'handler'
    })
    //const url = handler.addFunctionUrl({
    //  authType: FunctionUrlAuthType.NONE
    // });
    //new cdk.CfnOutput(this, 'url', {
    //  value: url.url
    //});

    const rule = new events.Rule(this, 'ScheduleRule', {
      schedule: events.Schedule.rate(cdk.Duration.minutes(1)),
    });

    rule.addTarget(new targets.LambdaFunction(periodicLambda));

    const dbSecret = secretsmanager.Secret.fromSecretNameV2(this, 'dbSecret', 'goldsky-pg-url');

    // Grant your Lambda access
    dbSecret.grantRead(periodicLambda);

    const goldsky_api = new apigateway.RestApi(this, 'api', {
      defaultCorsPreflightOptions: {
        allowOrigins: ['*'],
        allowMethods: ['ANY'],
      }
    })

    new cdk.CfnOutput(this, 'apiUrl', { value: goldsky_api.url });

    const trigger = goldsky_api.root.addResource('trigger')

    trigger.addMethod(
      'POST',
      new apigateway.LambdaIntegration(handler, { proxy: true })
    )
    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'GoldskyQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
  }
}
