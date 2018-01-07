
import os


# noinspection PyUnusedLocal
def export(request):
    return {
        'env': os.getenv('NODE_ENV', 'development'),

        # Google Settings
        'google_api_key': os.getenv('GOOGLE_API_KEY'),
        'ga_tracking_id': os.getenv('GA_TRACKING_ID'),
    }
