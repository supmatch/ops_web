import novaclient.client
from keystoneauth1.identity import v3
from keystoneauth1 import session
from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_keystone_creds():
    d = {}
    d['username'] = 'work'
    d['password'] = 'work'
    d['auth_url'] = 'http://controller1:5000/v3/'
    d['project_name'] = 'work'
    d['project_domain_id'] = 'default'
    d['user_domain_id'] = 'default'
    return d


def get_nova():
    kd_creds = get_keystone_creds()
    auth = v3.Password(**kd_creds)
    sess = session.Session(auth=auth)
    nova = novaclient.client.Client(2, session=sess)
    return nova


def check_name(request):
    name = request.GET['server_name']
    nova = get_nova()
    servers = nova.servers.list()
    for server in servers:
        if server.name == name:
            result = 'exist'
            return HttpResponse(result)
        else:
            result = 'success'
    return HttpResponse(result)


def create_server(request):
    if request.method == "POST":
        name = request.POST['server_name']
        image = request.POST['image']
        flavor = request.POST['flavor']
        nova = get_nova()
        results = nova.servers.create(name, image, flavor)
        return HttpResponse(results)
    else:
        return render(request, "appmanager/error.html")


def add_server_apply(request):
    nova = get_nova()
    flavors = nova.flavors.list()
    images = nova.glance.list()
    return render(request, 'appmanager/openstack.html', {'flavors': flavors, 'images': images})


def show_server_info(request):
    nova = get_nova()
    servers = nova.servers.list()
    for server in servers:
        try:
            server.image_name = nova.glance.find_image(server.image['id']).name
        except:
            server.image_name = 'None'
        server.ip = server.addresses['provider'][0]['addr']
        server.flavor_name = nova.flavors.get(server.flavor['id']).name
    paginator = Paginator(servers, 10)
    page = request.GET.get('page')
    try:
        server_infos = paginator.page(page)
    except PageNotAnInteger as e:
        server_infos = paginator.page(1)
    except EmptyPage as e:
        server_infos = paginator.page(paginator.num_pages)
    return render(request, 'appmanager/show_server_info.html', {"server_infos": server_infos})

