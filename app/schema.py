import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from datetime import datetime, date
from app.db.database import db_session
from app.db.Models.models import MissionsModel,CitiesModel,CountryModel,TargetsModel,Targets_typeModel
#יצירת המחלקות המגבילות כלומר כל שזה ושדה שיהיה מתאים לנו
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

#מחלקה של השאילתות
class Query(graphene.ObjectType):
    #כל משתנה מפעיל את השאילתה שעל השם שלו וגם מגדיר מה מקבל ומחזיר
    Mission_by_id = graphene.Field(Mission, mission_id=graphene.Int(required=True))
    Mission_by_date=graphene.List(Mission, start_date=graphene.Date(required=True),ana_data=graphene.Date(required=True))
    Missions_by_Country=graphene.List(Mission, country_id=graphene.Int(required=True))
    Target_by_Target__type_id=graphene.List(Target, target_type_id=graphene.Int(required=True))
    #ביצוע השאילתות בפועל כלומר לדאטה בייס
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
#הוספת משימה
class Addmission(graphene.Mutation):
        class Arguments:
            mission_date = graphene.Date(required=True)
            airborne_aircraft = graphene.Float(required=True)
            attacking_aircraft = graphene.Float(required=True)
            bombing_aircraft = graphene.Float(required=True)
            aircraft_returned = graphene.Float(required=True)
            aircraft_failed = graphene.Float(required=True)
            aircraft_damaged = graphene.Float(required=True)
            aircraft_lost = graphene.Float(required=True)

        mission = graphene.Field(lambda: Mission)

        def mutate(self, info, mission_date, airborne_aircraft, attacking_aircraft,bombing_aircraft,aircraft_returned,aircraft_failed,aircraft_damaged,aircraft_lost):

            new_Target = TargetsModel(mission_date=mission_date,airborne_aircraft=airborne_aircraft,attacking_aircraft=attacking_aircraft,
                                      bombing_aircraft=bombing_aircraft,aircraft_returned=aircraft_returned,aircraft_failed=aircraft_failed,aircraft_damaged=aircraft_damaged,aircraft_lost=aircraft_lost)
            try:
                birth_date_obj = datetime.strptime(mission_date, '%Y-%m-%d').date()
            except ValueError:
                raise Exception("Invalid birth date format. Expected 'YYYY-MM-DD'")
            db_session.add(new_Target)
            db_session.commit()
            return AddTarget(user=new_Target)

#הוספת מטרה
class AddTarget(graphene.Mutation):
    class Arguments:

        target_priority = graphene.Int(required=True)
        target_industry =  graphene.Int(required=True)
        mission_id =  graphene.Int(required=True)
        target_type_id = graphene.Int(required=True)
        city_id =  graphene.Int(required=True)

    Target = graphene.Field(lambda: Target)

    def mutate(self, info, target_priority, target_industry, mission_id,target_type_id,city_id):

        new_Target=TargetsModel(target_priority=target_priority,target_industry=target_industry,mission_id=mission_id,target_type_id=target_type_id,city_id=city_id)
        db_session.add(new_Target)
        db_session.commit()
        return AddTarget(user=new_Target)
#עדכון תוצאות התקיפה
class Update_results_attack(graphene.Mutation):
    class Arguments:
        mission_id = graphene.Int(required=True)
        airborne_aircraft = graphene.Float(required=True)
        attacking_aircraft = graphene.Float(required=True)
        bombing_aircraft = graphene.Float(required=True)
        aircraft_returned = graphene.Float(required=True)
        aircraft_failed = graphene.Float(required=True)
        aircraft_damaged = graphene.Float(required=True)
        aircraft_lost = graphene.Float(required=True)

    user = graphene.Field(lambda: Mission)

    # def mutate(self, info, airborne_aircraft= ,attacking_aircraft,bombing_aircraft,aircraft_returned,aircraft_failed,aircraft_damaged,aircraft_lost, mission_id ):
    #     results_attack = db_session.query(MissionsModel).get(user_id)
    #     if not user:
    #         raise Exception("User not found")
    #     user.name = new_name
    #     db_session.commit()
    #     return UpdateUserName(user=user)

class Mutation(graphene.ObjectType):
    add_Target = AddTarget.Field()
    add_mission= Addmission.Field()
schema = graphene.Schema(query=Query, Mutation=Mutation)
