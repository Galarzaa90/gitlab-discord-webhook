# GitLab Discord Webhook
![PyPI - Version](https://img.shields.io/pypi/v/gitlab-discord-webhook)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gitlab-discord-webhook)
![PyPI - Downloads](https://img.shields.io/pypi/dm/gitlab-discord-webhook)


A middleman between GitLab and Discord webhooks to show better formatted messages.

## Use instructions
In order to use this, you must have a public IP address, with port 7400 open.

- Install modules in `requirements.txt` (python 3.10 or higher)
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

## Running from Docker
![Docker Image Version](https://img.shields.io/docker/v/galarzaa90/gitlab-discord-webhook)
![Docker Image Size](https://img.shields.io/docker/image-size/galarzaa90/gitlab-discord-webhook)
![Docker Pulls](https://img.shields.io/docker/pulls/galarzaa90/gitlab-discord-webhook)


The image can be pulled from [Docker Hub](https://hub.docker.com/r/galarzaa90/gitlab-discord-webhook):

```shell
docker pull galarzaa90/gitlab-discord-webhook:latest
```

Alternatively, the image can be built from the root of the project's source.

```shell
docker build . -t gitlab-discord-webhook:local
```

To run the image:

```shell
docker run -p 7400:7400 --rm -ti gitlab-discord-webhook:local
```


## References
- [GitLab Webhooks Documentation](https://docs.gitlab.com/ee/user/project/integrations/webhooks.html)
- [Discord Webhooks Documentation](https://support.discordapp.com/hc/articles/228383668-Usando-Webhooks)
