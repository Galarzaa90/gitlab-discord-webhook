# GitLab Discord Webhook
A middleman between GitLab and Discord webhooks to show better formatted messages.

## Use instructions
In order to use this, you must have a public IP address, with port 7400 open.

- Install modules in `requirements.txt` (python 3.9 or higher)
```shell
python -m pip install -r requirements.txt
```
- Create a `config.ini` file, you can copy and rename `config-example.ini`.
- Create a discord webhook on the desired channel, and paste the URL in the `webhook` entry.
- Execute `main.py`
- Go to the desired GitLab project and go to `Settings > Integrations`
- Paste the public address of your instance
- Select the desired Triggers.
- Click `Add Webhook`.

From now on, changes to the project will be posted on the specified channel.
You can have multiple projects pointing to the same `gitlab-discord-webhook` instance,
but every instance will only post messages through a single Discord webhook.

## Supported Triggers
- [X] Push events
- [ ] Tag push events
- [X] Comments
- [ ] Confidential Comments
- [X] Issues events
- [ ] Confidential Issues events
- [X] Merge request events
- [ ] Job events
- [ ] Pipeline events
- [ ] Wiki Page events


## References
- [GitLab Webhooks Documentation](https://docs.gitlab.com/ee/user/project/integrations/webhooks.html)
- [Discord Webhooks Documentation](https://support.discordapp.com/hc/articles/228383668-Usando-Webhooks)
