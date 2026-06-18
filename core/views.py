from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import UserProfile, OTPVerification, Survey, SurveyOption, Vote
from .forms import UserRegistrationForm, OTPVerificationForm, SurveyCreationForm, VotingForm
from .utils import create_and_send_otp, verify_otp

def welcome_view(request):
    return render(request, 'welcome.html')

def home_view(request):
    # If user is already verified, redirect to survey list
    if request.session.get("is_verified"):
        return redirect("survey_list")

    if request.method == "POST":
        # Check if this is OTP verification
        if 'otp_code' in request.POST:
            return verify_otp_view(request)
        
        # Otherwise, it's user registration
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data["full_name"]
            mobile_number = form.cleaned_data["mobile_number"]

            # Store user data in session
            request.session["user_data"] = {
                "full_name": full_name,
                "mobile_number": mobile_number,
            }

            # Generate and send OTP
            otp = create_and_send_otp(mobile_number)
            if otp:
                request.session["otp_sent"] = True
                messages.success(request, f"OTP sent to {mobile_number}")
                return redirect("home")  # Redirect to refresh the page and show OTP input
            else:
                messages.error(request, "Failed to send OTP. Please try again.")
    else:
        form = UserRegistrationForm()

    otp_form = OTPVerificationForm()
    return render(
        request,
        "home.html",
        {
            "form": form,
            "otp_form": otp_form,
            "otp_sent": request.session.get("otp_sent", False),
        },
    )

def verify_otp_view(request):
    if not request.session.get('user_data'):
        messages.error(request, 'Session expired. Please start again.')
        return redirect('home')
    
    if request.method == "POST":
        otp_form = OTPVerificationForm(request.POST)
        if otp_form.is_valid():
            otp_code = otp_form.cleaned_data['otp_code']
            user_data = request.session['user_data']
            mobile_number = user_data['mobile_number']
            
            success, message = verify_otp(mobile_number, otp_code)
            
            if success:
                # Create or get user
                full_name_parts = user_data['full_name'].split(' ', 1)
                first_name = full_name_parts[0]
                last_name = full_name_parts[1] if len(full_name_parts) > 1 else ''
                
                user, created = User.objects.get_or_create(
                    username=mobile_number,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                    }
                )
                
                # Create or update user profile
                user_profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'mobile_number': mobile_number,
                        'is_mobile_verified': True
                    }
                )
                
                if not created:
                    user_profile.is_mobile_verified = True
                    user_profile.save()
                
                # Store user profile in session
                request.session['user_profile_id'] = user_profile.id
                request.session['is_verified'] = True
                
                # Clear temporary data
                del request.session['user_data']
                del request.session['otp_sent']
                
                messages.success(request, 'Mobile number verified successfully!')
                return redirect('survey_list')
            else:
                messages.error(request, message)
    
    # If verification failed, return to home with forms
    form = UserRegistrationForm()
    otp_form = OTPVerificationForm()
    return render(request, 'home.html', {
        'form': form,
        'otp_form': otp_form,
        'otp_sent': True
    })

def survey_list_view(request):
    if not request.session.get('is_verified'):
        messages.error(request, 'Please verify your mobile number first.')
        return redirect('home')
    
    surveys = Survey.objects.filter(is_active=True)
    user_profile_id = request.session.get('user_profile_id')
    
    # Check which surveys user has already voted on
    if user_profile_id:
        user_profile = UserProfile.objects.get(id=user_profile_id)
        voted_survey_ids = user_profile.vote_set.values_list('survey_id', flat=True)
    else:
        voted_survey_ids = []
    
    return render(request, 'survey_list.html', {
        'surveys': surveys,
        'voted_survey_ids': voted_survey_ids
    })

@require_http_methods(["POST"])
def resend_otp_view(request):
    user_data = request.session.get('user_data')
    if not user_data:
        return JsonResponse({'success': False, 'message': 'Session expired'})
    
    mobile_number = user_data['mobile_number']
    otp = create_and_send_otp(mobile_number)
    
    if otp:
        return JsonResponse({'success': True, 'message': f'OTP resent to {mobile_number}'})
    else:
        return JsonResponse({'success': False, 'message': 'Failed to send OTP'})

def vote_view(request, survey_id):
    if not request.session.get('is_verified'):
        messages.error(request, 'Please verify your mobile number first.')
        return redirect('home')
    
    try:
        survey = Survey.objects.get(id=survey_id, is_active=True)
    except Survey.DoesNotExist:
        messages.error(request, 'Survey not found or inactive.')
        return redirect('survey_list')
    
    user_profile_id = request.session.get('user_profile_id')
    user_profile = UserProfile.objects.get(id=user_profile_id)
    
    # Check if user has already voted
    if Vote.objects.filter(survey=survey, user_profile=user_profile).exists():
        messages.error(request, 'You have already voted on this survey.')
        return redirect('survey_list')
    
    if request.method == 'POST':
        form = VotingForm(survey, request.POST)
        if form.is_valid():
            selected_option_id = form.cleaned_data['selected_option']
            selected_option = SurveyOption.objects.get(id=selected_option_id)
            
            # Create vote
            Vote.objects.create(
                survey=survey,
                option=selected_option,
                user_profile=user_profile
            )
            
            messages.success(request, 'Your vote has been submitted successfully!')
            return redirect('survey_list')
    else:
        form = VotingForm(survey)
    
    return render(request, 'vote.html', {
        'survey': survey,
        'form': form
    })

def create_survey_view(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('welcome')
    
    if request.method == 'POST':
        survey_form = SurveyCreationForm(request.POST)
        
        # Get options from POST data
        options = []
        i = 0
        while f'option_{i}' in request.POST:
            option_text = request.POST.get(f'option_{i}').strip()
            if option_text:
                options.append(option_text)
            i += 1
        
        if survey_form.is_valid() and len(options) >= 2:
            from django.db import transaction
            with transaction.atomic():
                survey = survey_form.save(commit=False)
                survey.created_by = request.user
                survey.save()
                
                # Create options
                for idx, option_text in enumerate(options):
                    SurveyOption.objects.create(
                        survey=survey,
                        option_text=option_text,
                        order=idx
                    )
                
                messages.success(request, 'Survey created successfully!')
                return redirect('survey_list')
        else:
            if len(options) < 2:
                messages.error(request, 'Please provide at least 2 options.')
    else:
        survey_form = SurveyCreationForm()
    
    return render(request, 'create_survey.html', {
        'survey_form': survey_form
    })

def results_view(request, survey_id=None):
    if not request.session.get('is_verified'):
        messages.error(request, 'Please verify your mobile number first.')
        return redirect('home')
    
    surveys = Survey.objects.filter(is_active=True)
    
    if survey_id:
        try:
            selected_survey = Survey.objects.get(id=survey_id, is_active=True)
            # Get vote counts for each option
            from django.db.models import Count
            results = selected_survey.options.annotate(
                vote_count=Count('vote')
            ).order_by('order')
            
            total_votes = sum(result.vote_count for result in results)
            
            # Calculate percentages and average per option
            avg_per_option = (total_votes / results.count()) if results.count() > 0 else 0
            for result in results:
                result.percentage = (result.vote_count / total_votes * 100) if total_votes > 0 else 0
            
            return render(request, 'results.html', {
                'surveys': surveys,
                'selected_survey': selected_survey,
                'results': results,
                'total_votes': total_votes,
                'avg_per_option': avg_per_option
            })
        except Survey.DoesNotExist:
            messages.error(request, 'Survey not found.')
    
    return render(request, 'results.html', {
        'surveys': surveys
    })

def admin_dashboard_view(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('welcome')
    
    surveys = Survey.objects.all().order_by('-created_at')
    total_users = UserProfile.objects.filter(is_mobile_verified=True).count()
    total_votes = Vote.objects.count()
    
    return render(request, 'admin_dashboard.html', {
        'surveys': surveys,
        'total_users': total_users,
        'total_votes': total_votes
    })

