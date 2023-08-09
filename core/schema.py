import graphene

import mainapp.schema


class Query(mainapp.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
