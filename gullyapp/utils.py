import re
import math
from django.db.models import F
from .models import createTeam

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance

def find_nearby_teams(current_team, max_distance_km):
    teams = createTeam.objects.exclude(id=current_team.id)  
    nearby_teams = []

    
    current_lat, current_lon = map(float, re.findall(r'-?\d+\.\d+', current_team.location))

    for team in teams:
       
        team_lat, team_lon = map(float, re.findall(r'-?\d+\.\d+', team.location))
        print(f'Team: {team.name}, Distance: {haversine(current_lat, current_lon, team_lat, team_lon)} km')

        
        distance = haversine(current_lat, current_lon, team_lat, team_lon)

        
        if distance <= max_distance_km:
            team.distance = distance
            nearby_teams.append(team)

    
    nearby_teams = sorted(nearby_teams, key=lambda x: x.distance)

    return nearby_teams

from django.shortcuts import get_object_or_404
from .models import createTeam

def get_current_team(request):
    
    if request.user.is_authenticated:
        
        current_team = get_object_or_404(createTeam, teamcaptain=request.user)
        return current_team
    else:
        
        return None
