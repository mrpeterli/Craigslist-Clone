from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import requests
from main import models

# Create your views here.

BASE_CRAIGSLIST_URL = 'https://delhi.craigslist.org/search/?query={}'

def home(request):
    context = {}
    return render(request,'main/base.html',context)

def new_search(request):
    search  = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url  = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data,features="html.parser")
    post_listings = soup.find_all('li',{'class':'result-row'})
    final_postings = []
    print("hello")
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')
        try:
            post_price = post.find('span',{'class':'result-price'}).text
        except:
            post_price = 'N/A'
        #post_image = post.find(class_='result-image gallery')
        #post_image = post_image.get('img').get('src')
        new_response = requests.get(post_url)
        new_data = new_response.text
        soup = BeautifulSoup(new_data,features="html.parser")
        post_img = soup.findAll('img')
        try:
            post_img = post_img[0].get('src')
        except:
            post_img = ''
        # print(post_img)

        # print(post_title)
        # print(post_url)
        # print(post_price)
        final_postings.append((post_title,post_url,post_price,post_img))
    
    #print(final_postings)
    context = {
        'search': search,
        'final_postings':final_postings
    }
    return render(request,'main/new_search.html',context)

