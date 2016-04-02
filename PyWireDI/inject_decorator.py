def inject(method):
    def forward_method(*args, **kwargs):
        return method(*args, **kwargs)

    return forward_method
