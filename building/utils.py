def get_or_404(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def convert_string_to_display(string):
    words = string.split('_')
    capitalized_words = [word.capitalize() for word in words]
    display_string = ' '.join(capitalized_words)
    return display_string
