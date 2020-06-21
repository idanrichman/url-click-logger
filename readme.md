# URL-Redirector in AWS Lambda
### Add clicks tracking capabilities to any url link

## Deploy:
* edit config.json file and enter your database info & credentials
* create a function.zip file containing all the files in the repo
* deploy the code to AWS Lambda with:
    aws lambda update-function-code --function-name <your_function_name> --zip-file fileb://function.zip
    make sure to already have a <your_function_name> ready in Lambda, as this command only updates existing function
* Make sure you have an API Gateway that is linked to your lambda function, so it can be exposed to the world

* Currently supports only MySQL Databases

## Database Preparation
```sql
CREATE TABLE `redirect_log` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `target_url` text,
  `user_id` varchar(8) DEFAULT NULL,
  `request_header` text,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=210 DEFAULT CHARSET=utf8
```

## Usage
Just add a query string with 'link' parameter to the API endpoint.
It should look something like this:
https://XXXXXXXX.execute-api.eu-west-1.amazonaws.com/default/myfunction?link=https://www.google.com

Now, anyone clicking on that link will be redirected to google's homepage and that click will be logged into your database

## Disclaimer
Use at your own risk.