from covid import Covid
from django.shortcuts import render, HttpResponse
from .models import Country, State
# from rest_framework import viewsets
# from .serializers import CountrySerializer
from newsapi import NewsApiClient
import requests, json, os
import datetime
import smtplib, ssl

def getJsonDataByKey(filename, key):
    filepath = os.path.abspath(f"myapp/{filename}")
    with open(filepath) as file:
        data = json.load(file)
    return data[key]

def setJsonData(filename, key, newValue):
    try:
        filepath = os.path.abspath(f"myapp/{filename}")
        with open(filepath, 'r') as f:
            file = json.load(f)
        file[key] = newValue
        with open(filepath, "w") as jsonFile:
            json.dump(file, jsonFile)
    except:
        pass

def getNewsDetails():
    newsapi = NewsApiClient(api_key='d7ce122de0f84c77b35121f97ac2259f')
    top_headlines = newsapi.get_top_headlines(q='corona', language='en')
    return top_headlines['articles']

def update_country(request):
    covid = Covid()
    country_data = covid.get_data()
    for data in country_data:
        print(f"Data is {data['country']}")
        obj = Country(name=data['country'], confirmed=data['confirmed'],active=data['active'],recovered=data['recovered'],
                      deceased=data['deaths'],latitude=data['latitude'],longitude=data['longitude'],
                      last_update=data['last_update'])

        obj.save()
    country_data = Country.objects.values()
    total_confirmed = sum([data['confirmed'] for data in country_data])
    total_active = sum([data['active'] for data in country_data])

    total_recovered = sum([data['recovered'] for data in country_data])

    total_death = sum([data['deceased'] for data in country_data])
    today_date = datetime.datetime.now().date().strftime("%d-%m-%Y")
    if getJsonDataByKey("data.json", "date") != today_date:
        increase_confirmed = increase_recovered = increase_death = 0
        setJsonData("data.json", "confirmed", total_confirmed)
        setJsonData("data.json", "recovered", total_recovered)
        setJsonData("data.json", "death", total_death)
        setJsonData("data.json", "date", today_date)
    else:
        increase_confirmed = total_confirmed - getJsonDataByKey("data.json", "confirmed")
        increase_recovered = total_recovered - getJsonDataByKey("data.json", "recovered")
        increase_death = total_death - getJsonDataByKey("data.json", "death")

    sort_by_active = sorted(country_data, key=lambda data:data['active'], reverse=True)
    top_10_country = list()
    for data in sort_by_active:
        top_10_country.append(data['name'])
    top_10_country = ','.join([str(i) for i in (top_10_country[:10])])
    top_10_active = list()
    for data in sort_by_active:
        top_10_active.append(data['active'])
    top_10_active = ','.join([str(i) for i in (top_10_active[:10])])

    news_api = list()
    for data in getNewsDetails()[:100]:
        if "corona" in data['title'].lower() or "covid" in data['title'].lower():
            news_api.append({'title':data['title'].title(), 'url':data['url']})
    return render(request, "myapp/dashboard.html", {'country_data':country_data, 'total_confirmed':total_confirmed, 'top_10_country':top_10_country,
                                                    'increase_confirmed': increase_confirmed, 'increase_recovered':increase_recovered, 'increase_death':increase_death,
                                                    'top_10_active': top_10_active, 'total_active':total_active,
                                                    'total_recovered':total_recovered,'total_death':total_death, 'news_api':news_api})

def update_state_india(request, name):
    if name.lower() == "india":
        response = requests.get("https://api.rootnet.in/covid19-in/stats/latest").json()
        india = Country.objects.get(name="India")
        # print(india)
        state_data = response['data']['regional']
        for data in state_data:
            obj = State(name=data['loc'], country=india, confirmed=data['confirmedCasesIndian'], active=data['totalConfirmed'] - data['discharged'],
                          recovered=data['discharged'],
                          deceased=data['deaths'],
                          last_update=response['lastOriginUpdate'])

            obj.save()
        state_data = State.objects.filter(country="India").values()
        total_confirmed = sum([data['confirmed'] for data in state_data])
        total_active = sum([data['active'] for data in state_data])
        total_recovered = sum([data['recovered'] for data in state_data])
        total_death = sum([data['deceased'] for data in state_data])
        return render(request, "myapp/state.html", {'state_data': state_data, 'total_confirmed': total_confirmed,
                                                        'total_active': total_active, 'total_recovered': total_recovered,
                                                        'total_death': total_death})
    else:
        return HttpResponse("Under Progress....")

# update_state_india()

def contactus(request):
    if request.method == "POST":
        port = 465  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = "ernikhilkrjain@gmail.com"
        receiver_email = request.POST['email']
        password = "iamlearnate"
        message = f"""\
        Subject: Hi {request.POST['name']}

        Thank you for contacting us. We will get back to you soon."""

        server = smtplib.SMTP_SSL(smtp_server, port)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        server.quit()
    return HttpResponse("Hi")
