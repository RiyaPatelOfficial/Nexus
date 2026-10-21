def handle_uploaded_file(f):
    with open('client/static/client_assets/img/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)