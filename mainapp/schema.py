import datetime

import graphene
import requests
from django.conf import settings
from graphene_django import DjangoObjectType

from mainapp import models


# ==================================================
# Query (Read)
# ==================================================
# Note:
# Use plain (customized) ObjectType to add row_num field for display.
# If you don't need row_num, you can use DjangoObjectType like Mutation.
class MomentType(graphene.ObjectType):
    row_num = graphene.Int()

    # ----- Model Field -----
    title = graphene.String()
    city_name = graphene.String()
    weather_description = graphene.String()
    temp = graphene.Float()
    temp_min = graphene.Float()
    temp_max = graphene.Float()
    humidity = graphene.Float()
    comment = graphene.String()
    created_at = graphene.DateTime()

    # ----------

    class Meta:
        interfaces = (graphene.relay.Node,)


class MomentTypeConnection(graphene.relay.Connection):
    class Meta:
        node = MomentType


class Query(graphene.ObjectType):
    moment = graphene.relay.Node.Field(MomentType)
    moments = graphene.relay.ConnectionField(MomentTypeConnection)

    def resolve_moment(self, info, id):
        record = models.Moment.objects.get(id=id)
        return MomentType(
            row_num=1,
            title=record.title,
            city_name=record.city_name,
            weather_description=record.weather_description,
            temp=record.temp,
            temp_min=record.temp_min,
            temp_max=record.temp_max,
            humidity=record.humidity,
            comment=record.comment,
            created_at=record.created_at,
        )

    def resolve_moments(self, info, **kwargs):
        records = models.Moment.objects.all()
        results = []
        for i, record in enumerate(records):
            results.append(
                MomentType(
                    row_num=i + 1,
                    title=record.title,
                    city_name=record.city_name,
                    weather_description=record.weather_description,
                    temp=record.temp,
                    temp_min=record.temp_min,
                    temp_max=record.temp_max,
                    humidity=record.humidity,
                    comment=record.comment,
                    created_at=record.created_at,
                )
            )
        return results


# ==================================================
# ==================================================
# Mutation (Create, Update, Delete)
# ==================================================
class MomentDjangoType(DjangoObjectType):
    class Meta:
        model = models.Moment
        # Require django-filter to use filter function
        # filter_fields = ['name', 'ingredients']
        interfaces = (graphene.relay.Node,)
        fields = "__all__"


class MomentDjangoTypeConnection(graphene.relay.Connection):
    class Meta:
        node = MomentDjangoType


class MomentInput(graphene.InputObjectType):
    city_name = graphene.String(required=False)
    title = graphene.String(required=True)
    comment = graphene.String(required=True)


class CreateMoment(graphene.Mutation):
    class Arguments:
        input = MomentInput()

    moment = graphene.Field(MomentDjangoType)

    @classmethod
    def mutate(cls, root, info, input):
        moment = get_moment_from_weather_app_result(input.city_name)
        moment.title = input.title
        moment.comment = input.comment
        moment.save()

        return CreateMoment(moment=moment)


class UpdateMoment(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        input = MomentInput()

    moment = graphene.Field(MomentDjangoType)

    @classmethod
    def mutate(cls, root, info, id, input):
        moment = models.Moment.objects.get(pk=id)
        moment.title = input.title
        moment.comment = input.comment
        moment.save()
        return UpdateMoment(moment=moment)


class DeleteMoment(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    moment = graphene.Field(MomentDjangoType)

    @classmethod
    def mutate(cls, root, info, id):
        moment = models.Moment.objects.get(pk=id)
        moment.del_flg = True
        moment.deleted_at = datetime.datetime.now(datetime.timezone.utc).date()
        moment.save()
        return DeleteMoment(moment=moment)


def get_moment_from_weather_app_result(city_name):
    url = "https://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_key}"
    weather_api_reponse = requests.get(url.format(city_name=city_name, API_key=settings.WEATHER_API_KEY))
    weather_api_reponse_weather = weather_api_reponse.json()["weather"][0]
    weather_api_reponse_main = weather_api_reponse.json()["main"]
    new_moment = models.Moment(
        title="",
        city_name=city_name,
        weather_description=weather_api_reponse_weather["description"],
        temp=weather_api_reponse_main["temp"],
        temp_min=weather_api_reponse_main["temp_min"],
        temp_max=weather_api_reponse_main["temp_max"],
        humidity=weather_api_reponse_main["humidity"],
        comment="",
    )
    new_moment.save()
    return new_moment


class Mutation(graphene.ObjectType):
    create_moment = CreateMoment.Field()
    update_moment = UpdateMoment.Field()
    delete_moment = DeleteMoment.Field()
# ==================================================
