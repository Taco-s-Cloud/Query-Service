from datetime import datetime
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models.base_models import Task, Schedule, User
from app.database import get_db

class TaskType(SQLAlchemyObjectType):
    class Meta:
        model = Task

class ScheduleType(SQLAlchemyObjectType):
    class Meta:
        model = Schedule

class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User

class UserActivitiesType(graphene.ObjectType):
    tasks = graphene.List(TaskType)
    upcoming_tasks = graphene.List(TaskType)
    schedules = graphene.List(ScheduleType)
    upcoming_schedules = graphene.List(ScheduleType)
    total_tasks = graphene.Int()
    total_schedules = graphene.Int()
    completion_rate = graphene.Float()

class Query(graphene.ObjectType):
    user_activities = graphene.Field(
        UserActivitiesType,
        user_id=graphene.String(required=True)
    )

    def resolve_user_activities(self, info, user_id):
        db = next(get_db())
        now = datetime.utcnow()

        # Get tasks
        all_tasks = db.query(Task).filter(Task.user_id == user_id).all()
        upcoming_tasks = [t for t in all_tasks if t.due_date and t.due_date > now]

        # Get schedules
        all_schedules = db.query(Schedule).filter(Schedule.user_id == user_id).all()
        upcoming_schedules = [s for s in all_schedules if s.start_time > now]

        # Calculate completion rate
        completed_tasks = len([t for t in all_tasks if t.completed])
        completion_rate = (completed_tasks / len(all_tasks)) * 100 if all_tasks else 0

        return UserActivitiesType(
            tasks=all_tasks,
            upcoming_tasks=upcoming_tasks,
            schedules=all_schedules,
            upcoming_schedules=upcoming_schedules,
            total_tasks=len(all_tasks),
            total_schedules=len(all_schedules),
            completion_rate=completion_rate
        )

schema = graphene.Schema(query=Query)