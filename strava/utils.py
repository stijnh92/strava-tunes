def get_authorization_url():
    client_id = '47072'
    scope = 'read,activity:read'
    redirect_uri = 'http://localhost:8000/strava/callback'
    base_url = 'http://www.strava.com/oauth/authorize'
    authorization_url = f'{base_url}?client_id={client_id}&response_type=code' \
                        f'&redirect_uri={redirect_uri}&approval_prompt=force&scope={scope}'

    return authorization_url
