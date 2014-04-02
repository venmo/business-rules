def fn_name_to_pretty_description(name):
    return ' '.join([w.title() for w in name.split('_')])
