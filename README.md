# Twitter Hashtag scraper and lambda parser 

This project contains code for a pipeline which retrieves hashtags using the Twitter API and stores it in an Aurora database from the last 72 hours
Subsequently, the 'lambda' folder contains code for a Lambda function which reads data from the same database and gives back the top 10 hashtags in the Amsterdam Area

## Installation

### Application configuration
1. Spin up an EC2 instance using the AWS console or command line utility
2. Add all the files from the root directory in this repository
3. Configure the credentials.json with the appropriate values
4. Install pip, see: https://pip.pypa.io/en/stable/installing/
5. Run 'pip install' in the application folder

### Database configuration
1. Create a database on Aurora
2. Create a table called 'hashtagdata' with the fields 'combinedid' BIGINT, 'hashtag' STRING and 'created' DATETIME
3. Configure the Security Group in such a way to allow communication from the EC2 instance to the database by adding a rule to allow Aurora traffic (3306)

### Lambda configuration
1. Create a new lambda role with the AWSLambdaVPCAccessExecutionRole permission
2. Create a new Lambda function with this role and place it in the same VPC, Subnets and Security group as the database
3. Create a deployment package by running 'pip install pymysql -t .' in the lambda folder and zipping the folder contents
4. Upload the Deployment Package zip in the 'lambda' folder
5. Create a new API Gateway with default settings as input for the lambda function

Finally, start a scheduled cronjob on the ec2 instance for the application with atleast a 30 minute interval

## Usage

Run the application as follows
python scraper.py

Lambda usage is dynamic and results are gotten by doing a GET request to the API gateway URL

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

- Added functionality to retrieve tweets (21 Jul 2019)
- Added functionality to connect to an Aurora database (24 jul 2019)
- Added lambda functionality (25 jul 2019)

## Credits

Luuk Tersmette

## License
none
