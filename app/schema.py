import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from datetime import datetime, date
from app.db.database import db_session
from app.db.Models.models import MissionsModel,CitiesModel,CountryModel,TargetsModel,Targets_typeModel

class Cities(SQLAlchemyObjectType):
    class Meta:
        model = CitiesModel
        interfaces = (graphene.relay.Node,)

class Mission(SQLAlchemyObjectType):
    class Meta:
        model = MissionsModel
        interfaces = (graphene.relay.Node,)

class Targe(SQLAlchemyObjectType):
    class Meta:
        model = TargetsModel
        interfaces = (graphene.relay.Node,)

class Country(SQLAlchemyObjectType):
    class Meta:
        model = CountryModel
        interfaces = (graphene.relay.Node,)

class Target_type(SQLAlchemyObjectType):
    class Meta:
        model = Targets_typeModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):

    Mission_by_id = graphene.Field(Mission, mission_id=graphene.Int(required=True))
    def resolve_Mission_by_id(self, info, mission_id):
        return db_session.query(MissionsModel).get(mission_id)











#Mutations
    class AddTarget(graphene.Mutation):
        class Arguments:
            name = graphene.String(required=True)
            birth_date = graphene.String(required=True)  # Format: 'YYYY-MM-DD'
            address_id = graphene.Int(required=False)

        Target = graphene.Field(lambda: TargetsModel)

        def mutate(self, info, name, birth_date, address_id=None):
            try:
                birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
            except ValueError:
                raise Exception("Invalid birth date format. Expected 'YYYY-MM-DD'")
            new_Target = TargetsModel(name=name, birth_date=birth_date_obj, address_id=address_id)
            db_session.add(new_Target)
            db_session.commit()
            return AddTarget(user=new_Target)

schema = graphene.Schema(query=Query)
