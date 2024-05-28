## Invoke function synchronously

### aws lambda invoke --function-name mytestfunction --payload BASE64-ENCODED-STRING response.json

aws lambda invoke --function-name testFunction-20240527 --payload ewogICJrZXkxIjogImxhcnJ5IiwKICAia2V5MiI6ICJjdXJseSIsCiAgImtleTMiOiAibW9lIgp9 response.json

aws lambda invoke --function-name testFunction-20240527 outfile.json

## Invoke function asynchronously

### aws lambda invoke --function-name mytestfunction --invocation-type Event --payload BASE64-ENCODED-STRING response.json 

aws lambda invoke --function-name testFunction-20240527 --invocation-type Event --payload ewogICJrZXkxIjogImxhcnJ5IiwKICAia2V5MiI6ICJjdXJseSIsCiAgImtleTMiOiAibW9lIgp9 response2.json