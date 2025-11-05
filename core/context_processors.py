"""
Context processors for core app
"""


def site_context(request):
    """Add site-wide context variables"""
    return {
        'site_name': 'Kitchenware Marketplace',
        'site_version': '1.0',
    }
