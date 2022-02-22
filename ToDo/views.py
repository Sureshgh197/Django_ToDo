from django.shortcuts import (get_object_or_404,
                              render,redirect,
                              HttpResponseRedirect,
                              HttpResponse)
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render,HttpResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task,Category,RecycleBin
from datetime import datetime
from dateutil.parser import parse

# Create your views here.

class TaskList(ListView):
    template_name     =  'ToDo/index.html'

    def get_queryset(self):
        return Task.objects.all()

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['obj2'] = Category.objects.all()
        return data



def create(request):

    
    name        = request.POST.get('name')
    due_date    = request.POST.get('due_date')
    description = request.POST.get('description')
    priority    = request.POST.get('priority')
    category    = request.POST.get('category')

    foreign_cat = Category.objects.get(name=category)

    obj         = Task.objects.create(name=name,
    due_date    = due_date,
    description = description,
    priority    = priority,
    category    = foreign_cat,
    )

    obj.save()
    return redirect('/')



def update(request,id):
    # user         = request.user
    Task_obj     = Task.objects.filter(Q(id=id),)
    obj2         = Category.objects.all()
    if(Task_obj.exists()):
        obj         = Task.objects.get(id=id)
        return render(request,"ToDo/update.html",{'obj':obj,'obj2':obj2}) 

    else:
        return HttpResponse('This Record is not found your Tasks')



def update_data(request):
    # user    = request.user
    if request.method == 'POST':
        id              = request.POST.get('id')
        name            = request.POST.get('name')
        due_date        = request.POST.get('due_date') 
        # 2021-11-15T18:36
        description     = request.POST.get('description')
        priority        =request.POST.get('priority')
        category        = request.POST.get('category')
        status          = request.POST.get('status')        
       
        foreign_cat     = Category.objects.get(name=category)
        
        Task_obj        = Task.objects.filter(Q(id=id),)

        if(Task_obj.exists()):
            obj          = Task.objects.get(id=id)  
            
            # print(obj_str_time)          
            # obj_str_time = datetime.strptime(str(obj.due_date), "%Y-%m-%j %H:%M:%S")
            obj_str_time = parse(str(obj.due_date))
            
            obj.name     = name
            if due_date == '':
                pass
            else:
                inp_str_time     = datetime.strptime(due_date, "%Y-%m-%jT%H:%M")
                if(inp_str_time>obj_str_time):
                    obj.due_date = due_date
                    obj.save()
                    obj.postpones+=1

                else:
                    obj.due_date = due_date
                    obj.save()

            obj.description      = description
            obj.priority         = priority
            obj.category         = foreign_cat
            
            if status == "on":
                obj.status  = True
                obj.save()

            else:
                obj.status  = False
                obj.save()

            return redirect('/')
        else:
            return HttpResponse('This Record is not found your Tasks')

    return redirect('/')



def delete(request,id):
    user    = request.user

    if request.method =="GET":
        Task_obj    = Task.objects.filter(Q(id=id),)
        if(Task_obj.exists()):
            obj         = Task.objects.get(id=id)
            foreign_cat = Category.objects.get(name=obj.category.name)
        
            bin             = RecycleBin.objects.create(name=obj.name,
            due_date        = obj.due_date,
            idd             = obj.id,
            status          = obj.status,
            description     = obj.description,
            priority        = obj.priority,
            category        = foreign_cat,
            creation_date   = obj.creation_date,
            last_updated    = obj.last_updated,
            )

            bin.save()
            obj.delete()

            return HttpResponseRedirect("/")

        else:
            return HttpResponse('This Record is not found your Tasks')


def deleteRecycle(request,id):

    if request.method == "GET":
        obj     = RecycleBin.objects.get(idd=id)
        obj.delete()
        return redirect('//restore')



def rlistDelete(request):
    if request.method == "GET":
        ids     = request.GET.getlist('ids[]')
        for i in ids:
            obj     = RecycleBin.objects.get(idd=i)
            obj.delete()
        return (HttpResponse('hi'))



def tlistDelete(request):
    # user    = request.user
    if request.method=='GET':
        
        ids    = request.GET.getlist('ids[]')
        
        for i in ids:
            obj             = Task.objects.get(id=int(i))
            foreign_cat     = Category.objects.get(name=obj.category.name)

            bin             = RecycleBin.objects.create(name=obj.name,
            due_date        = obj.due_date,
            idd             = obj.id,
            status          = obj.status,
            description     = obj.description,
            priority        = obj.priority,
            category        = foreign_cat,
            creation_date   = obj.creation_date,
            last_updated    = obj.last_updated,

            )

            bin.save()
            obj.delete()
            
        return (HttpResponse('hi'))

    else:
        return (HttpResponse('hi'))        



def restore(request):
    # user    = request.user
    obj     = RecycleBin.objects.all()
    obj2    = Category.objects.all()

    return render(request,'ToDo/archieves.html',{'obj':obj,'obj2':obj2})


def restoreSelect(request,id):
    # user        = request.user
    Recycle_obj = RecycleBin.objects.filter(Q(idd=id),)
    
    if(Recycle_obj.exists()):
        obj             = RecycleBin.objects.get(idd=id)
        category        = obj.category        
        first_created   = obj.creation_date.date()
       
        Task_obj        = Task.objects.create(name=obj.name,
        due_date        = obj.due_date,
        description     = obj.description,
        priority        = obj.priority,
        category        = category,
        first_created   = obj.creation_date,
        restored        = True,
        old_id          = obj.idd,
        postpones       = obj.postpones,
        last_updated    = obj.last_updated,
        status          = obj.status,
        )

        Task_obj.save()
        obj.delete()

    else:
        return HttpResponse('You cannot restore this Record')

    return redirect('/')

def cat_add_page(request):
    if request.method == 'POST':
        
        cat_name = request.POST['cat']
        
        Category.objects.create(name=cat_name)
        return HttpResponse('hi')
    else:
        return render(request, "ToDo/AddCategory.html")