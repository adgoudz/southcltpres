
import os


# noinspection PyUnusedLocal
def export(request):
    return {
        'env': os.getenv('NODE_ENV', 'development')
    }
