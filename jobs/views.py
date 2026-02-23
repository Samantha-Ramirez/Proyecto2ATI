from django.shortcuts import render


def search_jobs(request):
    return render(request, 'search_jobs.html')


def apply_job(request, job_id):
    pass


def search_staff(request):
    return render(request, 'search_staff.html')


def post_job(request):
    return render(request, 'post_job.html')
