from .models import Course, Review, ReviewVote
from .forms import ReviewForm, CourseForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Max, Min

# Create your views here.



def course_list(request):
    query = request.GET.get('q')
    if query:
        courses = Course.objects.filter(Q(name__icontains=query) | Q(code__icontains=query))
    else:
        courses = Course.objects.all()

    level_100_courses = courses.filter(level=100).order_by('name')
    level_200_courses = courses.filter(level=200).order_by('name')
    level_300_courses = courses.filter(level=300).order_by('name')

    context = {
        'level_100_courses': level_100_courses,
        'level_200_courses': level_200_courses,
        'level_300_courses': level_300_courses,
    }

    return render(request, 'reviews/course_list.html', context)



@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    year_filter = request.GET.get('year')
    if year_filter:
        reviews = Review.objects.filter(course=course, created_date__year=year_filter).order_by('-created_date')
    else:
        reviews = Review.objects.filter(course=course).order_by('-created_date')

    # Get the range of years for which reviews are available
    review_date_range = Review.objects.aggregate(start_year=Min('created_date__year'), end_year=Max('created_date__year'))
    years = range(review_date_range['start_year'], review_date_range['end_year'] + 1) if review_date_range['start_year'] else []

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.user = request.user  # Set the user for the review
            review.save()
            # Redirect to the same course detail page after adding the review
            return redirect('reviews:course_detail', course_id=course_id)
    else:
        form = ReviewForm()

    if 'vote' in request.POST:
        review_id = request.POST.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        vote_type = request.POST.get('vote')  # 'upvote' or 'downvote'
        is_upvote = True if vote_type == 'upvote' else False

        # Check if the user has already voted
        existing_vote = ReviewVote.objects.filter(user=request.user, review=review).first()
        if existing_vote:
            # User has already voted, update vote if different
            if existing_vote.is_upvote != is_upvote:
                existing_vote.is_upvote = is_upvote
                existing_vote.save()  
        else:
            # Create a new vote
            ReviewVote.objects.create(user=request.user, review=review, is_upvote=is_upvote)

        return HttpResponseRedirect(request.path_info)


    
    context = {
        'course': course,
        'reviews': reviews,
        'form': form,
        'current_year': year_filter,
        'available_years': years
    }

    return render(request, 'reviews/course_detail.html', context)


@login_required
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect('reviews:course_detail', course_id=course.id)
    else:
        form = CourseForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'reviews/add_course.html', context)


