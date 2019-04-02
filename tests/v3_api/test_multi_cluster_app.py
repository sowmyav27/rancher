import pytest
from .common import *

namespace = {"namespace1": {"p_client": None, "ns": None,
                            "cluster": None, "project": None,
                            "project_id": None},
             "namespace2": {"p_client": None, "ns": None,
                            "cluster": None, "project": None,
                            "project_id": None}}

global_client = {"client": None}
answer_105version = {
    "values": {
        "defaultImage": "true",
        "externalDatabase.database": "",
        "externalDatabase.host": "",
        "externalDatabase.password": "",
        "externalDatabase.port": "3306",
        "externalDatabase.user": "",
        "image.repository": "bitnami/wordpress",
        "image.tag": "4.9.4",
        "ingress.enabled": "true",
        "ingress.hosts[0].name": "xip.io",
        "mariadb.enabled": "true",
        "mariadb.image.repository": "bitnami/mariadb",
        "mariadb.image.tag": "10.1.32",
        "mariadb.mariadbDatabase": "wordpress",
        "mariadb.mariadbPassword": "",
        "mariadb.mariadbUser": "wordpress",
        "mariadb.persistence.enabled": "false",
        "mariadb.persistence.existingClaim": "",
        "mariadb.persistence.size": "8Gi",
        "mariadb.persistence.storageClass": "",
        "nodePorts.http": "",
        "nodePorts.https": "",
        "persistence.enabled": "false",
        "persistence.existingClaim": "",
        "persistence.size": "10Gi",
        "persistence.storageClass": "",
        "serviceType": "NodePort",
        "wordpressEmail": "user@example.com",
        "wordpressPassword": "",
        "wordpressUsername": "user"
    }
}

answer = {
    "values": {
        "defaultImage": "true",
        "externalDatabase.database": "",
        "externalDatabase.host": "",
        "externalDatabase.password": "",
        "externalDatabase.port": "3306",
        "externalDatabase.user": "",
        "image.repository": "bitnami/wordpress",
        "image.tag": "4.9.8-debian-9",
        "ingress.enabled": "true",
        "ingress.hosts[0].name": "xip.io",
        "mariadb.db.name": "wordpress",
        "mariadb.db.user": "wordpress",
        "mariadb.enabled": "true",
        "mariadb.image.repository": "bitnami/mariadb",
        "mariadb.image.tag": "10.1.35-debian-9",
        "mariadb.mariadbPassword": "",
        "mariadb.master.persistence.enabled": "false",
        "mariadb.master.persistence.existingClaim": "",
        "mariadb.master.persistence.size": "8Gi",
        "mariadb.master.persistence.storageClass": "",
        "nodePorts.http": "",
        "nodePorts.https": "",
        "persistence.enabled": "false",
        "persistence.size": "10Gi",
        "persistence.storageClass": "",
        "serviceType": "NodePort",
        "wordpressEmail": "user@example.com",
        "wordpressPassword": "",
        "wordpressUsername": "user"
    }
}
ROLES = ["project-member"]
# TEMP_VER = "cattle-global-data:library-wordpress-1.0.5"
TEMP_VER = "cattle-global-data:library-wordpress-2.1.10"


def test_create_multi_cluster_app():
    targets = [{"projectId": namespace["namespace1"]["project_id"],
                "type": "target"},
               {"projectId": namespace["namespace2"]["project_id"],
                "type": "target"}]
    client = global_client["client"]
    p_client1 = namespace["namespace1"]["p_client"]
    p_client2 = namespace["namespace2"]["p_client"]
    multiClusterApp = client.create_multiClusterApp(templateVersionId=TEMP_VER,
                                                    targets=targets,
                                                    roles=ROLES,
                                                    name=random_name(),
                                                    answers=[answer])
    multiClusterApp = wait_for_mcapp_to_active(client, multiClusterApp)
    app_id1 = multiClusterApp.targets[0].appId
    app_id2 = multiClusterApp.targets[1].appId
    id1 = 0
    id2 = 0
    if app_id1 is None:
        id1 = 1
        print("app_id1 is None")
    assert id1 == 1
    if app_id2 is None:
        id2 = 1
        print("app_id2 is None")
    assert id2 == 1
    # verify if this app is available in the cluster/project
    multiClusterApp = validate_multi_cluster_app_cluster(app_id1,
                                                         app_id2,
                                                         p_client1,
                                                         p_client2,
                                                         multiClusterApp)


def test_edit_multi_cluster_app():
    client = global_client["client"]
    p_client1 = namespace["namespace1"]["p_client"]
    p_client2 = namespace["namespace2"]["p_client"]
    targets = [{"projectId": namespace["namespace1"]["project_id"],
                "type": "target"},
               {"projectId": namespace["namespace2"]["project_id"],
                "type": "target"}
               ]
    temp_ver = "cattle-global-data:library-wordpress-1.0.5"
    multiClusterApp = client.create_multiClusterApp(templateVersionId=temp_ver,
                                                    targets=targets,
                                                    roles=ROLES,
                                                    name=random_name(),
                                                    answers=[answer_105version]
                                                    )
    multiClusterApp = wait_for_mcapp_to_active(client, multiClusterApp)
    app_id1 = multiClusterApp.targets[0].appId
    app_id2 = multiClusterApp.targets[1].appId
    id1 = 0
    id2 = 0
    if app_id1 is None:
        id1 = 1
        print("app_id1 is None")
    assert id1 == 1
    if app_id2 is None:
        id2 = 1
        print("app_id2 is None")
    assert id2 == 1
    # verify if this app is available in the cluster/project
    validate_multi_cluster_app_cluster(app_id1, app_id2, p_client1, p_client2)
    print("created app")
    temp_ver = "cattle-global-data:library-wordpress-2.1.10"
    multiClusterApp = client.update(multiClusterApp, uuid=multiClusterApp.uuid,
                                    templateVersionId=temp_ver,
                                    roles=ROLES,
                                    answers=[answer])
    multiClusterApp = wait_for_mcapp_to_active(client, multiClusterApp)
    app_id1 = multiClusterApp.targets[0].appId
    app_id2 = multiClusterApp.targets[1].appId
    id1 = 0
    id2 = 0
    if app_id1 is None:
        id1 = 1
        print("app_id1 is None")
    assert id1 == 1
    if app_id2 is None:
        id2 = 1
        print("app_id2 is None")
    assert id2 == 1
    # verify if this app is available in the cluster/project
    validate_multi_cluster_app_cluster(app_id1, app_id2, p_client1, p_client2)


@pytest.fixture(scope='module', autouse="True")
def create_project_client(request):
    client, clusters = get_admin_client_and_cluster_mcapp()
    cluster1 = clusters[0]
    cluster2 = clusters[1]
    p1, ns1 = create_project_and_ns(ADMIN_TOKEN, cluster1, "testmcapp1")
    p_client1 = get_project_client_for_token(p1, ADMIN_TOKEN)
    p2, ns2 = create_project_and_ns(ADMIN_TOKEN, cluster2, "testmcapp2")
    p_client2 = get_project_client_for_token(p2, ADMIN_TOKEN)
    namespace["namespace1"]["project_id"] = p1.id
    namespace["namespace1"]["p_client"] = p_client1
    namespace["namespace1"]["ns"] = ns1
    namespace["namespace1"]["cluster"] = cluster1
    namespace["namespace1"]["project"] = p1
    namespace["namespace2"]["project_id"] = p2.id
    namespace["namespace2"]["p_client"] = p_client2
    namespace["namespace2"]["ns"] = ns2
    namespace["namespace2"]["cluster"] = cluster2
    namespace["namespace2"]["project"] = p2
    global_client["client"] = client

    def fin():
        client1 = get_admin_client()
        client1.delete(namespace["namespace1"]["project_id"])
        client1.delete(namespace["namespace2"]["project_id"])
    request.addfinalizer(fin)