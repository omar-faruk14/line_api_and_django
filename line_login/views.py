from django.shortcuts import render, redirect
from django.http import HttpResponse

import requests

def login(request):
    # Logic to pass the channel_id to the template
    channel_id = "2000133795"  # Replace with your actual channel ID
    return render(request, 'line_login/login.html', {'channel_id': channel_id})

def line_login_callback(request):
    if 'code' in request.GET:
        # Get the authorization code from the callback URL
        authorization_code = request.GET.get('code')

        # Exchange the authorization code for an access token
        access_token_url = 'https://api.line.me/oauth2/v2.1/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': 'http://127.0.0.1:8000/line-login/',  # Replace with your actual redirect URI
            'client_id': '2000133795',  # Replace with your actual channel ID
            'client_secret': '8b48b99c6e4e7aa063cdeca7097c4c7d',  # Replace with your actual channel secret
        }
        response = requests.post(access_token_url, headers=headers, data=data)
        if response.ok:
            access_token = response.json()['access_token']

            # Make an API call to get the user's profile using the access token
            profile_url = 'https://api.line.me/v2/profile'
            headers = {
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.get(profile_url, headers=headers)
            if response.ok:
                user_profile = response.json()
                user_name = user_profile['displayName']
                user_picture = user_profile['pictureUrl']
                user_id = user_profile['userId']

                # You can perform additional actions here, such as saving the user information to the database
                # or storing it in the session for future use
                return redirect('user_page', user_name=user_name, user_picture=user_picture, user_id=user_id)


    return HttpResponse("Invalid callback URL")

def user_page(request, user_name, user_picture, user_id):
    return render(request, 'line_login/user_details.html', {
        'user_name': user_name,
        'user_picture': user_picture,
        'user_id': user_id
    })
