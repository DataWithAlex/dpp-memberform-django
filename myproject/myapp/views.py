# myapp/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests

def home(request):
    return render(request, 'home.html', {"years": [str(year) for year in range(2024, 2017, -1)], "sessions": [str(i) for i in range(118, 99, -1)]})

def submit_form(request):
    if request.method == "POST":
        form_data = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "member_organization": request.POST.get("member_org"),
            "year": request.POST.get("selected_year"),
            "legislation_type": request.POST.get("legislation_type"),
            "session": request.POST.get("session") if request.POST.get("legislation_type") == "Federal Bills" else "N/A",
            "bill_number": request.POST.get("bill_number"),
            "bill_type": request.POST.get("federal_bill_type") if request.POST.get("legislation_type") == "Federal Bills" else request.POST.get("bill_type"),
            "support": request.POST.get("support"),
            "lan": "en"  # Default language to "en"
        }

        response = call_api(form_data, request.POST.get("legislation_type"))
        if "error" in response and response["error"] != "Error occurred: Expecting value: line 1 column 1 (char 0)":
            return JsonResponse({"error": response["error"]})
        else:
            return JsonResponse({"success": "Complete", "url": response.get("url", "")})
    else:
        return redirect('home')

def call_api(data, legislation_type):
    if legislation_type == "Federal Bills":
        api_url = "http://3.226.54.104:8080/process-federal-bill/"
    else:
        api_url = "http://3.226.54.104:8080/update-bill/"

    try:
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API request failed with status code {response.status_code}"}
    except Exception as e:
        if str(e) == "Expecting value: line 1 column 1 (char 0)":
            return {"success": "Complete"}
        else:
            return {"error": f"Error occurred: {str(e)}"}
