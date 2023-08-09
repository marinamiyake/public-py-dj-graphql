"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView

from core.schema import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    # API end point (Open GraphiQL window)
    #   GraphiQL window opens when you access to "http://127.0.0.1:8000/graphiql
    #   If you call API from the left side (Write query and run), you'll get result on the right side.
    #       [variables]
    #           first: Pagination unit (Page limit)
    #           after: Page (Set the "cursor" value of previous page(request)'s last node)
    #       [Query example]
    #           query {
    #             moments (first:1 after:"YXJyYXljb25uZWN0aW9uOjA=") {
    #               pageInfo {
    #             	  startCursor
    #                 endCursor
    #                 hasNextPage
    #                 hasPreviousPage
    #               }
    #               edges {
    #                 cursor
    #                 node {
    #                   rowNum
    #                   title
    #                   cityName
    #                   weatherDescription
    #                   temp
    #                   tempMin
    #                   humidity
    #                   comment
    #                   createdAt
    #                 }
    #               }
    #             }
    #           }
    #       [Result example]
    #           {
    #             "data": {
    #               "moments": {
    #                 "pageInfo": {
    #                   "startCursor": "YXJyYXljb25uZWN0aW9uOjE=",
    #                   "endCursor": "YXJyYXljb25uZWN0aW9uOjE=",
    #                   "hasNextPage": true,
    #                   "hasPreviousPage": false
    #                 },
    #                 "edges": [
    #                   {
    #                     "cursor": "YXJyYXljb25uZWN0aW9uOjE=",
    #                     "node": {
    #                       "rowNum": 2,
    #                       "title": "test admin title 2",
    #                       "cityName": "London",
    #                       "weatherDescription": "Cloudy",
    #                       "temp": 15.2,
    #                       "tempMin": 3.7,
    #                       "humidity": 65.7,
    #                       "comment": "test comment 2",
    #                       "createdAt": "2023-08-09T21:59:44.108129+00:00"
    #                     }
    #                   }
    #                 ]
    #               }
    #             }
    #           }
    path('graphiql/', GraphQLView.as_view(graphiql=True, schema=schema))
]
