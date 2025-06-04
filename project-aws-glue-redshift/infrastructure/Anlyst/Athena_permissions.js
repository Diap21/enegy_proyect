{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AthenaPermissions",
            "Effect": "Allow",
            "Action": [
                "athena:*"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Sid": "S3PermissionsforAthenaQueryResultstore",
            "Effect": "Allow",
            "Action": [
                "s3:*"
            ],
            "Resource": [
                "arn:aws:s3:::<athena_logs_bucket>",
                "arn:aws:s3:::<athena_logs_bucket>/*"
            ]
        }
    ]
}
