import boto3
import zipfile
import StringIO
import mimetypes
import boto3

from botocore.client import Config




def lambda_handler(event, context):
    # TODO implement
    
    try: 

        sns = boto3.resource('sns')
        topic = sns.Topic('arn:aws:sns:us-east-1:613530786381:DeployPortfolioTopic')
    
        s3 = boto3.resource('s3', config= Config(signature_version= 's3v4'))
    
        portfolio_bucket =  s3.Bucket('portfolio.gauravtiwari.ga')
        build_bucket = s3.Bucket('portfoliobuild.gauravtiwari.ga')
        
        
        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)
        
        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs= {'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL = 'public-read')
        
    
        print 'Job Done!'
        topic.publish(Subject="Portfolio", Message="Portfolio Deployed Successfully.")
    except:
        topic.publish(Subject="Portfolio", Message="Portfolio not Deployed Successfully.")
        raise

        

