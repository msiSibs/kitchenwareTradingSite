from django.shortcuts import render
from django.http import HttpResponse

# Stub views for marketplace app - to be implemented in Phase 3

def item_list_view(request):
    return HttpResponse("Item List View - Coming in Phase 3")

def item_detail_view(request, pk):
    return HttpResponse("Item Detail View - Coming in Phase 3")

def item_create_view(request):
    return HttpResponse("Item Create View - Coming in Phase 3")

def item_edit_view(request, pk):
    return HttpResponse("Item Edit View - Coming in Phase 3")

def item_delete_view(request, pk):
    return HttpResponse("Item Delete View - Coming in Phase 3")
