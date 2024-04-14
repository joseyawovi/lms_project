from django.shortcuts import redirect, render
from app.models import Categories,Course,Level, Video, UserCourse
from django.template.loader import render_to_string
from django.http import JsonResponse

from django.db.models import Avg,Sum
def base(request):
    return render(request,'base.html')

def home(request):
   
    category = Categories.objects.all().order_by('id')[0:6]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')

    context = {
        'category':category,
        'course':course,
    }
    print(context)
    return render(request, 'main/home.html',context)

def single_course(request):
    category = Categories.get_all_category()
    level = Level.objects.all()
    course = Course.objects.all()
    freeCourse_count =Course.objects.filter(price =0).count()
    paidCourse_count =Course.objects.filter(price__gte=1).count()

    print(freeCourse_count)
    context = {
        'category':category,
        'level':level,
        'course':course,
        'freeCourse_count':freeCourse_count,
        'paidCourse_count':paidCourse_count
    }
    return render(request, 'main/single_course.html',context)


def filter_data(request):
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    print(price)
    
    if price == ['pricefree']:
        course = Course.objects.filter(price=0)
    elif price == ['pricepaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['priceall']:
        course = Course.objects.all()
    elif category:
        course = Course.objects.filter(category__id__in=category).order_by('-id')
    
    elif level:
        course = Course.objects.filter(level__id__in=level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')
    
    context = {
        'course':course
    }
    t = render_to_string('ajax/course.html',context)
    return JsonResponse({'data': t})

def contact_us(request):
    category = Categories.get_all_category()
    context = {
        'category':category
    }
    return render(request, 'main/contact_us.html',context)

def about_us(request):
    category = Categories.get_all_category()
    context = {
        'category':category
    }
    return render(request, 'main/about_us.html',context)


def search_course(request):
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
    category = Categories.get_all_category()

    context = {
        'course':course,
        'category':category
    }
    return render(request,'search/search.html',context)

from django.shortcuts import render, redirect
from django.db.models import Sum

def course_detail(request, slug):
    category = Categories.get_all_category()
    time_duration = Video.objects.filter(course__slug=slug).aggregate(sum=Sum('time_duration'))

    try:
        course = Course.objects.get(slug=slug)  # Get the course object
        check_enroll = UserCourse.objects.get(user=request.user, course=course)
    except Course.DoesNotExist:
        return redirect('404')  # Redirect if course does not exist
    except UserCourse.DoesNotExist:
        check_enroll = None

    context = {
        'course': course,
        'category': category,
        'time_duration': time_duration['sum'] if time_duration['sum'] else 0,
        'check_enroll': check_enroll
    }
    return render(request, 'course/course_detail.html', context)


def page_not_found(request):
    category = Categories.get_all_category()

    context = {
        'category':category
    }
    return render(request,'error/404.html',context)


def checkout(request,slug):
    course =Course.objects.get(slug=slug)
    
    if course.price == 0:
        course = UserCourse(
            user = request.user,
            course = course
        )
        course.save()
        redirect('home')
    return render(request, 'checkout/checkout.html') 

def my_course(request):
    return render(request,'course/my_course.html')    