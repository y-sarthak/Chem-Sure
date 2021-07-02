from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from .forms import ChemForm
from .models import Chem
from django.conf import settings
from .data import dataset

import easyocr
reader = easyocr.Reader(['en'], gpu = False)


def remove_space(temp):
    
    ans=[]
    
    for t in temp:
        
        if len(t)==0:
            continue
        
        st=0
        for ch in t:
            if ch==' ':
                st=st+1
            else:
                break
        
        en=len(t)
        for ch in reversed(range(0, len(t))):
            if t[ch]==' ':
                en=en-1
            else:
                break
        
        ans.append(t[st:en])
        
    return ans


def search(temp):
    dic=[]

    s=0
    m=0
    h=0
    
    for st in temp:
        t = []
        for ke in dataset:
            if st==ke:
                t.append(ke)
                for i in dataset[ke]:
                    if i=='Safe':
                        s=s+1
                    elif i=='Moderate':
                        m=m+1
                    elif i=='Toxic':
                        h=h+1
                    t.append(i)
                dic.append(t)
                break
    
    return dic, s, m, h



def func(str):
    ans = []
    
    pre=0
    temp=""
    bra=0
    
    for string in str:
        x=0
        for j in range(len(string)):
            
            if string[j]=='(' and bra==0:
                bra=bra+1
                if pre==0:
                    ans.append(string[x:j-1])
                else:
                    if j-1<=0:
                        ans.append(temp)
                    else:
                        temp = temp + ' ' + string[x:j-1]
                        ans.append(temp)
                    pre=0
                continue
            if string[j]=='(':
                bra=bra+1
                continue
            if string[j]==')':
                if bra==1:
                    x=j+2
                bra=bra-1
            if bra>0:
                continue
            
            
            if string[j]==',' or string[j]==':' or string[j]==';':
                if pre==1:
                    temp = temp + ' ' + string[x:j]
                    ans.append(temp)
                    pre=0
                else:
                    ans.append(string[x:j])
                x=j+2
                
            elif j == len(string)-1:
                if string[j]==':':
                    ans.append(string[x:j])
                else:
                    temp = string[x:j+1]
                    pre=1
    if pre==1:
            ans.append(temp)
                
    ans = remove_space(ans)
    return search(ans)




def image_upload_view(request,*args,**kwargs):

	if request.method == 'POST':
		form = ChemForm(request.POST, request.FILES)

		if form.is_valid():
			form.save()
			ind = form.instance.id

			return redirect("http://127.0.0.1:8000/analysis/%s"%(ind))
	else:
		form = ChemForm()
	return render(request, 'image_upload.html', {'form' : form})


def Analysis(request,id,*args,**kwargs):

	objs=get_object_or_404(Chem,id=id)

	pa =  objs.image.url
	media_path = settings.MEDIA_ROOT

	path = media_path[0:-6] + pa
	result = reader.readtext(path, detail = 0)

	dic, s, m, h = func(result)
	# objs.delete()

	my_context={
	"object":dic,
    "safe" : s,
    "mod" : m,
    "toxic" : h
	}

	return render(request,"content.html",my_context)
