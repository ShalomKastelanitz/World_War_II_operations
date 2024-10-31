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

class Target(SQLAlchemyObjectType):
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
    Mission_by_date=graphene.List(Mission, start_date=graphene.Date(required=True),ana_data=graphene.Date(required=True))
    Missions_by_Country=graphene.List(Mission, country_id=graphene.Int(required=True))
    Target_by_Target__type_id=graphene.List(Target, target_type_id=graphene.Int(required=True))
    def resolve_Mission_by_id(self, info, mission_id):
        return db_session.query(MissionsModel).get(mission_id)

    def resolve_Mission_by_date(self, info, start_date, ana_data):
        return db_session.query(MissionsModel).filter(MissionsModel.mission_date.between(start_date, ana_data)).all()


    def resolve_Missions_by_Country(self, info, country_id):
        return db_session.query(MissionsModel).join(MissionsModel.targets).join(TargetsModel.city).filter(
            CitiesModel.country_id == country_id).all()

    def resolve_Target_by_Target__type_id(self, info, target_type_id):
        return db_session.query(TargetsModel).filter(TargetsModel.target_type_id == target_type_id).all()






#Mutations
class AddTarget(graphene.Mutation):
        class Arguments:
            mission_date = graphene.Date(required=True)
            airborne_aircraft = graphene.Float(required=True)
            attacking_aircraft = graphene.Float(required=True)
            bombing_aircraft = graphene.Float(required=True)
            aircraft_returned = graphene.Float(required=True)
            aircraft_failed = graphene.Float(required=True)
            aircraft_damaged = graphene.Float(required=True)
            aircraft_lost = graphene.Float(required=True)

        Target = graphene.Field(lambda: TargetsModel)

        def mutate(self, info, mission_date, airborne_aircraft, attacking_aircraft,bombing_aircraft,aircraft_returned,aircraft_failed,aircraft_damaged,aircraft_lost):

            new_Target = TargetsModel(mission_date=mission_date,airborne_aircraft=airborne_aircraft,attacking_aircraft=attacking_aircraft,
                                      bombing_aircraft=bombing_aircraft,aircraft_returned=aircraft_returned,aircraft_failed=aircraft_failed,aircraft_damaged=aircraft_damaged,aircraft_lost=aircraft_lost)
            db_session.add(new_Target)
            db_session.commit()
            return AddTarget(user=new_Target)
class Mutation(graphene.ObjectType):
    add_Target = AddTarget.Field()
schema = graphene.Schema(query=Query )
