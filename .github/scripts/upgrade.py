import subprocess
import semver

data = subprocess.Popen(('curl', '-L', '-s', 'https://registry.hub.docker.com/v2/repositories/amazon/aws-cli/tags?page_size=100'), stdout=subprocess.PIPE)
tagbytes = subprocess.check_output(('jq', '.results[].name'), stdin=data.stdout)
data.wait()
tags = tagbytes.decode("utf-8").replace('"','').split('\n')
# can we trust tags come back in version order? probably
latest = ''
for tag in tags:
  try:
    semver.VersionInfo.parse(tag)
    print(tag)
    latest = tag
    break
  except ValueError:
    continue

docker = open('layer/Dockerfile')
for i, line in enumerate(docker):
  if i==2:
    version = line.strip('\n').split(':')[1]
print(version)

if semver.compare(latest, version) == 1:
  print('there is a newer version')


# sed Dockerfile with new version
# 