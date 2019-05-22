# gitlab-webhook.py
A middleman between GitLab and Discord webhooks to show better formatted messages.

## Use instructions
In order to use this, you must have a public IP address, with port 7400 open.

- Install modules in `requirements.txt` (python 3.5.3 or higher)
```shell
python -m pip install -r requirements.txt
```
- Create a `config.ini` file, you can copy and rename `config-example.ini`.
- Create a discord webhook on the desired channel, and paste the URL in the `webhook` entry.
- Execute `main.py`
- Go to the desired GitLab project and go to `Settings > Integrations`
- Paste the following URL, replacing your IP or address:
```
http://0.0.0.0:7400/webhook/gitlab
```
- Select the desired Triggers.
- Click `Add Webhook`.

From now on, changes to the project will be posted on the specified channel.
You can have multiple projects pointing to the same `gitlab-webhook.py` instance,
but every instance will only post messages through a single discord webhook.

## Supported Triggers
- [X] Push events
- [ ] Tag push events
- [ ] Comments
- [ ] Confidential Comments
- [ ] Issues events
- [ ] Confidential Issues events
- [ ] Merge request events
- [ ] Job events
- [ ] Pipeline events
- [ ] Wiki Page events


## References
- [GitLab Webhooks Documentation](https://docs.gitlab.com/ee/user/project/integrations/webhooks.html)
- [Discord Webhooks Documentation](https://support.discordapp.com/hc/articles/228383668-Usando-Webhooks)