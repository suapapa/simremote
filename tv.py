import pywebostv.connection as tv_conn
import pywebostv.discovery as tv_disc
import file_store


def connect():
    store = file_store.load_store()
    try:
        tv_host = store['host']
        client = tv_conn.WebOSClient(tv_host, secure=False)
        client.connect()
    except:
        hosts = tv_disc.discover("urn:schemas-upnp-org:device:MediaRenderer:1",
                        keyword="LG", hosts=True, retries=3)
        if len(hosts) == 0:
            raise Exception("No TV found!")

        tv_host = hosts[0]
        client = tv_conn.WebOSClient(tv_host, secure=False)
        client.connect()
        store['host'] = tv_host

    for status in client.register(store):
        if status == tv_conn.WebOSClient.PROMPTED:
            print("Please accept the connect on the TV!")
        elif status == tv_conn.WebOSClient.REGISTERED:
            print("Registration successful!")

    file_store.save_store(store)
    return client