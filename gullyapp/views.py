from django.shortcuts import render,redirect
from django.http import request,HttpResponseRedirect,HttpResponse
from .models import createTeam
from . models import Carousel
from . models import Category
from . models import Userprofile
from .models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import F
from .models import createTeam,ShownTeamsHistory,MatchRequest
from .utils import get_current_team, find_nearby_teams

def home(request):
    print(type(id))
    return render(request,'home.html')

def index(request):
    
    return render(request, 'navigation.html' )

def main(request):
    data = Carousel.objects.all()
    context={'data':data}
    return render(request, 'index.html',context)

def adminLogin(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                msg = "User login successfully"
                return redirect('admindashboard')
            else:
                msg = "Invalid Credentials"
        except:
            msg = "Invalid Credentials"
    dic = {'msg': msg}
    return render(request, 'admin_login.html', dic)

def adminHome(request):
    return render(request, 'admin_base.html')

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin, login_url='admin_login')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def add_category(request):
    if request.method == "POST":
        name=request.POST.get('name')
        Category.objects.create(name=name)
        messages.info(request,"Category Added successfully")
        
    return render(request,'add_category.html')

def view_category(request):
    category=Category.objects.all()
    context={'category':category}
    return render(request,'view_category.html',context)

def edit_category(request, pid):
    category = Category.objects.get(id = pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        msg = "Category Updated"
        return redirect('view-category')
    return render(request, 'edit_category.html', locals())
    
    

def delete_category(request,pid):
    category=Category.objects.get(id=pid)
    category.delete()
    return redirect('view-category')



from django.contrib.auth.decorators import login_required
@login_required(login_url='userlogin')
def create_team(request):
    categories = Category.objects.all()  
    if createTeam.objects.filter(teamcaptain=request.user).exists():
        messages.error(request, "You have already created a team.")
        return render(request, 'createteam.html', {'categories': categories})

    if request.method == "POST":
        name = request.POST['name']
        cat_id = request.POST['category']
        contact = request.POST['contact']
        noofplayers = request.POST['noofplayers']
        image = request.FILES.get('image')  
        location = request.POST['location']

        try:
            cat_obj = Category.objects.get(id=cat_id)

            team_instance = createTeam(  
                name=name,
                contact=contact,
                category=cat_obj,
                noofplayers=noofplayers,
                image=image,
                location=location,
                teamcaptain=request.user  
            )

            team_instance.save()
            team_id = team_instance.id
            response = HttpResponseRedirect('/')
            response.set_cookie('tid',team_id)
            messages.success(request, "Team Created Successfully.")
            return response
            

 

        except Category.DoesNotExist:
            messages.error(request, f"Category with ID '{cat_id}' does not exist.")
            
    return render(request, 'createteam.html', {'categories': categories})

@login_required(login_url='userlogin')



def view_team(request, pid):
    if pid == 0:
        team = createTeam.objects.all()
    else:
        try:
            category = Category.objects.get(id=pid)
            team = createTeam.objects.filter(category=category)
        except Category.DoesNotExist:
            
            team = createTeam.objects.none()
            error_message = "The requested category does not exist."
            return render(request, "error_page.html", {'error_message': error_message})
    
    allcategory = Category.objects.all()
    return render(request, "jointeamview.html", {'team': team, 'allcategory': allcategory})


        
    
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import createTeam

from django.contrib import messages

def join_team(request, team_id):
    team = get_object_or_404(createTeam, id=team_id)

    if request.user.createTeam_set.exists():
        
        messages.warning(request, "You are already a member of a team.")
    else:
        
        messages.success(request, f"You have joined the team '{team.name}'!")

    # Redirect the user to the team page
    return render(request,'jointeamview.html')






from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Userprofile

from django.contrib.auth.models import User
from django.db import IntegrityError

def registration(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['mobile']
        image = request.FILES['image']

        
        if User.objects.filter(username=email).exists():
            messages.error(request, "A user with this email already exists.")
        else:
            
            user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password)
            Userprofile.objects.create(user=user, mobile=mobile, address=address, image=image)
            messages.success(request, "Registration successful")
            return redirect('userlogin')

    return render(request, 'registration.html', locals())



def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "User login successfully")
            
            team = list(Userprofile.objects.filter(user=user).values())
            print(team)
            
            if team:  
                id = team[0]['team_id']  
                print(id)
                response = HttpResponseRedirect("/")
                response.set_cookie('tid', id)
                return response
            else:
                messages.warning(request, "User has no associated team")  
        else:
            messages.error(request, "Invalid Credentials")
    return render(request, 'userlogin.html', locals())


def profile(request):
    data = Userprofile.objects.get(user=request.user)
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['mobile']
        try:
            image = request.FILES['image']
            data.image = image
            data.save()
        except MultiValueDictKeyError:
            pass
        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname)
        Userprofile .objects.filter(id=data.id).update(mobile=mobile, address=address)
        messages.success(request, "Profile updated")
        return redirect('profile')
    return render(request, 'profile.html', locals())

from django.shortcuts import render

def profile_view(request):
    user_avatar_url = request.user.profile.avatar.url 
    return render(request, 'profile.html', {'user_avatar_url': user_avatar_url})

def logoutuser(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('home')
def adminlogout(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('home')

def change_password(request):
    if request.method == 'POST':
        o = request.POST.get('old')
        n = request.POST.get('new')
        c = request.POST.get('confirm')
        user=authenticate(username=request.user.username,password=o)
        if user:
            if n==c:
                user.set_password(n)
                user.save()
                messages.success(request,"password Changed")
                return redirect('home')
            else:
                messages.warning(request, "Password not matching")
                return redirect('change_password')
        else:
            messages.error(request, "Invalid Password")
            return redirect('change_password')
    return render(request, 'change_password.html')


def team_detail(request, pid):
    team = createTeam.objects.get(id=pid)
    latest_product = createTeam.objects.filter().exclude(id=pid).order_by('-id')[:10]
    return render(request, "team_detail.html", locals())

@login_required(login_url='userlogin')
def search_opponents(request):
    current_team = get_current_team(request)

    if current_team:
        max_distance_km = 50  

        if request.method == 'POST':
            opponent_username = request.POST.get('opponent_username')

            
            opponent_team = get_object_or_404(createTeam, teamcaptain__username=opponent_username)

            
            match_request = MatchRequest.objects.create(team=current_team, opponent=opponent_team)
        
        current_team.shown_teams.clear()

        
        nearby_teams = find_nearby_teams(current_team, max_distance_km)

        
        for team in nearby_teams:
            ShownTeamsHistory.objects.create(team=current_team, shown_team=team)

        return render(request, 'opponents_search_results.html', {'nearby_teams': nearby_teams})

    else:
        
        return render(request, 'no_team.html')



from .models import MatchRequest, Notification

def request_for_match(request, opponent_id):
    current_team = get_current_team(request)
    opponent_team = createTeam.objects.get(id=opponent_id)

    
    match_request = MatchRequest.objects.create(team=current_team, opponent=opponent_team)

    
    opponent_captain = opponent_team.teamcaptain
    message = f"Match request received from {current_team.name}"
    Notification.objects.create(user=opponent_captain, message=message)

   
    return redirect('success_page')
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse







from django.http import HttpResponse, JsonResponse


def create_notification(request, user_id, message):
    user = get_object_or_404(User, id=user_id)
    Notification.objects.create(user=user, message=message)
    return HttpResponse("Notification created successfully!")
from django.shortcuts import render
from .models import Notification

def notification_panel(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notification_panel.html', {'notifications': notifications})

from django.utils.datastructures import MultiValueDictKeyError
from .models import Userprofile, createTeam, Notification

from django.urls import reverse
from django.utils.safestring import mark_safe

# views.py
import uuid


def challenge_opponent(request, team_captain_username):
    try:
        sender_team = get_object_or_404(createTeam, teamcaptain__username=request.user.username)
        recipient_team = get_object_or_404(createTeam, teamcaptain__username=team_captain_username)

        
        pid = sender_team.id  
        print("debug:rece id ",pid)

        

        message = mark_safe(
            f"{sender_team.name} wants to play a match with you."
            f"{sender_team.id}."
            
            
        )
        Notification.objects.create(
            user=recipient_team.teamcaptain,
            message=message,
            challenge_id=pid,  
        )

        messages.success(request, 'Challenge sent successfully!')
        return redirect('search_opponents')  

    except createTeam.DoesNotExist:
        messages.error(request, "Your team does not exist.")
        return redirect('some_redirect_view')
    
def accept_opponent(request, team_captain_username):
    try:
        sender_team = get_object_or_404(createTeam,teamcaptain__username=team_captain_username)
        recipient_team = get_object_or_404(createTeam, teamcaptain__username=request.user.username )

        
        pid = recipient_team.id  
        print(sender_team.id)

        

        message = mark_safe(
            f"{recipient_team.name} Accepted your request.."
            f"{recipient_team.id}"
            
           
            
            
        )
        Notification.objects.create(
            user=sender_team.teamcaptain,
            message=message,
            challenge_id=pid,  
        )

        messages.success(request, 'Challenge Accepted!')
        return redirect('/')  

    except createTeam.DoesNotExist:
        messages.error(request, "Your team does not exist.")
        return redirect('some_redirect_view')
def rejectopponent(request, team_captain_username):
    try:
        recipient_team= get_object_or_404(createTeam,teamcaptain__username=team_captain_username)
        sender_team = get_object_or_404(createTeam, teamcaptain__username=request.user.username )
        pid = recipient_team.id
        print(sender_team)
        print(recipient_team)

    
        message = mark_safe(
            f"{sender_team.name} Rejected your request."
            
        )
        print(message)
        Notification.objects.create(
            user=sender_team.teamcaptain,
            message=message,
            challenge_id=pid,  
        )
        

        messages.success(request, 'Challenge Rejected!')
        return redirect('/') 
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('/')



'''def challenge_opponent(request, team_captain_username):
    try:
        sender_team = get_object_or_404(createTeam, teamcaptain__username=request.user.username)
    except createTeam.DoesNotExist:
        messages.error(request, "Your team does not exist.")
        return redirect('some_redirect_view')

    recipient_team = get_object_or_404(createTeam, teamcaptain__username=team_captain_username)

    sender_team_name = sender_team.name
    team_details_url = reverse('team_detail', args=[sender_team.id])

    # Generate a unique challenge ID using uuid4
    challenge_id = str(uuid.uuid4())

    message = f"{sender_team_name} wants to play a match with you.  "
    Notification.objects.create(
        user=recipient_team.teamcaptain,
        message=message,
        challenge_id=challenge_id
    )

    messages.success(request, 'Challenge sent successfully!')
    return redirect('search_opponents')'''












#notification functions start-------




def update_team_location(request, team_id):
    if request.method == 'POST':
        location_data = request.POST.get('location')  
        print('Received Location:', location_data)
        
        team = createTeam.objects.get(id=team_id)
        team.location = location_data
        team.save()

        return JsonResponse({'status': 'Team location updated successfully'})

    return JsonResponse({'status': 'Invalid request'}, status=400)

import re
import haversine 

    
def fetch_nearby_teams(request):
    if request.method == 'POST':
        
        location_data = request.POST.get('location')

        
        current_lat, current_lon = map(float, re.findall(r'-?\d+\.\d+', location_data))

        
        max_distance_km = 50
        nearby_teams = createTeam.objects.all()  
        nearby_teams = [
            {
                'name': team.name,
                'distance': haversine(current_lat, current_lon, *map(float, re.findall(r'-?\d+\.\d+', team.location))),
            }
            for team in nearby_teams
        ]
        nearby_teams = [team for team in nearby_teams if team['distance'] <= max_distance_km]

        
        nearby_teams = sorted(nearby_teams, key=lambda x: x['distance'])

        return JsonResponse(nearby_teams, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# views.py

from django.shortcuts import render

def challenged_opponents(request):
    
    opponents = [{'username': 'User1'}, {'username': 'User2'}]  

    return JsonResponse(opponents, safe=False)

def chat(request):
    return render(request, 'chat.html')


from django.shortcuts import render



def infocard(request, pid):
    team = createTeam.objects.get(id=pid)
    return render(request, "incocard.html", locals())
def acceptedcard(request, pid):
    team = createTeam.objects.get(id=pid)
    return render(request, "acceptedinfo.html", locals())

def get_requested_user_details(request):
    
    pid = request.GET.get('pid')  

    try:
        team = createTeam.objects.get(id=pid)
        user_details = {
            'pid': team.id,
            'name': team.name,
            'contact': team.contact,
           
        }
        return JsonResponse(user_details)
    except createTeam.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
def redirect_to_page(request):
        action = request.GET.get('action')
        notification_id = request.GET.get('notification_id')

    
        return redirect('your_target_url')


def admin_dashboard(request):
    
    category = Category.objects.filter()
    user=User.objects.filter()
    teams=createTeam.objects.filter()
    
    return render(request, 'admin_dashboard.html', locals())

def edit_teams(request, pid):
    team = createTeam.objects.get(id=pid)
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get('name', '')
        cat = request.POST.get('category', '')
        contact = request.POST.get('contact', '') 
        try:
            image = request.FILES['image']
            team.image = image
            team.save()
        except:
            pass
        if cat:
            catobj = Category.objects.get(id=cat)
            createTeam.objects.filter(id=pid).update(name=name, contact=contact, category=catobj)
            messages.success(request, "Team Updated")
            return redirect('adminview_team')
        else:
            messages.error(request, "Category not provided")
    return render(request, 'adminEditteams.html', locals())
def delete_team(request, pid):
    team = createTeam.objects.get(id=pid)
    team.delete()
    messages.success(request, "Product Deleted")
    return redirect('adminview_team')


def admin_change_password(request):
    if request.method == 'POST':
        o = request.POST.get('currentpassword')
        n = request.POST.get('newpassword')
        c = request.POST.get('confirmpassword')
        user = authenticate(username=request.user.username, password=o)
        if user:
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('main')
            else:
                messages.success(request, "Password not matching")
                return redirect('admin_change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('admin_change_password')
    return render(request, 'admin_change_password.html')

def manage_user(request):
    user = Userprofile.objects.all()
    return render(request, 'manage_user.html', locals()) 
def delete_user(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('manage_user') 


def add_team(request):
    if request.method == "POST":
        
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        teamcaptain_id = request.POST.get('teamcaptain')
        contact = request.POST.get('contact')
        image = request.FILES.get('image') 
        noofplayers = request.POST.get('noofplayers')
        location = request.POST.get('location')
        
        # Create the team
        team = createTeam.objects.create(
            category_id=category_id,
            name=name,
            teamcaptain_id=teamcaptain_id,
            contact=contact,
            image=image,
            noofplayers=noofplayers,
            location=location
        )
        
        
        messages.success(request, 'Team added successfully!')
        
       
        return redirect('admin_team_view')  
        
    return render(request, 'admin_add_team.html')
        
    
def adminview_team(request):
    team = createTeam.objects.all()
    return render(request, 'admin_team_view.html', locals())


    
    


@login_required
def joinclan(request, pid):
    team = createTeam.objects.get(id=pid)  
    teamid=team.id
    user_profile = Userprofile.objects.get(user=request.user)
    print(teamid)
    if user_profile.team:   
        return JsonResponse({'status': 'error', 'message': 'You  already a member of a team.'}, status=400)
    else:  
        user_profile.team = team
        user_profile.save()
        response= HttpResponseRedirect(f"/clan/{team.id}" )
        response.set_cookie('tid',pid)
        return response
        return redirect('clan', clan_id=team.id)

def clan(request, clan_id):
    if clan_id is None:
        return render(request, "error.html", {"error_message": "You are not part of any clan."})
    try:
        
        team = createTeam.objects.get(id=clan_id)
        
        print("Debug: id", team.id)
        
        context = {
            'team': team,
}
        
        print(context)
        return render(request, "clan_details.html", context)
    except createTeam.DoesNotExist:
        return render(request, "error.html", {"error_message": "Team not found."})
    


@login_required
def leave_team(request):
    user_profile = Userprofile.objects.get(user=request.user)
    if user_profile.team:
        user_profile.team = None
        user_profile.save()
        messages.success(request, "You have successfully left the team.")
        response = redirect('join_team', pid=0)
        response.delete_cookie('tid')
        return response
    else:
        return JsonResponse({'status': 'error', 'message': "You are not a member of any team."})





















        









        
