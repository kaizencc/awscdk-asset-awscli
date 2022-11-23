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

# sed Dockerfile with new version
new = subprocess.Popen(('sed', '-i', '', '-e', "/amazon\\/aws-cli:/s/:.*/:%s/"%(latest), 'layer/Dockerfile'), stdout=subprocess.PIPE)