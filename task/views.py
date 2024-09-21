from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from DjangoMaster.utils import Utils


# Create your views here.
@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def getTask(request, id=None):
    user = request.user

    try:
        if request.method == "GET":
            with connection.cursor() as cursor:
                if id is None:
                    cursor.execute(
                        "select * from task_task where user_id=%s", [user.id]
                    )
                else:
                    cursor.execute(
                        "select * from task_task where id=%s and user_id=%s",
                        [id, user.id],
                    )
                result = Utils.dict_fetch_all(cursor)

                if len(result) == 0:
                    return Response(
                        {"success": False, "result": "Task Not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                else:
                    return Response(
                        {"success": True, "result": result}, status=status.HTTP_200_OK
                    )

        elif request.method == "POST":
            title = request.data.get("title")
            description = request.data.get("description")
            due_date = datetime.strptime(request.data.get("due_date"), "%Y-%m-%d")

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO task_task
                    (title, description, due_date, completed, user_id)
                    VALUES(%s, %s, %s, %s, %s)""",
                    [title, description, due_date, False, user.id],
                )
            return Response(
                {"success": True, "result": "Task Added!!"},
                status=status.HTTP_201_CREATED,
            )

        elif request.method == "PUT":
            title = request.data.get("title")
            description = request.data.get("description")
            due_date = datetime.strptime(request.data.get("due_date"), "%Y-%m-%d")
            completed = request.data.get("completed")

            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from task_task where id=%s and user_id=%s", [id, user.id]
                )
                result = Utils.dict_fetch_all(cursor)
                if len(result) == 0:
                    return Response(
                        {"success": False, "result": "Task Not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                else:
                    cursor.execute(
                        """
                        UPDATE task_task
                        SET title=%s, description=%s, due_date=%s, completed=%s, user_id=%s
                        WHERE id=%s""",
                        [title, description, due_date, completed, user.id, id],
                    )
                    return Response(
                        {"success": True, "result": result}, status=status.HTTP_200_OK
                    )

        elif request.method == "DELETE":
            with connection.cursor() as cursor:
                cursor.execute(
                    "select * from task_task where id=%s and user_id=%s", [id, user.id]
                )
                result = Utils.dict_fetch_all(cursor)

                if len(result) == 0:
                    return Response(
                        {"success": False, "result": "Task Not found"},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                else:
                    cursor.execute("delete from task_task where id=%s", [id])
                    return Response(
                        {"success": True, "result": "Deleted successfully!!"},
                        status=status.HTTP_200_OK,
                    )

    except Exception as e:
        return Response(
            {"success": False, "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
