from .models import createTeam

def custom_data(request, team_captain_username):
    # Filter the createTeam model based on the team captain's username
    sender_team = createTeam.objects.filter(teamcaptain__username=request.user.username)
    recipient_team = createTeam.objects.filter(teamcaptain__username=team_captain_username)

    # Define the data you want to pass to all templates
    data = {
        'sender_team': sender_team,
        'recipient_team': recipient_team,
        # Add more variables as needed
    }
    print(data)
    return data
