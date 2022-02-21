import hashlib
import hmac
import os
import requests
import json

from flask import Flask, request

app = Flask(__name__)


@app.route("/listener/repo-event", methods=['POST'])
def repo_event_listener():
    if verify_signature(request) != "OK":
        return '{"message":"X-Hub-Signature-256 does not match!!"}', 400
    request_body = request.json
    if request_body['action'] == "created":
        url = request_body['repository']['url']
        personal_token = os.environ.get("PERSONAL_GH_TOKEN")
        headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': 'token ' + personal_token}
        user = request_body['sender']['login']
        branch = "main"
        if set_branch_protection(url, headers, branch) != "OK":
            return '{"message":"Exception while setting branch protection !"}', 500
        if create_issue(url, headers, user) != "OK":
            return '{"message": "Branch protection rule created, however failed while creating issue !"}', 500
    return "OK"


def set_branch_protection(url, headers, branch):
    path = './rules/branch-protection-rule.json'
    url = url + "/branches/" + branch + "/protection"
    r = requests.put(url, data=open(path, 'rb'), headers=headers)
    if r.status_code == 200:
        print ("Branch protection rule created(updates it if already existing) !")
    return "OK"


def create_issue(url, headers, user):
    issue_json = '{"title":"Branch protection rule created/updated", "body":"@' + user + ' A new branch protection rule was added(updates it if already existing) in this repo"}'
    url = url + "/issues"
    r = requests.post(url, issue_json, headers=headers)
    if r.status_code == 201:
        print ("Issue created !")
    return "OK"


def verify_signature(req):
    signature = req.headers['X-Hub-Signature-256']
    local_key = os.environ.get("GITHUB_WEBHOOK_TOKEN")
    # local_key = os.environ.get("GITHUB_WEBHOOK_TOKEN_INVALID") # for testing
    hashname, hashval = signature.split("=")
    digest = hmac.new(
        key=local_key,
        msg=req.get_data(),
        digestmod=hashlib.sha256
    ).hexdigest()
    if hmac.compare_digest(digest.encode(), hashval.encode()):
        return "OK"

