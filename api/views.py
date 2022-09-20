import django.http
import api.models


def readings_by_mpan(request: django.http.HttpRequest, **kwargs):
    """
    Returns a list of meter readings for a specific mpan_core
    between the dates specified in the request
    """
    start_date, end_date = (
        request.GET.get("from"),
        request.GET.get("to"),
    )
    if start_date and not end_date:
        return django.http.JsonResponse(
            {
                "status": "ok",
                "readings": api.models.Reading.objects.get_for_mpan_after(
                    mpan_core=kwargs["mpan_core"], start_date=start_date
                ),
                "mpan_core": kwargs["mpan_core"],
                "url": request.path,
            },
            status=200,
        )
    if start_date and end_date:
        return django.http.JsonResponse(
            {
                "status": "ok",
                "readings": api.models.Reading.objects.get_for_mpan_between(
                    mpan_core=kwargs["mpan_core"],
                    start_date=start_date,
                    end_date=end_date,
                ),
                "mpan_core": kwargs["mpan_core"],
                "url": request.path,
            },
            status=200,
        )
    if not start_date and not end_date:
        return django.http.JsonResponse(
            {
                "status": "ok",
                "readings": api.models.Reading.objects.get_for_mpan(
                    mpan_core=kwargs["mpan_core"]
                ),
                "mpan_core": kwargs["mpan_core"],
                "url": request.path,
            },
            status=200,
        )
    if not start_date and end_date:
        return django.http.JsonResponse(
            {
                "status": "ok",
                "readings": api.models.Reading.objects.get_for_mpan_before(
                    mpan_core=kwargs["mpan_core"], end_date=end_date
                ),
                "mpan_core": kwargs["mpan_core"],
                "url": request.path,
            },
            status=200,
        )
    return django.http.JsonResponse(
        {
            "status": "error",
            "message": "Request was malformed. Check URL and parameters and try again.",
            "url": request.path,
        },
        status=400,
    )
