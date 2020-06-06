def get_authorization_url():
    base_url = 'http://www.last.fm/api/auth'
    api_key = '8263fd0740675f56f8d64dcac19c96d6'
    redirect_uri = 'http://localhost:8000/lastfm/callback'
    authorization_url = f'{base_url}/?api_key={api_key}&cb={redirect_uri}'

    return authorization_url
