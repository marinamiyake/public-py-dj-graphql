import graphene

from mainapp import models


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
