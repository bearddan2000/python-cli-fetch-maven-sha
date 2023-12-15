import urllib.request
import logging
logging.basicConfig(level=logging.INFO)

INSECURE = "http://insecure.repo1/maven.org/maven2"
SECURE = 'https://repo1.maven.org/maven2'

def fetch(url):
    # logging.info(url)
    with urllib.request.urlopen(url) as response:
        html = response.read()
        html = bytes(html)
    hash = str(html, encoding='ascii')
    # logging.info(hash)
    return hash

def divide_group(group_id):
    return "/".join(group_id.split('.'))

def bin_hash(group_id, artifact_id, version, scope):
    path = divide_group(group_id)
    url = f'{SECURE}/{path}/{artifact_id}/{version}/{artifact_id}-{version}.{scope}.sha1'
    return fetch(url)

def src_hash(group_id, artifact_id, version, scope):
    path = divide_group(group_id)
    if 'pom' in scope:
        url = f'{SECURE}/{path}/{artifact_id}/{version}/{artifact_id}-{version}.{scope}.sha1'
    else:
        url = f'{SECURE}/{path}/{artifact_id}/{version}/{artifact_id}-{version}-sources.{scope}.sha1'
    trimmed = fetch(url)
    # arr = trimmed.split()
    return trimmed

def maven_jar(group_id, artifact_id, version, scope='jar'):
    return {
       "group": group_id, 
       "artifact": artifact_id, 
       "version": version,
       "scope": scope,
       "bin_sha1": bin_hash(group_id, artifact_id, version, scope),
       "src_sha1": src_hash(group_id, artifact_id, version, scope)
    }

def print_cmd(d: dict):
    result = 'maven_jar('
    result += f"'{d['group']}',"
    result += f"'{d['artifact']}',"
    result += f"'{d['version']}',"
    result += f"'{d['bin_sha1']}',"
    result += f"'{d['src_sha1']}')"
    return result

lst = [
    maven_jar("mysql","mysql-connector-java","8.0.22"),
    maven_jar("log4j","log4j","1.2.17"),
    maven_jar("org.hibernate","hibernate-core","5.3.7.Final"),
    maven_jar("jakarta.xml.bind","jakarta.xml.bind-api","2.3.3"),
    maven_jar("jakarta.persistence","jakarta.persistence-api","3.1.0"),
    maven_jar("org.glassfish.jaxb","jaxb-runtime","2.3.3")
]
for x in lst:
    print(print_cmd(x))