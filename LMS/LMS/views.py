from django.shortcuts import redirect, render
from app.models import Categories,Course,Level
from django.template.loader import render_to_string
from django.http import JsonResponse

def base(request):
    return render(request,'base.html')

def home(request):
   
    category = Categories.objects.all().order_by('id')[0:5]
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

def course_detail(request,slug):
    
    course = Course.objects.filter(slug=slug)
    category = Categories.get_all_category()
    
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    
    context = {
        'course':course,
        'category':category
    }
    return render(request,'course/course_detail.html',context)

def page_not_found(request):
    category = Categories.get_all_category()

    context = {
        'category':category
    }
    return render(request,'error/404.html',context)