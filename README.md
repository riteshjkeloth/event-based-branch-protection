# Event based branch protection
This is a simple solution that listens to Github repo's webhook events and creates branch protection rules along with an issue.

### Requires
- Flask
- python(2.7)
  - requests module
  - hmac module
  - os module
- ngrok

### Steps to use
1. Update `rules/branch-protection-rule.json` in the repo with appropriate values. Read related [GITHUB REST API](https://docs.github.com/en/rest/reference/branches#update-branch-protection) documentation for more info.
2. Start  ngrok on a port \
   `e.g. ngrok http 5678`
3. Note the 'Forwarding' url from ngrok \
    `e.g. Forwarding 'https://1234-567-89-87-76.ngrok.io' -> http://localhost:5678`
4. Create/Update [webhook](https://docs.github.com/en/developers/webhooks-and-events/webhooks/creating-webhooks) for your Github organization \
   1. Use Forwarding url from above step and configure it for 'Payload URL' 
   `https://1234-567-89-87-76.ngrok.io`
   2. Select Content type as `application/json`
   3. Configure secret
      1. Can be generated using `ruby -rsecurerandom -e 'puts SecureRandom.hex(20)`
   4. Set the secret as an environment variable in your local
      `e.g. export GITHUB_WEBHOOK_TOKEN=fa98s7df98asf98asf`
5. set 'FLASK_APP' environment variable\
    `export FLASK_APP=branch-protection.py`
6. set personal Github token as an environment variable 'PERSONAL_GH_TOKEN'
    `export PERSONAL_GH_TOKEN=sdf8as9f7a9sf`
7. Start the web server \
   `flask run --host localhost --port 5678`
8. Create a repository in the organization
   1. Webhook posts a REST request towards webserver started in above step
   2. This in turn creates a branch protection rule and issue for the repo created tagging @mention the user specified in the POST request JSON.