# event-based-branch-protection
This solution listens to Github repo webhook events and creates branch protection rules along with a issue.

- python
  - flask framework
  - requests
  - hmac
  - os
- ngrok

### Steps
1. Update `rules/branch-protection-rule.json` in the repo with appropriate values.
2. Start  ngrok on a port \
   `e.g. ngrok http 5678`
3. Take the 'Forwarding' url from ngrok \
    `e.g. Forwarding https://9352-213-127-51-92.ngrok.io -> http://localhost:5678`
4. Create [webhook](https://docs.github.com/en/developers/webhooks-and-events/webhooks/creating-webhooks) at organization level \
   1. use 'Payload URL' taken from ngrok in above step
   `e.g. https://9352-213-127-51-92.ngrok.io`
   2. Content type as `application/json`
   3. Configure secret
      1. Can be generated using `ruby -rsecurerandom -e 'puts SecureRandom.hex(20)`
   4. Set the secret as a environment variable
      `e.g. export GITHUB_WEBHOOK_TOKEN=fa98s7df98asf98asf`
5. Start the web server \
   `flask run --host localhost --port 5678`
6. Create a repository in the organization
   1. Webhook posts a REST request towards webserver
   2. This inturn creates a branch protection rule and issue for the repo. 