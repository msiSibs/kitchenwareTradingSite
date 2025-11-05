from django.shortcuts import render
from django.http import HttpResponse

# Stub views for reviews app - to be implemented in Phase 7

def create_review_view(request, item_id):
    return HttpResponse("Create Review View - Coming in Phase 7")

def review_detail_view(request, pk):
    return HttpResponse("Review Detail View - Coming in Phase 7")

def review_delete_view(request, pk):
    return HttpResponse("Review Delete View - Coming in Phase 7")
